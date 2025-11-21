"""
Business logic for job listings management
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_, extract
from fastapi import HTTPException, status
from models import JobListing, Application, User, Department, ApplicationStatus
from pydantic_models import (
    CreateJobRequest, UpdateJobRequest, JobListingResponse,
    JobFilters, JobStatisticsResponse
)
from datetime import datetime, date
from typing import List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class JobService:
    """Service for job listings operations"""
    
    @staticmethod
    def _map_job_to_response(job: JobListing, include_details: bool = False) -> JobListingResponse:
        """Map job model to response schema"""
        response_data = {
            "id": job.id,
            "position": job.position,
            "department_id": job.department_id,
            "experience_required": job.experience_required,
            "skills_required": job.skills_required,
            "description": job.description,
            "ai_generated_description": job.ai_generated_description,
            "location": job.location,
            "employment_type": job.employment_type,
            "salary_range": job.salary_range,
            "is_active": job.is_active,
            "posted_by": job.posted_by,
            "posted_date": job.posted_date,
            "application_deadline": job.application_deadline,
            "created_at": job.created_at,
            "updated_at": job.updated_at,
            "application_count": len(job.applications) if hasattr(job, 'applications') else 0
        }
        
        if include_details:
            if job.department:
                response_data["department_name"] = job.department.name
            if job.posted_by_user:
                response_data["posted_by_name"] = job.posted_by_user.name
        
        return JobListingResponse(**response_data)
    
    @staticmethod
    def create_job(db: Session, request: CreateJobRequest, posted_by_id: int) -> JobListingResponse:
        """
        Create a new job listing
        
        Args:
            db: Database session
            request: Job creation request
            posted_by_id: ID of the user creating the job (HR)
            
        Returns:
            Created job listing
        """
        # Verify department exists
        department = db.query(Department).filter(Department.id == request.department_id).first()
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with ID {request.department_id} not found"
            )
        
        # Create new job
        new_job = JobListing(
            position=request.position,
            department_id=request.department_id,
            experience_required=request.experience_required,
            skills_required=request.skills_required,
            description=request.description,
            location=request.location,
            employment_type=request.employment_type.value,
            salary_range=request.salary_range,
            application_deadline=request.application_deadline,
            is_active=True,
            posted_by=posted_by_id,
            posted_date=datetime.utcnow()
        )
        
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        
        logger.info(f"Job created: {new_job.position} (ID: {new_job.id}) by user {posted_by_id}")
        
        return JobService._map_job_to_response(new_job, include_details=True)
    
    @staticmethod
    def get_job_by_id(db: Session, job_id: int, include_details: bool = True) -> JobListingResponse:
        """
        Get job by ID
        
        Args:
            db: Database session
            job_id: Job ID
            include_details: Include department and poster names
            
        Returns:
            Job listing details
        """
        job = db.query(JobListing).filter(JobListing.id == job_id).first()
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job with ID {job_id} not found"
            )
        
        return JobService._map_job_to_response(job, include_details=include_details)
    
    @staticmethod
    def get_all_jobs(
        db: Session,
        filters: Optional[JobFilters] = None,
        page: int = 1,
        page_size: int = 20,
        include_details: bool = True
    ) -> Tuple[List[JobListingResponse], int]:
        """
        Get all job listings with filters and pagination
        
        Args:
            db: Database session
            filters: Optional filters
            page: Page number (starts from 1)
            page_size: Number of items per page
            include_details: Include department and poster names
            
        Returns:
            Tuple of (job listings, total count)
        """
        query = db.query(JobListing)
        
        # Apply filters
        if filters:
            if filters.department_id is not None:
                query = query.filter(JobListing.department_id == filters.department_id)
            
            if filters.location:
                query = query.filter(JobListing.location.ilike(f"%{filters.location}%"))
            
            if filters.employment_type:
                query = query.filter(JobListing.employment_type == filters.employment_type)
            
            if filters.is_active is not None:
                query = query.filter(JobListing.is_active == filters.is_active)
            
            if filters.search:
                search_term = f"%{filters.search}%"
                query = query.filter(
                    or_(
                        JobListing.position.ilike(search_term),
                        JobListing.description.ilike(search_term),
                        JobListing.skills_required.ilike(search_term)
                    )
                )
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        query = query.order_by(JobListing.posted_date.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        
        jobs = query.all()
        
        # Map to response
        job_responses = [JobService._map_job_to_response(job, include_details) for job in jobs]
        
        return job_responses, total
    
    @staticmethod
    def update_job(
        db: Session,
        job_id: int,
        request: UpdateJobRequest,
        updated_by_id: int
    ) -> JobListingResponse:
        """
        Update an existing job listing
        
        Args:
            db: Database session
            job_id: Job ID to update
            request: Update request with fields to change
            updated_by_id: ID of the user updating the job
            
        Returns:
            Updated job listing
        """
        job = db.query(JobListing).filter(JobListing.id == job_id).first()
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job with ID {job_id} not found"
            )
        
        # Update fields if provided
        if request.position is not None:
            job.position = request.position
        
        if request.department_id is not None:
            # Verify department exists
            department = db.query(Department).filter(Department.id == request.department_id).first()
            if not department:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Department with ID {request.department_id} not found"
                )
            job.department_id = request.department_id
        
        if request.experience_required is not None:
            job.experience_required = request.experience_required
        
        if request.skills_required is not None:
            job.skills_required = request.skills_required
        
        if request.description is not None:
            job.description = request.description
        
        if request.location is not None:
            job.location = request.location
        
        if request.employment_type is not None:
            job.employment_type = request.employment_type.value
        
        if request.salary_range is not None:
            job.salary_range = request.salary_range
        
        if request.application_deadline is not None:
            job.application_deadline = request.application_deadline
        
        if request.is_active is not None:
            job.is_active = request.is_active
        
        job.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(job)
        
        logger.info(f"Job updated: {job.position} (ID: {job_id}) by user {updated_by_id}")
        
        return JobService._map_job_to_response(job, include_details=True)
    
    @staticmethod
    def delete_job(db: Session, job_id: int, deleted_by_id: int) -> dict:
        """
        Delete (deactivate) a job listing
        
        Args:
            db: Database session
            job_id: Job ID to delete
            deleted_by_id: ID of the user deleting the job
            
        Returns:
            Success message
        """
        job = db.query(JobListing).filter(JobListing.id == job_id).first()
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job with ID {job_id} not found"
            )
        
        # Check if there are pending applications
        pending_applications = db.query(Application).filter(
            Application.job_id == job_id,
            Application.status == ApplicationStatus.PENDING
        ).count()
        
        if pending_applications > 0:
            # Soft delete - just deactivate
            job.is_active = False
            job.updated_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"Job deactivated: {job.position} (ID: {job_id}) by user {deleted_by_id}")
            
            return {
                "message": f"Job '{job.position}' has been deactivated. {pending_applications} pending application(s) remain.",
                "deactivated": True
            }
        else:
            # Hard delete if no applications
            db.delete(job)
            db.commit()
            
            logger.info(f"Job deleted: {job.position} (ID: {job_id}) by user {deleted_by_id}")
            
            return {
                "message": f"Job '{job.position}' has been permanently deleted.",
                "deleted": True
            }
    
    @staticmethod
    def get_job_applications(db: Session, job_id: int) -> List[dict]:
        """
        Get all applications for a specific job
        
        Args:
            db: Database session
            job_id: Job ID
            
        Returns:
            List of applications
        """
        job = db.query(JobListing).filter(JobListing.id == job_id).first()
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job with ID {job_id} not found"
            )
        
        applications = db.query(Application).filter(Application.job_id == job_id).all()
        
        result = []
        for app in applications:
            result.append({
                "id": app.id,
                "applicant_name": app.applicant_name or (app.applicant.name if app.applicant else "Unknown"),
                "applicant_email": app.applicant_email or (app.applicant.email if app.applicant else "Unknown"),
                "applied_date": app.applied_date,
                "status": app.status.value if isinstance(app.status, ApplicationStatus) else app.status,
                "resume_path": app.resume_path
            })
        
        return result
    
    @staticmethod
    def get_job_statistics(db: Session) -> JobStatisticsResponse:
        """
        Get overall job statistics for HR dashboard
        
        Args:
            db: Database session
            
        Returns:
            Job statistics
        """
        # Total jobs
        total_jobs = db.query(JobListing).count()
        
        # Active jobs
        active_jobs = db.query(JobListing).filter(JobListing.is_active == True).count()
        
        # Closed jobs
        closed_jobs = total_jobs - active_jobs
        
        # Total applications
        total_applications = db.query(Application).count()
        
        # Applications this month
        current_month = datetime.utcnow().month
        current_year = datetime.utcnow().year
        applications_this_month = db.query(Application).filter(
            extract('month', Application.applied_date) == current_month,
            extract('year', Application.applied_date) == current_year
        ).count()
        
        # Top departments by job count
        top_departments = db.query(
            Department.name,
            func.count(JobListing.id).label('job_count')
        ).join(
            JobListing, Department.id == JobListing.department_id
        ).group_by(
            Department.name
        ).order_by(
            func.count(JobListing.id).desc()
        ).limit(5).all()
        
        top_dept_list = [{"department": dept.name, "job_count": dept.job_count} for dept in top_departments]
        
        return JobStatisticsResponse(
            total_jobs=total_jobs,
            active_jobs=active_jobs,
            closed_jobs=closed_jobs,
            total_applications=total_applications,
            applications_this_month=applications_this_month,
            top_departments=top_dept_list
        )

