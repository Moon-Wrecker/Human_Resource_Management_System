"""
FastAPI routes for attendance management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from datetime import date, datetime
from database import get_db
from models import User
from utils.dependencies import get_current_active_user, require_hr, require_manager, require_hr_or_manager
from services.attendance_service import AttendanceService
from pydantic_models import (
    PunchInRequest, PunchInResponse, PunchOutRequest, PunchOutResponse,
    AttendanceHistoryResponse, AttendanceSummaryResponse,
    TeamAttendanceResponse, AllAttendanceResponse,
    MarkAttendanceRequest, MarkAttendanceResponse,
    AttendanceRecordResponse, MessageResponse
)
import math

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/punch-in", response_model=PunchInResponse, status_code=status.HTTP_200_OK)
async def punch_in(
    request: PunchInRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    **Punch in for the day**
    
    - **Employee Action**: Mark attendance by punching in
    - **Time Restrictions**: 
        - Can only punch in between 6:00 AM and 12:00 PM (noon)
        - Cannot punch in twice on the same day
    - **Status Options**: `present` or `wfh` (work from home)
    - **Location**: Default is "office", can be "home" or "client-site"
    
    **Business Rules:**
    - If already punched in today, returns existing record
    - Creates new attendance record with check-in time
    - Validates time constraints (6 AM - 12 PM)
    
    **Returns:**
    - Attendance record with check-in details
    - `already_punched_in` flag if duplicate attempt
    """
    attendance, already_punched_in = AttendanceService.punch_in(db, current_user.id, request)
    
    message = "Already punched in for today" if already_punched_in else "Punched in successfully"
    
    return PunchInResponse(
        message=message,
        attendance=attendance,
        already_punched_in=already_punched_in
    )


