"""
Leave Service - Business logic for leave management
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_, or_
from fastapi import HTTPException, status
from models import User, LeaveRequest, LeaveType, LeaveStatus
from schemas.leave_schemas import (
    LeaveRequestCreate,
    LeaveRequestUpdate,
    LeaveStatusUpdate,
    LeaveRequestResponse,
    LeaveBalanceResponse,
    LeaveStatsResponse
)
from typing import List, Tuple, Optional
from datetime import datetime, timedelta, date
import logging

logger = logging.getLogger(__name__)


class LeaveService:
    """Service class for leave management operations"""
    
    @staticmethod
    def apply_for_leave(
        db: Session,
        employee_id: int,
        leave_data: LeaveRequestCreate
    ) -> LeaveRequestResponse:
        """Apply for leave (employee)"""
        try:
            # Get employee
            employee = db.query(User).filter(User.id == employee_id).first()
            if not employee:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Employee not found"
                )
            
            # Calculate days requested
            days_requested = (leave_data.end_date - leave_data.start_date).days + 1
            if days_requested <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid date range"
                )
            
            # Check leave balance
            leave_type_map = {
                "casual": (employee.casual_leave_balance, "casual"),
                "sick": (employee.sick_leave_balance, "sick"),
                "annual": (employee.annual_leave_balance, "annual")
            }
            
            if leave_data.leave_type.value in leave_type_map:
                balance, leave_name = leave_type_map[leave_data.leave_type.value]
                if days_requested > balance:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Insufficient {leave_name} leave balance. Available: {balance}, Requested: {days_requested}"
                    )
            
            # Map to enum
            leave_type_enum = LeaveType[leave_data.leave_type.value.upper()]
            
            # Create leave request
            leave_request = LeaveRequest(
                employee_id=employee_id,
                leave_type=leave_type_enum,
                start_date=leave_data.start_date,
                end_date=leave_data.end_date,
                days_requested=days_requested,
                subject=leave_data.subject,
                reason=leave_data.reason,
                description=leave_data.description,
                status=LeaveStatus.PENDING
            )
            
            db.add(leave_request)
            db.commit()
            db.refresh(leave_request)
            
            logger.info(f"Leave request created: {leave_request.id} by employee {employee_id}")
            
            return LeaveService._format_leave_response(leave_request, db)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating leave request: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create leave request: {str(e)}"
            )
    
    @staticmethod
    def get_my_leave_requests(
        db: Session,
        employee_id: int,
        skip: int = 0,
        limit: int = 100,
        status_filter: Optional[str] = None,
        leave_type_filter: Optional[str] = None
    ) -> Tuple[List[LeaveRequestResponse], int]:
        """Get my leave requests"""
        query = db.query(LeaveRequest).filter(LeaveRequest.employee_id == employee_id)
        
        # Status filter
        if status_filter:
            try:
                status_enum = LeaveStatus[status_filter.upper()]
                query = query.filter(LeaveRequest.status == status_enum)
            except KeyError:
                pass
        
        # Leave type filter
        if leave_type_filter:
            try:
                type_enum = LeaveType[leave_type_filter.upper()]
                query = query.filter(LeaveRequest.leave_type == type_enum)
            except KeyError:
                pass
        
        total = query.count()
        leaves = query.order_by(LeaveRequest.requested_date.desc()).offset(skip).limit(limit).all()
        
        formatted_leaves = [LeaveService._format_leave_response(l, db) for l in leaves]
        return formatted_leaves, total
    
    @staticmethod
    def get_team_leave_requests(
        db: Session,
        manager_id: int,
        skip: int = 0,
        limit: int = 100,
        status_filter: Optional[str] = None
    ) -> Tuple[List[LeaveRequestResponse], int]:
        """Get team leave requests (manager)"""
        # Get all team members
        team_members = db.query(User).filter(User.manager_id == manager_id).all()
        team_member_ids = [m.id for m in team_members]
        
        if not team_member_ids:
            return [], 0
        
        query = db.query(LeaveRequest).filter(LeaveRequest.employee_id.in_(team_member_ids))
        
        # Status filter
        if status_filter:
            try:
                status_enum = LeaveStatus[status_filter.upper()]
                query = query.filter(LeaveRequest.status == status_enum)
            except KeyError:
                pass
        
        total = query.count()
        leaves = query.order_by(LeaveRequest.requested_date.desc()).offset(skip).limit(limit).all()
        
        formatted_leaves = [LeaveService._format_leave_response(l, db) for l in leaves]
        return formatted_leaves, total
    
    @staticmethod
    def get_all_leave_requests(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status_filter: Optional[str] = None,
        leave_type_filter: Optional[str] = None,
        employee_id_filter: Optional[int] = None
    ) -> Tuple[List[LeaveRequestResponse], int]:
        """Get all leave requests (HR)"""
        query = db.query(LeaveRequest)
        
        # Employee filter
        if employee_id_filter:
            query = query.filter(LeaveRequest.employee_id == employee_id_filter)
        
        # Status filter
        if status_filter:
            try:
                status_enum = LeaveStatus[status_filter.upper()]
                query = query.filter(LeaveRequest.status == status_enum)
            except KeyError:
                pass
        
        # Leave type filter
        if leave_type_filter:
            try:
                type_enum = LeaveType[leave_type_filter.upper()]
                query = query.filter(LeaveRequest.leave_type == type_enum)
            except KeyError:
                pass
        
        total = query.count()
        leaves = query.order_by(LeaveRequest.requested_date.desc()).offset(skip).limit(limit).all()
        
        formatted_leaves = [LeaveService._format_leave_response(l, db) for l in leaves]
        return formatted_leaves, total
    
    @staticmethod
    def get_leave_request_by_id(db: Session, leave_id: int) -> LeaveRequestResponse:
        """Get leave request by ID"""
        leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
        
        if not leave:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Leave request {leave_id} not found"
            )
        
        return LeaveService._format_leave_response(leave, db)
    
    @staticmethod
    def update_leave_request(
        db: Session,
        leave_id: int,
        employee_id: int,
        leave_data: LeaveRequestUpdate
    ) -> LeaveRequestResponse:
        """Update leave request (employee, only if pending)"""
        leave = db.query(LeaveRequest).filter(
            LeaveRequest.id == leave_id,
            LeaveRequest.employee_id == employee_id
        ).first()
        
        if not leave:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Leave request not found"
            )
        
        if leave.status != LeaveStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update leave request that has been processed"
            )
        
        try:
            # Update fields
            update_data = leave_data.dict(exclude_unset=True)
            
            # Recalculate days if dates changed
            if 'start_date' in update_data or 'end_date' in update_data:
                start = update_data.get('start_date', leave.start_date)
                end = update_data.get('end_date', leave.end_date)
                days_requested = (end - start).days + 1
                
                if days_requested <= 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid date range"
                    )
                
                update_data['days_requested'] = days_requested
            
            for field, value in update_data.items():
                setattr(leave, field, value)
            
            db.commit()
            db.refresh(leave)
            
            logger.info(f"Leave request updated: {leave_id}")
            
            return LeaveService._format_leave_response(leave, db)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating leave request: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update leave request: {str(e)}"
            )
    
    @staticmethod
    def approve_or_reject_leave(
        db: Session,
        leave_id: int,
        approver_id: int,
        status_data: LeaveStatusUpdate
    ) -> LeaveRequestResponse:
        """Approve or reject leave (manager/HR)"""
        leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
        
        if not leave:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Leave request not found"
            )
        
        if leave.status != LeaveStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Leave request already {leave.status.value}"
            )
        
        try:
            # Map to enum
            new_status = LeaveStatus[status_data.status.value.upper()]
            
            # If approving, deduct from balance
            if new_status == LeaveStatus.APPROVED:
                employee = db.query(User).filter(User.id == leave.employee_id).first()
                if employee:
                    if leave.leave_type == LeaveType.CASUAL:
                        employee.casual_leave_balance -= leave.days_requested
                    elif leave.leave_type == LeaveType.SICK:
                        employee.sick_leave_balance -= leave.days_requested
                    elif leave.leave_type == LeaveType.ANNUAL:
                        employee.annual_leave_balance -= leave.days_requested
            
            # Update leave request
            leave.status = new_status
            leave.approved_by = approver_id
            leave.approved_date = datetime.utcnow()
            leave.rejection_reason = status_data.rejection_reason
            
            db.commit()
            db.refresh(leave)
            
            logger.info(f"Leave request {leave_id} {new_status.value} by {approver_id}")
            
            return LeaveService._format_leave_response(leave, db)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating leave status: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update leave status: {str(e)}"
            )
    
    @staticmethod
    def cancel_leave_request(db: Session, leave_id: int, employee_id: int) -> None:
        """Cancel leave request (employee, only if pending)"""
        leave = db.query(LeaveRequest).filter(
            LeaveRequest.id == leave_id,
            LeaveRequest.employee_id == employee_id
        ).first()
        
        if not leave:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Leave request not found"
            )
        
        if leave.status != LeaveStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot cancel leave request that has been processed"
            )
        
        try:
            db.delete(leave)
            db.commit()
            logger.info(f"Leave request cancelled: {leave_id}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error cancelling leave request: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to cancel leave request: {str(e)}"
            )
    
    @staticmethod
    def get_leave_balance(db: Session, employee_id: int) -> LeaveBalanceResponse:
        """Get leave balance for employee"""
        employee = db.query(User).filter(User.id == employee_id).first()
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )
        
        return LeaveBalanceResponse(
            employee_id=employee.id,
            employee_name=employee.name,
            casual_leave_balance=employee.casual_leave_balance,
            sick_leave_balance=employee.sick_leave_balance,
            annual_leave_balance=employee.annual_leave_balance,
            wfh_balance=employee.wfh_balance
        )
    
    @staticmethod
    def get_leave_stats(db: Session) -> LeaveStatsResponse:
        """Get leave statistics (HR)"""
        # Total and by status
        total_requests = db.query(LeaveRequest).count()
        pending_requests = db.query(LeaveRequest).filter(LeaveRequest.status == LeaveStatus.PENDING).count()
        approved_requests = db.query(LeaveRequest).filter(LeaveRequest.status == LeaveStatus.APPROVED).count()
        rejected_requests = db.query(LeaveRequest).filter(LeaveRequest.status == LeaveStatus.REJECTED).count()
        
        # By leave type
        type_results = db.query(
            LeaveRequest.leave_type,
            func.count(LeaveRequest.id)
        ).group_by(LeaveRequest.leave_type).all()
        by_leave_type = {ltype.value: count for ltype, count in type_results}
        
        # By status
        status_results = db.query(
            LeaveRequest.status,
            func.count(LeaveRequest.id)
        ).group_by(LeaveRequest.status).all()
        by_status = {stat.value: count for stat, count in status_results}
        
        # By month (current year)
        current_year = datetime.utcnow().year
        month_results = db.query(
            extract('month', LeaveRequest.start_date).label('month'),
            func.count(LeaveRequest.id)
        ).filter(
            extract('year', LeaveRequest.start_date) == current_year
        ).group_by('month').all()
        by_month = {int(month): count for month, count in month_results}
        
        return LeaveStatsResponse(
            total_requests=total_requests,
            pending_requests=pending_requests,
            approved_requests=approved_requests,
            rejected_requests=rejected_requests,
            by_leave_type=by_leave_type,
            by_status=by_status,
            by_month=by_month
        )
    
    @staticmethod
    def _format_leave_response(leave: LeaveRequest, db: Session) -> LeaveRequestResponse:
        """Format leave request to response schema"""
        # Get employee name
        employee = db.query(User).filter(User.id == leave.employee_id).first()
        employee_name = employee.name if employee else None
        
        # Get approver name
        approver_name = None
        if leave.approved_by:
            approver = db.query(User).filter(User.id == leave.approved_by).first()
            approver_name = approver.name if approver else None
        
        return LeaveRequestResponse(
            id=leave.id,
            employee_id=leave.employee_id,
            employee_name=employee_name,
            leave_type=leave.leave_type.value if leave.leave_type else None,
            start_date=leave.start_date,
            end_date=leave.end_date,
            days_requested=leave.days_requested,
            subject=leave.subject,
            reason=leave.reason,
            description=leave.description,
            status=leave.status.value if leave.status else 'pending',
            approved_by=leave.approved_by,
            approved_by_name=approver_name,
            approved_date=leave.approved_date,
            rejection_reason=leave.rejection_reason,
            requested_date=leave.requested_date
        )

