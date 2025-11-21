"""
Skills/Modules Management API Routes
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import User
from schemas.skill_schemas import (
    SkillModuleCreate,
    SkillModuleUpdate,
    SkillModuleResponse,
    SkillModuleListResponse,
    EnrollmentCreate,
    EnrollmentProgressUpdate,
    EnrollmentCompleteRequest,
    EnrollmentResponse,
    MyEnrollmentResponse,
    EnrollmentListResponse,
    SkillStatsResponse,
    MessageResponse
)
from services.skill_service import SkillService
from utils.dependencies import get_current_active_user, require_hr
import math

router = APIRouter(prefix="/skills", tags=["Skills/Modules Management"])


# ========== Module Management (HR Only) ==========

@router.post("/modules", response_model=SkillModuleResponse, status_code=status.HTTP_201_CREATED)
async def create_module(
    module_data: SkillModuleCreate,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Create new skill module (HR only).
    
    **Access**: HR only
    
    **Body**:
    - name: Module name (required, unique)
    - description: Module description (optional)
    - category: Module category (optional)
    - module_link: External link to course/resource (optional)
    - duration_hours: Estimated duration (optional)
    - difficulty_level: beginner/intermediate/advanced (optional)
    - skill_areas: Comma-separated skill areas (optional)
    - is_active: Active status (default: true)
    
    **Returns**: Created module
    """
    return SkillService.create_module(db, module_data)


