"""
Pydantic schemas for Employee Management API
"""
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from datetime import date, datetime


# Request Schemas
class EmployeeCreate(BaseModel):
    """Schema for creating new employee (HR only)"""
    # Basic Info
    name: str = Field(..., min_length=2, max_length=100, description="Employee name")
    email: EmailStr = Field(..., description="Employee email (must be unique)")
    password: str = Field(..., min_length=6, description="Initial password")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    
    # Work Info
    employee_id: Optional[str] = Field(None, description="Employee ID (auto-generated if not provided)")
    job_role: Optional[str] = Field(None, max_length=100, description="Job position/title")
    department_id: Optional[int] = Field(None, gt=0, description="Department ID")
    team_id: Optional[int] = Field(None, gt=0, description="Team ID")
    manager_id: Optional[int] = Field(None, gt=0, description="Manager user ID")
    
    # Role & Hierarchy
    role: str = Field(default="employee", description="User role: employee, manager, hr")
    hierarchy_level: Optional[int] = Field(None, ge=1, le=7, description="Hierarchy level (1=CEO, 7=Junior)")
    
    # Dates
    date_of_birth: Optional[date] = None
    hire_date: Optional[date] = None
    
    # Compensation
    salary: Optional[float] = Field(None, ge=0, description="Monthly salary")
    
    # Emergency Contact
    emergency_contact: Optional[str] = Field(None, description="Emergency contact details")
    
    # Leave Balances
    casual_leave_balance: int = Field(12, ge=0, description="Casual leave balance")
    sick_leave_balance: int = Field(12, ge=0, description="Sick leave balance")
    annual_leave_balance: int = Field(15, ge=0, description="Annual leave balance")
    wfh_balance: int = Field(24, ge=0, description="Work from home balance")
    
    @validator('role')
    def validate_role(cls, v):
        allowed_roles = ['employee', 'manager', 'hr', 'admin']
        if v.lower() not in allowed_roles:
            raise ValueError(f'role must be one of: {", ".join(allowed_roles)}')
        return v.lower()


class EmployeeUpdate(BaseModel):
    """Schema for updating employee (HR only)"""
    # Basic Info
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    
    # Work Info
    employee_id: Optional[str] = None
    job_role: Optional[str] = Field(None, max_length=100)
    department_id: Optional[int] = Field(None, gt=0)
    team_id: Optional[int] = Field(None, gt=0)
    manager_id: Optional[int] = Field(None, gt=0)
    
    # Role & Hierarchy
    role: Optional[str] = None
    hierarchy_level: Optional[int] = Field(None, ge=1, le=7)
    
    # Dates
    date_of_birth: Optional[date] = None
    hire_date: Optional[date] = None
    
    # Compensation
    salary: Optional[float] = Field(None, ge=0)
    
    # Status
    is_active: Optional[bool] = None
    
    # Emergency Contact
    emergency_contact: Optional[str] = None
    
    # Leave Balances
    casual_leave_balance: Optional[int] = Field(None, ge=0)
    sick_leave_balance: Optional[int] = Field(None, ge=0)
    annual_leave_balance: Optional[int] = Field(None, ge=0)
    wfh_balance: Optional[int] = Field(None, ge=0)
    
    @validator('role')
    def validate_role(cls, v):
        if v is not None:
            allowed_roles = ['employee', 'manager', 'hr', 'admin']
            if v.lower() not in allowed_roles:
                raise ValueError(f'role must be one of: {", ".join(allowed_roles)}')
            return v.lower()
        return v


# Response Schemas
class EmployeeResponse(BaseModel):
    """Schema for employee response"""
    id: int
    employee_id: Optional[str]
    name: str
    email: str
    phone: Optional[str]
    
    # Work Info
    job_role: Optional[str]
    department: Optional[str]  # Department name
    department_id: Optional[int]
    team: Optional[str]  # Team name
    team_id: Optional[int]
    manager: Optional[str]  # Manager name
    manager_id: Optional[int]
    
    # Role & Status
    role: str
    hierarchy_level: Optional[int]
    is_active: bool
    
    # Dates
    date_of_birth: Optional[date]
    hire_date: Optional[date]
    created_at: datetime
    
    # Compensation (only for HR view)
    salary: Optional[float] = None
    
    # Documents
    aadhar_document_path: Optional[str]
    pan_document_path: Optional[str]
    profile_image_path: Optional[str]
    
    # Emergency Contact
    emergency_contact: Optional[str]
    
    # Leave Balances
    casual_leave_balance: int
    sick_leave_balance: int
    annual_leave_balance: int
    wfh_balance: int
    
    class Config:
        from_attributes = True


class EmployeeListItem(BaseModel):
    """Schema for employee list item (summary)"""
    id: int
    employee_id: Optional[str]
    name: str
    email: str
    phone: Optional[str]
    job_role: Optional[str]
    department: Optional[str]
    team: Optional[str]
    manager: Optional[str]
    role: str
    is_active: bool
    hire_date: Optional[date]
    
    class Config:
        from_attributes = True


class EmployeeListResponse(BaseModel):
    """Schema for paginated employee list"""
    employees: List[EmployeeListItem]
    total: int
    page: int
    page_size: int
    total_pages: int


class EmployeeStatsResponse(BaseModel):
    """Schema for employee statistics"""
    total_employees: int
    active_employees: int
    inactive_employees: int
    by_department: dict
    by_role: dict
    by_team: dict
    recent_hires: int  # Last 30 days
    average_tenure_days: float


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str

