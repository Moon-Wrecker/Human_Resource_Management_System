"""
Department Service - Business logic for department management
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from models import Department, User, Team
from schemas.department_schemas import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    DepartmentDetailResponse,
    DepartmentStatsResponse
)
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class DepartmentService:
    """Service class for department operations"""
    
    @staticmethod
    def create_department(
        db: Session,
        department_data: DepartmentCreate
    ) -> DepartmentResponse:
        """Create new department"""
        try:
            # Check if department name already exists
            existing_name = db.query(Department).filter(
                Department.name == department_data.name
            ).first()
            
            if existing_name:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Department with name '{department_data.name}' already exists"
                )
            
            # Check if department code already exists
            if department_data.code:
                existing_code = db.query(Department).filter(
                    Department.code == department_data.code
                ).first()
                
                if existing_code:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Department with code '{department_data.code}' already exists"
                    )
            
            # Verify head exists if provided
            if department_data.head_id:
                head_user = db.query(User).filter(User.id == department_data.head_id).first()
                if not head_user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with ID {department_data.head_id} not found"
                    )
            
            # Create department
            new_department = Department(
                name=department_data.name,
                code=department_data.code,
                description=department_data.description,
                head_id=department_data.head_id
            )
            
            db.add(new_department)
            db.commit()
            db.refresh(new_department)
            
            logger.info(f"Department created: {new_department.name} ({new_department.id})")
            
            return DepartmentService._format_department_response(new_department, db)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating department: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create department: {str(e)}"
            )
    
    @staticmethod
    def get_department_by_id(
        db: Session,
        department_id: int,
        include_teams: bool = False
    ):
        """Get department by ID"""
        department = db.query(Department).filter(Department.id == department_id).first()
        
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with ID {department_id} not found"
            )
        
        if include_teams:
            return DepartmentService._format_department_detail_response(department, db)
        else:
            return DepartmentService._format_department_response(department, db)
    
    @staticmethod
    def get_all_departments(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        include_inactive: bool = False,
        search: str = None
    ) -> Tuple[List[DepartmentResponse], int]:
        """Get all departments"""
        query = db.query(Department)
        
        # Filter active/inactive
        if not include_inactive:
            query = query.filter(Department.is_active == True)
        
        # Search filter
        if search:
            query = query.filter(
                (Department.name.ilike(f"%{search}%")) |
                (Department.code.ilike(f"%{search}%"))
            )
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        departments = query.order_by(Department.name).offset(skip).limit(limit).all()
        
        # Format responses
        formatted_departments = [
            DepartmentService._format_department_response(d, db) for d in departments
        ]
        
        return formatted_departments, total
    
    @staticmethod
    def update_department(
        db: Session,
        department_id: int,
        department_data: DepartmentUpdate
    ) -> DepartmentResponse:
        """Update department"""
        department = db.query(Department).filter(Department.id == department_id).first()
        
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with ID {department_id} not found"
            )
        
        try:
            # Check for duplicate name
            if department_data.name:
                existing = db.query(Department).filter(
                    Department.name == department_data.name,
                    Department.id != department_id
                ).first()
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Department with name '{department_data.name}' already exists"
                    )
            
            # Check for duplicate code
            if department_data.code:
                existing = db.query(Department).filter(
                    Department.code == department_data.code,
                    Department.id != department_id
                ).first()
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Department with code '{department_data.code}' already exists"
                    )
            
            # Verify head exists if provided
            if department_data.head_id:
                head_user = db.query(User).filter(User.id == department_data.head_id).first()
                if not head_user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with ID {department_data.head_id} not found"
                    )
            
            # Update fields
            update_data = department_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(department, field, value)
            
            db.commit()
            db.refresh(department)
            
            logger.info(f"Department updated: {department.name} ({department_id})")
            
            return DepartmentService._format_department_response(department, db)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating department: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update department: {str(e)}"
            )
    
    @staticmethod
    def delete_department(db: Session, department_id: int) -> None:
        """Delete department (soft delete)"""
        department = db.query(Department).filter(Department.id == department_id).first()
        
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with ID {department_id} not found"
            )
        
        # Check if department has employees
        employee_count = db.query(User).filter(User.department_id == department_id).count()
        if employee_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete department with {employee_count} employees. Please reassign employees first."
            )
        
        try:
            # Soft delete
            department.is_active = False
            db.commit()
            logger.info(f"Department deleted: {department.name} ({department_id})")
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting department: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete department: {str(e)}"
            )
    
    @staticmethod
    def get_department_stats(db: Session) -> DepartmentStatsResponse:
        """Get department statistics"""
        # Total departments
        total_departments = db.query(Department).filter(Department.is_active == True).count()
        
        # Active departments
        active_departments = total_departments
        
        # Total employees
        total_employees = db.query(User).filter(User.is_active == True).count()
        
        # Total teams
        total_teams = db.query(Team).filter(Team.is_active == True).count()
        
        # Departments without head
        departments_without_head = db.query(Department).filter(
            Department.is_active == True,
            Department.head_id.is_(None)
        ).count()
        
        # Largest department
        largest_dept_result = db.query(
            Department.id,
            Department.name,
            func.count(User.id).label('employee_count')
        ).join(User, User.department_id == Department.id).filter(
            Department.is_active == True
        ).group_by(Department.id, Department.name).order_by(
            func.count(User.id).desc()
        ).first()
        
        largest_department = None
        if largest_dept_result:
            largest_department = {
                "id": largest_dept_result.id,
                "name": largest_dept_result.name,
                "employee_count": largest_dept_result.employee_count
            }
        
        return DepartmentStatsResponse(
            total_departments=total_departments,
            active_departments=active_departments,
            total_employees=total_employees,
            total_teams=total_teams,
            departments_without_head=departments_without_head,
            largest_department=largest_department
        )
    
    @staticmethod
    def _format_department_response(department: Department, db: Session) -> DepartmentResponse:
        """Format department model to response schema"""
        # Get head details
        head_name = None
        if department.head_id:
            head_user = db.query(User).filter(User.id == department.head_id).first()
            head_name = head_user.name if head_user else None
        
        # Count employees
        employee_count = db.query(User).filter(
            User.department_id == department.id,
            User.is_active == True
        ).count()
        
        # Count teams
        team_count = db.query(Team).filter(
            Team.department_id == department.id,
            Team.is_active == True
        ).count()
        
        return DepartmentResponse(
            id=department.id,
            name=department.name,
            code=department.code,
            description=department.description,
            head_id=department.head_id,
            head_name=head_name,
            employee_count=employee_count,
            team_count=team_count,
            is_active=department.is_active,
            created_at=department.created_at
        )
    
    @staticmethod
    def _format_department_detail_response(department: Department, db: Session) -> DepartmentDetailResponse:
        """Format department model to detailed response schema with teams"""
        # Get basic response
        basic_response = DepartmentService._format_department_response(department, db)
        
        # Get teams
        teams = db.query(Team).filter(
            Team.department_id == department.id,
            Team.is_active == True
        ).all()
        
        teams_info = []
        for team in teams:
            manager_name = None
            if team.manager_id:
                manager = db.query(User).filter(User.id == team.manager_id).first()
                manager_name = manager.name if manager else None
            
            member_count = db.query(User).filter(
                User.team_id == team.id,
                User.is_active == True
            ).count()
            
            teams_info.append({
                "id": team.id,
                "name": team.name,
                "description": team.description,
                "manager_id": team.manager_id,
                "manager_name": manager_name,
                "member_count": member_count
            })
        
        return DepartmentDetailResponse(
            **basic_response.dict(),
            teams=teams_info
        )

