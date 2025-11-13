"""
Pydantic schemas for attendance management
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date, time
from enum import Enum


class AttendanceStatusEnum(str, Enum):
    """Attendance status options"""
    PRESENT = "present"
    ABSENT = "absent"
    LEAVE = "leave"
    WFH = "wfh"
    HOLIDAY = "holiday"


class PunchInRequest(BaseModel):
    """Request to punch in"""
    location: Optional[str] = Field(default="office", description="Location: office, home, client-site")
    status: AttendanceStatusEnum = Field(default=AttendanceStatusEnum.PRESENT, description="Attendance type: present or wfh")
    notes: Optional[str] = Field(default=None, max_length=500, description="Additional notes")


class PunchOutRequest(BaseModel):
    """Request to punch out"""
    notes: Optional[str] = Field(default=None, max_length=500, description="Additional notes")


class AttendanceRecordResponse(BaseModel):
    """Single attendance record response"""
    id: int
    employee_id: int
    employee_name: Optional[str] = None
    employee_employee_id: Optional[str] = None  # Employee ID code like EMP001
    date: date
    status: str
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    hours_worked: Optional[float] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PunchInResponse(BaseModel):
    """Response after successful punch in"""
    message: str
    attendance: AttendanceRecordResponse
    already_punched_in: bool = False


class PunchOutResponse(BaseModel):
    """Response after successful punch out"""
    message: str
    attendance: AttendanceRecordResponse
    hours_worked: float


class AttendanceHistoryResponse(BaseModel):
    """Attendance history with pagination"""
    total: int
    page: int
    page_size: int
    total_pages: int
    records: List[AttendanceRecordResponse]


class AttendanceSummaryResponse(BaseModel):
    """Monthly attendance summary"""
    employee_id: int
    employee_name: str
    month: int
    year: int
    
    # Counts
    total_present: int = 0
    total_absent: int = 0
    total_leave: int = 0
    total_wfh: int = 0
    total_holiday: int = 0
    total_working_days: int
    
    # Time statistics
    total_hours_worked: float = 0
    average_hours_per_day: float = 0
    late_arrivals: int = 0  # After 9:30 AM
    early_departures: int = 0  # Before 5:30 PM
    
    # Percentages
    attendance_percentage: float = 0
    
    # Date range
    from_date: date
    to_date: date


class TeamAttendanceRecord(BaseModel):
    """Team member attendance record for managers"""
    employee_id: int
    employee_name: str
    employee_employee_id: str
    job_role: Optional[str] = None
    date: date
    status: str
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    hours_worked: Optional[float] = None
    location: Optional[str] = None


class TeamAttendanceResponse(BaseModel):
    """Team attendance overview"""
    date: date
    total_team_members: int
    present: int
    absent: int
    on_leave: int
    wfh: int
    records: List[TeamAttendanceRecord]


class MarkAttendanceRequest(BaseModel):
    """HR request to manually mark attendance"""
    employee_id: int = Field(..., description="Employee ID to mark attendance for")
    attendance_date: date = Field(..., description="Date for attendance")
    status: AttendanceStatusEnum = Field(..., description="Attendance status")
    check_in_time: Optional[datetime] = Field(default=None, description="Check-in time (optional)")
    check_out_time: Optional[datetime] = Field(default=None, description="Check-out time (optional)")
    location: Optional[str] = Field(default="office", description="Location")
    notes: Optional[str] = Field(default=None, max_length=500, description="Reason for manual entry")
    
    @validator('check_out_time')
    def check_out_after_check_in(cls, v, values):
        if v and values.get('check_in_time') and v < values['check_in_time']:
            raise ValueError('Check-out time must be after check-in time')
        return v


class MarkAttendanceResponse(BaseModel):
    """Response after marking attendance"""
    message: str
    attendance: AttendanceRecordResponse
    marked_by: str


class AllAttendanceFilters(BaseModel):
    """Filters for HR to view all attendance"""
    date: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    department_id: Optional[int] = None
    team_id: Optional[int] = None
    status: Optional[AttendanceStatusEnum] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=100)


class DepartmentAttendanceStats(BaseModel):
    """Department-wise attendance statistics"""
    department_id: int
    department_name: str
    total_employees: int
    present: int
    absent: int
    on_leave: int
    wfh: int
    attendance_percentage: float


class AllAttendanceResponse(BaseModel):
    """All attendance overview for HR"""
    date: date
    total_employees: int
    present: int
    absent: int
    on_leave: int
    wfh: int
    
    department_stats: List[DepartmentAttendanceStats]
    records: List[AttendanceRecordResponse]
    
    # Pagination
    total_records: int
    page: int
    page_size: int
    total_pages: int


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True

