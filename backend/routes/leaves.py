"""
Leave Management API Routes
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import User
from schemas.leave_schemas import (
    LeaveRequestCreate,
    LeaveRequestUpdate,
    LeaveStatusUpdate,
    LeaveRequestResponse,
    LeaveBalanceResponse,
    LeaveListResponse,
    LeaveStatsResponse,
    MessageResponse
)
from services.leave_service import LeaveService
from utils.dependencies import get_current_active_user, require_hr_or_manager
import math

router = APIRouter(prefix="/leaves", tags=["Leave Management"])


@router.post("", response_model=LeaveRequestResponse, status_code=status.HTTP_201_CREATED)
async def apply_for_leave(
    leave_data: LeaveRequestCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Apply for leave (employee).
    
    **Access**: All authenticated users
    
    **Features**:
    - Auto-calculates days requested
    - Validates leave balance before submission
    - Checks date range validity
    - Submits as PENDING status
    
    **Body**:
    - leave_type: casual, sick, annual, maternity, paternity
    - start_date: Leave start date (YYYY-MM-DD)
    - end_date: Leave end date (YYYY-MM-DD)
    - subject: Request subject (optional)
    - reason: Reason for leave (optional)
    - description: Detailed description (optional)
    
    **Returns**: Created leave request
    """
    return LeaveService.apply_for_leave(db, current_user.id, leave_data)


