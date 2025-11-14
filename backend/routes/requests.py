"""
API routes for Team Requests management
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from schemas.request_schemas import (
    RequestCreate,
    RequestUpdate,
    RequestStatusUpdate,
    RequestResponse,
    RequestListResponse,
    RequestStatsResponse,
    MessageResponse
)
from services import request_service
from utils.dependencies import get_current_user, require_hr, require_hr_or_manager


router = APIRouter(
    prefix="/requests",
    tags=["Team Requests"]
)


@router.post(
    "",
    response_model=RequestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a request",
    description="Submit a new request (leave, WFH, equipment, travel, etc.)"
)
async def submit_request(
    request_data: RequestCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit a new request.
    
    **Access**: All authenticated users (employees, managers, HR)
    
    **Request Types**:
    - `wfh`: Work from home request
    - `leave`: Leave request (use /leaves for leave with balance management)
    - `equipment`: Equipment request
    - `travel`: Travel request
    - `other`: Other requests
    """
    return request_service.create_request(
        db=db,
        request_data=request_data,
        employee_id=current_user["user_id"]
    )


@router.get(
    "/me",
    response_model=RequestListResponse,
    summary="Get my requests",
    description="Get all requests submitted by the current user"
)
async def get_my_requests(
    request_type: Optional[str] = Query(None, description="Filter by request type (wfh, leave, equipment, travel, other)"),
    status: Optional[str] = Query(None, description="Filter by status (pending, approved, rejected)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all requests submitted by the current user with filtering and pagination.
    
    **Access**: All authenticated users
    """
    return request_service.get_my_requests(
        db=db,
        employee_id=current_user["user_id"],
        request_type=request_type,
        status=status,
        page=page,
        page_size=page_size
    )


@router.get(
    "/team",
    response_model=RequestListResponse,
    summary="Get team requests",
    description="Get all requests from team members (Manager only)"
)
async def get_team_requests(
    request_type: Optional[str] = Query(None, description="Filter by request type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    employee_id: Optional[int] = Query(None, description="Filter by specific employee"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(require_hr_or_manager),
    db: Session = Depends(get_db)
):
    """
    Get all requests from team members reporting to the current manager.
    
    **Access**: Managers and HR
    
    **Note**: HR users should use `/requests/all` for full access.
    """
    return request_service.get_team_requests(
        db=db,
        manager_id=current_user["user_id"],
        request_type=request_type,
        status=status,
        employee_id=employee_id,
        page=page,
        page_size=page_size
    )


@router.get(
    "/all",
    response_model=RequestListResponse,
    summary="Get all requests",
    description="Get all requests in the organization (HR only)"
)
async def get_all_requests(
    request_type: Optional[str] = Query(None, description="Filter by request type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    employee_id: Optional[int] = Query(None, description="Filter by specific employee"),
    search: Optional[str] = Query(None, description="Search in employee name, subject, or description"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Get all requests in the organization with advanced filtering.
    
    **Access**: HR only
    """
    return request_service.get_all_requests(
        db=db,
        request_type=request_type,
        status=status,
        employee_id=employee_id,
        search=search,
        page=page,
        page_size=page_size
    )


@router.get(
    "/stats",
    response_model=RequestStatsResponse,
    summary="Get request statistics",
    description="Get request statistics (scoped by role)"
)
async def get_request_statistics(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get request statistics.
    
    **Access**:
    - **Employee**: Statistics for their own requests
    - **Manager**: Statistics for team requests
    - **HR**: Statistics for all requests
    """
    return request_service.get_request_statistics(
        db=db,
        user_id=current_user["user_id"],
        user_role=current_user["role"]
    )


@router.get(
    "/{request_id}",
    response_model=RequestResponse,
    summary="Get request by ID",
    description="Get detailed information about a specific request"
)
async def get_request_by_id(
    request_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get request by ID with role-based access control.
    
    **Access**:
    - **Employee**: Can view their own requests
    - **Manager**: Can view team requests
    - **HR**: Can view all requests
    """
    return request_service.get_request_by_id(
        db=db,
        request_id=request_id,
        user_id=current_user["user_id"],
        user_role=current_user["role"]
    )


@router.put(
    "/{request_id}",
    response_model=RequestResponse,
    summary="Update request",
    description="Update a pending request (Employee only, own requests)"
)
async def update_request(
    request_id: int,
    request_data: RequestUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a pending request.
    
    **Access**: Employee (can only update their own pending requests)
    
    **Note**: Only pending requests can be updated.
    """
    return request_service.update_request(
        db=db,
        request_id=request_id,
        request_data=request_data,
        employee_id=current_user["user_id"]
    )


@router.put(
    "/{request_id}/status",
    response_model=RequestResponse,
    summary="Approve or reject request",
    description="Approve or reject a request (Manager/HR)"
)
async def update_request_status(
    request_id: int,
    status_update: RequestStatusUpdate,
    current_user: dict = Depends(require_hr_or_manager),
    db: Session = Depends(get_db)
):
    """
    Approve or reject a pending request.
    
    **Access**: 
    - **Manager**: Can approve/reject team requests
    - **HR**: Can approve/reject all requests
    
    **Note**: Only pending requests can be approved/rejected.
    """
    return request_service.update_request_status(
        db=db,
        request_id=request_id,
        status_update=status_update,
        approver_id=current_user["user_id"],
        approver_role=current_user["role"]
    )


@router.delete(
    "/{request_id}",
    response_model=MessageResponse,
    summary="Delete request",
    description="Delete a pending request (Employee only, own requests)"
)
async def delete_request(
    request_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a pending request.
    
    **Access**: Employee (can only delete their own pending requests)
    
    **Note**: Only pending requests can be deleted.
    """
    return request_service.delete_request(
        db=db,
        request_id=request_id,
        employee_id=current_user["user_id"]
    )

