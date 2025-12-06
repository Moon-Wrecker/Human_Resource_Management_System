"""
Dashboard API Routes
Endpoints for HR, Manager, and Employee dashboards
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from datetime import date

from database import get_db
from models import User, UserRole
from utils.dependencies import (
    get_current_active_user,
    require_hr,
    require_manager,
    require_employee,
)
from services.dashboard_service import DashboardService
from pydantic_models import (
    HRDashboardResponse,
    ManagerDashboardResponse,
    EmployeeDashboardResponse,
    PerformanceMetrics,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# ==================== HR Dashboard Endpoints ====================


@router.get(
    "/hr",
    response_model=HRDashboardResponse,
    status_code=status.HTTP_200_OK,
    summary="Get HR Dashboard Data",
    description="Get complete dashboard data for HR including departments, attendance, applications",
    responses={
        200: {
            "description": "HR dashboard data retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "departments": [
                            {
                                "department_id": 1,
                                "department_name": "Engineering",
                                "employee_count": 20,
                            }
                        ],
                        "department_attendance": [
                            {
                                "department_id": 1,
                                "department_name": "Engineering",
                                "present_percentage": 85.5,
                                "absent_percentage": 14.5,
                            }
                        ],
                        "department_modules": [
                            {
                                "department_id": 1,
                                "department_name": "Engineering",
                                "modules_completed": 45,
                            }
                        ],
                        "active_applications": [
                            {
                                "application_id": 1,
                                "applicant_name": "John Doe",
                                "applied_role": "Software Engineer",
                                "applied_date": "2025-11-10T10:00:00",
                                "status": "pending",
                                "source": "referral",
                            }
                        ],
                        "total_employees": 57,
                        "total_departments": 5,
                        "total_active_applications": 10,
                    }
                }
            },
        },
        403: {"description": "Access forbidden - HR role required"},
    },
)
async def get_hr_dashboard(
    current_user: Annotated[User, Depends(require_hr)], db: Session = Depends(get_db)
):
    """
    ## HR Dashboard

    Get comprehensive dashboard data for HR users including:
    - Department-wise employee counts
    - Department-wise attendance statistics
    - Department-wise skill modules completion
    - Active job applications
    - Overall statistics

    **Access:** HR only
    """
    try:
        dashboard_data = DashboardService.get_hr_dashboard_data(db)
        return dashboard_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch HR dashboard data: {str(e)}",
        )


# ==================== Manager Dashboard Endpoints ====================


@router.get(
    "/manager",
    response_model=ManagerDashboardResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Manager Dashboard Data",
    description="Get complete dashboard data for Manager including personal info and team overview",
    responses={
        200: {
            "description": "Manager dashboard data retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "personal_info": {
                            "casual_leave": 8,
                            "sick_leave": 10,
                            "annual_leave": 12,
                            "wfh_balance": 8,
                        },
                        "today_attendance": {
                            "date": "2025-11-13",
                            "check_in_time": "2025-11-13T09:04:00",
                            "check_out_time": None,
                            "status": "present",
                            "hours_worked": None,
                        },
                        "upcoming_holidays": [],
                        "team_stats": {
                            "team_id": 1,
                            "team_name": "Backend Team",
                            "total_members": 8,
                            "team_training_hours": 1300.0,
                            "team_performance_score": 3.9,
                        },
                        "team_goals": {
                            "total_goals": 20,
                            "completed_goals": 15,
                            "in_progress_goals": 3,
                            "not_started_goals": 2,
                            "completion_percentage": 75.0,
                        },
                        "team_attendance": [],
                        "team_modules_leaderboard": [],
                        "learner_rank": 3,
                    }
                }
            },
        },
        403: {"description": "Access forbidden - Manager role required"},
    },
)
async def get_manager_dashboard(
    current_user: Annotated[User, Depends(require_manager)],
    db: Session = Depends(get_db),
):
    """
    ## Manager Dashboard

    Get comprehensive dashboard data for Manager users including:
    - Personal information (leave balance, attendance)
    - Upcoming holidays
    - Team statistics
    - Team goals progress
    - Team member attendance
    - Team learning leaderboard
    - Personal learner rank

    **Access:** Manager only
    """
    try:
        dashboard_data = DashboardService.get_manager_dashboard_data(db, current_user)
        return dashboard_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch Manager dashboard data: {str(e)}",
        )


# ==================== Employee Dashboard Endpoints ====================


@router.get(
    "/employee",
    response_model=EmployeeDashboardResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Employee Dashboard Data",
    description="Get complete dashboard data for Employee including personal info and learning goals",
    responses={
        200: {
            "description": "Employee dashboard data retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "employee_name": "John Doe",
                        "leave_balance": {
                            "casual_leave": 8,
                            "sick_leave": 10,
                            "annual_leave": 12,
                            "wfh_balance": 8,
                        },
                        "today_attendance": {
                            "date": "2025-11-13",
                            "check_in_time": "2025-11-13T09:04:00",
                            "check_out_time": None,
                            "status": "present",
                            "hours_worked": None,
                        },
                        "upcoming_holidays": [
                            {
                                "id": 1,
                                "name": "Diwali",
                                "description": "Festival of Lights",
                                "start_date": "2025-11-01",
                                "end_date": "2025-11-01",
                                "is_mandatory": True,
                                "holiday_type": "festival",
                            }
                        ],
                        "learning_goals": {
                            "total_goals": 5,
                            "completed_goals": 4,
                            "pending_goals": 1,
                            "completion_percentage": 80.0,
                        },
                        "learner_rank": 3,
                    }
                }
            },
        },
        403: {"description": "Access forbidden - Employee role required"},
    },
)
async def get_employee_dashboard(
    current_user: Annotated[User, Depends(require_employee)],
    db: Session = Depends(get_db),
):
    """
    ## Employee Dashboard

    Get comprehensive dashboard data for Employee users including:
    - Employee name
    - Leave balance (casual, sick, annual, WFH)
    - Today's attendance (check-in/out times)
    - Upcoming holidays
    - Learning goals statistics
    - Personal learner rank

    **Access:** Employee only
    """
    try:
        dashboard_data = DashboardService.get_employee_dashboard_data(db, current_user)
        return dashboard_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch Employee dashboard data: {str(e)}",
        )


# ==================== Common/Shared Endpoints ====================


@router.get(
    "/me",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Get Dashboard Data for Current User",
    description="Automatically routes to appropriate dashboard based on user role",
    responses={200: {"description": "Dashboard data retrieved successfully"}},
)
async def get_my_dashboard(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    """
    ## My Dashboard

    Get dashboard data for the currently authenticated user.
    Automatically routes to the appropriate dashboard based on user role:
    - HR users get HR dashboard
    - Manager users get Manager dashboard
    - Employee users get Employee dashboard

    **Access:** All authenticated users
    """
    try:
        if current_user.role == UserRole.HR:
            dashboard_data = DashboardService.get_hr_dashboard_data(db)
        elif current_user.role == UserRole.MANAGER:
            dashboard_data = DashboardService.get_manager_dashboard_data(
                db, current_user
            )
        elif current_user.role == UserRole.EMPLOYEE:
            dashboard_data = DashboardService.get_employee_dashboard_data(
                db, current_user
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user role"
            )

        return {"role": current_user.role.value, "dashboard_data": dashboard_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch dashboard data: {str(e)}",
        )


# ==================== Performance/Analytics Endpoints ====================


@router.get(
    "/performance/me",
    response_model=PerformanceMetrics,
    status_code=status.HTTP_200_OK,
    summary="Get My Performance Metrics",
    description="Get performance metrics for the current user with optional date filtering",
)
async def get_my_performance(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
    start_date: Optional[date] = Query(default=None, description="Start date for performance data (optional)"),
    end_date: Optional[date] = Query(default=None, description="End date for performance data (optional, default: today)"),
    months: int = Query(default=12, ge=1, le=24, description="Number of months of data to retrieve (used if start_date not provided)")
):
    """
    ## My Performance Metrics
    
    Get detailed performance metrics for the currently authenticated user.
    
    **Query Parameters:**
    - `start_date`: Start date for data range (optional, overrides months parameter)
    - `end_date`: End date for data range (optional, defaults to today)
    - `months`: Number of months back from today (used if start_date not provided)
    
    **Access:** All authenticated users
    """
    try:
        performance_data = DashboardService.get_employee_performance_metrics(
            db, current_user.id, start_date, end_date, months
        )
        return performance_data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch performance metrics: {str(e)}"
        )


@router.get(
    "/performance/{employee_id}",
    response_model=PerformanceMetrics,
    status_code=status.HTTP_200_OK,
    summary="Get Employee Performance Metrics",
    description="Get detailed performance metrics for an employee including monthly module completion",
    responses={
        200: {"description": "Performance metrics retrieved successfully"},
        403: {
            "description": "Access forbidden - Cannot view other employee's performance"
        },
        404: {"description": "Employee not found"},
    },
)
async def get_employee_performance(
    employee_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
    months: int = Query(
        default=12, ge=1, le=24, description="Number of months of data to retrieve"
    ),
):
    """
    ## Employee Performance Metrics

    Get detailed performance metrics for an employee including:
    - Monthly module completion trend
    - Total modules completed
    - Attendance rate
    - Goals completion rate

    **Access Control:**
    - HR can view any employee's performance
    - Manager can view their team members' performance
    - Employee can only view their own performance
    """
    try:
        # Check access permissions
        if current_user.role == UserRole.HR:
            # HR can view anyone
            pass
        elif current_user.role == UserRole.MANAGER:
            # Manager can view their team members
            employee = db.query(User).filter(User.id == employee_id).first()
            if not employee:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
                )
            if employee.manager_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only view performance of your team members",
                )
        elif current_user.role == UserRole.EMPLOYEE:
            # Employee can only view their own
            if employee_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only view your own performance",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user role"
            )

        performance_data = DashboardService.get_employee_performance_metrics(
            db, employee_id, months
        )
        return performance_data

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch performance metrics: {str(e)}",
        )
