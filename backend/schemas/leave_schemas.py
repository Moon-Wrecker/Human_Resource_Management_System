"""
Pydantic schemas for Leave Management API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


# Enums
class LeaveTypeEnum(str, Enum):
    CASUAL = "casual"
    SICK = "sick"
    ANNUAL = "annual"
    MATERNITY = "maternity"
    PATERNITY = "paternity"


class LeaveStatusEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


# Request Schemas
class LeaveRequestCreate(BaseModel):
    """Schema for creating leave request"""
    leave_type: LeaveTypeEnum = Field(..., description="Type of leave")
    start_date: date = Field(..., description="Leave start date")
    end_date: date = Field(..., description="Leave end date")
    subject: Optional[str] = Field(None, max_length=200, description="Request subject")
    reason: Optional[str] = Field(None, description="Reason for leave")
    description: Optional[str] = Field(None, description="Detailed description")
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be on or after start_date')
        return v


class LeaveRequestUpdate(BaseModel):
    """Schema for updating leave request (before approval)"""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    subject: Optional[str] = Field(None, max_length=200)
    reason: Optional[str] = None
    description: Optional[str] = None
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v is not None and 'start_date' in values and values['start_date'] is not None:
            if v < values['start_date']:
                raise ValueError('end_date must be on or after start_date')
        return v


class LeaveStatusUpdate(BaseModel):
    """Schema for approving/rejecting leave"""
    status: LeaveStatusEnum = Field(..., description="New status")
    rejection_reason: Optional[str] = Field(None, description="Reason for rejection (required if rejecting)")
    
    @validator('rejection_reason')
    def validate_rejection_reason(cls, v, values):
        if 'status' in values and values['status'] == LeaveStatusEnum.REJECTED and not v:
            raise ValueError('rejection_reason is required when rejecting leave')
        return v


# Response Schemas
class LeaveRequestResponse(BaseModel):
    """Schema for leave request response"""
    id: int
    employee_id: int
    employee_name: Optional[str]
    
    # Leave details
    leave_type: str
    start_date: date
    end_date: date
    days_requested: int
    
    # Request details
    subject: Optional[str]
    reason: Optional[str]
    description: Optional[str]
    
    # Approval workflow
    status: str
    approved_by: Optional[int]
    approved_by_name: Optional[str]
    approved_date: Optional[datetime]
    rejection_reason: Optional[str]
    
    # Timestamps
    requested_date: datetime
    
    class Config:
        from_attributes = True


class LeaveBalanceResponse(BaseModel):
    """Schema for leave balance response"""
    employee_id: int
    employee_name: str
    casual_leave_balance: int
    sick_leave_balance: int
    annual_leave_balance: int
    wfh_balance: int
    
    class Config:
        from_attributes = True


class LeaveListResponse(BaseModel):
    """Schema for paginated leave list"""
    leaves: List[LeaveRequestResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class LeaveStatsResponse(BaseModel):
    """Schema for leave statistics"""
    total_requests: int
    pending_requests: int
    approved_requests: int
    rejected_requests: int
    by_leave_type: dict
    by_status: dict
    by_month: dict


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str

