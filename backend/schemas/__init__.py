"""
Pydantic schemas for API request/response validation
"""
from .auth_schemas import (
    LoginRequest,
    LoginResponse,
    TokenResponse,
    UserInfoResponse,
    RefreshTokenRequest,
    ChangePasswordRequest,
    ResetPasswordRequest,
    MessageResponse
)

from .dashboard_schemas import (
    HRDashboardResponse,
    ManagerDashboardResponse,
    EmployeeDashboardResponse,
    PerformanceMetrics,
    HolidayInfo,
    LeaveBalanceInfo,
    AttendanceInfo
)

__all__ = [
    # Auth schemas
    "LoginRequest",
    "LoginResponse",
    "TokenResponse",
    "UserInfoResponse",
    "RefreshTokenRequest",
    "ChangePasswordRequest",
    "ResetPasswordRequest",
    "MessageResponse",
    # Dashboard schemas
    "HRDashboardResponse",
    "ManagerDashboardResponse",
    "EmployeeDashboardResponse",
    "PerformanceMetrics",
    "HolidayInfo",
    "LeaveBalanceInfo",
    "AttendanceInfo"
]

