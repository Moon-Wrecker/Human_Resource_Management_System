"""
Profile Service - Business logic for profile management
"""
import os
import shutil
from datetime import datetime, date
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, extract
from fastapi import UploadFile, HTTPException, status

from models import (
    User, UserRole, Department, Team, Goal, GoalStatus,
    SkillModuleEnrollment, ModuleStatus, Attendance, AttendanceStatus,
    LeaveRequest, LeaveStatus
)
from config import settings


class ProfileService:
    """Service for profile-related operations"""
    
    @staticmethod
    def get_user_profile(db: Session, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get complete user profile with all related information
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Complete profile dictionary or None if user not found
        """
        user = db.query(User).options(
            joinedload(User.department_obj),
            joinedload(User.team_obj),
            joinedload(User.manager)
        ).filter(User.id == user_id).first()
        
        if not user:
            return None
        
        # Build profile response
        profile = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "employee_id": user.employee_id,
            "role": user.role.value if user.role else "employee",
            
            # Job details
            "job_role": user.job_role,
            "job_level": user.job_level,
            "hierarchy_level": user.hierarchy_level,
            "hire_date": user.hire_date,
            "salary": user.salary if user.role in [UserRole.HR, UserRole.MANAGER] else None,
            
            # Organization
            "department_id": user.department_id,
            "department_name": user.department_obj.name if user.department_obj else None,
            "team_id": user.team_id,
            "team_name": user.team_obj.name if user.team_obj else None,
            
            # Manager info
            "manager_id": user.manager_id,
            "manager_name": user.manager.name if user.manager else None,
            "manager_email": user.manager.email if user.manager else None,
            
            # Leave balances
            "casual_leave_balance": user.casual_leave_balance,
            "sick_leave_balance": user.sick_leave_balance,
            "annual_leave_balance": user.annual_leave_balance,
            "wfh_balance": user.wfh_balance,
            
            # Documents
            "profile_image_path": user.profile_image_path,
            "profile_image_url": f"/{user.profile_image_path}" if user.profile_image_path else None,
            "aadhar_document_path": user.aadhar_document_path,
            "aadhar_document_url": f"/{user.aadhar_document_path}" if user.aadhar_document_path else None,
            "pan_document_path": user.pan_document_path,
            "pan_document_url": f"/{user.pan_document_path}" if user.pan_document_path else None,
            
            # Metadata
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
        
        return profile
    
    @staticmethod
    def update_user_profile(
        db: Session,
        user_id: int,
        update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Update user profile with provided data
        
        Args:
            db: Database session
            user_id: User ID
            update_data: Dictionary with fields to update
            
        Returns:
            Updated profile dictionary or None if user not found
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return None
        
        # Update allowed fields
        allowed_fields = ['name', 'phone']
        for field, value in update_data.items():
            if field in allowed_fields and value is not None:
                setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        
        try:
            db.commit()
            db.refresh(user)
            return ProfileService.get_user_profile(db, user_id)
        except Exception as e:
            db.rollback()
            raise e
    
    @staticmethod
    def upload_profile_image(
        db: Session,
        user_id: int,
        file: UploadFile
    ) -> Dict[str, Any]:
        """
        Upload and save user profile image
        
        Args:
            db: Database session
            user_id: User ID
            file: Uploaded file
            
        Returns:
            Upload result dictionary
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Validate file type
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}"
            )
        
        # Create filename
        timestamp = int(datetime.utcnow().timestamp())
        safe_name = user.employee_id or f"user_{user_id}"
        filename = f"profile_{safe_name}_{timestamp}{file_ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, "profiles", filename)
        
        # Delete old profile image if exists
        if user.profile_image_path and os.path.exists(user.profile_image_path):
            try:
                os.remove(user.profile_image_path)
            except:
                pass
        
        # Save new file
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save file: {str(e)}"
            )
        
        # Update user record
        user.profile_image_path = file_path
        user.updated_at = datetime.utcnow()
        
        try:
            db.commit()
            db.refresh(user)
        except Exception as e:
            # Clean up uploaded file if database update fails
            if os.path.exists(file_path):
                os.remove(file_path)
            db.rollback()
            raise e
        
        return {
            "message": "Profile image uploaded successfully",
            "document_type": "profile_image",
            "file_path": file_path,
            "file_url": f"/{file_path}",
            "uploaded_at": datetime.utcnow()
        }
    
    @staticmethod
    def upload_document(
        db: Session,
        user_id: int,
        document_type: str,
        file: UploadFile
    ) -> Dict[str, Any]:
        """
        Upload and save user document (Aadhar, PAN, etc.)
        
        Args:
            db: Database session
            user_id: User ID
            document_type: Type of document ('aadhar' or 'pan')
            file: Uploaded file
            
        Returns:
            Upload result dictionary
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Validate document type
        valid_doc_types = ['aadhar', 'pan']
        if document_type not in valid_doc_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid document type. Allowed: {', '.join(valid_doc_types)}"
            )
        
        # Validate file type
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in settings.ALLOWED_DOCUMENT_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_DOCUMENT_EXTENSIONS)}"
            )
        
        # Create filename
        timestamp = int(datetime.utcnow().timestamp())
        safe_name = user.employee_id or f"user_{user_id}"
        filename = f"{document_type}_{safe_name}_{timestamp}{file_ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, "documents", filename)
        
        # Get the field name for this document type
        field_name = f"{document_type}_document_path"
        
        # Delete old document if exists
        old_path = getattr(user, field_name, None)
        if old_path and os.path.exists(old_path):
            try:
                os.remove(old_path)
            except:
                pass
        
        # Save new file
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save file: {str(e)}"
            )
        
        # Update user record
        setattr(user, field_name, file_path)
        user.updated_at = datetime.utcnow()
        
        try:
            db.commit()
            db.refresh(user)
        except Exception as e:
            # Clean up uploaded file if database update fails
            if os.path.exists(file_path):
                os.remove(file_path)
            db.rollback()
            raise e
        
        return {
            "message": f"{document_type.upper()} document uploaded successfully",
            "document_type": document_type,
            "file_path": file_path,
            "file_url": f"/{file_path}",
            "uploaded_at": datetime.utcnow()
        }
    
    @staticmethod
    def get_user_documents(db: Session, user_id: int) -> Dict[str, Any]:
        """
        Get all uploaded documents for a user
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Dictionary with document information
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        documents = {}
        
        # Profile image
        if user.profile_image_path:
            documents["profile_image"] = {
                "path": user.profile_image_path,
                "url": f"/{user.profile_image_path}",
                "uploaded_at": user.updated_at
            }
        
        # Aadhar card
        if user.aadhar_document_path:
            documents["aadhar_card"] = {
                "path": user.aadhar_document_path,
                "url": f"/{user.aadhar_document_path}",
                "uploaded_at": user.updated_at
            }
        
        # PAN card
        if user.pan_document_path:
            documents["pan_card"] = {
                "path": user.pan_document_path,
                "url": f"/{user.pan_document_path}",
                "uploaded_at": user.updated_at
            }
        
        return documents
    
    @staticmethod
    def delete_document(
        db: Session,
        user_id: int,
        document_type: str
    ) -> Dict[str, str]:
        """
        Delete a user document
        
        Args:
            db: Database session
            user_id: User ID
            document_type: Type of document to delete
            
        Returns:
            Success message dictionary
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Map document types to field names
        field_map = {
            "profile_image": "profile_image_path",
            "aadhar": "aadhar_document_path",
            "pan": "pan_document_path"
        }
        
        if document_type not in field_map:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid document type. Allowed: {', '.join(field_map.keys())}"
            )
        
        field_name = field_map[document_type]
        file_path = getattr(user, field_name, None)
        
        if not file_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{document_type} document not found"
            )
        
        # Delete file from filesystem
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to delete file: {str(e)}"
                )
        
        # Update database
        setattr(user, field_name, None)
        user.updated_at = datetime.utcnow()
        
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        
        return {
            "message": f"{document_type} document deleted successfully"
        }
    
    @staticmethod
    def get_manager_info(db: Session, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get manager information for a user
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Manager information dictionary or None
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user or not user.manager_id:
            return None
        
        manager = db.query(User).options(
            joinedload(User.department_obj)
        ).filter(User.id == user.manager_id).first()
        
        if not manager:
            return None
        
        return {
            "id": manager.id,
            "name": manager.name,
            "email": manager.email,
            "phone": manager.phone,
            "employee_id": manager.employee_id,
            "job_role": manager.job_role,
            "department_name": manager.department_obj.name if manager.department_obj else None,
            "profile_image_url": f"/{manager.profile_image_path}" if manager.profile_image_path else None
        }
    
    @staticmethod
    def get_team_members(db: Session, user_id: int) -> Dict[str, Any]:
        """
        Get team members for a manager
        
        Args:
            db: Database session
            user_id: Manager's user ID
            
        Returns:
            Team information with members
        """
        user = db.query(User).options(
            joinedload(User.team_obj),
            joinedload(User.department_obj)
        ).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get team members (people who report to this user)
        team_members = db.query(User).filter(
            User.manager_id == user_id,
            User.is_active == True
        ).all()
        
        members_list = []
        for member in team_members:
            members_list.append({
                "id": member.id,
                "name": member.name,
                "email": member.email,
                "employee_id": member.employee_id,
                "job_role": member.job_role,
                "job_level": member.job_level,
                "phone": member.phone,
                "profile_image_url": f"/{member.profile_image_path}" if member.profile_image_path else None,
                "is_active": member.is_active
            })
        
        return {
            "team_id": user.team_id,
            "team_name": user.team_obj.name if user.team_obj else None,
            "department_name": user.department_obj.name if user.department_obj else None,
            "total_members": len(members_list),
            "members": members_list
        }
    
    @staticmethod
    def get_profile_stats(db: Session, user_id: int) -> Dict[str, Any]:
        """
        Get profile statistics and analytics
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Statistics dictionary
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        current_year = datetime.utcnow().year
        
        # Goals statistics
        total_goals = db.query(func.count(Goal.id)).filter(
            Goal.employee_id == user_id
        ).scalar() or 0
        
        completed_goals = db.query(func.count(Goal.id)).filter(
            Goal.employee_id == user_id,
            Goal.status == GoalStatus.COMPLETED
        ).scalar() or 0
        
        in_progress_goals = db.query(func.count(Goal.id)).filter(
            Goal.employee_id == user_id,
            Goal.status == GoalStatus.IN_PROGRESS
        ).scalar() or 0
        
        # Skill modules statistics
        total_skill_modules = db.query(func.count(SkillModuleEnrollment.id)).filter(
            SkillModuleEnrollment.employee_id == user_id
        ).scalar() or 0
        
        completed_skill_modules = db.query(func.count(SkillModuleEnrollment.id)).filter(
            SkillModuleEnrollment.employee_id == user_id,
            SkillModuleEnrollment.status == ModuleStatus.COMPLETED
        ).scalar() or 0
        
        # Total training hours (sum of duration_hours from completed modules)
        # This is a simplified calculation - you might want to join with SkillModule table
        total_training_hours = db.query(
            func.coalesce(func.sum(SkillModuleEnrollment.progress_percentage), 0)
        ).filter(
            SkillModuleEnrollment.employee_id == user_id,
            SkillModuleEnrollment.status == ModuleStatus.COMPLETED
        ).scalar() or 0.0
        
        # Attendance percentage (current year)
        total_attendance_days = db.query(func.count(Attendance.id)).filter(
            Attendance.employee_id == user_id,
            extract('year', Attendance.date) == current_year
        ).scalar() or 0
        
        present_days = db.query(func.count(Attendance.id)).filter(
            Attendance.employee_id == user_id,
            extract('year', Attendance.date) == current_year,
            Attendance.status.in_([AttendanceStatus.PRESENT, AttendanceStatus.WFH])
        ).scalar() or 0
        
        attendance_percentage = (present_days / total_attendance_days * 100) if total_attendance_days > 0 else 0.0
        
        # Leaves taken this year
        leaves_taken = db.query(func.count(LeaveRequest.id)).filter(
            LeaveRequest.employee_id == user_id,
            extract('year', LeaveRequest.start_date) == current_year,
            LeaveRequest.status == LeaveStatus.APPROVED
        ).scalar() or 0
        
        return {
            "total_goals": total_goals,
            "completed_goals": completed_goals,
            "in_progress_goals": in_progress_goals,
            "total_skill_modules": total_skill_modules,
            "completed_skill_modules": completed_skill_modules,
            "total_training_hours": round(total_training_hours / 10, 1),  # Simplified conversion
            "attendance_percentage": round(attendance_percentage, 1),
            "leaves_taken_this_year": leaves_taken
        }

