"""
Centralized Pydantic Models for HRMS Backend
All request/response schemas in one file for better organization
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime, date, time
from enum import Enum


# ============================================================================
# AUTHENTICATION SCHEMAS
# ============================================================================

class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "sarah.johnson@company.com",
                "password": "password123"
            }
        }


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600
            }
        }


class UserInfoResponse(BaseModel):
    """User info included in token response"""
    id: int
    email: str
    name: str
    role: str
    employee_id: Optional[str] = None
    department_id: Optional[int] = None
    job_role: Optional[str] = None
    hierarchy_level: Optional[int] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "sarah.johnson@company.com",
                "name": "Sarah Johnson",
                "role": "HR",
                "employee_id": "EMP001",
                "department_id": 2,
                "job_role": "HR Manager",
                "hierarchy_level": 3
            }
        }


class LoginResponse(BaseModel):
    """Complete login response with tokens and user info"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserInfoResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600,
                "user": {
                    "id": 1,
                    "email": "sarah.johnson@company.com",
                    "name": "Sarah Johnson",
                    "role": "HR",
                    "employee_id": "EMP001",
                    "department_id": 2,
                    "job_role": "HR Manager",
                    "hierarchy_level": 3
                }
            }
        }


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str = Field(..., description="Valid refresh token")
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class ChangePasswordRequest(BaseModel):
    """Change password request schema"""
    current_password: str = Field(..., min_length=6, description="Current password")
    new_password: str = Field(..., min_length=6, description="New password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "oldpassword123",
                "new_password": "newpassword456"
            }
        }


class ResetPasswordRequest(BaseModel):
    """Reset password request schema (by HR/Manager)"""
    employee_id: int = Field(..., description="Employee ID to reset password for")
    new_password: str = Field(..., min_length=6, description="New temporary password")
    require_change_on_login: bool = Field(default=True, description="Force password change on next login")
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": 5,
                "new_password": "TempPass123!",
                "require_change_on_login": True
            }
        }


# ============================================================================
# DASHBOARD SCHEMAS
# ============================================================================

class HolidayInfo(BaseModel):
    """Holiday information"""
    id: int
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    is_mandatory: bool = True
    holiday_type: Optional[str] = None
    
    class Config:
        from_attributes = True


class AttendanceInfo(BaseModel):
    """Attendance check-in/out information"""
    date: date
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    status: str
    hours_worked: Optional[float] = None
    
    class Config:
        from_attributes = True


class LeaveBalanceInfo(BaseModel):
    """Leave balance information"""
    casual_leave: int = 0
    sick_leave: int = 0
    annual_leave: int = 0
    wfh_balance: int = 0


class DepartmentEmployeeCount(BaseModel):
    """Department with employee count"""
    department_id: int
    department_name: str
    employee_count: int


class DepartmentAttendance(BaseModel):
    """Department attendance statistics"""
    department_id: int
    department_name: str
    present_percentage: float = Field(..., ge=0, le=100)
    absent_percentage: float = Field(..., ge=0, le=100)


class DepartmentModulesCompleted(BaseModel):
    """Department skill modules completion"""
    department_id: int
    department_name: str
    modules_completed: int


class ActiveApplicationInfo(BaseModel):
    """Active job application info"""
    application_id: int
    applicant_name: str
    applied_role: str
    applied_date: datetime
    status: str
    source: Optional[str] = None
    
    class Config:
        from_attributes = True


class HRDashboardResponse(BaseModel):
    """Complete HR Dashboard data"""
    departments: List[DepartmentEmployeeCount]
    department_attendance: List[DepartmentAttendance]
    department_modules: List[DepartmentModulesCompleted]
    active_applications: List[ActiveApplicationInfo]
    total_employees: int
    total_departments: int
    total_active_applications: int


class TeamMemberAttendance(BaseModel):
    """Team member attendance statistics"""
    employee_id: int
    employee_name: str
    present_percentage: float = Field(..., ge=0, le=100)
    absent_percentage: float = Field(..., ge=0, le=100)


class TeamMemberModules(BaseModel):
    """Team member skill modules completion"""
    employee_id: int
    employee_name: str
    modules_completed: int


class TeamGoalsStats(BaseModel):
    """Team goals statistics"""
    total_goals: int
    completed_goals: int
    in_progress_goals: int
    not_started_goals: int
    completion_percentage: float = Field(..., ge=0, le=100)


class TeamStats(BaseModel):
    """Team statistics"""
    team_id: int
    team_name: str
    total_members: int
    team_training_hours: float
    team_performance_score: float


class ManagerDashboardResponse(BaseModel):
    """Complete Manager Dashboard data"""
    personal_info: LeaveBalanceInfo
    today_attendance: Optional[AttendanceInfo] = None
    upcoming_holidays: List[HolidayInfo]
    team_stats: Optional[TeamStats] = None
    team_goals: TeamGoalsStats
    team_attendance: List[TeamMemberAttendance]
    team_modules_leaderboard: List[TeamMemberModules]
    learner_rank: Optional[int] = None


class GoalStats(BaseModel):
    """Employee goals statistics"""
    total_goals: int
    completed_goals: int
    pending_goals: int
    completion_percentage: float = Field(..., ge=0, le=100)


class EmployeeDashboardResponse(BaseModel):
    """Complete Employee Dashboard data"""
    employee_name: str
    leave_balance: LeaveBalanceInfo
    today_attendance: Optional[AttendanceInfo] = None
    upcoming_holidays: List[HolidayInfo]
    learning_goals: GoalStats
    learner_rank: Optional[int] = None


class MonthlyModulesCompleted(BaseModel):
    """Monthly modules completion data for graphs"""
    month: str
    modules_completed: int


