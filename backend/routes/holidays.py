"""
Holiday API Routes
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import User, UserRole
from schemas.holiday_schemas import (
    HolidayCreate,
    HolidayUpdate,
    HolidayResponse,
    HolidayListResponse,
    HolidayStatsResponse,
    MessageResponse
)
from services.holiday_service import HolidayService
from utils.dependencies import get_current_user, require_hr, require_hr_or_manager

router = APIRouter(prefix="/holidays", tags=["Holidays"])


@router.post("", response_model=HolidayResponse, status_code=status.HTTP_201_CREATED)
async def create_holiday(
    holiday_data: HolidayCreate,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Create a new holiday (HR only).
    
    **Access**: HR only
    
    **Permissions**:
    - Only HR can create holidays
    
    **Validation**:
    - end_date must be on or after start_date
    - holiday_type must be valid (national, religious, company, regional, optional)
    - Holiday name must be unique for overlapping dates
    """
    return HolidayService.create_holiday(db, holiday_data, current_user.id)


@router.get("", response_model=HolidayListResponse)
async def get_holidays(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    include_inactive: bool = Query(False, description="Include inactive holidays"),
    holiday_type: Optional[str] = Query(None, description="Filter by type"),
    year: Optional[int] = Query(None, description="Filter by year"),
    upcoming_only: bool = Query(False, description="Show only upcoming holidays"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of holidays with filters.
    
    **Access**: All authenticated users
    
    **Query Parameters**:
    - `page`: Page number (default: 1)
    - `page_size`: Items per page (default: 50, max: 100)
    - `include_inactive`: Include inactive holidays (default: false)
    - `holiday_type`: Filter by type (national, religious, company, regional, optional)
    - `year`: Filter by year (e.g., 2025)
    - `upcoming_only`: Show only future holidays (default: false)
    
    **Returns**: Paginated list of holidays
    """
    skip = (page - 1) * page_size
    
    holidays, total = HolidayService.get_all_holidays(
        db=db,
        skip=skip,
        limit=page_size,
        include_inactive=include_inactive,
        holiday_type=holiday_type,
        year=year,
        upcoming_only=upcoming_only
    )
    
    return HolidayListResponse(
        holidays=holidays,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/upcoming", response_model=list[HolidayResponse])
async def get_upcoming_holidays(
    days_ahead: int = Query(90, ge=1, le=365, description="Days to look ahead"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get upcoming holidays (next N days).
    
    **Access**: All authenticated users
    
    **Query Parameters**:
    - `days_ahead`: Number of days to look ahead (default: 90, max: 365)
    - `limit`: Maximum number of results (default: 10, max: 50)
    
    **Returns**: List of upcoming holidays sorted by date
    
    **Use Case**: For dashboards to show upcoming holidays
    """
    return HolidayService.get_upcoming_holidays(db, days_ahead, limit)


@router.get("/stats", response_model=HolidayStatsResponse)
async def get_holiday_stats(
    current_user: User = Depends(require_hr_or_manager),
    db: Session = Depends(get_db)
):
    """
    Get holiday statistics.
    
    **Access**: HR and Managers
    
    **Returns**:
    - Total holidays
    - Mandatory vs optional holidays
    - Upcoming holidays count
    - Holidays this month/year
    - Breakdown by type
    
    **Use Case**: For HR dashboard analytics
    """
    return HolidayService.get_holiday_stats(db)


@router.get("/{holiday_id}", response_model=HolidayResponse)
async def get_holiday(
    holiday_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get holiday details by ID.
    
    **Access**: All authenticated users
    
    **Path Parameters**:
    - `holiday_id`: Holiday ID
    
    **Returns**: Holiday details
    """
    return HolidayService.get_holiday_by_id(db, holiday_id)


@router.put("/{holiday_id}", response_model=HolidayResponse)
async def update_holiday(
    holiday_id: int,
    holiday_data: HolidayUpdate,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Update holiday (HR only).
    
    **Access**: HR only
    
    **Path Parameters**:
    - `holiday_id`: Holiday ID
    
    **Body**: Fields to update (all optional)
    
    **Returns**: Updated holiday
    """
    return HolidayService.update_holiday(db, holiday_id, holiday_data)


@router.delete("/{holiday_id}", response_model=MessageResponse)
async def delete_holiday(
    holiday_id: int,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """
    Delete holiday (soft delete, HR only).
    
    **Access**: HR only
    
    **Path Parameters**:
    - `holiday_id`: Holiday ID
    
    **Returns**: Success message
    
    **Note**: This is a soft delete (sets is_active to false)
    """
    HolidayService.delete_holiday(db, holiday_id)
    return MessageResponse(message=f"Holiday {holiday_id} deleted successfully")

