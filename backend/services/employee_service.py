"""
Employee Service - Business logic for employee management (HR only)
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_, or_
from fastapi import HTTPException, status
from models import User, Department, Team, UserRole
from schemas.employee_schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeListItem,
    EmployeeStatsResponse
)
from utils.password_utils import hash_password
from typing import List, Tuple, Optional
from datetime import datetime, timedelta
import logging
import random
import string

logger = logging.getLogger(__name__)


class EmployeeService:
    """Service class for employee management operations (HR only)"""
    
    @staticmethod
    def create_employee(
        db: Session,
        employee_data: EmployeeCreate
    ) -> EmployeeResponse:
        """Create new employee (HR only)"""
        try:
            # Check if email already exists
            existing_email = db.query(User).filter(User.email == employee_data.email).first()
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email '{employee_data.email}' already exists"
                )
            
            # Generate employee_id if not provided
            employee_id = employee_data.employee_id
            if not employee_id:
                employee_id = EmployeeService._generate_employee_id(db)
            else:
                # Check if employee_id already exists
                existing_id = db.query(User).filter(User.employee_id == employee_id).first()
                if existing_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Employee ID '{employee_id}' already exists"
                    )
            
            # Validate department exists
            if employee_data.department_id:
                dept = db.query(Department).filter(Department.id == employee_data.department_id).first()
                if not dept:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Department with ID {employee_data.department_id} not found"
                    )
            
            # Validate team exists
            if employee_data.team_id:
                team = db.query(Team).filter(Team.id == employee_data.team_id).first()
                if not team:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Team with ID {employee_data.team_id} not found"
                    )
            
            # Validate manager exists
            if employee_data.manager_id:
                manager = db.query(User).filter(User.id == employee_data.manager_id).first()
                if not manager:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Manager with ID {employee_data.manager_id} not found"
                    )
            
            # Hash password
            hashed_password = hash_password(employee_data.password)
            
            # Convert role string to UserRole enum
            role_map = {
                'employee': UserRole.EMPLOYEE,
                'manager': UserRole.MANAGER,
                'hr': UserRole.HR,
                'admin': UserRole.ADMIN
            }
            user_role = role_map.get(employee_data.role.lower(), UserRole.EMPLOYEE)
            
            # Create employee
            new_employee = User(
                employee_id=employee_id,
                name=employee_data.name,
                email=employee_data.email,
                password_hash=hashed_password,
                phone=employee_data.phone,
                job_role=employee_data.job_role,
                department_id=employee_data.department_id,
                team_id=employee_data.team_id,
                manager_id=employee_data.manager_id,
                role=user_role,
                hierarchy_level=employee_data.hierarchy_level,
                date_of_birth=employee_data.date_of_birth,
                hire_date=employee_data.hire_date or datetime.utcnow().date(),
                salary=employee_data.salary,
                emergency_contact=employee_data.emergency_contact,
                casual_leave_balance=employee_data.casual_leave_balance,
                sick_leave_balance=employee_data.sick_leave_balance,
                annual_leave_balance=employee_data.annual_leave_balance,
                wfh_balance=employee_data.wfh_balance,
                is_active=True
            )
            
            db.add(new_employee)
            db.commit()
            db.refresh(new_employee)
            
            logger.info(f"Employee created: {new_employee.name} ({new_employee.id})")
            
            return EmployeeService._format_employee_response(new_employee, db)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating employee: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create employee: {str(e)}"
            )
    
    @staticmethod
    def get_employee_by_id(db: Session, employee_id: int) -> EmployeeResponse:
        """Get employee by ID (HR only)"""
        employee = db.query(User).filter(User.id == employee_id).first()
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        
        return EmployeeService._format_employee_response(employee, db)
    
    @staticmethod
    def get_all_employees(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        department_id: Optional[int] = None,
        team_id: Optional[int] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Tuple[List[EmployeeListItem], int]:
        """Get all employees with filters (HR only)"""
        query = db.query(User)
        
        # Search filter (name or email or employee_id)
        if search:
            query = query.filter(
                or_(
                    User.name.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                    User.employee_id.ilike(f"%{search}%")
                )
            )
        
        # Department filter
        if department_id:
            query = query.filter(User.department_id == department_id)
        
        # Team filter
        if team_id:
            query = query.filter(User.team_id == team_id)
        
        # Role filter
        if role:
            role_map = {
                'employee': UserRole.EMPLOYEE,
                'manager': UserRole.MANAGER,
                'hr': UserRole.HR,
                'admin': UserRole.ADMIN
            }
            user_role = role_map.get(role.lower())
            if user_role:
                query = query.filter(User.role == user_role)
        
        # Active/Inactive filter
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        employees = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
        
        # Format responses
        formatted_employees = [
            EmployeeService._format_employee_list_item(e, db) for e in employees
        ]
        
        return formatted_employees, total
    
    @staticmethod
    def update_employee(
        db: Session,
        employee_id: int,
        employee_data: EmployeeUpdate
    ) -> EmployeeResponse:
        """Update employee (HR only)"""
        employee = db.query(User).filter(User.id == employee_id).first()
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        
        try:
            # Check for duplicate email
            if employee_data.email:
                existing = db.query(User).filter(
                    User.email == employee_data.email,
                    User.id != employee_id
                ).first()
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Email '{employee_data.email}' already exists"
                    )
            
            # Check for duplicate employee_id
            if employee_data.employee_id:
                existing = db.query(User).filter(
                    User.employee_id == employee_data.employee_id,
                    User.id != employee_id
                ).first()
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Employee ID '{employee_data.employee_id}' already exists"
                    )
            
            # Validate department exists
            if employee_data.department_id:
                dept = db.query(Department).filter(Department.id == employee_data.department_id).first()
                if not dept:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Department with ID {employee_data.department_id} not found"
                    )
            
            # Validate team exists
            if employee_data.team_id:
                team = db.query(Team).filter(Team.id == employee_data.team_id).first()
                if not team:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Team with ID {employee_data.team_id} not found"
                    )
            
            # Validate manager exists
            if employee_data.manager_id:
                manager = db.query(User).filter(User.id == employee_data.manager_id).first()
                if not manager:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Manager with ID {employee_data.manager_id} not found"
                    )
            
            # Update fields
            update_data = employee_data.dict(exclude_unset=True)
            
            # Handle role conversion
            if 'role' in update_data and update_data['role']:
                role_map = {
                    'employee': UserRole.EMPLOYEE,
                    'manager': UserRole.MANAGER,
                    'hr': UserRole.HR,
                    'admin': UserRole.ADMIN
                }
                update_data['role'] = role_map.get(update_data['role'].lower(), UserRole.EMPLOYEE)
            
            for field, value in update_data.items():
                setattr(employee, field, value)
            
            db.commit()
            db.refresh(employee)
            
            logger.info(f"Employee updated: {employee.name} ({employee_id})")
            
            return EmployeeService._format_employee_response(employee, db)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating employee: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update employee: {str(e)}"
            )
    
    @staticmethod
    def deactivate_employee(db: Session, employee_id: int) -> None:
        """Deactivate employee (soft delete, HR only)"""
        employee = db.query(User).filter(User.id == employee_id).first()
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        
        # Check if employee is a manager with active team members
        team_members = db.query(User).filter(
            User.manager_id == employee_id,
            User.is_active == True
        ).count()
        
        if team_members > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot deactivate employee with {team_members} active team members. Please reassign them first."
            )
        
        try:
            employee.is_active = False
            db.commit()
            logger.info(f"Employee deactivated: {employee.name} ({employee_id})")
        except Exception as e:
            db.rollback()
            logger.error(f"Error deactivating employee: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to deactivate employee: {str(e)}"
            )
    
    @staticmethod
    def get_employee_stats(db: Session) -> EmployeeStatsResponse:
        """Get employee statistics (HR only)"""
        # Total and active/inactive
        total_employees = db.query(User).count()
        active_employees = db.query(User).filter(User.is_active == True).count()
        inactive_employees = total_employees - active_employees
        
        # By department
        dept_results = db.query(
            Department.name,
            func.count(User.id)
        ).join(User, User.department_id == Department.id).filter(
            User.is_active == True
        ).group_by(Department.name).all()
        
        by_department = {dept: count for dept, count in dept_results}
        
        # By role
        role_results = db.query(
            User.role,
            func.count(User.id)
        ).filter(User.is_active == True).group_by(User.role).all()
        
        by_role = {role.value if hasattr(role, 'value') else str(role): count for role, count in role_results}
        
        # By team
        team_results = db.query(
            Team.name,
            func.count(User.id)
        ).join(User, User.team_id == Team.id).filter(
            User.is_active == True
        ).group_by(Team.name).all()
        
        by_team = {team: count for team, count in team_results}
        
        # Recent hires (last 30 days)
        thirty_days_ago = datetime.utcnow().date() - timedelta(days=30)
        recent_hires = db.query(User).filter(
            User.hire_date >= thirty_days_ago,
            User.is_active == True
        ).count()
        
        # Average tenure
        avg_tenure_query = db.query(
            func.avg(func.julianday(datetime.utcnow().date()) - func.julianday(User.hire_date))
        ).filter(
            User.is_active == True,
            User.hire_date.isnot(None)
        ).scalar()
        
        average_tenure_days = float(avg_tenure_query) if avg_tenure_query else 0.0
        
        return EmployeeStatsResponse(
            total_employees=total_employees,
            active_employees=active_employees,
            inactive_employees=inactive_employees,
            by_department=by_department,
            by_role=by_role,
            by_team=by_team,
            recent_hires=recent_hires,
            average_tenure_days=average_tenure_days
        )
    
    @staticmethod
    def _generate_employee_id(db: Session) -> str:
        """Generate unique employee ID"""
        while True:
            # Format: EMP + 5 random digits
            emp_id = "EMP" + ''.join(random.choices(string.digits, k=5))
            
            # Check if it exists
            existing = db.query(User).filter(User.employee_id == emp_id).first()
            if not existing:
                return emp_id
    
    @staticmethod
    def _format_employee_response(employee: User, db: Session) -> EmployeeResponse:
        """Format employee model to response schema"""
        # Get department name
        department_name = None
        if employee.department_id:
            dept = db.query(Department).filter(Department.id == employee.department_id).first()
            if dept:
                department_name = dept.name
        
        # Get team name
        team_name = None
        if employee.team_id:
            team = db.query(Team).filter(Team.id == employee.team_id).first()
            if team:
                team_name = team.name
        
        # Get manager name
        manager_name = None
        if employee.manager_id:
            manager = db.query(User).filter(User.id == employee.manager_id).first()
            if manager:
                manager_name = manager.name
        
        return EmployeeResponse(
            id=employee.id,
            employee_id=employee.employee_id,
            name=employee.name,
            email=employee.email,
            phone=employee.phone,
            job_role=employee.job_role,
            department=department_name,
            department_id=employee.department_id,
            team=team_name,
            team_id=employee.team_id,
            manager=manager_name,
            manager_id=employee.manager_id,
            role=employee.role.value if employee.role else 'employee',
            hierarchy_level=employee.hierarchy_level,
            is_active=employee.is_active,
            date_of_birth=employee.date_of_birth,
            hire_date=employee.hire_date,
            created_at=employee.created_at,
            salary=employee.salary,
            aadhar_document_path=employee.aadhar_document_path,
            pan_document_path=employee.pan_document_path,
            profile_image_path=employee.profile_image_path,
            casual_leave_balance=employee.casual_leave_balance,
            sick_leave_balance=employee.sick_leave_balance,
            annual_leave_balance=employee.annual_leave_balance,
            wfh_balance=employee.wfh_balance
        )
    
    @staticmethod
    def _format_employee_list_item(employee: User, db: Session) -> EmployeeListItem:
        """Format employee model to list item schema"""
        # Get department name
        department_name = None
        if employee.department_id:
            dept = db.query(Department).filter(Department.id == employee.department_id).first()
            if dept:
                department_name = dept.name
        
        # Get team name
        team_name = None
        if employee.team_id:
            team = db.query(Team).filter(Team.id == employee.team_id).first()
            if team:
                team_name = team.name
        
        # Get manager name
        manager_name = None
        if employee.manager_id:
            manager = db.query(User).filter(User.id == employee.manager_id).first()
            if manager:
                manager_name = manager.name
        
        return EmployeeListItem(
            id=employee.id,
            employee_id=employee.employee_id,
            name=employee.name,
            email=employee.email,
            phone=employee.phone,
            job_role=employee.job_role,
            department=department_name,
            team=team_name,
            manager=manager_name,
            role=employee.role.value if employee.role else 'employee',
            is_active=employee.is_active,
            hire_date=employee.hire_date
        )