class PerformanceMetrics(BaseModel):
    """Employee performance metrics"""
    employee_id: int
    employee_name: str
    monthly_modules: List[MonthlyModulesCompleted]
    total_modules_completed: int
    attendance_rate: float = Field(..., ge=0, le=100)
    goals_completion_rate: float = Field(..., ge=0, le=100)


# ============================================================================
# PROFILE SCHEMAS
# ============================================================================

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
    
    # Personal Information
    date_of_birth: Optional[date] = None
    emergency_contact: Optional[str] = None
    
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


class UpdateProfileRequest(BaseModel):
    """Update profile request - only editable fields"""
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Full name")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")


class DocumentUploadResponse(BaseModel):
    """Response after document upload"""
    message: str
    document_type: str
    file_path: str
    file_url: str
    uploaded_at: datetime


class UserDocumentsResponse(BaseModel):
    """User's uploaded documents"""
    profile_image: Optional[dict] = None
    aadhar_card: Optional[dict] = None
    pan_card: Optional[dict] = None


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


class TeamResponse(BaseModel):
    """Complete team response with members"""
    team_id: Optional[int] = None
    team_name: Optional[str] = None
    department_name: Optional[str] = None
    total_members: int = 0
    members: list[TeamMemberResponse] = []


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


# ============================================================================
# ATTENDANCE SCHEMAS
# ============================================================================

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


# ============================================================================
# JOB LISTINGS SCHEMAS
# ============================================================================

class EmploymentTypeEnum(str, Enum):
    """Employment type options"""
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"


class JobStatusEnum(str, Enum):
    """Job listing status"""
    ACTIVE = "active"
    CLOSED = "closed"
    DRAFT = "draft"


class CreateJobRequest(BaseModel):
    """Request to create a new job listing"""
    position: str = Field(..., min_length=3, max_length=100, description="Job position/title")
    department_id: int = Field(..., description="Department ID")
    experience_required: Optional[str] = Field(default=None, max_length=50, description="Required experience (e.g., '2-4 years')")
    skills_required: Optional[str] = Field(default=None, description="Required skills (comma-separated)")
    description: Optional[str] = Field(default=None, description="Job description")
    location: Optional[str] = Field(default="Remote", max_length=100, description="Job location")
    employment_type: EmploymentTypeEnum = Field(default=EmploymentTypeEnum.FULL_TIME, description="Employment type")
    salary_range: Optional[str] = Field(default=None, max_length=50, description="Salary range (e.g., '5-7 LPA')")
    application_deadline: Optional[date] = Field(default=None, description="Application deadline")
    
    @validator('application_deadline')
    def deadline_must_be_future(cls, v):
        if v and v < date.today():
            raise ValueError('Application deadline must be in the future')
        return v


class UpdateJobRequest(BaseModel):
    """Request to update an existing job listing"""
    position: Optional[str] = Field(default=None, min_length=3, max_length=100, description="Job position/title")
    department_id: Optional[int] = Field(default=None, description="Department ID")
    experience_required: Optional[str] = Field(default=None, max_length=50, description="Required experience")
    skills_required: Optional[str] = Field(default=None, description="Required skills")
    description: Optional[str] = Field(default=None, description="Job description")
    location: Optional[str] = Field(default=None, max_length=100, description="Job location")
    employment_type: Optional[EmploymentTypeEnum] = Field(default=None, description="Employment type")
    salary_range: Optional[str] = Field(default=None, max_length=50, description="Salary range")
    application_deadline: Optional[date] = Field(default=None, description="Application deadline")
    is_active: Optional[bool] = Field(default=None, description="Job active status")
    
    @validator('application_deadline')
    def deadline_must_be_future(cls, v):
        if v and v < date.today():
            raise ValueError('Application deadline must be in the future')
        return v


class JobListingResponse(BaseModel):
    """Single job listing response"""
    id: int
    position: str
    department_id: int
    department_name: Optional[str] = None
    experience_required: Optional[str] = None
    skills_required: Optional[str] = None
    description: Optional[str] = None
    ai_generated_description: Optional[str] = None
    location: Optional[str] = None
    employment_type: str
    salary_range: Optional[str] = None
    is_active: bool
    posted_by: int
    posted_by_name: Optional[str] = None
    posted_date: datetime
    application_deadline: Optional[date] = None
    application_count: Optional[int] = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class JobListingsResponse(BaseModel):
    """Paginated list of job listings"""
    total: int = Field(..., description="Total number of jobs")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")
    jobs: List[JobListingResponse] = Field(..., description="List of job listings")


class JobFilters(BaseModel):
    """Filters for job listings"""
    department_id: Optional[int] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    is_active: Optional[bool] = True
    search: Optional[str] = None  # Search in position, description, skills


class GenerateJDRequest(BaseModel):
    """Request to generate job description using AI"""
    position: str = Field(..., description="Job position/title")
    department_id: int = Field(..., description="Department ID")
    experience_required: Optional[str] = Field(default=None, description="Required experience")
    skills_required: Optional[str] = Field(default=None, description="Required skills")


class GenerateJDResponse(BaseModel):
    """Response with AI-generated job description"""
    position: str
    generated_description: str
    suggestions: Optional[dict] = None


class JobStatisticsResponse(BaseModel):
    """Job statistics for HR dashboard"""
    total_jobs: int
    active_jobs: int
    closed_jobs: int
    total_applications: int
    applications_this_month: int
    top_departments: List[dict]  # [{"department": "Engineering", "job_count": 5}]


# ============================================================================
# JOB APPLICATIONS SCHEMAS
# ============================================================================

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


class ResumeUploadResponse(BaseModel):
    """Resume upload response"""
    message: str
    resume_path: str
    file_size: int


# ============================================================================
# COMMON/GENERIC SCHEMAS
# ============================================================================

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation completed successfully",
                "success": True
            }
        }

