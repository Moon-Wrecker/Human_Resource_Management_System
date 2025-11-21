"""
Pydantic schemas for Holiday API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime


# Request Schemas
class HolidayCreate(BaseModel):
    """Schema for creating holiday"""
    name: str = Field(..., min_length=3, max_length=100, description="Holiday name")
    description: Optional[str] = Field(None, description="Holiday description")
    start_date: date = Field(..., description="Holiday start date")
    end_date: date = Field(..., description="Holiday end date")
    is_mandatory: bool = Field(True, description="Is this a mandatory holiday")
    holiday_type: Optional[str] = Field(None, description="Type: national, religious, company, regional")
    
    @validator('end_date')
    def validate_dates(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be on or after start_date')
        return v
    
    @validator('holiday_type')
    def validate_holiday_type(cls, v):
        if v is not None:
            allowed_types = ['national', 'religious', 'company', 'regional', 'optional']
            if v not in allowed_types:
                raise ValueError(f'holiday_type must be one of: {", ".join(allowed_types)}')
        return v


class HolidayUpdate(BaseModel):
    """Schema for updating holiday"""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_mandatory: Optional[bool] = None
    holiday_type: Optional[str] = None
    is_active: Optional[bool] = None
    
    @validator('holiday_type')
    def validate_holiday_type(cls, v):
        if v is not None:
            allowed_types = ['national', 'religious', 'company', 'regional', 'optional']
            if v not in allowed_types:
                raise ValueError(f'holiday_type must be one of: {", ".join(allowed_types)}')
        return v


# Response Schemas
class HolidayResponse(BaseModel):
    """Schema for holiday response"""
    id: int
    name: str
    description: Optional[str]
    start_date: date
    end_date: date
    is_mandatory: bool
    holiday_type: Optional[str]
    is_active: bool
    created_by: Optional[int]
    created_by_name: Optional[str]
    created_at: datetime
    duration_days: int
    
    class Config:
        from_attributes = True


class HolidayListResponse(BaseModel):
    """Schema for list of holidays"""
    holidays: List[HolidayResponse]
    total: int
    page: int
    page_size: int


class HolidayStatsResponse(BaseModel):
    """Schema for holiday statistics"""
    total_holidays: int
    mandatory_holidays: int
    optional_holidays: int
    upcoming_holidays: int
    holidays_this_month: int
    holidays_this_year: int
    by_type: dict


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str

