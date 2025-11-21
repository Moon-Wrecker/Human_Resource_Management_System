"""
Employee Management API Routes (HR only)
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import User
from schemas.employee_schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeListResponse,
    EmployeeStatsResponse,
    MessageResponse
)
from services.employee_service import EmployeeService
from utils.dependencies import require_hr
import math

router = APIRouter(prefix="/employees", tags=["Employee Management"])


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee_data: EmployeeCreate,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Create a new employee (HR only).
    
    **Access**: HR only
    
    **Features**:
    - Creates new user account with hashed password
    - Auto-generates employee_id if not provided
    - Validates department, team, and manager
    - Sets initial leave balances
    - Email must be unique
    
    **Body**:
    - name: Employee name (required)
    - email: Email address (required, unique)
    - password: Initial password (required, min 6 chars)
    - phone: Phone number (optional)
    - employee_id: Employee ID (optional, auto-generated)
    - position: Job title (optional)
    - department_id: Department ID (optional)
    - team_id: Team ID (optional)
    - manager_id: Manager user ID (optional)
    - role: User role - employee/manager/hr (default: employee)
    - hierarchy_level: 1-7 (1=CEO, 7=Junior)
    - date_of_birth: Date of birth (optional)
    - join_date: Join date (optional, defaults to today)
    - salary: Monthly salary (optional)
    - Leave balances (optional, defaults provided)
    
    **Returns**: Created employee details
    """
    return EmployeeService.create_employee(db, employee_data)


@router.get("", response_model=EmployeeListResponse)
async def get_employees(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by name, email, or employee ID"),
    department_id: Optional[int] = Query(None, description="Filter by department"),
    team_id: Optional[int] = Query(None, description="Filter by team"),
    role: Optional[str] = Query(None, description="Filter by role (employee/manager/hr)"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Get list of all employees with filters (HR only).
    
    **Access**: HR only
    
    **Query Parameters**:
    - `page`: Page number (default: 1)
    - `page_size`: Items per page (default: 50, max: 100)
    - `search`: Search by name, email, or employee ID
    - `department_id`: Filter by department
    - `team_id`: Filter by team
    - `role`: Filter by role (employee/manager/hr)
    - `is_active`: Filter by active status (true/false)
    
    **Returns**: Paginated list of employees (summary view)
    
    **Use Case**: 
    - Employee list page in HR dashboard
    - Search and filter employees
    - Export employee data
    """
    skip = (page - 1) * page_size
    
    employees, total = EmployeeService.get_all_employees(
        db=db,
        skip=skip,
        limit=page_size,
        search=search,
        department_id=department_id,
        team_id=team_id,
        role=role,
        is_active=is_active
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    
    return EmployeeListResponse(
        employees=employees,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/stats", response_model=EmployeeStatsResponse)
async def get_employee_stats(
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Get employee statistics (HR only).
    
    **Access**: HR only
    
    **Returns**:
    - Total employees
    - Active vs inactive employees
    - Breakdown by department
    - Breakdown by role
    - Breakdown by team
    - Recent hires (last 30 days)
    - Average tenure in days
    
    **Use Case**: HR dashboard analytics and reports
    """
    return EmployeeService.get_employee_stats(db)


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: int,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Get employee details by ID (HR only).
    
    **Access**: HR only
    
    **Path Parameters**:
    - `employee_id`: Employee user ID
    
    **Returns**: Complete employee details including:
    - Basic info (name, email, phone)
    - Work info (position, department, team, manager)
    - Role and hierarchy
    - Dates (DOB, join date)
    - Compensation (salary)
    - Document paths
    - Leave balances
    
    **Use Case**: 
    - View employee details modal
    - Edit employee form pre-fill
    - Employee profile for HR
    """
    return EmployeeService.get_employee_by_id(db, employee_id)


@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Update employee details (HR only).
    
    **Access**: HR only
    
    **Path Parameters**:
    - `employee_id`: Employee user ID
    
    **Body**: Fields to update (all optional)
    - name, email, phone
    - employee_id, position
    - department_id, team_id, manager_id
    - role, hierarchy_level
    - date_of_birth, join_date
    - salary
    - is_active
    - emergency_contact
    - Leave balances
    
    **Validation**:
    - Email must be unique
    - Employee ID must be unique
    - Department, team, and manager must exist
    
    **Returns**: Updated employee details
    
    **Use Case**: Edit employee form in HR dashboard
    """
    return EmployeeService.update_employee(db, employee_id, employee_data)


@router.delete("/{employee_id}", response_model=MessageResponse)
async def deactivate_employee(
    employee_id: int,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Deactivate employee (soft delete, HR only).
    
    **Access**: HR only
    
    **Path Parameters**:
    - `employee_id`: Employee user ID
    
    **Validation**:
    - Cannot deactivate employee with active team members
    - Must reassign team members to another manager first
    
    **Returns**: Success message
    
    **Note**: 
    - This is a soft delete (sets is_active to false)
    - Employee data is preserved for historical records
    - Deactivated employees cannot login
    
    **Use Case**: Employee offboarding/termination
    """
    EmployeeService.deactivate_employee(db, employee_id)
    return MessageResponse(message=f"Employee {employee_id} deactivated successfully")

