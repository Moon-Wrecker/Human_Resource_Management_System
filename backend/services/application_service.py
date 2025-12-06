"""
Business logic for job applications management
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_, extract
from fastapi import HTTPException, status, UploadFile
from models import (
    Application,
    JobListing,
    User,
    Department,
    ApplicationStatus,
    UserRole,
)
from pydantic_models import (
    CreateApplicationRequest,
    UpdateApplicationStatusRequest,
    ApplicationResponse,
    ApplicationFilters,
    ApplicationStatisticsResponse,
)
from datetime import datetime
from typing import List, Optional, Tuple
import logging
import os
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


class ApplicationService:
    """Service for job applications operations"""

    # File upload settings
    MAX_RESUME_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}
    UPLOAD_DIR = "uploads/resumes"

    @staticmethod
    def _ensure_upload_dir():
        """Ensure upload directory exists"""
        Path(ApplicationService.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _map_application_to_response(
        application: Application, include_details: bool = False
    ) -> ApplicationResponse:
        """Map application model to response schema"""
        response_data = {
            "id": application.id,
            "job_id": application.job_id,
            "applicant_id": application.applicant_id,
            "applicant_name": application.applicant_name,
            "applicant_email": application.applicant_email,
            "applicant_phone": application.applicant_phone,
            "resume_path": application.resume_path,
            "cover_letter": application.cover_letter,
            "source": application.source,
            "referred_by": application.referred_by,
            "status": application.status.value
            if isinstance(application.status, ApplicationStatus)
            else application.status,
            "screening_score": application.screening_score,
            "screening_notes": application.screening_notes,
            "applied_date": application.applied_date,
            "reviewed_date": application.reviewed_date,
        }

        if include_details:
            if application.job:
                response_data["job_position"] = application.job.position
                if application.job.department:
                    response_data["job_department"] = application.job.department.name

            if application.referrer:
                response_data["referrer_name"] = application.referrer.name

        return ApplicationResponse(**response_data)

    @staticmethod
    def create_application(
        db: Session,
        request: CreateApplicationRequest,
        applicant_user_id: Optional[int] = None,
    ) -> ApplicationResponse:
        """
        Create a new job application

        Args:
            db: Database session
            request: Application creation request
            applicant_user_id: ID of logged-in user (for internal applications)

        Returns:
            Created application
        """
        # Verify job exists and is active
        job = (
            db.query(JobListing)
            .filter(JobListing.id == request.job_id, JobListing.is_active == True)
            .first()
        )

        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Active job with ID {request.job_id} not found",
            )

        # Check deadline
        if (
            job.application_deadline
            and job.application_deadline < datetime.now().date()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Application deadline has passed for this job",
            )

        user = None
        if applicant_user_id:
            user = db.query(User).filter(User.id == applicant_user_id).first()

        # Allow HR/Manager to create multiple applications for dummy candidates
        if not (user and user.role in [UserRole.HR, UserRole.MANAGER]):
            # Check if already applied (prevent duplicate applications)
            existing_query = db.query(Application).filter(
                Application.job_id == request.job_id
            )

            if applicant_user_id:
                existing_query = existing_query.filter(
                    Application.applicant_id == applicant_user_id
                )
            else:
                existing_query = existing_query.filter(
                    Application.applicant_email == request.applicant_email
                )

            if existing_query.first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You have already applied for this job",
                )

        # Verify referrer if provided
        if request.referred_by:
            referrer = db.query(User).filter(User.id == request.referred_by).first()
            if not referrer:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Referrer with ID {request.referred_by} not found",
                )

        # Create application
        new_application = Application(
            job_id=request.job_id,
            applicant_id=applicant_user_id,
            applicant_name=request.applicant_name,
            applicant_email=request.applicant_email,
            applicant_phone=request.applicant_phone,
            cover_letter=request.cover_letter,
            source=request.source.value,
            referred_by=request.referred_by,
            status=ApplicationStatus.PENDING,
            applied_date=datetime.utcnow(),
        )

        db.add(new_application)
        db.commit()
        db.refresh(new_application)

        logger.info(
            f"Application created: ID {new_application.id} for job {request.job_id}"
        )

        return ApplicationService._map_application_to_response(
            new_application, include_details=True
        )

    @staticmethod
    def get_application_by_id(db: Session, application_id: int) -> ApplicationResponse:
        """Get application by ID with details"""
        application = (
            db.query(Application).filter(Application.id == application_id).first()
        )

        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {application_id} not found",
            )

        return ApplicationService._map_application_to_response(
            application, include_details=True
        )

    @staticmethod
    def get_all_applications(
        db: Session,
        filters: Optional[ApplicationFilters] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[ApplicationResponse], int]:
        """Get all applications with filters and pagination"""
        query = db.query(Application)

        # Apply filters
        if filters:
            if filters.job_id is not None:
                query = query.filter(Application.job_id == filters.job_id)

            if filters.status:
                query = query.filter(Application.status == filters.status)

            if filters.source:
                query = query.filter(Application.source == filters.source)

            if filters.search:
                search_term = f"%{filters.search}%"
                query = query.filter(
                    or_(
                        Application.applicant_name.ilike(search_term),
                        Application.applicant_email.ilike(search_term),
                    )
                )

        # Get total count
        total = query.count()

        # Apply pagination and ordering
        query = query.order_by(Application.applied_date.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)

        applications = query.all()

        # Map to response
        application_responses = [
            ApplicationService._map_application_to_response(app, include_details=True)
            for app in applications
        ]

        return application_responses, total

    @staticmethod
    def get_my_applications(
        db: Session, user_id: int, page: int = 1, page_size: int = 20
    ) -> Tuple[List[ApplicationResponse], int]:
        """Get applications for a specific user"""
        query = db.query(Application).filter(Application.applicant_id == user_id)

        # Get total count
        total = query.count()

        # Apply pagination and ordering
        query = query.order_by(Application.applied_date.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)

        applications = query.all()

        # Map to response
        application_responses = [
            ApplicationService._map_application_to_response(app, include_details=True)
            for app in applications
        ]

        return application_responses, total

    @staticmethod
    def update_application_status(
        db: Session,
        application_id: int,
        request: UpdateApplicationStatusRequest,
        reviewed_by_id: int,
    ) -> ApplicationResponse:
        """Update application status (HR only)"""
        application = (
            db.query(Application).filter(Application.id == application_id).first()
        )

        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {application_id} not found",
            )

        # Update status
        application.status = ApplicationStatus[request.status.value.upper()]

        if request.screening_notes:
            application.screening_notes = request.screening_notes

        if request.screening_score is not None:
            application.screening_score = request.screening_score

        # Set reviewed date if moving from pending
        if (
            application.status != ApplicationStatus.PENDING
            and not application.reviewed_date
        ):
            application.reviewed_date = datetime.utcnow()

        db.commit()
        db.refresh(application)

        logger.info(
            f"Application {application_id} status updated to {request.status.value} by user {reviewed_by_id}"
        )

        return ApplicationService._map_application_to_response(
            application, include_details=True
        )

    @staticmethod
    async def upload_resume(db: Session, application_id: int, file: UploadFile) -> dict:
        """Upload resume for an application"""
        # Verify application exists
        application = (
            db.query(Application).filter(Application.id == application_id).first()
        )

        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {application_id} not found",
            )

        # Validate file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ApplicationService.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed: {', '.join(ApplicationService.ALLOWED_EXTENSIONS)}",
            )

        # Validate file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning

        if file_size > ApplicationService.MAX_RESUME_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size: {ApplicationService.MAX_RESUME_SIZE / (1024 * 1024)}MB",
            )

        # Ensure upload directory exists
        ApplicationService._ensure_upload_dir()

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"resume_{application_id}_{timestamp}{file_ext}"
        file_path = os.path.join(ApplicationService.UPLOAD_DIR, safe_filename)

        # Delete old resume if exists
        if application.resume_path and os.path.exists(application.resume_path):
            try:
                os.remove(application.resume_path)
            except Exception as e:
                logger.warning(f"Failed to delete old resume: {e}")

        # Save file
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            logger.error(f"Failed to save resume: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save resume file",
            )

        # Update application
        application.resume_path = file_path
        db.commit()

        logger.info(f"Resume uploaded for application {application_id}: {file_path}")

        return {
            "message": "Resume uploaded successfully",
            "resume_path": file_path,
            "file_size": file_size,
        }

    @staticmethod
    def delete_application(
        db: Session, application_id: int, deleted_by_id: int
    ) -> dict:
        """Delete an application (HR only or applicant before review)"""
        application = (
            db.query(Application).filter(Application.id == application_id).first()
        )

        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {application_id} not found",
            )

        # Delete resume file if exists
        if application.resume_path and os.path.exists(application.resume_path):
            try:
                os.remove(application.resume_path)
            except Exception as e:
                logger.warning(f"Failed to delete resume file: {e}")

        # Delete application
        db.delete(application)
        db.commit()

        logger.info(f"Application {application_id} deleted by user {deleted_by_id}")

        return {"message": "Application deleted successfully"}

    @staticmethod
    def get_application_statistics(db: Session) -> ApplicationStatisticsResponse:
        """Get overall application statistics for HR dashboard"""
        # Total applications
        total_applications = db.query(Application).count()

        # By status
        pending = (
            db.query(Application)
            .filter(Application.status == ApplicationStatus.PENDING)
            .count()
        )
        reviewed = (
            db.query(Application)
            .filter(Application.status == ApplicationStatus.REVIEWED)
            .count()
        )
        shortlisted = (
            db.query(Application)
            .filter(Application.status == ApplicationStatus.SHORTLISTED)
            .count()
        )
        rejected = (
            db.query(Application)
            .filter(Application.status == ApplicationStatus.REJECTED)
            .count()
        )
        hired = (
            db.query(Application)
            .filter(Application.status == ApplicationStatus.HIRED)
            .count()
        )

        # Applications this month
        current_month = datetime.utcnow().month
        current_year = datetime.utcnow().year
        applications_this_month = (
            db.query(Application)
            .filter(
                extract("month", Application.applied_date) == current_month,
                extract("year", Application.applied_date) == current_year,
            )
            .count()
        )

        # Top jobs by application count
        top_jobs = (
            db.query(
                JobListing.position,
                func.count(Application.id).label("application_count"),
            )
            .join(Application, JobListing.id == Application.job_id)
            .group_by(JobListing.position)
            .order_by(func.count(Application.id).desc())
            .limit(5)
            .all()
        )

        top_jobs_list = [
            {"position": job.position, "application_count": job.application_count}
            for job in top_jobs
        ]

        # Applications by source
        applications_by_source = {}
        sources = (
            db.query(Application.source, func.count(Application.id).label("count"))
            .group_by(Application.source)
            .all()
        )

        for source_data in sources:
            applications_by_source[source_data.source] = source_data.count

        return ApplicationStatisticsResponse(
            total_applications=total_applications,
            pending_applications=pending,
            reviewed_applications=reviewed,
            shortlisted_applications=shortlisted,
            rejected_applications=rejected,
            hired_applications=hired,
            applications_this_month=applications_this_month,
            top_jobs=top_jobs_list,
            applications_by_source=applications_by_source,
        )
