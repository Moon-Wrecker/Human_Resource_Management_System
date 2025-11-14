"""
Holiday Service - Business logic for holiday management
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_, or_
from fastapi import HTTPException, status
from models import Holiday, User
from schemas.holiday_schemas import (
    HolidayCreate,
    HolidayUpdate,
    HolidayResponse,
    HolidayStatsResponse
)
from typing import List, Optional, Tuple
from datetime import datetime, date, timedelta
import logging

logger = logging.getLogger(__name__)


class HolidayService:
    """Service class for holiday operations"""
    
    @staticmethod
    def create_holiday(
        db: Session,
        holiday_data: HolidayCreate,
        created_by_user_id: int
    ) -> HolidayResponse:
        """Create new holiday"""
        try:
            # Check for overlapping holidays with same name
            existing = db.query(Holiday).filter(
                and_(
                    Holiday.name == holiday_data.name,
                    Holiday.is_active == True,
                    or_(
                        and_(
                            Holiday.start_date <= holiday_data.end_date,
                            Holiday.end_date >= holiday_data.start_date
                        )
                    )
                )
            ).first()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Holiday '{holiday_data.name}' already exists for overlapping dates"
                )
            
            # Create holiday
            new_holiday = Holiday(
                name=holiday_data.name,
                description=holiday_data.description,
                start_date=holiday_data.start_date,
                end_date=holiday_data.end_date,
                is_mandatory=holiday_data.is_mandatory,
                holiday_type=holiday_data.holiday_type,
                created_by=created_by_user_id
            )
            
            db.add(new_holiday)
            db.commit()
            db.refresh(new_holiday)
            
            logger.info(f"Holiday created: {new_holiday.name} ({new_holiday.id})")
            
            return HolidayService._format_holiday_response(new_holiday, db)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating holiday: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create holiday: {str(e)}"
            )
    
    @staticmethod
    def get_holiday_by_id(db: Session, holiday_id: int) -> HolidayResponse:
        """Get holiday by ID"""
        holiday = db.query(Holiday).filter(Holiday.id == holiday_id).first()
        
        if not holiday:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Holiday with ID {holiday_id} not found"
            )
        
        return HolidayService._format_holiday_response(holiday, db)
    
    @staticmethod
    def get_all_holidays(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        include_inactive: bool = False,
        holiday_type: Optional[str] = None,
        year: Optional[int] = None,
        upcoming_only: bool = False
    ) -> Tuple[List[HolidayResponse], int]:
        """Get all holidays with filters"""
        query = db.query(Holiday)
        
        # Filter active/inactive
        if not include_inactive:
            query = query.filter(Holiday.is_active == True)
        
        # Filter by type
        if holiday_type:
            query = query.filter(Holiday.holiday_type == holiday_type)
        
        # Filter by year
        if year:
            query = query.filter(extract('year', Holiday.start_date) == year)
        
        # Filter upcoming only
        if upcoming_only:
            today = date.today()
            query = query.filter(Holiday.end_date >= today)
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        holidays = query.order_by(Holiday.start_date.asc()).offset(skip).limit(limit).all()
        
        # Format responses
        formatted_holidays = [
            HolidayService._format_holiday_response(h, db) for h in holidays
        ]
        
        return formatted_holidays, total
    
    @staticmethod
    def get_upcoming_holidays(
        db: Session,
        days_ahead: int = 90,
        limit: int = 10
    ) -> List[HolidayResponse]:
        """Get upcoming holidays (next N days)"""
        today = date.today()
        end_date = today + timedelta(days=days_ahead)
        
        holidays = db.query(Holiday).filter(
            and_(
                Holiday.is_active == True,
                Holiday.start_date >= today,
                Holiday.start_date <= end_date
            )
        ).order_by(Holiday.start_date.asc()).limit(limit).all()
        
        return [HolidayService._format_holiday_response(h, db) for h in holidays]
    
    @staticmethod
    def update_holiday(
        db: Session,
        holiday_id: int,
        holiday_data: HolidayUpdate
    ) -> HolidayResponse:
        """Update holiday"""
        holiday = db.query(Holiday).filter(Holiday.id == holiday_id).first()
        
        if not holiday:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Holiday with ID {holiday_id} not found"
            )
        
        try:
            # Update fields
            update_data = holiday_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(holiday, field, value)
            
            db.commit()
            db.refresh(holiday)
            
            logger.info(f"Holiday updated: {holiday.name} ({holiday_id})")
            
            return HolidayService._format_holiday_response(holiday, db)
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating holiday: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update holiday: {str(e)}"
            )
    
    @staticmethod
    def delete_holiday(db: Session, holiday_id: int) -> None:
        """Delete holiday (soft delete)"""
        holiday = db.query(Holiday).filter(Holiday.id == holiday_id).first()
        
        if not holiday:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Holiday with ID {holiday_id} not found"
            )
        
        try:
            # Soft delete
            holiday.is_active = False
            db.commit()
            logger.info(f"Holiday deleted: {holiday.name} ({holiday_id})")
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting holiday: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete holiday: {str(e)}"
            )
    
    @staticmethod
    def get_holiday_stats(db: Session) -> HolidayStatsResponse:
        """Get holiday statistics"""
        now = date.today()
        current_year = now.year
        current_month = now.month
        
        # Total holidays
        total_holidays = db.query(Holiday).filter(Holiday.is_active == True).count()
        
        # Mandatory vs optional
        mandatory = db.query(Holiday).filter(
            and_(Holiday.is_active == True, Holiday.is_mandatory == True)
        ).count()
        
        optional = total_holidays - mandatory
        
        # Upcoming holidays
        upcoming = db.query(Holiday).filter(
            and_(
                Holiday.is_active == True,
                Holiday.start_date >= now
            )
        ).count()
        
        # This month
        this_month = db.query(Holiday).filter(
            and_(
                Holiday.is_active == True,
                extract('year', Holiday.start_date) == current_year,
                extract('month', Holiday.start_date) == current_month
            )
        ).count()
        
        # This year
        this_year = db.query(Holiday).filter(
            and_(
                Holiday.is_active == True,
                extract('year', Holiday.start_date) == current_year
            )
        ).count()
        
        # By type
        by_type_results = db.query(
            Holiday.holiday_type,
            func.count(Holiday.id)
        ).filter(
            and_(Holiday.is_active == True, Holiday.holiday_type.isnot(None))
        ).group_by(Holiday.holiday_type).all()
        
        by_type = {holiday_type: count for holiday_type, count in by_type_results}
        
        return HolidayStatsResponse(
            total_holidays=total_holidays,
            mandatory_holidays=mandatory,
            optional_holidays=optional,
            upcoming_holidays=upcoming,
            holidays_this_month=this_month,
            holidays_this_year=this_year,
            by_type=by_type
        )
    
    @staticmethod
    def _format_holiday_response(holiday: Holiday, db: Session) -> HolidayResponse:
        """Format holiday model to response schema"""
        # Get creator details
        created_by_user = None
        created_by_name = None
        if holiday.created_by:
            created_by_user = db.query(User).filter(User.id == holiday.created_by).first()
            created_by_name = created_by_user.name if created_by_user else None
        
        # Calculate duration
        duration_days = (holiday.end_date - holiday.start_date).days + 1
        
        return HolidayResponse(
            id=holiday.id,
            name=holiday.name,
            description=holiday.description,
            start_date=holiday.start_date,
            end_date=holiday.end_date,
            is_mandatory=holiday.is_mandatory,
            holiday_type=holiday.holiday_type,
            is_active=holiday.is_active,
            created_by=holiday.created_by,
            created_by_name=created_by_name,
            created_at=holiday.created_at,
            duration_days=duration_days
        )

