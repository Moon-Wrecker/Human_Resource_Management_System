"""
Service layer for Team Requests management
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, extract
from typing import Optional, List, Dict
from datetime import datetime, date
from fastapi import HTTPException, status

from models import Request, User, RequestType, LeaveStatus
from schemas.request_schemas import (
    RequestCreate,
    RequestUpdate,
    RequestStatusUpdate,
    RequestResponse,
    RequestListResponse,
    RequestStatsResponse
)


def create_request(db: Session, request_data: RequestCreate, employee_id: int) -> RequestResponse:
    """
    Create a new request (employee)
    """
    # Create request
    db_request = Request(
        employee_id=employee_id,
        request_type=RequestType[request_data.request_type.upper()],
        subject=request_data.subject,
        description=request_data.description,
        request_date=request_data.request_date,
        status=LeaveStatus.PENDING,
        submitted_date=datetime.utcnow()
    )
    
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    
    return _request_to_response(db, db_request)


def get_my_requests(
    db: Session,
    employee_id: int,
    request_type: Optional[str] = None,
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 10
) -> RequestListResponse:
    """
    Get employee's own requests with filters
    """
    query = db.query(Request).filter(Request.employee_id == employee_id)
    
    # Apply filters
    if request_type:
        query = query.filter(Request.request_type == RequestType[request_type.upper()])
    
    if status:
        query = query.filter(Request.status == LeaveStatus[status.upper()])
    
    # Order by most recent first
    query = query.order_by(Request.submitted_date.desc())
    
    # Get total count
    total = query.count()
    
    # Pagination
    offset = (page - 1) * page_size
    requests = query.offset(offset).limit(page_size).all()
    
    return RequestListResponse(
        requests=[_request_to_response(db, req) for req in requests],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


def get_team_requests(
    db: Session,
    manager_id: int,
    request_type: Optional[str] = None,
    status: Optional[str] = None,
    employee_id: Optional[int] = None,
    page: int = 1,
    page_size: int = 10
) -> RequestListResponse:
    """
    Get requests from team members reporting to this manager
    """
    # Get all employees reporting to this manager
    team_members = db.query(User.id).filter(User.manager_id == manager_id).all()
    team_member_ids = [member[0] for member in team_members]
    
    if not team_member_ids:
        return RequestListResponse(
            requests=[],
            total=0,
            page=page,
            page_size=page_size,
            total_pages=0
        )
    
    query = db.query(Request).filter(Request.employee_id.in_(team_member_ids))
    
    # Apply filters
    if request_type:
        query = query.filter(Request.request_type == RequestType[request_type.upper()])
    
    if status:
        query = query.filter(Request.status == LeaveStatus[status.upper()])
    
    if employee_id:
        query = query.filter(Request.employee_id == employee_id)
    
    # Order by status (pending first), then by date
    query = query.order_by(
        Request.status.asc(),
        Request.submitted_date.desc()
    )
    
    # Get total count
    total = query.count()
    
    # Pagination
    offset = (page - 1) * page_size
    requests = query.offset(offset).limit(page_size).all()
    
    return RequestListResponse(
        requests=[_request_to_response(db, req) for req in requests],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


def get_all_requests(
    db: Session,
    request_type: Optional[str] = None,
    status: Optional[str] = None,
    employee_id: Optional[int] = None,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 10
) -> RequestListResponse:
    """
    Get all requests (HR only) with advanced filters
    """
    query = db.query(Request)
    
    # Apply filters
    if request_type:
        query = query.filter(Request.request_type == RequestType[request_type.upper()])
    
    if status:
        query = query.filter(Request.status == LeaveStatus[status.upper()])
    
    if employee_id:
        query = query.filter(Request.employee_id == employee_id)
    
    if search:
        # Search in employee name, subject, or description
        query = query.join(User, Request.employee_id == User.id).filter(
            or_(
                User.full_name.ilike(f"%{search}%"),
                Request.subject.ilike(f"%{search}%"),
                Request.description.ilike(f"%{search}%")
            )
        )
    
    # Order by status (pending first), then by date
    query = query.order_by(
        Request.status.asc(),
        Request.submitted_date.desc()
    )
    
    # Get total count
    total = query.count()
    
    # Pagination
    offset = (page - 1) * page_size
    requests = query.offset(offset).limit(page_size).all()
    
    return RequestListResponse(
        requests=[_request_to_response(db, req) for req in requests],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


def get_request_by_id(db: Session, request_id: int, user_id: int, user_role: str) -> RequestResponse:
    """
    Get request by ID with access control
    """
    db_request = db.query(Request).filter(Request.id == request_id).first()
    
    if not db_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )
    
    # Access control: Employee can see own, Manager can see team's, HR can see all
    if user_role == "employee":
        if db_request.employee_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own requests"
            )
    elif user_role == "manager":
        # Check if requester is in manager's team
        employee = db.query(User).filter(User.id == db_request.employee_id).first()
        if employee and employee.manager_id != user_id:
            # Not in team, check if it's manager's own request
            if db_request.employee_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only view requests from your team members"
                )
    # HR can see all (no check needed)
    
    return _request_to_response(db, db_request)


def update_request(db: Session, request_id: int, request_data: RequestUpdate, employee_id: int) -> RequestResponse:
    """
    Update request (employee, only if pending)
    """
    db_request = db.query(Request).filter(
        Request.id == request_id,
        Request.employee_id == employee_id
    ).first()
    
    if not db_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found or you don't have permission"
        )
    
    # Can only update pending requests
    if db_request.status != LeaveStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only update pending requests"
        )
    
    # Update fields
    update_data = request_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_request, field, value)
    
    db.commit()
    db.refresh(db_request)
    
    return _request_to_response(db, db_request)


def update_request_status(
    db: Session,
    request_id: int,
    status_update: RequestStatusUpdate,
    approver_id: int,
    approver_role: str
) -> RequestResponse:
    """
    Approve or reject request (Manager/HR)
    """
    db_request = db.query(Request).filter(Request.id == request_id).first()
    
    if not db_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )
    
    # Can only approve/reject pending requests
    if db_request.status != LeaveStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only approve/reject pending requests"
        )
    
    # Access control: Manager can approve team's requests, HR can approve all
    if approver_role == "manager":
        employee = db.query(User).filter(User.id == db_request.employee_id).first()
        if employee and employee.manager_id != approver_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only approve/reject requests from your team members"
            )
    # HR can approve all (no check needed)
    
    # Update status
    db_request.status = LeaveStatus[status_update.status.upper()]
    db_request.approved_by = approver_id
    db_request.approved_date = datetime.utcnow()
    
    if status_update.status == "rejected":
        db_request.rejection_reason = status_update.rejection_reason
    
    db.commit()
    db.refresh(db_request)
    
    return _request_to_response(db, db_request)


def delete_request(db: Session, request_id: int, employee_id: int) -> dict:
    """
    Delete request (employee, only if pending)
    """
    db_request = db.query(Request).filter(
        Request.id == request_id,
        Request.employee_id == employee_id
    ).first()
    
    if not db_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found or you don't have permission"
        )
    
    # Can only delete pending requests
    if db_request.status != LeaveStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only delete pending requests"
        )
    
    db.delete(db_request)
    db.commit()
    
    return {"message": "Request deleted successfully"}


def get_request_statistics(db: Session, user_id: Optional[int] = None, user_role: str = "hr") -> RequestStatsResponse:
    """
    Get request statistics (HR for all, Manager for team, Employee for self)
    """
    query = db.query(Request)
    
    # Apply scope based on role
    if user_role == "employee":
        query = query.filter(Request.employee_id == user_id)
    elif user_role == "manager":
        # Get team member IDs
        team_members = db.query(User.id).filter(User.manager_id == user_id).all()
        team_member_ids = [member[0] for member in team_members]
        if team_member_ids:
            query = query.filter(Request.employee_id.in_(team_member_ids))
    # HR can see all (no filter)
    
    # Total counts
    total_requests = query.count()
    pending_requests = query.filter(Request.status == LeaveStatus.PENDING).count()
    approved_requests = query.filter(Request.status == LeaveStatus.APPROVED).count()
    rejected_requests = query.filter(Request.status == LeaveStatus.REJECTED).count()
    
    # By request type
    by_type = db.query(
        Request.request_type,
        func.count(Request.id)
    ).group_by(Request.request_type)
    
    if user_role == "employee":
        by_type = by_type.filter(Request.employee_id == user_id)
    elif user_role == "manager":
        team_members = db.query(User.id).filter(User.manager_id == user_id).all()
        team_member_ids = [member[0] for member in team_members]
        if team_member_ids:
            by_type = by_type.filter(Request.employee_id.in_(team_member_ids))
    
    by_request_type = {str(rt.value): count for rt, count in by_type.all()}
    
    # By status
    by_stat = db.query(
        Request.status,
        func.count(Request.id)
    ).group_by(Request.status)
    
    if user_role == "employee":
        by_stat = by_stat.filter(Request.employee_id == user_id)
    elif user_role == "manager":
        team_members = db.query(User.id).filter(User.manager_id == user_id).all()
        team_member_ids = [member[0] for member in team_members]
        if team_member_ids:
            by_stat = by_stat.filter(Request.employee_id.in_(team_member_ids))
    
    by_status = {str(st.value): count for st, count in by_stat.all()}
    
    # By month (last 6 months)
    by_month_query = db.query(
        func.strftime('%Y-%m', Request.submitted_date).label('month'),
        func.count(Request.id)
    ).group_by('month').order_by('month')
    
    if user_role == "employee":
        by_month_query = by_month_query.filter(Request.employee_id == user_id)
    elif user_role == "manager":
        team_members = db.query(User.id).filter(User.manager_id == user_id).all()
        team_member_ids = [member[0] for member in team_members]
        if team_member_ids:
            by_month_query = by_month_query.filter(Request.employee_id.in_(team_member_ids))
    
    by_month = {month: count for month, count in by_month_query.all()}
    
    return RequestStatsResponse(
        total_requests=total_requests,
        pending_requests=pending_requests,
        approved_requests=approved_requests,
        rejected_requests=rejected_requests,
        by_request_type=by_request_type,
        by_status=by_status,
        by_month=by_month
    )


def _request_to_response(db: Session, request: Request) -> RequestResponse:
    """
    Convert Request model to RequestResponse schema
    """
    # Get employee name
    employee = db.query(User).filter(User.id == request.employee_id).first()
    employee_name = employee.name if employee else None
    
    # Get approver name if approved
    approver_name = None
    if request.approved_by:
        approver = db.query(User).filter(User.id == request.approved_by).first()
        approver_name = approver.name if approver else None
    
    return RequestResponse(
        id=request.id,
        employee_id=request.employee_id,
        employee_name=employee_name,
        request_type=request.request_type.value,
        subject=request.subject,
        description=request.description,
        request_date=request.request_date,
        status=request.status.value,
        approved_by=request.approved_by,
        approved_by_name=approver_name,
        approved_date=request.approved_date,
        rejection_reason=request.rejection_reason,
        submitted_date=request.submitted_date
    )

