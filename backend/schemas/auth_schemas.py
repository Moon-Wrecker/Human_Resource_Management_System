"""
Pydantic schemas for authentication
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


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


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation completed successfully"
            }
        }

