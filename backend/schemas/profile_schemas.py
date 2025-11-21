"""
Pydantic schemas for profile management
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, date


class ProfileResponse(BaseModel):
    """Complete user profile response"""
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    employee_id: Optional[str] = None
    role: str
    
    # Job details
    job_role: Optional[str] = None
    job_level: Optional[str] = None
    hierarchy_level: Optional[int] = None
    hire_date: Optional[date] = None
    salary: Optional[float] = None
    
    # Organization
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    team_id: Optional[int] = None
    team_name: Optional[str] = None
    
    # Manager info
    manager_id: Optional[int] = None
    manager_name: Optional[str] = None
    manager_email: Optional[str] = None
    
    # Leave balances
    casual_leave_balance: int = 0
    sick_leave_balance: int = 0
    annual_leave_balance: int = 0
    wfh_balance: int = 0
    
    # Documents
    profile_image_path: Optional[str] = None
    profile_image_url: Optional[str] = None
    aadhar_document_path: Optional[str] = None
    aadhar_document_url: Optional[str] = None
    pan_document_path: Optional[str] = None
    pan_document_url: Optional[str] = None
    
    # Metadata
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 3,
                "name": "John Doe",
                "email": "john.doe@company.com",
                "phone": "+91 9876543210",
                "employee_id": "EMP003",
                "role": "employee",
                "job_role": "Software Developer",
                "job_level": "Senior",
                "hierarchy_level": 5,
                "hire_date": "2023-01-15",
                "department_id": 1,
                "department_name": "Engineering",
                "team_id": 1,
                "team_name": "Backend Team",
                "manager_id": 2,
                "manager_name": "Michael Chen",
                "manager_email": "michael.chen@company.com",
                "casual_leave_balance": 8,
                "sick_leave_balance": 10,
                "annual_leave_balance": 12,
                "wfh_balance": 20,
                "profile_image_url": "/uploads/profiles/john_doe.jpg",
                "aadhar_document_url": "/uploads/documents/aadhar_john.pdf",
                "pan_document_url": "/uploads/documents/pan_john.pdf",
                "is_active": True,
                "created_at": "2023-01-15T10:00:00",
                "updated_at": "2025-11-13T10:00:00"
            }
        }


class UpdateProfileRequest(BaseModel):
    """Update profile request - only editable fields"""
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Full name")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe Updated",
                "phone": "+91 9876543210"
            }
        }


class DocumentUploadResponse(BaseModel):
    """Response after document upload"""
    message: str
    document_type: str
    file_path: str
    file_url: str
    uploaded_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Document uploaded successfully",
                "document_type": "aadhar",
                "file_path": "uploads/documents/aadhar_john_doe_1234567890.pdf",
                "file_url": "/uploads/documents/aadhar_john_doe_1234567890.pdf",
                "uploaded_at": "2025-11-13T10:30:00"
            }
        }


class UserDocumentsResponse(BaseModel):
    """User's uploaded documents"""
    profile_image: Optional[dict] = None
    aadhar_card: Optional[dict] = None
    pan_card: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "profile_image": {
                    "path": "uploads/profiles/john_doe.jpg",
                    "url": "/uploads/profiles/john_doe.jpg",
                    "uploaded_at": "2025-11-10T10:00:00"
                },
                "aadhar_card": {
                    "path": "uploads/documents/aadhar_john.pdf",
                    "url": "/uploads/documents/aadhar_john.pdf",
                    "uploaded_at": "2025-11-10T11:00:00"
                },
                "pan_card": {
                    "path": "uploads/documents/pan_john.pdf",
                    "url": "/uploads/documents/pan_john.pdf",
                    "uploaded_at": "2025-11-10T11:30:00"
                }
            }
        }


class ManagerInfoResponse(BaseModel):
    """Manager information response"""
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    employee_id: Optional[str] = None
    job_role: Optional[str] = None
    department_name: Optional[str] = None
    profile_image_url: Optional[str] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 2,
                "name": "Michael Chen",
                "email": "michael.chen@company.com",
                "phone": "+91 9876543211",
                "employee_id": "EMP002",
                "job_role": "Engineering Manager",
                "department_name": "Engineering",
                "profile_image_url": "/uploads/profiles/michael_chen.jpg"
            }
        }


class TeamMemberResponse(BaseModel):
    """Team member basic info"""
    id: int
    name: str
    email: str
    employee_id: Optional[str] = None
    job_role: Optional[str] = None
    job_level: Optional[str] = None
    phone: Optional[str] = None
    profile_image_url: Optional[str] = None
    is_active: bool = True
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 3,
                "name": "John Doe",
                "email": "john.doe@company.com",
                "employee_id": "EMP003",
                "job_role": "Software Developer",
                "job_level": "Senior",
                "phone": "+91 9876543210",
                "profile_image_url": "/uploads/profiles/john_doe.jpg",
                "is_active": True
            }
        }


class TeamResponse(BaseModel):
    """Complete team response with members"""
    team_id: Optional[int] = None
    team_name: Optional[str] = None
    department_name: Optional[str] = None
    total_members: int = 0
    members: list[TeamMemberResponse] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "team_id": 1,
                "team_name": "Backend Team",
                "department_name": "Engineering",
                "total_members": 5,
                "members": [
                    {
                        "id": 3,
                        "name": "John Doe",
                        "email": "john.doe@company.com",
                        "employee_id": "EMP003",
                        "job_role": "Software Developer",
                        "job_level": "Senior",
                        "is_active": True
                    }
                ]
            }
        }


class ProfileStatsResponse(BaseModel):
    """Profile statistics and analytics"""
    total_goals: int = 0
    completed_goals: int = 0
    in_progress_goals: int = 0
    total_skill_modules: int = 0
    completed_skill_modules: int = 0
    total_training_hours: float = 0.0
    attendance_percentage: float = 0.0
    leaves_taken_this_year: int = 0
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_goals": 10,
                "completed_goals": 7,
                "in_progress_goals": 3,
                "total_skill_modules": 15,
                "completed_skill_modules": 12,
                "total_training_hours": 120.5,
                "attendance_percentage": 95.5,
                "leaves_taken_this_year": 5
            }
        }


class MessageResponse(BaseModel):
    """Generic success message response"""
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation completed successfully"
            }
        }

