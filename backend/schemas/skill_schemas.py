"""
Pydantic schemas for Skills/Modules Management API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


# Enums
class ModuleStatusEnum(str, Enum):
    NOT_STARTED = "not_started"
    PENDING = "pending"
    COMPLETED = "completed"


class DifficultyLevelEnum(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


# Module Schemas
class SkillModuleCreate(BaseModel):
    """Schema for creating skill module (HR only)"""
    name: str = Field(..., min_length=3, max_length=200, description="Module name")
    description: Optional[str] = Field(None, description="Module description")
    category: Optional[str] = Field(None, max_length=100, description="Module category")
    module_link: Optional[str] = Field(None, max_length=500, description="External module link")
    duration_hours: Optional[float] = Field(None, ge=0, description="Duration in hours")
    difficulty_level: Optional[DifficultyLevelEnum] = Field(None, description="Difficulty level")
    skill_areas: Optional[str] = Field(None, description="Comma-separated skill areas")
    is_active: bool = Field(True, description="Module active status")


class SkillModuleUpdate(BaseModel):
    """Schema for updating skill module (HR only)"""
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    module_link: Optional[str] = Field(None, max_length=500)
    duration_hours: Optional[float] = Field(None, ge=0)
    difficulty_level: Optional[DifficultyLevelEnum] = None
    skill_areas: Optional[str] = None
    is_active: Optional[bool] = None


class SkillModuleResponse(BaseModel):
    """Schema for skill module response"""
    id: int
    name: str
    description: Optional[str]
    category: Optional[str]
    module_link: Optional[str]
    duration_hours: Optional[float]
    difficulty_level: Optional[str]
    skill_areas: Optional[str]
    is_active: bool
    created_at: datetime
    
    # Enrollment stats
    total_enrollments: Optional[int] = 0
    completed_count: Optional[int] = 0
    
    class Config:
        from_attributes = True


class SkillModuleListResponse(BaseModel):
    """Schema for paginated module list"""
    modules: List[SkillModuleResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# Enrollment Schemas
class EnrollmentCreate(BaseModel):
    """Schema for enrolling in a module"""
    module_id: int = Field(..., gt=0, description="Module ID to enroll in")
    target_completion_date: Optional[date] = Field(None, description="Target completion date")


class EnrollmentProgressUpdate(BaseModel):
    """Schema for updating enrollment progress"""
    progress_percentage: float = Field(..., ge=0, le=100, description="Progress percentage (0-100)")
    status: Optional[ModuleStatusEnum] = Field(None, description="Module status")
    
    @validator('status')
    def validate_status_with_progress(cls, v, values):
        if v == ModuleStatusEnum.COMPLETED and 'progress_percentage' in values:
            if values['progress_percentage'] < 100:
                raise ValueError('progress_percentage must be 100 when marking as completed')
        return v


class EnrollmentCompleteRequest(BaseModel):
    """Schema for marking module as complete"""
    score: Optional[float] = Field(None, ge=0, le=100, description="Score/grade (0-100)")
    certificate_path: Optional[str] = Field(None, description="Path to certificate file")


class EnrollmentResponse(BaseModel):
    """Schema for enrollment response"""
    id: int
    employee_id: int
    employee_name: Optional[str]
    module_id: int
    module_name: Optional[str]
    
    # Progress tracking
    status: str
    progress_percentage: float
    enrolled_date: date
    started_date: Optional[date]
    completed_date: Optional[date]
    target_completion_date: Optional[date]
    
    # Results
    certificate_path: Optional[str]
    score: Optional[float]
    
    created_at: datetime
    
    class Config:
        from_attributes = True


class MyEnrollmentResponse(BaseModel):
    """Schema for my enrollments with module details"""
    id: int
    module_id: int
    module_name: str
    module_description: Optional[str]
    module_link: Optional[str]
    category: Optional[str]
    duration_hours: Optional[float]
    difficulty_level: Optional[str]
    
    # My progress
    status: str
    progress_percentage: float
    enrolled_date: date
    started_date: Optional[date]
    completed_date: Optional[date]
    target_completion_date: Optional[date]
    score: Optional[float]
    certificate_path: Optional[str]
    
    class Config:
        from_attributes = True


class EnrollmentListResponse(BaseModel):
    """Schema for paginated enrollment list"""
    enrollments: List[EnrollmentResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class SkillStatsResponse(BaseModel):
    """Schema for skills statistics"""
    total_modules: int
    active_modules: int
    total_enrollments: int
    completed_enrollments: int
    in_progress_enrollments: int
    by_category: dict
    by_difficulty: dict
    by_status: dict
    average_completion_rate: float


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str

