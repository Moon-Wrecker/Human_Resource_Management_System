"""
FastAPI routes for job listings management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from database import get_db
from models import User
from utils.dependencies import get_current_active_user, require_hr
from services.job_service import JobService
from pydantic_models import (
    CreateJobRequest, UpdateJobRequest, JobListingResponse,
    JobListingsResponse, JobFilters, JobStatisticsResponse,
    MessageResponse
)
import math

router = APIRouter(prefix="/jobs", tags=["Job Listings"])


@router.post("", response_model=JobListingResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_hr)])
async def create_job(
    request: CreateJobRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    **Create a new job listing** (HR only)
    
    - **HR Action**: Post a new job opening
    - **Required Fields**: position, department_id
    - **Optional**: experience, skills, description, location, salary, deadline
    
    **Business Rules:**
    - Only HR can create job listings
    - Department must exist
    - Application deadline must be in the future
    - Job is automatically set to active status
    
    **Returns:**
    - Created job listing with full details
    """
    job = JobService.create_job(db, request, current_user.id)
    return job


@router.get("", response_model=JobListingsResponse, status_code=status.HTTP_200_OK)
async def get_all_jobs(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
    department_id: Optional[int] = Query(default=None, description="Filter by department"),
    location: Optional[str] = Query(default=None, description="Filter by location"),
    employment_type: Optional[str] = Query(default=None, description="Filter by employment type"),
    is_active: Optional[bool] = Query(default=True, description="Filter by active status"),
    search: Optional[str] = Query(default=None, description="Search in position, description, skills"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page")
):
    """
    **Get all job listings**
    
    - **All Roles**: View job listings
    - **Filters**: department, location, employment type, active status, search
    - **Pagination**: Configurable page size (max 100)
    - **Sorting**: Newest jobs first
    
    **Use Cases:**
    - Employees: Browse internal job opportunities
    - Managers: View openings in their department
    - HR: Manage all job postings
    
    **Returns:**
    - Paginated list of job listings
    - Total count and page information
    """
    filters = JobFilters(
        department_id=department_id,
        location=location,
        employment_type=employment_type,
        is_active=is_active,
        search=search
    )
    
    jobs, total = JobService.get_all_jobs(db, filters, page, page_size, include_details=True)
    
    total_pages = math.ceil(total / page_size)
    
    return JobListingsResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        jobs=jobs
    )


@router.get("/statistics", response_model=JobStatisticsResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(require_hr)])
async def get_job_statistics(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    **Get job statistics** (HR only)
    
    - **HR Dashboard**: Overview of recruitment metrics
    - **Metrics**: Total jobs, active, closed, applications
    - **Trends**: Applications this month
    - **Insights**: Top hiring departments
    
    **Returns:**
    - Comprehensive job and application statistics
    """
    stats = JobService.get_job_statistics(db)
    return stats


@router.get("/{job_id}", response_model=JobListingResponse, status_code=status.HTTP_200_OK)
async def get_job_by_id(
    job_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    **Get job details by ID**
    
    - **All Roles**: View specific job details
    - **Details Include**: Full description, requirements, salary, department
    - **Additional Info**: Number of applications, posted by, posted date
    
    **Returns:**
    - Complete job listing details
    """
    job = JobService.get_job_by_id(db, job_id, include_details=True)
    return job


@router.put("/{job_id}", response_model=JobListingResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(require_hr)])
async def update_job(
    job_id: int,
    request: UpdateJobRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    **Update job listing** (HR only)
    
    - **HR Action**: Edit job posting details
    - **Partial Updates**: Only provide fields to change
    - **Common Updates**: Close job, extend deadline, update requirements
    
    **Business Rules:**
    - Only HR can update jobs
    - Can update active status to close job
    - Cannot set past deadline dates
    
    **Returns:**
    - Updated job listing
    """
    job = JobService.update_job(db, job_id, request, current_user.id)
    return job


@router.delete("/{job_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK,
               dependencies=[Depends(require_hr)])
async def delete_job(
    job_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    **Delete job listing** (HR only)
    
    - **HR Action**: Remove job posting
    - **Soft Delete**: If pending applications exist, job is deactivated
    - **Hard Delete**: If no applications, job is permanently removed
    
    **Business Rules:**
    - Protects pending applications
    - Maintains audit trail for active applications
    
    **Returns:**
    - Success message with deletion type
    """
    result = JobService.delete_job(db, job_id, current_user.id)
    return MessageResponse(message=result["message"])


@router.get("/{job_id}/applications", response_model=list, status_code=status.HTTP_200_OK,
            dependencies=[Depends(require_hr)])
async def get_job_applications(
    job_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    **Get all applications for a job** (HR only)
    
    - **HR View**: See who applied for this position
    - **Application Details**: Name, email, status, resume link
    - **Filtering**: Can be filtered by status in frontend
    
    **Returns:**
    - List of applications for the specified job
    """
    applications = JobService.get_job_applications(db, job_id)
    return applications

