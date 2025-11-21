"""
Pydantic schemas for dashboard APIs
All dashboard data structures for HR, Manager, and Employee dashboards
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date


# ==================== Common/Shared Schemas ====================

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
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Diwali",
                "description": "Festival of Lights",
                "start_date": "2025-11-01",
                "end_date": "2025-11-01",
                "is_mandatory": True,
                "holiday_type": "festival"
            }
        }


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
    
    class Config:
        json_schema_extra = {
            "example": {
                "casual_leave": 8,
                "sick_leave": 10,
                "annual_leave": 12,
                "wfh_balance": 8
            }
        }


# ==================== HR Dashboard Schemas ====================

class DepartmentEmployeeCount(BaseModel):
    """Department with employee count"""
    department_id: int
    department_name: str
    employee_count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "department_id": 1,
                "department_name": "Engineering",
                "employee_count": 20
            }
        }


class DepartmentAttendance(BaseModel):
    """Department attendance statistics"""
    department_id: int
    department_name: str
    present_percentage: float = Field(..., ge=0, le=100)
    absent_percentage: float = Field(..., ge=0, le=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "department_id": 1,
                "department_name": "Engineering",
                "present_percentage": 85.5,
                "absent_percentage": 14.5
            }
        }


class DepartmentModulesCompleted(BaseModel):
    """Department skill modules completion"""
    department_id: int
    department_name: str
    modules_completed: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "department_id": 1,
                "department_name": "Engineering",
                "modules_completed": 45
            }
        }


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
        json_schema_extra = {
            "example": {
                "application_id": 1,
                "applicant_name": "John Doe",
                "applied_role": "Software Engineer",
                "applied_date": "2025-11-10T10:00:00",
                "status": "pending",
                "source": "referral"
            }
        }


class HRDashboardResponse(BaseModel):
    """Complete HR Dashboard data"""
    departments: List[DepartmentEmployeeCount]
    department_attendance: List[DepartmentAttendance]
    department_modules: List[DepartmentModulesCompleted]
    active_applications: List[ActiveApplicationInfo]
    total_employees: int
    total_departments: int
    total_active_applications: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "departments": [
                    {
                        "department_id": 1,
                        "department_name": "Engineering",
                        "employee_count": 20
                    }
                ],
                "department_attendance": [
                    {
                        "department_id": 1,
                        "department_name": "Engineering",
                        "present_percentage": 85.5,
                        "absent_percentage": 14.5
                    }
                ],
                "department_modules": [
                    {
                        "department_id": 1,
                        "department_name": "Engineering",
                        "modules_completed": 45
                    }
                ],
                "active_applications": [
                    {
                        "application_id": 1,
                        "applicant_name": "John Doe",
                        "applied_role": "Software Engineer",
                        "applied_date": "2025-11-10T10:00:00",
                        "status": "pending",
                        "source": "referral"
                    }
                ],
                "total_employees": 57,
                "total_departments": 5,
                "total_active_applications": 10
            }
        }


# ==================== Manager Dashboard Schemas ====================

class TeamMemberAttendance(BaseModel):
    """Team member attendance statistics"""
    employee_id: int
    employee_name: str
    present_percentage: float = Field(..., ge=0, le=100)
    absent_percentage: float = Field(..., ge=0, le=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": 5,
                "employee_name": "Alice Smith",
                "present_percentage": 90.0,
                "absent_percentage": 10.0
            }
        }


class TeamMemberModules(BaseModel):
    """Team member skill modules completion"""
    employee_id: int
    employee_name: str
    modules_completed: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": 5,
                "employee_name": "Alice Smith",
                "modules_completed": 12
            }
        }


class TeamGoalsStats(BaseModel):
    """Team goals statistics"""
    total_goals: int
    completed_goals: int
    in_progress_goals: int
    not_started_goals: int
    completion_percentage: float = Field(..., ge=0, le=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_goals": 20,
                "completed_goals": 15,
                "in_progress_goals": 3,
                "not_started_goals": 2,
                "completion_percentage": 75.0
            }
        }


class TeamStats(BaseModel):
    """Team statistics"""
    team_id: int
    team_name: str
    total_members: int
    team_training_hours: float
    team_performance_score: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "team_id": 1,
                "team_name": "Backend Team",
                "total_members": 8,
                "team_training_hours": 1300.0,
                "team_performance_score": 3.9
            }
        }


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
    
    class Config:
        json_schema_extra = {
            "example": {
                "personal_info": {
                    "casual_leave": 8,
                    "sick_leave": 10,
                    "annual_leave": 12,
                    "wfh_balance": 8
                },
                "today_attendance": {
                    "date": "2025-11-13",
                    "check_in_time": "2025-11-13T09:04:00",
                    "check_out_time": None,
                    "status": "present",
                    "hours_worked": None
                },
                "upcoming_holidays": [],
                "team_stats": {
                    "team_id": 1,
                    "team_name": "Backend Team",
                    "total_members": 8,
                    "team_training_hours": 1300.0,
                    "team_performance_score": 3.9
                },
                "team_goals": {
                    "total_goals": 20,
                    "completed_goals": 15,
                    "in_progress_goals": 3,
                    "not_started_goals": 2,
                    "completion_percentage": 75.0
                },
                "team_attendance": [],
                "team_modules_leaderboard": [],
                "learner_rank": 3
            }
        }


# ==================== Employee Dashboard Schemas ====================

class GoalStats(BaseModel):
    """Employee goals statistics"""
    total_goals: int
    completed_goals: int
    pending_goals: int
    completion_percentage: float = Field(..., ge=0, le=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_goals": 5,
                "completed_goals": 4,
                "pending_goals": 1,
                "completion_percentage": 80.0
            }
        }


class EmployeeDashboardResponse(BaseModel):
    """Complete Employee Dashboard data"""
    employee_name: str
    leave_balance: LeaveBalanceInfo
    today_attendance: Optional[AttendanceInfo] = None
    upcoming_holidays: List[HolidayInfo]
    learning_goals: GoalStats
    learner_rank: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_name": "John Doe",
                "leave_balance": {
                    "casual_leave": 8,
                    "sick_leave": 10,
                    "annual_leave": 12,
                    "wfh_balance": 8
                },
                "today_attendance": {
                    "date": "2025-11-13",
                    "check_in_time": "2025-11-13T09:04:00",
                    "check_out_time": None,
                    "status": "present",
                    "hours_worked": None
                },
                "upcoming_holidays": [
                    {
                        "id": 1,
                        "name": "Diwali",
                        "description": "Festival of Lights",
                        "start_date": "2025-11-01",
                        "end_date": "2025-11-01",
                        "is_mandatory": True,
                        "holiday_type": "festival"
                    }
                ],
                "learning_goals": {
                    "total_goals": 5,
                    "completed_goals": 4,
                    "pending_goals": 1,
                    "completion_percentage": 80.0
                },
                "learner_rank": 3
            }
        }


# ==================== Stats/Analytics Schemas ====================

class MonthlyModulesCompleted(BaseModel):
    """Monthly modules completion data for graphs"""
    month: str
    modules_completed: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "month": "January",
                "modules_completed": 5
            }
        }


class PerformanceMetrics(BaseModel):
    """Employee performance metrics"""
    employee_id: int
    employee_name: str
    monthly_modules: List[MonthlyModulesCompleted]
    total_modules_completed: int
    attendance_rate: float = Field(..., ge=0, le=100)
    goals_completion_rate: float = Field(..., ge=0, le=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": 5,
                "employee_name": "John Doe",
                "monthly_modules": [
                    {"month": "January", "modules_completed": 3},
                    {"month": "February", "modules_completed": 5}
                ],
                "total_modules_completed": 25,
                "attendance_rate": 95.5,
                "goals_completion_rate": 80.0
            }
        }


