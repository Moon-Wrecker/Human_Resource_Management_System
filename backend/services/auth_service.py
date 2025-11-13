"""
Authentication service - Business logic for auth operations
"""
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from models import User
from utils.password_utils import hash_password, verify_password
from utils.jwt_utils import create_access_token, create_refresh_token, verify_token
from pydantic_models import UserInfoResponse
from config import settings


class AuthService:
    """Authentication service class"""
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password
        
        Args:
            db: Database session
            email: User email
            password: Plain text password
            
        Returns:
            User object if authenticated, None otherwise
        """
        # Find user by email
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            return None
        
        # Check if user is active
        if not user.is_active:
            return None
        
        # Verify password
        if not verify_password(password, user.password_hash):
            return None
        
        return user
    
    @staticmethod
    def create_tokens(user: User) -> Tuple[str, str, int]:
        """
        Create access and refresh tokens for user
        
        Args:
            user: User object
            
        Returns:
            Tuple of (access_token, refresh_token, expires_in_seconds)
        """
        # Prepare token data
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role.value,
            "employee_id": user.employee_id
        }
        
        # Create tokens
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token({"user_id": user.id})
        
        # Calculate expiration in seconds
        expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        
        return access_token, refresh_token, expires_in
    
    @staticmethod
    def get_user_info(user: User) -> UserInfoResponse:
        """
        Convert User model to UserInfoResponse schema
        
        Args:
            user: User object
            
        Returns:
            UserInfoResponse schema
        """
        return UserInfoResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role.value,
            employee_id=user.employee_id,
            department_id=user.department_id,
            job_role=user.job_role,
            hierarchy_level=user.hierarchy_level
        )
    
    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> Optional[Tuple[str, int]]:
        """
        Generate new access token from refresh token
        
        Args:
            db: Database session
            refresh_token: Valid refresh token
            
        Returns:
            Tuple of (new_access_token, expires_in) or None if invalid
        """
        # Verify refresh token
        payload = verify_token(refresh_token, token_type="refresh")
        
        if not payload:
            return None
        
        # Get user from database
        user_id = payload.get("user_id")
        user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
        
        if not user:
            return None
        
        # Create new access token
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role.value,
            "employee_id": user.employee_id
        }
        
        access_token = create_access_token(token_data)
        expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        
        return access_token, expires_in
    
    @staticmethod
    def change_password(db: Session, user: User, current_password: str, new_password: str) -> bool:
        """
        Change user password
        
        Args:
            db: Database session
            user: User object
            current_password: Current password to verify
            new_password: New password to set
            
        Returns:
            True if successful, False otherwise
        """
        # Verify current password
        if not verify_password(current_password, user.password_hash):
            return False
        
        # Hash and update new password
        user.password_hash = hash_password(new_password)
        db.commit()
        
        return True
    
    @staticmethod
    def reset_password(db: Session, employee_id: int, new_password: str) -> bool:
        """
        Reset user password (by HR/Manager)
        
        Args:
            db: Database session
            employee_id: Employee ID to reset password for
            new_password: New temporary password
            
        Returns:
            True if successful, False otherwise
        """
        user = db.query(User).filter(User.id == employee_id, User.is_active == True).first()
        
        if not user:
            return False
        
        # Hash and update password
        user.password_hash = hash_password(new_password)
        db.commit()
        
        return True
    
    @staticmethod
    def get_current_user(db: Session, token: str) -> Optional[User]:
        """
        Get current user from access token
        
        Args:
            db: Database session
            token: JWT access token
            
        Returns:
            User object or None if invalid
        """
        payload = verify_token(token, token_type="access")
        
        if not payload:
            return None
        
        user_id = payload.get("user_id")
        user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
        
        return user

