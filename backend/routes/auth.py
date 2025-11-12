"""
Authentication routes - Login, token refresh, password management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from services.auth_service import AuthService
from schemas.auth_schemas import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    TokenResponse,
    ChangePasswordRequest,
    ResetPasswordRequest,
    MessageResponse
)
from models import User, UserRole
from typing import Annotated

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


# Dependency to get current user from token
async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user
    """
    token = credentials.credentials
    user = AuthService.get_current_user(db, token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


# Dependency to check if user is HR or Manager
async def require_hr_or_manager(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    Dependency to ensure user is HR or Manager
    """
    if current_user.role not in [UserRole.HR, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR or Manager can perform this action"
        )
    return current_user


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="User Login",
    description="Authenticate user with email and password, returns JWT tokens and user info",
    responses={
        200: {
            "description": "Login successful",
            "content": {
                "application/json": {
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
            }
        },
        401: {"description": "Invalid credentials or user inactive"}
    }
)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    ## User Login
    
    Authenticate user and return JWT access token and refresh token.
    
    **Note**: There is no public signup. HR/Manager adds employees to the system.
    
    ### Request Body:
    - **email**: User email address
    - **password**: User password
    
    ### Response:
    - **access_token**: JWT token for API authentication (expires in 60 minutes)
    - **refresh_token**: Token to get new access token (expires in 30 days)
    - **token_type**: Always "bearer"
    - **expires_in**: Access token expiration time in seconds
    - **user**: User information object
    
    ### Test Credentials:
    - HR: `sarah.johnson@company.com` / `password123`
    - Manager: `michael.chen@company.com` / `password123`
    - Employee: `john.doe@company.com` / `password123`
    """
    # Authenticate user
    user = AuthService.authenticate_user(db, login_data.email, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create tokens
    access_token, refresh_token, expires_in = AuthService.create_tokens(user)
    
    # Get user info
    user_info = AuthService.get_user_info(user)
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=expires_in,
        user=user_info
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh Access Token",
    description="Get new access token using refresh token",
    responses={
        200: {"description": "New access token generated"},
        401: {"description": "Invalid or expired refresh token"}
    }
)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    ## Refresh Access Token
    
    Get a new access token using a valid refresh token.
    Use this when the access token expires.
    
    ### Request Body:
    - **refresh_token**: Valid refresh token from login response
    
    ### Response:
    - **access_token**: New JWT access token
    - **token_type**: Always "bearer"
    - **expires_in**: Token expiration time in seconds
    """
    result = AuthService.refresh_access_token(db, refresh_data.refresh_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token, expires_in = result
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_data.refresh_token,  # Return same refresh token
        token_type="bearer",
        expires_in=expires_in
    )


@router.get(
    "/me",
    response_model=None,
    summary="Get Current User",
    description="Get current authenticated user information",
    responses={
        200: {"description": "User information retrieved"},
        401: {"description": "Not authenticated"}
    }
)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """
    ## Get Current User
    
    Get information about the currently authenticated user.
    
    **Requires**: Valid access token in Authorization header
    
    ### Response:
    Returns complete user information including role, department, and hierarchy.
    """
    return AuthService.get_user_info(current_user)


@router.post(
    "/change-password",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Change Password",
    description="Change current user's password",
    responses={
        200: {"description": "Password changed successfully"},
        400: {"description": "Current password is incorrect"},
        401: {"description": "Not authenticated"}
    }
)
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    ## Change Password
    
    Change the current user's password.
    
    **Requires**: Valid access token in Authorization header
    
    ### Request Body:
    - **current_password**: Current password for verification
    - **new_password**: New password (minimum 6 characters)
    
    ### Response:
    - Success message if password changed
    """
    success = AuthService.change_password(
        db,
        current_user,
        password_data.current_password,
        password_data.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    return MessageResponse(message="Password changed successfully")


@router.post(
    "/reset-password",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Reset Employee Password (HR/Manager Only)",
    description="Reset password for an employee (HR/Manager access required)",
    responses={
        200: {"description": "Password reset successfully"},
        403: {"description": "Insufficient permissions"},
        404: {"description": "Employee not found"},
        401: {"description": "Not authenticated"}
    }
)
async def reset_password(
    reset_data: ResetPasswordRequest,
    current_user: Annotated[User, Depends(require_hr_or_manager)],
    db: Session = Depends(get_db)
):
    """
    ## Reset Employee Password
    
    Reset password for an employee. Only HR or Manager can perform this action.
    
    **Requires**:
    - Valid access token in Authorization header
    - User role must be HR or MANAGER
    
    ### Request Body:
    - **employee_id**: ID of employee to reset password for
    - **new_password**: New temporary password
    - **require_change_on_login**: Force password change on next login (default: true)
    
    ### Response:
    - Success message if password reset
    """
    success = AuthService.reset_password(
        db,
        reset_data.employee_id,
        reset_data.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found or inactive"
        )
    
    return MessageResponse(
        message=f"Password reset successfully for employee ID {reset_data.employee_id}"
    )


@router.post(
    "/logout",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout",
    description="Logout user (client-side token invalidation)",
    responses={
        200: {"description": "Logged out successfully"}
    }
)
async def logout():
    """
    ## Logout
    
    Logout current user. Since we're using JWT tokens, this is primarily handled
    client-side by removing the tokens from storage.
    
    **Client should**:
    - Remove access_token from storage
    - Remove refresh_token from storage
    - Clear any user state
    
    ### Response:
    - Success message
    """
    return MessageResponse(message="Logged out successfully")

