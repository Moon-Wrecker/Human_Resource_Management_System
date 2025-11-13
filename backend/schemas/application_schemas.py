"""
Pydantic schemas for job applications management
"""
from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ApplicationStatusEnum(str, Enum):
    """Application status options"""
    PENDING = "pending"
    REVIEWED = "reviewed"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    HIRED = "hired"


class ApplicationSourceEnum(str, Enum):
    """Application source options"""
    SELF_APPLIED = "self-applied"
    REFERRAL = "referral"
    RECRUITMENT = "recruitment"
    INTERNAL = "internal"


class CreateApplicationRequest(BaseModel):
    """Request to create a new application"""
    job_id: int = Field(..., description="Job listing ID")
    applicant_name: str = Field(..., min_length=2, max_length=100, description="Applicant name")
    applicant_email: EmailStr = Field(..., description="Applicant email")
    applicant_phone: Optional[str] = Field(default=None, max_length=20, description="Applicant phone")
    cover_letter: Optional[str] = Field(default=None, max_length=2000, description="Cover letter")
    source: ApplicationSourceEnum = Field(default=ApplicationSourceEnum.SELF_APPLIED, description="Application source")
    referred_by: Optional[int] = Field(default=None, description="Referrer user ID (if applicable)")
    
    @validator('applicant_phone')
    def validate_phone(cls, v):
        if v and not v.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValueError('Phone number must contain only digits, +, -, and spaces')
        return v


class UpdateApplicationStatusRequest(BaseModel):
    """Request to update application status"""
    status: ApplicationStatusEnum = Field(..., description="New application status")
    screening_notes: Optional[str] = Field(default=None, max_length=1000, description="Screening notes or feedback")
    screening_score: Optional[float] = Field(default=None, ge=0, le=100, description="Screening score (0-100)")


class ApplicationResponse(BaseModel):
    """Single application response"""
    id: int
    job_id: int
    job_position: Optional[str] = None
    job_department: Optional[str] = None
    applicant_id: Optional[int] = None
    applicant_name: str
    applicant_email: str
    applicant_phone: Optional[str] = None
    resume_path: Optional[str] = None
    cover_letter: Optional[str] = None
    source: str
    referred_by: Optional[int] = None
    referrer_name: Optional[str] = None
    status: str
    screening_score: Optional[float] = None
    screening_notes: Optional[str] = None
    applied_date: datetime
    reviewed_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ApplicationsListResponse(BaseModel):
    """Paginated list of applications"""
    total: int = Field(..., description="Total number of applications")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")
    applications: List[ApplicationResponse] = Field(..., description="List of applications")


class ApplicationFilters(BaseModel):
    """Filters for applications"""
    job_id: Optional[int] = None
    status: Optional[str] = None
    source: Optional[str] = None
    search: Optional[str] = None  # Search in applicant name, email


class ApplicationStatisticsResponse(BaseModel):
    """Application statistics for HR dashboard"""
    total_applications: int
    pending_applications: int
    reviewed_applications: int
    shortlisted_applications: int
    rejected_applications: int
    hired_applications: int
    applications_this_month: int
    top_jobs: List[dict]  # [{"position": "Developer", "application_count": 15}]
    applications_by_source: dict  # {"self-applied": 50, "referral": 20, "recruitment": 10}


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str


class ResumeUploadResponse(BaseModel):
    """Resume upload response"""
    message: str
    resume_path: str
    file_size: int

