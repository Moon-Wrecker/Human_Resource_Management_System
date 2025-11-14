"""
Feedback Service - Business logic for feedback management
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_, or_
from fastapi import HTTPException, status
from models import Feedback, User
from schemas.feedback_schemas import (
    FeedbackCreate,
    FeedbackUpdate,
    FeedbackResponse,
    FeedbackStatsResponse
)
from typing import List, Optional, Tuple
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class FeedbackService:
    """Service class for feedback operations"""
    
    @staticmethod
    def create_feedback(
        db: Session,
        feedback_data: FeedbackCreate,
        given_by_user_id: int
    ) -> FeedbackResponse:
        """
        Create new feedback
        
        Args:
            db: Database session
            feedback_data: Feedback creation data
            given_by_user_id: ID of user giving feedback
            
        Returns:
            FeedbackResponse with created feedback
        """
        try:
            # Verify employee exists
            employee = db.query(User).filter(User.id == feedback_data.employee_id).first()
            if not employee:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Employee with ID {feedback_data.employee_id} not found"
                )
            
            # Verify giver exists
            giver = db.query(User).filter(User.id == given_by_user_id).first()
            if not giver:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Feedback giver not found"
                )
            
            # Create feedback
            new_feedback = Feedback(
                employee_id=feedback_data.employee_id,
                given_by=given_by_user_id,
                subject=feedback_data.subject,
                description=feedback_data.description,
                feedback_type=feedback_data.feedback_type,
                rating=feedback_data.rating
            )
            
            db.add(new_feedback)
            db.commit()
            db.refresh(new_feedback)
            
            logger.info(f"Feedback created: ID {new_feedback.id} by user {given_by_user_id} for employee {feedback_data.employee_id}")
            
            return FeedbackService._format_feedback_response(new_feedback, db)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating feedback: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create feedback: {str(e)}"
            )
    
    @staticmethod
    def get_feedback_by_id(
        db: Session,
        feedback_id: int,
        current_user: User
    ) -> FeedbackResponse:
        """Get feedback by ID with access control"""
        feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
        
        if not feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Feedback with ID {feedback_id} not found"
            )
        
        # Access control: Only employee who received it, giver, or HR can view
        if current_user.role != "HR" and current_user.id not in [feedback.employee_id, feedback.given_by]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to view this feedback"
            )
        
        return FeedbackService._format_feedback_response(feedback, db)
    
    @staticmethod
    def get_feedback_for_employee(
        db: Session,
        employee_id: int,
        current_user: User,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        feedback_type: Optional[str] = None
    ) -> Tuple[List[FeedbackResponse], int]:
        """
        Get all feedback for a specific employee
        
        Args:
            db: Database session
            employee_id: ID of employee
            current_user: Current authenticated user
            skip: Pagination offset
            limit: Page size
            start_date: Filter by start date
            end_date: Filter by end date
            feedback_type: Filter by type
            
        Returns:
            Tuple of (feedback list, total count)
        """
        # Access control
        if current_user.role == "EMPLOYEE" and current_user.id != employee_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own feedback"
            )
        
        # Build query
        query = db.query(Feedback).filter(Feedback.employee_id == employee_id)
        
        # Apply filters
        if start_date:
            query = query.filter(Feedback.given_on >= start_date)
        if end_date:
            query = query.filter(Feedback.given_on <= end_date)
        if feedback_type:
            query = query.filter(Feedback.feedback_type == feedback_type)
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        feedback_list = query.order_by(Feedback.given_on.desc()).offset(skip).limit(limit).all()
        
        # Format responses
        formatted_feedback = [
            FeedbackService._format_feedback_response(f, db) for f in feedback_list
        ]
        
        return formatted_feedback, total
    
    @staticmethod
    def get_feedback_given_by(
        db: Session,
        given_by_user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[FeedbackResponse], int]:
        """Get all feedback given by a specific user (managers/HR)"""
        query = db.query(Feedback).filter(Feedback.given_by == given_by_user_id)
        
        total = query.count()
        feedback_list = query.order_by(Feedback.given_on.desc()).offset(skip).limit(limit).all()
        
        formatted_feedback = [
            FeedbackService._format_feedback_response(f, db) for f in feedback_list
        ]
        
        return formatted_feedback, total
    
    @staticmethod
    def get_all_feedback(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        employee_id: Optional[int] = None,
        given_by: Optional[int] = None,
        feedback_type: Optional[str] = None
    ) -> Tuple[List[FeedbackResponse], int]:
        """Get all feedback (HR only)"""
        query = db.query(Feedback)
        
        # Apply filters
        if employee_id:
            query = query.filter(Feedback.employee_id == employee_id)
        if given_by:
            query = query.filter(Feedback.given_by == given_by)
        if feedback_type:
            query = query.filter(Feedback.feedback_type == feedback_type)
        
        total = query.count()
        feedback_list = query.order_by(Feedback.given_on.desc()).offset(skip).limit(limit).all()
        
        formatted_feedback = [
            FeedbackService._format_feedback_response(f, db) for f in feedback_list
        ]
        
        return formatted_feedback, total
    
    @staticmethod
    def update_feedback(
        db: Session,
        feedback_id: int,
        feedback_data: FeedbackUpdate,
        current_user: User
    ) -> FeedbackResponse:
        """Update feedback (only by person who gave it)"""
        feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
        
        if not feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Feedback with ID {feedback_id} not found"
            )
        
        # Only the person who gave the feedback can update it
        if current_user.id != feedback.given_by:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update feedback you gave"
            )
        
        try:
            # Update fields
            update_data = feedback_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(feedback, field, value)
            
            db.commit()
            db.refresh(feedback)
            
            logger.info(f"Feedback updated: ID {feedback_id} by user {current_user.id}")
            
            return FeedbackService._format_feedback_response(feedback, db)
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating feedback: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update feedback: {str(e)}"
            )
    
    @staticmethod
    def delete_feedback(
        db: Session,
        feedback_id: int,
        current_user: User
    ) -> None:
        """Delete feedback (only by person who gave it or HR)"""
        feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
        
        if not feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Feedback with ID {feedback_id} not found"
            )
        
        # Only giver or HR can delete
        if current_user.role != "HR" and current_user.id != feedback.given_by:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete feedback you gave"
            )
        
        try:
            db.delete(feedback)
            db.commit()
            logger.info(f"Feedback deleted: ID {feedback_id} by user {current_user.id}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting feedback: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete feedback: {str(e)}"
            )
    
    @staticmethod
    def get_feedback_stats(db: Session, employee_id: Optional[int] = None) -> FeedbackStatsResponse:
        """Get feedback statistics"""
        now = datetime.utcnow()
        month_ago = now - timedelta(days=30)
        quarter_ago = now - timedelta(days=90)
        
        # Base query
        query = db.query(Feedback)
        if employee_id:
            query = query.filter(Feedback.employee_id == employee_id)
        
        # Total feedback
        total_feedback = query.count()
        
        # This month
        this_month = query.filter(Feedback.given_on >= month_ago).count()
        
        # This quarter
        this_quarter = query.filter(Feedback.given_on >= quarter_ago).count()
        
        # Average rating
        avg_rating = db.query(func.avg(Feedback.rating)).filter(
            Feedback.rating.isnot(None)
        ).scalar()
        if employee_id:
            avg_rating = db.query(func.avg(Feedback.rating)).filter(
                and_(Feedback.employee_id == employee_id, Feedback.rating.isnot(None))
            ).scalar()
        
        # By type
        by_type_query = query.filter(Feedback.feedback_type.isnot(None))
        if employee_id:
            by_type_query = by_type_query.filter(Feedback.employee_id == employee_id)
        
        by_type_results = db.query(
            Feedback.feedback_type,
            func.count(Feedback.id)
        ).filter(
            Feedback.feedback_type.isnot(None)
        ).group_by(Feedback.feedback_type).all()
        
        if employee_id:
            by_type_results = db.query(
                Feedback.feedback_type,
                func.count(Feedback.id)
            ).filter(
                and_(Feedback.employee_id == employee_id, Feedback.feedback_type.isnot(None))
            ).group_by(Feedback.feedback_type).all()
        
        by_type = {feedback_type: count for feedback_type, count in by_type_results}
        
        # Recent feedback
        recent_query = query.order_by(Feedback.given_on.desc()).limit(5).all()
        recent_feedback = [
            FeedbackService._format_feedback_response(f, db) for f in recent_query
        ]
        
        return FeedbackStatsResponse(
            total_feedback=total_feedback,
            this_month=this_month,
            this_quarter=this_quarter,
            average_rating=round(float(avg_rating), 2) if avg_rating else None,
            by_type=by_type,
            recent_feedback=recent_feedback
        )
    
    @staticmethod
    def _format_feedback_response(feedback: Feedback, db: Session) -> FeedbackResponse:
        """Format feedback model to response schema"""
        # Get employee and giver details
        employee = db.query(User).filter(User.id == feedback.employee_id).first()
        giver = db.query(User).filter(User.id == feedback.given_by).first()
        
        return FeedbackResponse(
            id=feedback.id,
            employee_id=feedback.employee_id,
            employee_name=employee.name if employee else "Unknown",
            given_by=feedback.given_by,
            given_by_name=giver.name if giver else "Unknown",
            subject=feedback.subject,
            description=feedback.description,
            feedback_type=feedback.feedback_type,
            rating=feedback.rating,
            given_on=feedback.given_on
        )