@router.post("/punch-out", response_model=PunchOutResponse, status_code=status.HTTP_200_OK)
async def punch_out(
    request: PunchOutRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    **Punch out for the day**
    
    - **Employee Action**: Mark end of work day by punching out
    - **Prerequisites**: Must have punched in first
    - **Auto-calculation**: Calculates total hours worked
    
    **Business Rules:**
    - Requires existing punch-in record for today
    - Cannot punch out before punch-in time
    - Cannot punch out twice
    - Automatically calculates hours worked
    
    **Returns:**
    - Updated attendance record with check-out time
    - Total hours worked for the day
    """
    attendance, hours_worked = AttendanceService.punch_out(db, current_user.id, request)
    
    return PunchOutResponse(
        message=f"Punched out successfully. You worked {hours_worked} hours today.",
        attendance=attendance,
        hours_worked=hours_worked
    )


@router.get("/today", response_model=Optional[AttendanceRecordResponse], status_code=status.HTTP_200_OK)
async def get_today_attendance(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    **Get today's attendance status**
    
    - **Quick check**: See if you've punched in/out today
    - **Returns**: Today's attendance record or null if not punched in
    
    **Use Cases:**
    - Check if already punched in before attempting punch-in
    - Display current status on dashboard
    - Show hours worked so far
    """
    return AttendanceService.get_today_status(db, current_user.id)


@router.get("/me", response_model=AttendanceHistoryResponse, status_code=status.HTTP_200_OK)
async def get_my_attendance_history(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
    start_date: Optional[date] = Query(default=None, description="Start date (default: 30 days ago)"),
    end_date: Optional[date] = Query(default=None, description="End date (default: today)"),
    status: Optional[str] = Query(default=None, description="Filter by status: present, absent, leave, wfh, holiday"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=30, ge=1, le=100, description="Records per page")
):
    """
    **Get my attendance history**
    
    - **View**: Personal attendance records with pagination
    - **Default**: Last 30 days
    - **Filters**: Date range, status type
    
    **Query Parameters:**
    - `start_date`: Filter from this date (optional)
    - `end_date`: Filter until this date (optional)
    - `status`: Filter by attendance type (optional)
    - `page`: Page number for pagination
    - `page_size`: Records per page (max 100)
    
    **Returns:**
    - List of attendance records (ordered by date desc)
    - Pagination metadata (total, pages, current page)
    - Each record includes check-in, check-out, hours worked
    """
    records, total = AttendanceService.get_my_attendance(
        db, current_user.id, start_date, end_date, status, page, page_size
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    
    return AttendanceHistoryResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        records=records
    )


@router.get("/me/summary", response_model=AttendanceSummaryResponse, status_code=status.HTTP_200_OK)
async def get_my_attendance_summary(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
    month: Optional[int] = Query(default=None, ge=1, le=12, description="Month (1-12, default: current month)"),
    year: Optional[int] = Query(default=None, ge=2020, le=2100, description="Year (default: current year)")
):
    """
    **Get monthly attendance summary**
    
    - **Overview**: Comprehensive monthly statistics
    - **Default**: Current month
    - **Analytics**: Attendance %, hours worked, punctuality
    
    **Statistics Included:**
    - Total days: present, absent, leave, WFH, holidays
    - Total hours worked and average per day
    - Attendance percentage
    - Late arrivals count (after 9:30 AM)
    - Early departures count (before 5:30 PM)
    
    **Use Cases:**
    - Monthly performance review
    - Self-assessment of punctuality
    - Track work hours
    """
    return AttendanceService.get_my_summary(db, current_user.id, month, year)


@router.get("/team", response_model=TeamAttendanceResponse, status_code=status.HTTP_200_OK)
async def get_team_attendance(
    current_user: Annotated[User, Depends(require_manager)],
    db: Session = Depends(get_db),
    date: Optional[date] = Query(default=None, description="Target date (default: today)")
):
    """
    **Get team attendance (Manager only)**
    
    - **Manager View**: See entire team's attendance for a specific date
    - **Default**: Today's attendance
    - **Real-time**: Monitor team presence
    
    **Access:** Managers only (must have team members)
    
    **Returns:**
    - List of all team members with their attendance status
    - Summary counts: present, absent, on leave, WFH
    - Individual check-in/out times and hours worked
    - Total team size
    
    **Use Cases:**
    - Daily team attendance monitoring
    - Identify absentees
    - Plan team meetings based on availability
    """
    target_date = date if date else datetime.now().date()
    
    records, total_members, present, absent, on_leave, wfh = AttendanceService.get_team_attendance(
        db, current_user.id, target_date
    )
    
    return TeamAttendanceResponse(
        date=target_date,
        total_team_members=total_members,
        present=present,
        absent=absent,
        on_leave=on_leave,
        wfh=wfh,
        records=records
    )


@router.get("/all", response_model=AllAttendanceResponse, status_code=status.HTTP_200_OK)
async def get_all_attendance(
    current_user: Annotated[User, Depends(require_hr)],
    db: Session = Depends(get_db),
    date: Optional[date] = Query(default=None, description="Specific date"),
    start_date: Optional[date] = Query(default=None, description="Start date for range"),
    end_date: Optional[date] = Query(default=None, description="End date for range"),
    department_id: Optional[int] = Query(default=None, description="Filter by department"),
    team_id: Optional[int] = Query(default=None, description="Filter by team"),
    status: Optional[str] = Query(default=None, description="Filter by status"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=50, ge=1, le=100, description="Records per page")
):
    """
    **Get all attendance records (HR only)**
    
    - **Company-wide View**: See all employees' attendance
    - **Advanced Filters**: By date, department, team, status
    - **Analytics**: Department-wise statistics
    
    **Access:** HR only
    
    **Query Parameters:**
    - `date`: View specific date (overrides date range)
    - `start_date`, `end_date`: Date range for reports
    - `department_id`: Filter by department
    - `team_id`: Filter by team
    - `status`: Filter by attendance status
    - Pagination: page, page_size
    
    **Returns:**
    - All attendance records matching filters
    - Department-wise statistics
    - Summary counts by status
    - Pagination metadata
    
    **Use Cases:**
    - Company-wide attendance reports
    - Department comparison
    - Identify attendance trends
    - Export data for payroll
    """
    records, total_count, dept_stats = AttendanceService.get_all_attendance(
        db,
        date,
        start_date,
        end_date,
        department_id,
        team_id,
        status,
        page,
        page_size
    )
    
    # Calculate overall statistics
    target_date = date if date else (start_date if start_date else datetime.now().date())
    
    # Get all active employees count
    from models import User as UserModel
    total_employees = db.query(UserModel).filter(UserModel.is_active == True).count()
    
    # Count by status from records
    present = sum(1 for r in records if r.status == "present")
    absent = sum(1 for r in records if r.status == "absent")
    on_leave = sum(1 for r in records if r.status == "leave")
    wfh = sum(1 for r in records if r.status == "wfh")
    
    total_pages = math.ceil(total_count / page_size) if total_count > 0 else 1
    
    return AllAttendanceResponse(
        date=target_date,
        total_employees=total_employees,
        present=present,
        absent=absent,
        on_leave=on_leave,
        wfh=wfh,
        department_stats=dept_stats,
        records=records,
        total_records=total_count,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.post("/mark", response_model=MarkAttendanceResponse, status_code=status.HTTP_200_OK)
async def mark_attendance_manually(
    request: MarkAttendanceRequest,
    current_user: Annotated[User, Depends(require_hr)],
    db: Session = Depends(get_db)
):
    """
    **Manually mark attendance (HR only)**
    
    - **HR Action**: Manually add or correct attendance records
    - **Full Control**: Can set any date, status, and times
    - **Audit Trail**: Tracks who made the manual entry
    
    **Access:** HR only
    
    **Use Cases:**
    - Correct mistakes in attendance
    - Mark attendance for employees who forgot to punch in
    - Add leave/holiday records retroactively
    - Handle special cases (half-day, late arrival permissions)
    
    **Request Body:**
    - `employee_id`: Employee to mark attendance for
    - `date`: Date of attendance
    - `status`: Attendance status (present, absent, leave, wfh, holiday)
    - `check_in_time`, `check_out_time`: Optional times
    - `location`: Optional location
    - `notes`: Reason for manual entry (recommended)
    
    **Returns:**
    - Created/updated attendance record
    - Name of HR person who marked it
    - Confirmation message
    
    **Note:** Manual entries are logged with HR's name in notes for audit purposes
    """
    attendance, marked_by_name = AttendanceService.mark_attendance(db, request, current_user.id)
    
    return MarkAttendanceResponse(
        message=f"Attendance marked successfully for {request.attendance_date}",
        attendance=attendance,
        marked_by=marked_by_name
    )


@router.delete("/{attendance_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def delete_attendance_record(
    attendance_id: int,
    current_user: Annotated[User, Depends(require_hr)],
    db: Session = Depends(get_db)
):
    """
    **Delete attendance record (HR only)**
    
    - **HR Action**: Remove incorrect attendance records
    - **Permanent**: Hard delete from database
    - **Use Carefully**: Cannot be undone
    
    **Access:** HR only
    
    **Use Cases:**
    - Remove duplicate entries
    - Clean up test data
    - Correct major mistakes
    
    **Recommendation:** Consider using `mark` endpoint to update instead of deleting
    """
    from models import Attendance
    
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )
    
    db.delete(attendance)
    db.commit()
    
    return MessageResponse(
        message=f"Attendance record {attendance_id} deleted successfully",
        success=True
    )

