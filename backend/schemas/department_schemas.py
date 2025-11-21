"""
Pydantic schemas for Department API
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Request Schemas
class DepartmentCreate(BaseModel):
    """Schema for creating department"""
    name: str = Field(..., min_length=2, max_length=100, description="Department name")
    code: Optional[str] = Field(None, max_length=20, description="Department code (e.g., ENG, HR)")
    description: Optional[str] = Field(None, description="Department description")
    head_id: Optional[int] = Field(None, gt=0, description="Department head user ID")


class DepartmentUpdate(BaseModel):
    """Schema for updating department"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    code: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    head_id: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None


# Response Schemas
class DepartmentResponse(BaseModel):
    """Schema for department response"""
    id: int
    name: str
    code: Optional[str]
    description: Optional[str]
    head_id: Optional[int]
    head_name: Optional[str]
    employee_count: int
    team_count: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class DepartmentDetailResponse(BaseModel):
    """Schema for detailed department response with teams"""
    id: int
    name: str
    code: Optional[str]
    description: Optional[str]
    head_id: Optional[int]
    head_name: Optional[str]
    employee_count: int
    team_count: int
    is_active: bool
    created_at: datetime
    teams: List[dict]  # List of team info
    
    class Config:
        from_attributes = True


class DepartmentListResponse(BaseModel):
    """Schema for list of departments"""
    departments: List[DepartmentResponse]
    total: int


class DepartmentStatsResponse(BaseModel):
    """Schema for department statistics"""
    total_departments: int
    active_departments: int
    total_employees: int
    total_teams: int
    departments_without_head: int
    largest_department: Optional[dict]


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str

