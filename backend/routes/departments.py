"""
Department API Routes
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional, Union
from database import get_db
from models import User, UserRole
from schemas.department_schemas import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    DepartmentDetailResponse,
    DepartmentListResponse,
    DepartmentStatsResponse,
    MessageResponse
)
from services.department_service import DepartmentService
from utils.dependencies import get_current_user, require_hr, require_hr_or_manager

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.post("", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(
    department_data: DepartmentCreate,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Create a new department (HR only).
    
    **Access**: HR only
    
    **Permissions**:
    - Only HR can create departments
    
    **Validation**:
    - Department name must be unique
    - Department code must be unique (if provided)
    - Head user must exist (if provided)
    """
    return DepartmentService.create_department(db, department_data)


@router.get("", response_model=DepartmentListResponse)
async def get_departments(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    include_inactive: bool = Query(False, description="Include inactive departments"),
    search: Optional[str] = Query(None, description="Search by name or code"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of departments.
    
    **Access**: All authenticated users
    
    **Query Parameters**:
    - `page`: Page number (default: 1)
    - `page_size`: Items per page (default: 50, max: 100)
    - `include_inactive`: Include inactive departments (default: false)
    - `search`: Search by name or code
    
    **Returns**: Paginated list of departments with employee/team counts
    """
    skip = (page - 1) * page_size
    
    departments, total = DepartmentService.get_all_departments(
        db=db,
        skip=skip,
        limit=page_size,
        include_inactive=include_inactive,
        search=search
    )
    
    return DepartmentListResponse(
        departments=departments,
        total=total
    )


@router.get("/stats", response_model=DepartmentStatsResponse)
async def get_department_stats(
    current_user: User = Depends(require_hr_or_manager),
    db: Session = Depends(get_db)
):
    """
    Get department statistics.
    
    **Access**: HR and Managers
    
    **Returns**:
    - Total departments
    - Active departments
    - Total employees across all departments
    - Total teams
    - Departments without head
    - Largest department info
    
    **Use Case**: For HR dashboard analytics
    """
    return DepartmentService.get_department_stats(db)


@router.get("/{department_id}", response_model=Union[DepartmentResponse, DepartmentDetailResponse])
async def get_department(
    department_id: int,
    include_teams: bool = Query(False, description="Include team details"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get department details by ID.
    
    **Access**: All authenticated users
    
    **Path Parameters**:
    - `department_id`: Department ID
    
    **Query Parameters**:
    - `include_teams`: Include detailed team information (default: false)
    
    **Returns**: Department details (with teams if requested)
    """
    return DepartmentService.get_department_by_id(db, department_id, include_teams)


@router.put("/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: int,
    department_data: DepartmentUpdate,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Update department (HR only).
    
    **Access**: HR only
    
    **Path Parameters**:
    - `department_id`: Department ID
    
    **Body**: Fields to update (all optional)
    
    **Validation**:
    - Name must be unique (if changed)
    - Code must be unique (if changed)
    - Head user must exist (if provided)
    
    **Returns**: Updated department
    """
    return DepartmentService.update_department(db, department_id, department_data)


@router.delete("/{department_id}", response_model=MessageResponse)
async def delete_department(
    department_id: int,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Delete department (soft delete, HR only).
    
    **Access**: HR only
    
    **Path Parameters**:
    - `department_id`: Department ID
    
    **Validation**:
    - Cannot delete department with employees
    - Must reassign employees first
    
    **Returns**: Success message
    
    **Note**: This is a soft delete (sets is_active to false)
    """
    DepartmentService.delete_department(db, department_id)
    return MessageResponse(message=f"Department {department_id} deleted successfully")

