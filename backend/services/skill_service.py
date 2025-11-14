"""
Skills/Modules Service - Business logic for skill development and module management
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from fastapi import HTTPException, status
from models import User, SkillModule, SkillModuleEnrollment, ModuleStatus
from schemas.skill_schemas import (
    SkillModuleCreate,
    SkillModuleUpdate,
    SkillModuleResponse,
    EnrollmentCreate,
    EnrollmentProgressUpdate,
    EnrollmentCompleteRequest,
    EnrollmentResponse,
    MyEnrollmentResponse,
    SkillStatsResponse
)
from typing import List, Tuple, Optional
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)


class SkillService:
    """Service class for skills/modules management"""
    
    # ========== Module Management (HR Only) ==========
    
    @staticmethod
    def create_module(
        db: Session,
        module_data: SkillModuleCreate
    ) -> SkillModuleResponse:
        """Create new skill module (HR only)"""
        try:
            # Check if module name already exists
            existing = db.query(SkillModule).filter(SkillModule.name == module_data.name).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Module with name '{module_data.name}' already exists"
                )
            
            # Create module
            new_module = SkillModule(
                name=module_data.name,
                description=module_data.description,
                category=module_data.category,
                module_link=module_data.module_link,
                duration_hours=module_data.duration_hours,
                difficulty_level=module_data.difficulty_level.value if module_data.difficulty_level else None,
                skill_areas=module_data.skill_areas,
                is_active=module_data.is_active
            )
            
            db.add(new_module)
            db.commit()
            db.refresh(new_module)
            
            logger.info(f"Module created: {new_module.name} ({new_module.id})")
            
            return SkillService._format_module_response(new_module, db)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating module: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create module: {str(e)}"
            )
    
    @staticmethod
    def get_all_modules(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        include_inactive: bool = False
    ) -> Tuple[List[SkillModuleResponse], int]:
        """Get all modules with filters"""
        query = db.query(SkillModule)
        
        # Active filter
        if not include_inactive:
            query = query.filter(SkillModule.is_active == True)
        
        # Search filter
        if search:
            query = query.filter(
                or_(
                    SkillModule.name.ilike(f"%{search}%"),
                    SkillModule.description.ilike(f"%{search}%"),
                    SkillModule.skill_areas.ilike(f"%{search}%")
                )
            )
        
        # Category filter
        if category:
            query = query.filter(SkillModule.category.ilike(f"%{category}%"))
        
        # Difficulty filter
        if difficulty:
            query = query.filter(SkillModule.difficulty_level == difficulty)
        
        total = query.count()
        modules = query.order_by(SkillModule.created_at.desc()).offset(skip).limit(limit).all()
        
        formatted_modules = [SkillService._format_module_response(m, db) for m in modules]
        return formatted_modules, total
    
    @staticmethod
    def get_module_by_id(db: Session, module_id: int) -> SkillModuleResponse:
        """Get module by ID"""
        module = db.query(SkillModule).filter(SkillModule.id == module_id).first()
        
        if not module:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Module {module_id} not found"
            )
        
        return SkillService._format_module_response(module, db)
    
    @staticmethod
    def update_module(
        db: Session,
        module_id: int,
        module_data: SkillModuleUpdate
    ) -> SkillModuleResponse:
        """Update module (HR only)"""
        module = db.query(SkillModule).filter(SkillModule.id == module_id).first()
        
        if not module:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Module {module_id} not found"
            )
        
        try:
            # Check for duplicate name
            if module_data.name:
                existing = db.query(SkillModule).filter(
                    SkillModule.name == module_data.name,
                    SkillModule.id != module_id
                ).first()
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Module with name '{module_data.name}' already exists"
                    )
            
            # Update fields
            update_data = module_data.dict(exclude_unset=True)
            
            # Handle difficulty_level enum
            if 'difficulty_level' in update_data and update_data['difficulty_level']:
                update_data['difficulty_level'] = update_data['difficulty_level'].value
            
            for field, value in update_data.items():
                setattr(module, field, value)
            
            db.commit()
            db.refresh(module)
            
            logger.info(f"Module updated: {module.name} ({module_id})")
            
            return SkillService._format_module_response(module, db)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating module: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update module: {str(e)}"
            )
    
    @staticmethod
    def delete_module(db: Session, module_id: int) -> None:
        """Delete module (soft delete, HR only)"""
        module = db.query(SkillModule).filter(SkillModule.id == module_id).first()
        
        if not module:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Module {module_id} not found"
            )
        
        # Check if module has enrollments
        enrollment_count = db.query(SkillModuleEnrollment).filter(
            SkillModuleEnrollment.module_id == module_id
        ).count()
        
        if enrollment_count > 0:
            # Soft delete only
            module.is_active = False
            db.commit()
            logger.info(f"Module soft-deleted (has enrollments): {module.name} ({module_id})")
        else:
            # Hard delete if no enrollments
            db.delete(module)
            db.commit()
            logger.info(f"Module deleted: {module_id}")
    
    # ========== Enrollment Management (Employee) ==========
    
    @staticmethod
    def enroll_in_module(
        db: Session,
        employee_id: int,
        enrollment_data: EnrollmentCreate
    ) -> EnrollmentResponse:
        """Enroll in a module (employee)"""
        try:
            # Check if module exists and is active
            module = db.query(SkillModule).filter(
                SkillModule.id == enrollment_data.module_id,
                SkillModule.is_active == True
            ).first()
            
            if not module:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Module not found or inactive"
                )
            
            # Check if already enrolled
            existing = db.query(SkillModuleEnrollment).filter(
                SkillModuleEnrollment.employee_id == employee_id,
                SkillModuleEnrollment.module_id == enrollment_data.module_id
            ).first()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Already enrolled in this module"
                )
            
            # Create enrollment
            enrollment = SkillModuleEnrollment(
                employee_id=employee_id,
                module_id=enrollment_data.module_id,
                status=ModuleStatus.NOT_STARTED,
                progress_percentage=0.0,
                enrolled_date=date.today(),
                target_completion_date=enrollment_data.target_completion_date
            )
            
            db.add(enrollment)
            db.commit()
            db.refresh(enrollment)
            
            logger.info(f"Enrollment created: Employee {employee_id} in Module {enrollment_data.module_id}")
            
            return SkillService._format_enrollment_response(enrollment, db)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating enrollment: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to enroll in module: {str(e)}"
            )
    
    @staticmethod
    def get_my_enrollments(
        db: Session,
        employee_id: int,
        skip: int = 0,
        limit: int = 100,
        status_filter: Optional[str] = None
    ) -> Tuple[List[MyEnrollmentResponse], int]:
        """Get my enrollments (employee)"""
        query = db.query(SkillModuleEnrollment).filter(
            SkillModuleEnrollment.employee_id == employee_id
        )
        
        # Status filter
        if status_filter:
            try:
                status_enum = ModuleStatus[status_filter.upper().replace(' ', '_')]
                query = query.filter(SkillModuleEnrollment.status == status_enum)
            except KeyError:
                pass
        
        total = query.count()
        enrollments = query.order_by(SkillModuleEnrollment.enrolled_date.desc()).offset(skip).limit(limit).all()
        
        formatted_enrollments = [SkillService._format_my_enrollment_response(e, db) for e in enrollments]
        return formatted_enrollments, total
    
    @staticmethod
    def get_all_enrollments(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        employee_id_filter: Optional[int] = None,
        module_id_filter: Optional[int] = None,
        status_filter: Optional[str] = None
    ) -> Tuple[List[EnrollmentResponse], int]:
        """Get all enrollments (HR)"""
        query = db.query(SkillModuleEnrollment)
        
        # Employee filter
        if employee_id_filter:
            query = query.filter(SkillModuleEnrollment.employee_id == employee_id_filter)
        
        # Module filter
        if module_id_filter:
            query = query.filter(SkillModuleEnrollment.module_id == module_id_filter)
        
        # Status filter
        if status_filter:
            try:
                status_enum = ModuleStatus[status_filter.upper().replace(' ', '_')]
                query = query.filter(SkillModuleEnrollment.status == status_enum)
            except KeyError:
                pass
        
        total = query.count()
        enrollments = query.order_by(SkillModuleEnrollment.enrolled_date.desc()).offset(skip).limit(limit).all()
        
        formatted_enrollments = [SkillService._format_enrollment_response(e, db) for e in enrollments]
        return formatted_enrollments, total
    
    @staticmethod
    def update_enrollment_progress(
        db: Session,
        enrollment_id: int,
        employee_id: int,
        progress_data: EnrollmentProgressUpdate
    ) -> EnrollmentResponse:
        """Update enrollment progress (employee)"""
        enrollment = db.query(SkillModuleEnrollment).filter(
            SkillModuleEnrollment.id == enrollment_id,
            SkillModuleEnrollment.employee_id == employee_id
        ).first()
        
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )
        
        try:
            # Update progress
            enrollment.progress_percentage = progress_data.progress_percentage
            
            # Update status if provided
            if progress_data.status:
                new_status = ModuleStatus[progress_data.status.value.upper().replace(' ', '_')]
                enrollment.status = new_status
                
                # Set started_date if moving from NOT_STARTED
                if enrollment.started_date is None and new_status != ModuleStatus.NOT_STARTED:
                    enrollment.started_date = date.today()
            else:
                # Auto-update status based on progress
                if progress_data.progress_percentage == 0:
                    enrollment.status = ModuleStatus.NOT_STARTED
                elif progress_data.progress_percentage == 100:
                    enrollment.status = ModuleStatus.COMPLETED
                    if not enrollment.completed_date:
                        enrollment.completed_date = date.today()
                else:
                    enrollment.status = ModuleStatus.PENDING
                    if enrollment.started_date is None:
                        enrollment.started_date = date.today()
            
            db.commit()
            db.refresh(enrollment)
            
            logger.info(f"Enrollment progress updated: {enrollment_id}")
            
            return SkillService._format_enrollment_response(enrollment, db)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating enrollment progress: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update enrollment progress: {str(e)}"
            )
    
    @staticmethod
    def mark_enrollment_complete(
        db: Session,
        enrollment_id: int,
        employee_id: int,
        complete_data: EnrollmentCompleteRequest
    ) -> EnrollmentResponse:
        """Mark enrollment as complete (employee)"""
        enrollment = db.query(SkillModuleEnrollment).filter(
            SkillModuleEnrollment.id == enrollment_id,
            SkillModuleEnrollment.employee_id == employee_id
        ).first()
        
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )
        
        try:
            enrollment.status = ModuleStatus.COMPLETED
            enrollment.progress_percentage = 100.0
            enrollment.completed_date = date.today()
            enrollment.score = complete_data.score
            enrollment.certificate_path = complete_data.certificate_path
            
            if enrollment.started_date is None:
                enrollment.started_date = date.today()
            
            db.commit()
            db.refresh(enrollment)
            
            logger.info(f"Enrollment marked complete: {enrollment_id}")
            
            return SkillService._format_enrollment_response(enrollment, db)
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error marking enrollment complete: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to mark enrollment complete: {str(e)}"
            )
    
    @staticmethod
    def get_skill_stats(db: Session) -> SkillStatsResponse:
        """Get skill statistics (HR)"""
        # Total modules
        total_modules = db.query(SkillModule).count()
        active_modules = db.query(SkillModule).filter(SkillModule.is_active == True).count()
        
        # Total enrollments
        total_enrollments = db.query(SkillModuleEnrollment).count()
        completed_enrollments = db.query(SkillModuleEnrollment).filter(
            SkillModuleEnrollment.status == ModuleStatus.COMPLETED
        ).count()
        in_progress_enrollments = db.query(SkillModuleEnrollment).filter(
            SkillModuleEnrollment.status == ModuleStatus.PENDING
        ).count()
        
        # By category
        category_results = db.query(
            SkillModule.category,
            func.count(SkillModule.id)
        ).filter(SkillModule.is_active == True).group_by(SkillModule.category).all()
        by_category = {cat if cat else "Uncategorized": count for cat, count in category_results}
        
        # By difficulty
        difficulty_results = db.query(
            SkillModule.difficulty_level,
            func.count(SkillModule.id)
        ).filter(SkillModule.is_active == True).group_by(SkillModule.difficulty_level).all()
        by_difficulty = {diff if diff else "Unspecified": count for diff, count in difficulty_results}
        
        # By status
        status_results = db.query(
            SkillModuleEnrollment.status,
            func.count(SkillModuleEnrollment.id)
        ).group_by(SkillModuleEnrollment.status).all()
        by_status = {stat.value if stat else "unknown": count for stat, count in status_results}
        
        # Average completion rate
        avg_completion_rate = (completed_enrollments / total_enrollments * 100) if total_enrollments > 0 else 0.0
        
        return SkillStatsResponse(
            total_modules=total_modules,
            active_modules=active_modules,
            total_enrollments=total_enrollments,
            completed_enrollments=completed_enrollments,
            in_progress_enrollments=in_progress_enrollments,
            by_category=by_category,
            by_difficulty=by_difficulty,
            by_status=by_status,
            average_completion_rate=round(avg_completion_rate, 2)
        )
    
    # ========== Helper Methods ==========
    
    @staticmethod
    def _format_module_response(module: SkillModule, db: Session) -> SkillModuleResponse:
        """Format module to response schema"""
        # Get enrollment counts
        total_enrollments = db.query(SkillModuleEnrollment).filter(
            SkillModuleEnrollment.module_id == module.id
        ).count()
        
        completed_count = db.query(SkillModuleEnrollment).filter(
            SkillModuleEnrollment.module_id == module.id,
            SkillModuleEnrollment.status == ModuleStatus.COMPLETED
        ).count()
        
        return SkillModuleResponse(
            id=module.id,
            name=module.name,
            description=module.description,
            category=module.category,
            module_link=module.module_link,
            duration_hours=module.duration_hours,
            difficulty_level=module.difficulty_level,
            skill_areas=module.skill_areas,
            is_active=module.is_active,
            created_at=module.created_at,
            total_enrollments=total_enrollments,
            completed_count=completed_count
        )
    
    @staticmethod
    def _format_enrollment_response(enrollment: SkillModuleEnrollment, db: Session) -> EnrollmentResponse:
        """Format enrollment to response schema"""
        # Get employee name
        employee = db.query(User).filter(User.id == enrollment.employee_id).first()
        employee_name = employee.name if employee else None
        
        # Get module name
        module = db.query(SkillModule).filter(SkillModule.id == enrollment.module_id).first()
        module_name = module.name if module else None
        
        return EnrollmentResponse(
            id=enrollment.id,
            employee_id=enrollment.employee_id,
            employee_name=employee_name,
            module_id=enrollment.module_id,
            module_name=module_name,
            status=enrollment.status.value if enrollment.status else 'not_started',
            progress_percentage=enrollment.progress_percentage,
            enrolled_date=enrollment.enrolled_date,
            started_date=enrollment.started_date,
            completed_date=enrollment.completed_date,
            target_completion_date=enrollment.target_completion_date,
            certificate_path=enrollment.certificate_path,
            score=enrollment.score,
            created_at=enrollment.created_at
        )
    
    @staticmethod
    def _format_my_enrollment_response(enrollment: SkillModuleEnrollment, db: Session) -> MyEnrollmentResponse:
        """Format enrollment with module details for 'my enrollments' view"""
        # Get module details
        module = db.query(SkillModule).filter(SkillModule.id == enrollment.module_id).first()
        
        return MyEnrollmentResponse(
            id=enrollment.id,
            module_id=enrollment.module_id,
            module_name=module.name if module else "Unknown",
            module_description=module.description if module else None,
            module_link=module.module_link if module else None,
            category=module.category if module else None,
            duration_hours=module.duration_hours if module else None,
            difficulty_level=module.difficulty_level if module else None,
            status=enrollment.status.value if enrollment.status else 'not_started',
            progress_percentage=enrollment.progress_percentage,
            enrolled_date=enrollment.enrolled_date,
            started_date=enrollment.started_date,
            completed_date=enrollment.completed_date,
            target_completion_date=enrollment.target_completion_date,
            score=enrollment.score,
            certificate_path=enrollment.certificate_path
        )

