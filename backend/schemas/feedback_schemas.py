"""
Pydantic schemas for Feedback API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


# Request Schemas
class FeedbackCreate(BaseModel):
    """Schema for creating feedback"""
    employee_id: int = Field(..., description="ID of employee receiving feedback", gt=0)
    subject: str = Field(..., min_length=3, max_length=200, description="Feedback subject")
    description: str = Field(..., min_length=10, description="Detailed feedback")
    feedback_type: Optional[str] = Field(None, description="Type: positive, constructive, goal-related, performance")
    rating: Optional[float] = Field(None, ge=1.0, le=5.0, description="Rating (1-5)")
    
    @validator('feedback_type')
    def validate_feedback_type(cls, v):
        if v is not None:
            allowed_types = ['positive', 'constructive', 'goal-related', 'performance', 'general']
            if v not in allowed_types:
                raise ValueError(f'feedback_type must be one of: {", ".join(allowed_types)}')
        return v


class FeedbackUpdate(BaseModel):
    """Schema for updating feedback"""
    subject: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    feedback_type: Optional[str] = None
    rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    
    @validator('feedback_type')
    def validate_feedback_type(cls, v):
        if v is not None:
            allowed_types = ['positive', 'constructive', 'goal-related', 'performance', 'general']
            if v not in allowed_types:
                raise ValueError(f'feedback_type must be one of: {", ".join(allowed_types)}')
        return v


# Response Schemas
class FeedbackResponse(BaseModel):
    """Schema for feedback response"""
    id: int
    employee_id: int
    employee_name: str
    given_by: int
    given_by_name: str
    subject: str
    description: str
    feedback_type: Optional[str]
    rating: Optional[float]
    given_on: datetime
    
    class Config:
        from_attributes = True


class FeedbackListResponse(BaseModel):
    """Schema for list of feedback"""
    feedback: List[FeedbackResponse]
    total: int
    page: int
    page_size: int


class FeedbackStatsResponse(BaseModel):
    """Schema for feedback statistics"""
    total_feedback: int
    this_month: int
    this_quarter: int
    average_rating: Optional[float]
    by_type: dict
    recent_feedback: List[FeedbackResponse]


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str

