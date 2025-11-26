"""
Business logic for attendance management
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from fastapi import HTTPException, status
from models import Attendance, User, Department, Team, AttendanceStatus, UserRole
from pydantic_models import (
    PunchInRequest, PunchOutRequest, MarkAttendanceRequest,
    AttendanceRecordResponse, AttendanceSummaryResponse,
    TeamAttendanceRecord, DepartmentAttendanceStats
)
from datetime import datetime, date, time, timedelta
from typing import List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class AttendanceService:
    """Service for attendance operations"""
    
    # Business rules (flexible for testing)
    EARLIEST_PUNCH_IN = time(0, 0)  # 12:00 AM (midnight) - flexible for testing
    LATEST_PUNCH_IN = time(23, 59)   # 11:59 PM - flexible for testing
    STANDARD_START_TIME = time(9, 30)  # 9:30 AM
    STANDARD_END_TIME = time(17, 30)  # 5:30 PM
    
    @staticmethod
    def _map_attendance_to_response(attendance: Attendance, include_employee_details: bool = False) -> AttendanceRecordResponse:
        """Map attendance model to response schema"""
        response_data = {
            "id": attendance.id,
            "employee_id": attendance.employee_id,
            "date": attendance.date,
            "status": attendance.status.value if isinstance(attendance.status, AttendanceStatus) else attendance.status,
            "check_in_time": attendance.check_in_time,
            "check_out_time": attendance.check_out_time,
            "hours_worked": attendance.hours_worked,
            "location": attendance.location,
            "notes": attendance.notes,
            "created_at": attendance.created_at,
            "updated_at": attendance.updated_at
        }
        
        if include_employee_details and attendance.employee:
            response_data["employee_name"] = attendance.employee.name
            response_data["employee_employee_id"] = attendance.employee.employee_id
        
        return AttendanceRecordResponse(**response_data)
    
    @staticmethod
    def punch_in(db: Session, user_id: int, request: PunchInRequest) -> Tuple[AttendanceRecordResponse, bool]:
        """
        Employee punches in for the day
        
        Returns:
            Tuple of (attendance_record, already_punched_in)
        """
        today = date.today()
        current_time = datetime.now()
        
        # Validate punch-in time
        if current_time.time() < AttendanceService.EARLIEST_PUNCH_IN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot punch in before {AttendanceService.EARLIEST_PUNCH_IN.strftime('%I:%M %p')}"
            )
        
        if current_time.time() > AttendanceService.LATEST_PUNCH_IN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot punch in after {AttendanceService.LATEST_PUNCH_IN.strftime('%I:%M %p')}. Please contact HR."
            )
        
        # Check if already punched in today
        existing_attendance = db.query(Attendance).filter(
            Attendance.employee_id == user_id,
            Attendance.date == today
        ).first()
        
        if existing_attendance:
            if existing_attendance.check_in_time:
                # Already punched in
                return AttendanceService._map_attendance_to_response(existing_attendance), True
            else:
                # Update existing record (was marked absent or leave)
                existing_attendance.check_in_time = current_time
                existing_attendance.status = AttendanceStatus[request.status.value.upper()]
                existing_attendance.location = request.location
                if request.notes:
                    existing_attendance.notes = request.notes
                existing_attendance.updated_at = current_time
                db.commit()
                db.refresh(existing_attendance)
                return AttendanceService._map_attendance_to_response(existing_attendance), False
        
        # Create new attendance record
        new_attendance = Attendance(
            employee_id=user_id,
            date=today,
            status=AttendanceStatus[request.status.value.upper()],
            check_in_time=current_time,
            location=request.location,
            notes=request.notes,
            created_at=current_time,
            updated_at=current_time
        )
        
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)
        
        logger.info(f"User {user_id} punched in at {current_time}")
        
        return AttendanceService._map_attendance_to_response(new_attendance), False
    
    @staticmethod
    def punch_out(db: Session, user_id: int, request: PunchOutRequest) -> Tuple[AttendanceRecordResponse, float]:
        """
        Employee punches out for the day
        
        Returns:
            Tuple of (attendance_record, hours_worked)
        """
        today = date.today()
        current_time = datetime.now()
        
        # Find today's attendance record
        attendance = db.query(Attendance).filter(
            Attendance.employee_id == user_id,
            Attendance.date == today
        ).first()
        
        if not attendance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No punch-in record found for today. Please punch in first."
            )
        
        if not attendance.check_in_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot punch out without punching in first"
            )
        
        if attendance.check_out_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already punched out for today"
            )
        
        # Validate punch-out time
        if current_time <= attendance.check_in_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Punch-out time cannot be before or equal to punch-in time"
            )
        
        # Calculate hours worked
        time_diff = current_time - attendance.check_in_time
        hours_worked = round(time_diff.total_seconds() / 3600, 2)
        
        # Update attendance record
        attendance.check_out_time = current_time
        attendance.hours_worked = hours_worked
        if request.notes:
            attendance.notes = attendance.notes + " | " + request.notes if attendance.notes else request.notes
        attendance.updated_at = current_time
        
        db.commit()
        db.refresh(attendance)
        
        logger.info(f"User {user_id} punched out at {current_time}, worked {hours_worked} hours")
        
        return AttendanceService._map_attendance_to_response(attendance), hours_worked
    
    @staticmethod
    def get_my_attendance(
        db: Session,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        status_filter: Optional[str] = None,
        page: int = 1,
        page_size: int = 30
    ) -> Tuple[List[AttendanceRecordResponse], int]:
        """
        Get attendance history for current user
        
        Returns:
            Tuple of (attendance_records, total_count)
        """
        # Default to last 30 days if no date range provided
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        # Build query
        query = db.query(Attendance).filter(
            Attendance.employee_id == user_id,
            Attendance.date >= start_date,
            Attendance.date <= end_date
        )
        
        # Apply status filter
        if status_filter:
            try:
                status_enum = AttendanceStatus[status_filter.upper()]
                query = query.filter(Attendance.status == status_enum)
            except KeyError:
                pass  # Invalid status, ignore filter
        
        # Get total count
        total_count = query.count()
        
        # Apply pagination
        offset = (page - 1) * page_size
        records = query.order_by(Attendance.date.desc()).offset(offset).limit(page_size).all()
        
        return [AttendanceService._map_attendance_to_response(r) for r in records], total_count
    
    @staticmethod
    def get_my_summary(db: Session, user_id: int, month: Optional[int] = None, year: Optional[int] = None) -> AttendanceSummaryResponse:
        """
        Get monthly attendance summary for current user
        """
        # Default to current month
        if not month or not year:
            today = date.today()
            month = today.month
            year = today.year
        
        # Get user details
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Calculate date range
        from_date = date(year, month, 1)
        if month == 12:
            to_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            to_date = date(year, month + 1, 1) - timedelta(days=1)
        
        # Ensure to_date is not in the future
        if to_date > date.today():
            to_date = date.today()
        
        # Get all attendance records for the month
        records = db.query(Attendance).filter(
            Attendance.employee_id == user_id,
            Attendance.date >= from_date,
            Attendance.date <= to_date
        ).all()
        
        # Calculate statistics
        total_present = sum(1 for r in records if r.status == AttendanceStatus.PRESENT)
        total_absent = sum(1 for r in records if r.status == AttendanceStatus.ABSENT)
        total_leave = sum(1 for r in records if r.status == AttendanceStatus.LEAVE)
        total_wfh = sum(1 for r in records if r.status == AttendanceStatus.WFH)
        total_holiday = sum(1 for r in records if r.status == AttendanceStatus.HOLIDAY)
        
        # Calculate total hours
        total_hours = sum(r.hours_worked or 0 for r in records)
        
        # Calculate late arrivals and early departures
        late_arrivals = 0
        early_departures = 0
        
        for r in records:
            if r.check_in_time:
                if r.check_in_time.time() > AttendanceService.STANDARD_START_TIME:
                    late_arrivals += 1
            if r.check_out_time:
                if r.check_out_time.time() < AttendanceService.STANDARD_END_TIME:
                    early_departures += 1
        
        # Calculate working days (excluding holidays)
        working_days = (to_date - from_date).days + 1 - total_holiday
        
        # Calculate attendance percentage
        attendance_percentage = 0
        if working_days > 0:
            attended_days = total_present + total_wfh
            attendance_percentage = round((attended_days / working_days) * 100, 2)
        
        # Calculate average hours
        average_hours = round(total_hours / working_days, 2) if working_days > 0 else 0
        
        return AttendanceSummaryResponse(
            employee_id=user_id,
            employee_name=user.name,
            month=month,
            year=year,
            total_present=total_present,
            total_absent=total_absent,
            total_leave=total_leave,
            total_wfh=total_wfh,
            total_holiday=total_holiday,
            total_working_days=working_days,
            total_hours_worked=round(total_hours, 2),
            average_hours_per_day=average_hours,
            late_arrivals=late_arrivals,
            early_departures=early_departures,
            attendance_percentage=attendance_percentage,
            from_date=from_date,
            to_date=to_date
        )
    
    @staticmethod
    def get_team_attendance(
        db: Session,
        manager_id: int,
        target_date: Optional[date] = None
    ) -> Tuple[List[TeamAttendanceRecord], int, int, int, int, int]:
        """
        Get team attendance for a manager (today or specific date)
        
        Returns:
            Tuple of (records, total_members, present, absent, on_leave, wfh)
        """
        if not target_date:
            target_date = date.today()
        
        # Get manager's team members
        team_members = db.query(User).filter(User.manager_id == manager_id, User.is_active == True).all()
        
        if not team_members:
            return [], 0, 0, 0, 0, 0
        
        team_member_ids = [member.id for member in team_members]
        
        # Get attendance records for the team on target date
        attendance_records = db.query(Attendance).filter(
            Attendance.employee_id.in_(team_member_ids),
            Attendance.date == target_date
        ).all()
        
        # Create a map of employee_id to attendance
        attendance_map = {record.employee_id: record for record in attendance_records}
        
        # Build response records
        team_records = []
        present = 0
        absent = 0
        on_leave = 0
        wfh = 0
        
        for member in team_members:
            attendance = attendance_map.get(member.id)
            
            if attendance:
                status = attendance.status.value if isinstance(attendance.status, AttendanceStatus) else attendance.status
                
                # Count by status
                if status == "present":
                    present += 1
                elif status == "absent":
                    absent += 1
                elif status == "leave":
                    on_leave += 1
                elif status == "wfh":
                    wfh += 1
                
                team_records.append(TeamAttendanceRecord(
                    employee_id=member.id,
                    employee_name=member.name,
                    employee_employee_id=member.employee_id or f"EMP{member.id:03d}",
                    job_role=member.job_role,
                    date=target_date,
                    status=status,
                    check_in_time=attendance.check_in_time,
                    check_out_time=attendance.check_out_time,
                    hours_worked=attendance.hours_worked,
                    location=attendance.location
                ))
            else:
                # No attendance record means absent
                absent += 1
                team_records.append(TeamAttendanceRecord(
                    employee_id=member.id,
                    employee_name=member.name,
                    employee_employee_id=member.employee_id or f"EMP{member.id:03d}",
                    job_role=member.job_role,
                    date=target_date,
                    status="absent",
                    check_in_time=None,
                    check_out_time=None,
                    hours_worked=None,
                    location=None
                ))
        
        total_members = len(team_members)
        
        return team_records, total_members, present, absent, on_leave, wfh
    
    @staticmethod
    def get_all_attendance(
        db: Session,
        target_date: Optional[date] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        department_id: Optional[int] = None,
        team_id: Optional[int] = None,
        status_filter: Optional[str] = None,
        page: int = 1,
        page_size: int = 50
    ) -> Tuple[List[AttendanceRecordResponse], int, List[DepartmentAttendanceStats]]:
        """
        Get all attendance records (HR only)
        
        Returns:
            Tuple of (attendance_records, total_count, department_stats)
        """
        # Determine date range
        if target_date:
            start_date = target_date
            end_date = target_date
        elif not start_date or not end_date:
            target_date = date.today()
            start_date = target_date
            end_date = target_date
        
        # Build query with joins
        query = db.query(Attendance).join(User, Attendance.employee_id == User.id)
        
        # Apply date filter
        query = query.filter(
            Attendance.date >= start_date,
            Attendance.date <= end_date
        )
        
        # Apply department filter
        if department_id:
            query = query.filter(User.department_id == department_id)
        
        # Apply team filter
        if team_id:
            query = query.filter(User.team_id == team_id)
        
        # Apply status filter
        if status_filter:
            try:
                status_enum = AttendanceStatus[status_filter.upper()]
                query = query.filter(Attendance.status == status_enum)
            except KeyError:
                pass
        
        # Get total count
        total_count = query.count()
        
        # Apply pagination
        offset = (page - 1) * page_size
        records = query.order_by(Attendance.date.desc(), User.name).offset(offset).limit(page_size).all()
        
        # Calculate department-wise statistics for the date range
        department_stats = AttendanceService._get_department_stats(db, start_date, end_date)
        
        return (
            [AttendanceService._map_attendance_to_response(r, include_employee_details=True) for r in records],
            total_count,
            department_stats
        )
    
    @staticmethod
    def _get_department_stats(db: Session, start_date: date, end_date: date) -> List[DepartmentAttendanceStats]:
        """Calculate department-wise attendance statistics"""
        departments = db.query(Department).filter(Department.is_active == True).all()
        
        stats = []
        for dept in departments:
            # Get all employees in department
            employees = db.query(User).filter(
                User.department_id == dept.id,
                User.is_active == True
            ).all()
            
            if not employees:
                continue
            
            employee_ids = [e.id for e in employees]
            
            # Get attendance records for this department in date range
            attendance_records = db.query(Attendance).filter(
                Attendance.employee_id.in_(employee_ids),
                Attendance.date >= start_date,
                Attendance.date <= end_date
            ).all()
            
            # Count by status
            present = sum(1 for r in attendance_records if r.status == AttendanceStatus.PRESENT)
            absent = sum(1 for r in attendance_records if r.status == AttendanceStatus.ABSENT)
            on_leave = sum(1 for r in attendance_records if r.status == AttendanceStatus.LEAVE)
            wfh = sum(1 for r in attendance_records if r.status == AttendanceStatus.WFH)
            
            # Calculate attendance percentage
            working_days = (end_date - start_date).days + 1
            expected_attendance = len(employees) * working_days
            actual_attendance = present + wfh
            attendance_percentage = round((actual_attendance / expected_attendance * 100), 2) if expected_attendance > 0 else 0
            
            stats.append(DepartmentAttendanceStats(
                department_id=dept.id,
                department_name=dept.name,
                total_employees=len(employees),
                present=present,
                absent=absent,
                on_leave=on_leave,
                wfh=wfh,
                attendance_percentage=attendance_percentage
            ))
        
        return stats
    
    @staticmethod
    def mark_attendance(
        db: Session,
        request: MarkAttendanceRequest,
        marked_by_id: int
    ) -> Tuple[AttendanceRecordResponse, str]:
        """
        HR manually marks attendance for an employee
        
        Returns:
            Tuple of (attendance_record, marked_by_name)
        """
        # Verify employee exists
        employee = db.query(User).filter(User.id == request.employee_id).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )
        
        # Get who is marking
        marked_by = db.query(User).filter(User.id == marked_by_id).first()
        marked_by_name = marked_by.name if marked_by else "Unknown"
        
        # Check if attendance already exists for this date
        existing = db.query(Attendance).filter(
            Attendance.employee_id == request.employee_id,
            Attendance.date == request.attendance_date
        ).first()
        
        # Calculate hours if both times provided
        hours_worked = None
        if request.check_in_time and request.check_out_time:
            time_diff = request.check_out_time - request.check_in_time
            hours_worked = round(time_diff.total_seconds() / 3600, 2)
        
        if existing:
            # Update existing record
            existing.status = AttendanceStatus[request.status.value.upper()]
            existing.check_in_time = request.check_in_time
            existing.check_out_time = request.check_out_time
            existing.hours_worked = hours_worked
            existing.location = request.location
            
            # Add note about manual marking
            manual_note = f"Manually marked by {marked_by_name} (HR)"
            if request.notes:
                existing.notes = f"{manual_note}: {request.notes}"
            else:
                existing.notes = manual_note
            
            existing.updated_at = datetime.now()
            
            db.commit()
            db.refresh(existing)
            
            logger.info(f"HR {marked_by_id} updated attendance for employee {request.employee_id} on {request.attendance_date}")
            
            return AttendanceService._map_attendance_to_response(existing), marked_by_name
        else:
            # Create new record
            manual_note = f"Manually marked by {marked_by_name} (HR)"
            notes = f"{manual_note}: {request.notes}" if request.notes else manual_note
            
            new_attendance = Attendance(
                employee_id=request.employee_id,
                date=request.attendance_date,
                status=AttendanceStatus[request.status.value.upper()],
                check_in_time=request.check_in_time,
                check_out_time=request.check_out_time,
                hours_worked=hours_worked,
                location=request.location,
                notes=notes,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            db.add(new_attendance)
            db.commit()
            db.refresh(new_attendance)
            
            logger.info(f"HR {marked_by_id} manually marked attendance for employee {request.employee_id} on {request.attendance_date}")
            
            return AttendanceService._map_attendance_to_response(new_attendance), marked_by_name
    
    @staticmethod
    def get_today_status(db: Session, user_id: int) -> Optional[AttendanceRecordResponse]:
        """
        Get today's attendance status for a user
        """
        today = date.today()
        attendance = db.query(Attendance).filter(
            Attendance.employee_id == user_id,
            Attendance.date == today
        ).first()
        
        if attendance:
            return AttendanceService._map_attendance_to_response(attendance)
        return None

