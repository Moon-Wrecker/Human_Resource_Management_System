"""
API routes for job applications management
"""
from fastapi import APIRouter, Depends, Query, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
import math
import os

from database import get_db
from utils.dependencies import get_current_user, get_current_active_user, require_hr
from models import User, UserRole
from services.application_service import ApplicationService
from services.auth_service import AuthService
from pydantic_models import (
    CreateApplicationRequest,
    UpdateApplicationStatusRequest,
    ApplicationResponse,
    ApplicationsListResponse,
    ApplicationFilters,
    ApplicationStatisticsResponse,
    MessageResponse,
    ResumeUploadResponse
)

router = APIRouter(prefix="/applications", tags=["applications"])

security = HTTPBearer(auto_error=False)  # auto_error=False makes authentication optional


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Optional authentication dependency - returns User if authenticated, None otherwise
    """
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        user = AuthService.get_current_user(db, token)
        return user
    except:
        return None


@router.post(
    "/",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Apply for a job",
    description="Create a new job application. Internal employees are automatically linked to their user account."
)
async def create_application(
    request: CreateApplicationRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Create a new job application
    
    - **job_id**: ID of the job listing to apply for
    - **applicant_name**: Name of the applicant
    - **applicant_email**: Email address (must be unique per job)
    - **applicant_phone**: Phone number (optional)
    - **cover_letter**: Cover letter text (optional, max 2000 chars)
    - **source**: Application source (self-applied, referral, recruitment, internal)
    - **referred_by**: User ID of referrer (optional, if source is referral)
    
    **Access**: Public or authenticated users
    """
    applicant_user_id = current_user.id if current_user else None
    return ApplicationService.create_application(db, request, applicant_user_id)


@router.get(
    "/me",
    response_model=ApplicationsListResponse,
    summary="Get my applications",
    description="Retrieve all applications submitted by the current user with pagination"
)
def get_my_applications(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all applications for the current user
    
    **Access**: Authenticated users only
    
    Returns paginated list of user's applications with job details
    """
    applications, total = ApplicationService.get_my_applications(
        db, current_user.id, page, page_size
    )
    
    total_pages = math.ceil(total / page_size)
    
    return ApplicationsListResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        applications=applications
    )


@router.get(
    "/statistics",
    response_model=ApplicationStatisticsResponse,
    summary="Get application statistics",
    description="Retrieve overall application statistics for HR dashboard"
)
def get_application_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr)
):
    """
    Get application statistics
    
    **Access**: HR only
    
    Returns:
    - Total applications count
    - Applications by status (pending, reviewed, shortlisted, rejected, hired)
    - Applications this month
    - Top jobs by application count
    - Applications by source
    """
    return ApplicationService.get_application_statistics(db)


@router.get(
    "/",
    response_model=ApplicationsListResponse,
    summary="Get all applications",
    description="Retrieve all applications with filtering and pagination (HR only)"
)
def get_all_applications(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    job_id: Optional[int] = Query(None, description="Filter by job ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    source: Optional[str] = Query(None, description="Filter by source"),
    search: Optional[str] = Query(None, description="Search in applicant name/email"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr)
):
    """
    Get all applications (HR only)
    
    **Access**: HR only
    
    **Filters**:
    - job_id: Show applications for specific job
    - status: Filter by status (pending, reviewed, shortlisted, rejected, hired)
    - source: Filter by source (self-applied, referral, recruitment, internal)
    - search: Search in applicant name or email
    
    Returns paginated list with full details
    """
    filters = ApplicationFilters(
        job_id=job_id,
        status=status,
        source=source,
        search=search
    )
    
    applications, total = ApplicationService.get_all_applications(
        db, filters, page, page_size
    )
    
    total_pages = math.ceil(total / page_size)
    
    return ApplicationsListResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        applications=applications
    )


@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
    summary="Get application details",
    description="Retrieve detailed information about a specific application"
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get application by ID
    
    **Access**:
    - HR: Can view all applications
    - Employees: Can only view their own applications
    
    Returns full application details including job info and referrer
    """
    application = ApplicationService.get_application_by_id(db, application_id)
    
    # Authorization check: HR can view all, employees can only view their own
    if current_user.role != UserRole.HR:
        if application.applicant_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own applications"
            )
    
    return application


@router.put(
    "/{application_id}/status",
    response_model=ApplicationResponse,
    summary="Update application status",
    description="Update the status of an application with optional screening notes and score (HR only)"
)
def update_application_status(
    application_id: int,
    request: UpdateApplicationStatusRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr)
):
    """
    Update application status (HR only)
    
    **Access**: HR only
    
    **Status options**:
    - pending: Initial state
    - reviewed: Application has been reviewed
    - shortlisted: Candidate shortlisted for interview
    - rejected: Application rejected
    - hired: Candidate hired
    
    Can also add screening notes and score (0-100)
    """
    return ApplicationService.update_application_status(
        db, application_id, request, current_user.id
    )


@router.post(
    "/{application_id}/resume",
    response_model=ResumeUploadResponse,
    summary="Upload resume",
    description="Upload resume file for an application (PDF, DOC, DOCX, max 5MB)"
)
async def upload_resume(
    application_id: int,
    file: UploadFile = File(..., description="Resume file (PDF, DOC, DOCX)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload resume for an application
    
    **Access**:
    - HR: Can upload for any application
    - Employees: Can only upload for their own applications
    
    **File requirements**:
    - Format: PDF, DOC, or DOCX
    - Max size: 5MB
    
    Replaces existing resume if already uploaded
    """
    # Get application to check ownership
    application = ApplicationService.get_application_by_id(db, application_id)
    
    # Authorization check
    if current_user.role != UserRole.HR:
        if application.applicant_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only upload resume for your own applications"
            )
    
    result = await ApplicationService.upload_resume(db, application_id, file)
    
    return ResumeUploadResponse(**result)


@router.get(
    "/{application_id}/resume",
    summary="Download resume",
    description="Download the resume file for an application"
)
def download_resume(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Download resume for an application
    
    **Access**:
    - HR: Can download any resume
    - Employees: Can only download their own resumes
    
    Returns the resume file as a download
    """
    # Get application
    application = ApplicationService.get_application_by_id(db, application_id)
    
    # Authorization check
    if current_user.role != UserRole.HR:
        if application.applicant_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only download your own resume"
            )
    
    # Check if resume exists
    if not application.resume_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No resume uploaded for this application"
        )
    
    if not os.path.exists(application.resume_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume file not found on server"
        )
    
    # Return file
    filename = os.path.basename(application.resume_path)
    return FileResponse(
        path=application.resume_path,
        filename=filename,
        media_type='application/octet-stream'
    )


@router.delete(
    "/{application_id}",
    response_model=MessageResponse,
    summary="Delete application",
    description="Delete an application (HR only or applicant before review)"
)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete an application
    
    **Access**:
    - HR: Can delete any application
    - Employees: Can only delete their own applications if status is pending
    
    Also deletes associated resume file
    """
    # Get application
    application = ApplicationService.get_application_by_id(db, application_id)
    
    # Authorization check
    if current_user.role != UserRole.HR:
        if application.applicant_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own applications"
            )
        if application.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete applications that are still pending"
            )
    
    return ApplicationService.delete_application(db, application_id, current_user.id)

