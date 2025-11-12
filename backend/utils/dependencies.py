"""
Reusable dependencies for FastAPI routes
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Annotated
from database import get_db
from services.auth_service import AuthService
from models import User, UserRole

security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from Bearer token
    
    Raises:
        HTTPException: 401 if token is invalid or user not found
        
    Returns:
        User: Current authenticated user
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


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    Dependency to ensure user is active
    
    Raises:
        HTTPException: 403 if user is not active
        
    Returns:
        User: Active user
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


async def require_hr(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """
    Dependency to ensure user is HR
    
    Raises:
        HTTPException: 403 if user is not HR
        
    Returns:
        User: HR user
    """
    if current_user.role != UserRole.HR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can perform this action"
        )
    return current_user


async def require_manager(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """
    Dependency to ensure user is Manager
    
    Raises:
        HTTPException: 403 if user is not Manager
        
    Returns:
        User: Manager user
    """
    if current_user.role != UserRole.MANAGER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Manager can perform this action"
        )
    return current_user


async def require_hr_or_manager(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """
    Dependency to ensure user is HR or Manager
    
    Raises:
        HTTPException: 403 if user is neither HR nor Manager
        
    Returns:
        User: HR or Manager user
    """
    if current_user.role not in [UserRole.HR, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR or Manager can perform this action"
        )
    return current_user


async def require_employee(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """
    Dependency to ensure user is Employee
    
    Raises:
        HTTPException: 403 if user is not Employee
        
    Returns:
        User: Employee user
    """
    if current_user.role != UserRole.EMPLOYEE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Employee can perform this action"
        )
    return current_user

