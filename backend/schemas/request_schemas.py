"""
Pydantic schemas for Team Requests API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


# Enums
class RequestTypeEnum(str, Enum):
    WFH = "wfh"
    LEAVE = "leave"
    EQUIPMENT = "equipment"
    TRAVEL = "travel"
    OTHER = "other"


class RequestStatusEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


# Request Schemas
class RequestCreate(BaseModel):
    """Schema for creating request"""
    request_type: RequestTypeEnum = Field(..., description="Type of request")
    subject: str = Field(..., min_length=3, max_length=200, description="Request subject")
    description: str = Field(..., min_length=10, description="Detailed description")
    request_date: Optional[date] = Field(None, description="Requested date (optional)")


class RequestUpdate(BaseModel):
    """Schema for updating request (employee, only if pending)"""
    subject: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    request_date: Optional[date] = None


class RequestStatusUpdate(BaseModel):
    """Schema for approving/rejecting request"""
    status: RequestStatusEnum = Field(..., description="New status (approved/rejected)")
    rejection_reason: Optional[str] = Field(None, description="Reason for rejection (required if rejecting)")
    
    @validator('rejection_reason')
    def validate_rejection_reason(cls, v, values):
        if 'status' in values and values['status'] == RequestStatusEnum.REJECTED and not v:
            raise ValueError('rejection_reason is required when rejecting request')
        return v


# Response Schemas
class RequestResponse(BaseModel):
    """Schema for request response"""
    id: int
    employee_id: int
    employee_name: Optional[str]
    
    # Request details
    request_type: str
    subject: str
    description: str
    request_date: Optional[date]
    
    # Approval workflow
    status: str
    approved_by: Optional[int]
    approved_by_name: Optional[str]
    approved_date: Optional[datetime]
    rejection_reason: Optional[str]
    
    # Timestamps
    submitted_date: datetime
    
    class Config:
        from_attributes = True


class RequestListResponse(BaseModel):
    """Schema for paginated request list"""
    requests: List[RequestResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class RequestStatsResponse(BaseModel):
    """Schema for request statistics"""
    total_requests: int
    pending_requests: int
    approved_requests: int
    rejected_requests: int
    by_request_type: dict
    by_status: dict
    by_month: dict


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str

