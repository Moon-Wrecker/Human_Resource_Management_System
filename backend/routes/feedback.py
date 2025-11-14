"""
Feedback routes - API endpoints for feedback management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from datetime import datetime
from database import get_db
from models import User
from utils.dependencies import get_current_active_user, require_hr_or_manager
from services.feedback_service import FeedbackService
from schemas.feedback_schemas import (
    FeedbackCreate,
    FeedbackUpdate,
    FeedbackResponse,
    FeedbackListResponse,
    FeedbackStatsResponse,
    MessageResponse
)

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.get(
    "/me",
    response_model=FeedbackListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get My Feedback",
    description="Get all feedback received by the current user"
)
async def get_my_feedback(
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(100, ge=1, le=500, description="Page size"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    feedback_type: Optional[str] = Query(None, description="Filter by type"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all feedback received by the authenticated user.
    
    **Filters**:
    - `start_date`: Filter feedback from this date onwards
    - `end_date`: Filter feedback up to this date
    - `feedback_type`: Filter by feedback type (positive, constructive, etc.)
    """
    feedback, total = FeedbackService.get_feedback_for_employee(
        db=db,
        employee_id=current_user.id,
        current_user=current_user,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        feedback_type=feedback_type
    )
    
    return FeedbackListResponse(
        feedback=feedback,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get(
    "/employee/{employee_id}",
    response_model=FeedbackListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Employee Feedback",
    description="Get all feedback for a specific employee (Manager/HR only)"
)
async def get_employee_feedback(
    employee_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    feedback_type: Optional[str] = Query(None),
    current_user: User = Depends(require_hr_or_manager),
    db: Session = Depends(get_db)
):
    """
    Get all feedback for a specific employee.
    
    **Access**: Manager (team members only) or HR (all employees)
    """
    feedback, total = FeedbackService.get_feedback_for_employee(
        db=db,
        employee_id=employee_id,
        current_user=current_user,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        feedback_type=feedback_type
    )
    
    return FeedbackListResponse(
        feedback=feedback,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get(
    "/given",
    response_model=FeedbackListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Feedback I Gave",
    description="Get all feedback given by the current user (Manager/HR only)"
)
async def get_feedback_given(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(require_hr_or_manager),
    db: Session = Depends(get_db)
):
    """
    Get all feedback given by the authenticated user.
    
    **Access**: Manager or HR only
    """
    feedback, total = FeedbackService.get_feedback_given_by(
        db=db,
        given_by_user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    
    return FeedbackListResponse(
        feedback=feedback,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get(
    "",
    response_model=FeedbackListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get All Feedback",
    description="Get all feedback in the system (HR only)"
)
async def get_all_feedback(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    employee_id: Optional[int] = Query(None, description="Filter by employee"),
    given_by: Optional[int] = Query(None, description="Filter by giver"),
    feedback_type: Optional[str] = Query(None, description="Filter by type"),
    current_user: User = Depends(require_hr_or_manager),
    db: Session = Depends(get_db)
):
    """
    Get all feedback with filters.
    
    **Access**: HR only
    
    **Filters**:
    - `employee_id`: Show feedback for specific employee
    - `given_by`: Show feedback given by specific user
    - `feedback_type`: Filter by feedback type
    """
    if current_user.role != "HR":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can view all feedback"
        )
    
    feedback, total = FeedbackService.get_all_feedback(
        db=db,
        skip=skip,
        limit=limit,
        employee_id=employee_id,
        given_by=given_by,
        feedback_type=feedback_type
    )
    
    return FeedbackListResponse(
        feedback=feedback,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get(
    "/{feedback_id}",
    response_model=FeedbackResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Feedback by ID",
    description="Get specific feedback details"
)
async def get_feedback(
    feedback_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get feedback by ID.
    
    **Access**: Employee who received it, giver, or HR
    """
    return FeedbackService.get_feedback_by_id(
        db=db,
        feedback_id=feedback_id,
        current_user=current_user
    )


@router.post(
    "",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Feedback",
    description="Create new feedback (Manager/HR only)"
)
async def create_feedback(
    feedback_data: FeedbackCreate,
    current_user: User = Depends(require_hr_or_manager),
    db: Session = Depends(get_db)
):
    """
    Create new feedback for an employee.
    
    **Access**: Manager or HR only
    
    **Feedback Types**:
    - `positive`: Positive feedback/appreciation
    - `constructive`: Areas for improvement
    - `goal-related`: Related to goals
    - `performance`: Performance review feedback
    - `general`: General feedback
    
    **Rating**: Optional 1-5 scale
    """
    return FeedbackService.create_feedback(
        db=db,
        feedback_data=feedback_data,
        given_by_user_id=current_user.id
    )


@router.put(
    "/{feedback_id}",
    response_model=FeedbackResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Feedback",
    description="Update feedback (only by person who gave it)"
)
async def update_feedback(
    feedback_id: int,
    feedback_data: FeedbackUpdate,
    current_user: User = Depends(require_hr_or_manager),
    db: Session = Depends(get_db)
):
    """
    Update existing feedback.
    
    **Access**: Only the person who gave the feedback can update it
    """
    return FeedbackService.update_feedback(
        db=db,
        feedback_id=feedback_id,
        feedback_data=feedback_data,
        current_user=current_user
    )


@router.delete(
    "/{feedback_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete Feedback",
    description="Delete feedback (giver or HR)"
)
async def delete_feedback(
    feedback_id: int,
    current_user: User = Depends(require_hr_or_manager),
    db: Session = Depends(get_db)
):
    """
    Delete feedback.
    
    **Access**: Person who gave it or HR
    """
    FeedbackService.delete_feedback(
        db=db,
        feedback_id=feedback_id,
        current_user=current_user
    )
    
    return MessageResponse(message=f"Feedback {feedback_id} deleted successfully")


@router.get(
    "/stats/summary",
    response_model=FeedbackStatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Feedback Statistics",
    description="Get feedback statistics"
)
async def get_feedback_stats(
    employee_id: Optional[int] = Query(None, description="Stats for specific employee"),
    current_user: User = Depends(require_hr_or_manager),
    db: Session = Depends(get_db)
):
    """
    Get feedback statistics.
    
    **Access**: Manager or HR
    
    **Returns**:
    - Total feedback count
    - This month count
    - This quarter count
    - Average rating
    - Breakdown by feedback type
    - Recent feedback list
    """
    return FeedbackService.get_feedback_stats(db=db, employee_id=employee_id)