@router.get("/modules", response_model=SkillModuleListResponse)
async def get_modules(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search in name, description, skill areas"),
    category: Optional[str] = Query(None, description="Filter by category"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty level"),
    include_inactive: bool = Query(False, description="Include inactive modules"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all skill modules with filters.
    
    **Access**: All authenticated users
    
    **Query Parameters**:
    - `page`: Page number (default: 1)
    - `page_size`: Items per page (default: 50, max: 100)
    - `search`: Search in name, description, skill areas
    - `category`: Filter by category
    - `difficulty`: Filter by difficulty (beginner/intermediate/advanced)
    - `include_inactive`: Include inactive modules (default: false)
    
    **Returns**: Paginated list of modules with enrollment stats
    
    **Use Case**: Skill development page to browse available modules
    """
    skip = (page - 1) * page_size
    
    modules, total = SkillService.get_all_modules(
        db=db,
        skip=skip,
        limit=page_size,
        search=search,
        category=category,
        difficulty=difficulty,
        include_inactive=include_inactive
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    
    return SkillModuleListResponse(
        modules=modules,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/modules/{module_id}", response_model=SkillModuleResponse)
async def get_module(
    module_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get module details by ID.
    
    **Access**: All authenticated users
    
    **Path Parameters**:
    - `module_id`: Module ID
    
    **Returns**: Module details with enrollment stats
    """
    return SkillService.get_module_by_id(db, module_id)


@router.put("/modules/{module_id}", response_model=SkillModuleResponse)
async def update_module(
    module_id: int,
    module_data: SkillModuleUpdate,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Update skill module (HR only).
    
    **Access**: HR only
    
    **Path Parameters**:
    - `module_id`: Module ID
    
    **Body**: Fields to update (all optional)
    - name, description, category
    - module_link, duration_hours
    - difficulty_level, skill_areas
    - is_active
    
    **Returns**: Updated module
    """
    return SkillService.update_module(db, module_id, module_data)


@router.delete("/modules/{module_id}", response_model=MessageResponse)
async def delete_module(
    module_id: int,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Delete skill module (HR only).
    
    **Access**: HR only
    
    **Path Parameters**:
    - `module_id`: Module ID
    
    **Note**: 
    - If module has enrollments: Soft delete (sets is_active to false)
    - If no enrollments: Hard delete
    
    **Returns**: Success message
    """
    SkillService.delete_module(db, module_id)
    return MessageResponse(message=f"Module {module_id} deleted successfully")


# ========== Enrollment Management (Employee) ==========

@router.post("/enroll", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def enroll_in_module(
    enrollment_data: EnrollmentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Enroll in a skill module (employee).
    
    **Access**: All authenticated users
    
    **Body**:
    - module_id: Module ID to enroll in (required)
    - target_completion_date: Target completion date (optional)
    
    **Validation**:
    - Module must be active
    - Cannot enroll in same module twice
    
    **Returns**: Created enrollment
    """
    return SkillService.enroll_in_module(db, current_user.id, enrollment_data)


@router.get("/my-enrollments", response_model=list[MyEnrollmentResponse])
async def get_my_enrollments(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status (not_started/pending/completed)"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get my enrollments (employee).
    
    **Access**: All authenticated users
    
    **Query Parameters**:
    - `page`: Page number (default: 1)
    - `page_size`: Items per page (default: 50, max: 100)
    - `status`: Filter by status (not_started/pending/completed)
    
    **Returns**: List of my enrollments with module details
    
    **Use Case**: My learning dashboard
    """
    skip = (page - 1) * page_size
    
    enrollments, total = SkillService.get_my_enrollments(
        db=db,
        employee_id=current_user.id,
        skip=skip,
        limit=page_size,
        status_filter=status
    )
    
    return enrollments


@router.get("/enrollments", response_model=EnrollmentListResponse)
async def get_all_enrollments(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    module_id: Optional[int] = Query(None, description="Filter by module ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Get all enrollments (HR).
    
    **Access**: HR only
    
    **Query Parameters**:
    - `page`: Page number (default: 1)
    - `page_size`: Items per page (default: 50, max: 100)
    - `employee_id`: Filter by employee ID
    - `module_id`: Filter by module ID
    - `status`: Filter by status
    
    **Returns**: Paginated list of all enrollments
    
    **Use Case**: HR dashboard for tracking employee learning
    """
    skip = (page - 1) * page_size
    
    enrollments, total = SkillService.get_all_enrollments(
        db=db,
        skip=skip,
        limit=page_size,
        employee_id_filter=employee_id,
        module_id_filter=module_id,
        status_filter=status
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    
    return EnrollmentListResponse(
        enrollments=enrollments,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.put("/enrollments/{enrollment_id}/progress", response_model=EnrollmentResponse)
async def update_enrollment_progress(
    enrollment_id: int,
    progress_data: EnrollmentProgressUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update enrollment progress (employee).
    
    **Access**: All authenticated users (own enrollments only)
    
    **Path Parameters**:
    - `enrollment_id`: Enrollment ID
    
    **Body**:
    - progress_percentage: Progress (0-100) (required)
    - status: Module status (optional, auto-updated based on progress)
    
    **Features**:
    - Auto-updates status based on progress if not provided
    - Sets started_date on first progress update
    - Sets completed_date when marking as completed
    
    **Returns**: Updated enrollment
    """
    return SkillService.update_enrollment_progress(db, enrollment_id, current_user.id, progress_data)


@router.patch("/enrollments/{enrollment_id}/complete", response_model=EnrollmentResponse)
async def mark_enrollment_complete(
    enrollment_id: int,
    complete_data: EnrollmentCompleteRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Mark enrollment as complete (employee).
    
    **Access**: All authenticated users (own enrollments only)
    
    **Path Parameters**:
    - `enrollment_id`: Enrollment ID
    
    **Body**:
    - score: Final score/grade 0-100 (optional)
    - certificate_path: Path to certificate (optional)
    
    **Features**:
    - Sets status to COMPLETED
    - Sets progress to 100%
    - Records completion date
    - Records score and certificate
    
    **Returns**: Updated enrollment
    """
    return SkillService.mark_enrollment_complete(db, enrollment_id, current_user.id, complete_data)


@router.get("/stats", response_model=SkillStatsResponse)
async def get_skill_stats(
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Get skills statistics (HR).
    
    **Access**: HR only
    
    **Returns**:
    - Total/active modules
    - Total/completed/in-progress enrollments
    - Breakdown by category
    - Breakdown by difficulty
    - Breakdown by status
    - Average completion rate
    
    **Use Case**: HR dashboard analytics
    """
    return SkillService.get_skill_stats(db)

