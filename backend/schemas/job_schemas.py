"""
Pydantic schemas for job listings management
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class EmploymentTypeEnum(str, Enum):
    """Employment type options"""
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"


class JobStatusEnum(str, Enum):
    """Job listing status"""
    ACTIVE = "active"
    CLOSED = "closed"
    DRAFT = "draft"


class CreateJobRequest(BaseModel):
    """Request to create a new job listing"""
    position: str = Field(..., min_length=3, max_length=100, description="Job position/title")
    department_id: int = Field(..., description="Department ID")
    experience_required: Optional[str] = Field(default=None, max_length=50, description="Required experience (e.g., '2-4 years')")
    skills_required: Optional[str] = Field(default=None, description="Required skills (comma-separated)")
    description: Optional[str] = Field(default=None, description="Job description")
    location: Optional[str] = Field(default="Remote", max_length=100, description="Job location")
    employment_type: EmploymentTypeEnum = Field(default=EmploymentTypeEnum.FULL_TIME, description="Employment type")
    salary_range: Optional[str] = Field(default=None, max_length=50, description="Salary range (e.g., '5-7 LPA')")
    application_deadline: Optional[date] = Field(default=None, description="Application deadline")
    
    @validator('application_deadline')
    def deadline_must_be_future(cls, v):
        if v and v < date.today():
            raise ValueError('Application deadline must be in the future')
        return v


class UpdateJobRequest(BaseModel):
    """Request to update an existing job listing"""
    position: Optional[str] = Field(default=None, min_length=3, max_length=100, description="Job position/title")
    department_id: Optional[int] = Field(default=None, description="Department ID")
    experience_required: Optional[str] = Field(default=None, max_length=50, description="Required experience")
    skills_required: Optional[str] = Field(default=None, description="Required skills")
    description: Optional[str] = Field(default=None, description="Job description")
    location: Optional[str] = Field(default=None, max_length=100, description="Job location")
    employment_type: Optional[EmploymentTypeEnum] = Field(default=None, description="Employment type")
    salary_range: Optional[str] = Field(default=None, max_length=50, description="Salary range")
    application_deadline: Optional[date] = Field(default=None, description="Application deadline")
    is_active: Optional[bool] = Field(default=None, description="Job active status")
    
    @validator('application_deadline')
    def deadline_must_be_future(cls, v):
        if v and v < date.today():
            raise ValueError('Application deadline must be in the future')
        return v


class JobListingResponse(BaseModel):
    """Single job listing response"""
    id: int
    position: str
    department_id: int
    department_name: Optional[str] = None
    experience_required: Optional[str] = None
    skills_required: Optional[str] = None
    description: Optional[str] = None
    ai_generated_description: Optional[str] = None
    location: Optional[str] = None
    employment_type: str
    salary_range: Optional[str] = None
    is_active: bool
    posted_by: int
    posted_by_name: Optional[str] = None
    posted_date: datetime
    application_deadline: Optional[date] = None
    application_count: Optional[int] = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class JobListingsResponse(BaseModel):
    """Paginated list of job listings"""
    total: int = Field(..., description="Total number of jobs")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")
    jobs: List[JobListingResponse] = Field(..., description="List of job listings")


class JobFilters(BaseModel):
    """Filters for job listings"""
    department_id: Optional[int] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    is_active: Optional[bool] = True
    search: Optional[str] = None  # Search in position, description, skills


class GenerateJDRequest(BaseModel):
    """Request to generate job description using AI"""
    position: str = Field(..., description="Job position/title")
    department_id: int = Field(..., description="Department ID")
    experience_required: Optional[str] = Field(default=None, description="Required experience")
    skills_required: Optional[str] = Field(default=None, description="Required skills")


class GenerateJDResponse(BaseModel):
    """Response with AI-generated job description"""
    position: str
    generated_description: str
    suggestions: Optional[dict] = None


class JobStatisticsResponse(BaseModel):
    """Job statistics for HR dashboard"""
    total_jobs: int
    active_jobs: int
    closed_jobs: int
    total_applications: int
    applications_this_month: int
    top_departments: List[dict]  # [{"department": "Engineering", "job_count": 5}]


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str