@router.get("/me", response_model=LeaveListResponse)
async def get_my_leave_requests(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status (pending/approved/rejected)"),
    leave_type: Optional[str] = Query(None, description="Filter by leave type"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get my leave requests (employee).
    
    **Access**: All authenticated users
    
    **Query Parameters**:
    - `page`: Page number (default: 1)
    - `page_size`: Items per page (default: 50, max: 100)
    - `status`: Filter by status (pending/approved/rejected)
    - `leave_type`: Filter by leave type (casual/sick/annual/etc)
    
    **Returns**: Paginated list of my leave requests
    """
    skip = (page - 1) * page_size
    
    leaves, total = LeaveService.get_my_leave_requests(
        db=db,
        employee_id=current_user.id,
        skip=skip,
        limit=page_size,
        status_filter=status,
        leave_type_filter=leave_type
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    
    return LeaveListResponse(
        leaves=leaves,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/team", response_model=LeaveListResponse)
async def get_team_leave_requests(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status"),
    current_user: User = Depends(require_hr_or_manager),
    db: Session = Depends(get_db)
):
    """
    Get team leave requests (manager).
    
    **Access**: Managers and HR
    
    **Query Parameters**:
    - `page`: Page number (default: 1)
    - `page_size`: Items per page (default: 50, max: 100)
    - `status`: Filter by status (pending/approved/rejected)
    
    **Returns**: Paginated list of team leave requests
    
    **Use Case**: Manager dashboard to approve/reject team leaves
    """
    skip = (page - 1) * page_size
    
    leaves, total = LeaveService.get_team_leave_requests(
        db=db,
        manager_id=current_user.id,
        skip=skip,
        limit=page_size,
        status_filter=status
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    
    return LeaveListResponse(
        leaves=leaves,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/all", response_model=LeaveListResponse)
async def get_all_leave_requests(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status"),
    leave_type: Optional[str] = Query(None, description="Filter by leave type"),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    current_user: User = Depends(require_hr_or_manager),
    db: Session = Depends(get_db)
):
    """
    Get all leave requests (HR).
    
    **Access**: HR and Managers
    
    **Query Parameters**:
    - `page`: Page number (default: 1)
    - `page_size`: Items per page (default: 50, max: 100)
    - `status`: Filter by status
    - `leave_type`: Filter by leave type
    - `employee_id`: Filter by employee ID
    
    **Returns**: Paginated list of all leave requests
    
    **Use Case**: HR dashboard for leave management
    """
    skip = (page - 1) * page_size
    
    leaves, total = LeaveService.get_all_leave_requests(
        db=db,
        skip=skip,
        limit=page_size,
        status_filter=status,
        leave_type_filter=leave_type,
        employee_id_filter=employee_id
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    
    return LeaveListResponse(
        leaves=leaves,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/balance/me", response_model=LeaveBalanceResponse)
async def get_my_leave_balance(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get my leave balance (employee).
    
    **Access**: All authenticated users
    
    **Returns**:
    - Casual leave balance
    - Sick leave balance
    - Annual leave balance
    - WFH balance
    
    **Use Case**: Display in dashboard, attendance page
    """
    return LeaveService.get_leave_balance(db, current_user.id)


@router.get("/balance/{employee_id}", response_model=LeaveBalanceResponse)
async def get_employee_leave_balance(
    employee_id: int,
    current_user: User = Depends(require_hr_or_manager),
    db: Session = Depends(get_db)
):
    """
    Get employee leave balance (HR/Manager).
    
    **Access**: HR and Managers
    
    **Path Parameters**:
    - `employee_id`: Employee user ID
    
    **Returns**: Employee leave balances
    """
    return LeaveService.get_leave_balance(db, employee_id)


@router.get("/{leave_id}", response_model=LeaveRequestResponse)
async def get_leave_request(
    leave_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get leave request by ID.
    
    **Access**: All authenticated users
    
    **Path Parameters**:
    - `leave_id`: Leave request ID
    
    **Returns**: Leave request details
    """
    return LeaveService.get_leave_request_by_id(db, leave_id)


@router.put("/{leave_id}", response_model=LeaveRequestResponse)
async def update_leave_request(
    leave_id: int,
    leave_data: LeaveRequestUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update leave request (employee, only if pending).
    
    **Access**: All authenticated users (own requests only)
    
    **Path Parameters**:
    - `leave_id`: Leave request ID
    
    **Body**: Fields to update (all optional)
    - start_date, end_date
    - subject, reason, description
    
    **Validation**:
    - Can only update own leave requests
    - Can only update if status is PENDING
    - Days will be recalculated if dates change
    
    **Returns**: Updated leave request
    """
    return LeaveService.update_leave_request(db, leave_id, current_user.id, leave_data)


@router.patch("/{leave_id}/status", response_model=LeaveRequestResponse)
async def update_leave_status(
    leave_id: int,
    status_data: LeaveStatusUpdate,
    current_user: User = Depends(require_hr_or_manager),
    db: Session = Depends(get_db)
):
    """
    Approve or reject leave request (manager/HR).
    
    **Access**: Managers and HR
    
    **Path Parameters**:
    - `leave_id`: Leave request ID
    
    **Body**:
    - status: approved or rejected
    - rejection_reason: Required if rejecting
    
    **Features**:
    - Auto-deducts leave balance when approving
    - Records approver and approval date
    - Cannot approve/reject if already processed
    
    **Returns**: Updated leave request
    """
    return LeaveService.approve_or_reject_leave(db, leave_id, current_user.id, status_data)


@router.delete("/{leave_id}", response_model=MessageResponse)
async def cancel_leave_request(
    leave_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Cancel leave request (employee, only if pending).
    
    **Access**: All authenticated users (own requests only)
    
    **Path Parameters**:
    - `leave_id`: Leave request ID
    
    **Validation**:
    - Can only cancel own leave requests
    - Can only cancel if status is PENDING
    
    **Returns**: Success message
    """
    LeaveService.cancel_leave_request(db, leave_id, current_user.id)
    return MessageResponse(message=f"Leave request {leave_id} cancelled successfully")


@router.get("/stats/summary", response_model=LeaveStatsResponse)
async def get_leave_stats(
    current_user: User = Depends(require_hr_or_manager),
    db: Session = Depends(get_db)
):
    """
    Get leave statistics (HR/Manager).
    
    **Access**: HR and Managers
    
    **Returns**:
    - Total requests
    - Pending/approved/rejected counts
    - Breakdown by leave type
    - Breakdown by status
    - Monthly breakdown (current year)
    
    **Use Case**: HR dashboard analytics
    """
    return LeaveService.get_leave_stats(db)

