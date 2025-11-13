"""
Dashboard Service - Business logic for dashboard data
Handles data aggregation and computation for HR, Manager, and Employee dashboards
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, case
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
from models import (
    User, UserRole, Department, Team, Application, ApplicationStatus,
    Attendance, AttendanceStatus, LeaveRequest, Goal, GoalStatus,
    SkillModuleEnrollment, ModuleStatus, Holiday, PerformanceReport
)
from schemas.dashboard_schemas import (
    DepartmentEmployeeCount, DepartmentAttendance, DepartmentModulesCompleted,
    ActiveApplicationInfo, HRDashboardResponse, TeamMemberAttendance,
    TeamMemberModules, TeamGoalsStats, TeamStats, ManagerDashboardResponse,
    GoalStats, EmployeeDashboardResponse, LeaveBalanceInfo, AttendanceInfo,
    HolidayInfo, PerformanceMetrics, MonthlyModulesCompleted
)


class DashboardService:
    """Service class for dashboard operations"""
    
    # ==================== Common Helper Methods ====================
    
    @staticmethod
    def get_upcoming_holidays(db: Session, limit: int = 10) -> List[HolidayInfo]:
        """Get upcoming holidays"""
        today = date.today()
        holidays = db.query(Holiday).filter(
            Holiday.start_date >= today,
            Holiday.is_active == True
        ).order_by(Holiday.start_date).limit(limit).all()
        
        return [HolidayInfo.model_validate(h) for h in holidays]
    
    @staticmethod
    def get_today_attendance(db: Session, employee_id: int) -> Optional[AttendanceInfo]:
        """Get today's attendance for an employee"""
        today = date.today()
        attendance = db.query(Attendance).filter(
            Attendance.employee_id == employee_id,
            Attendance.date == today
        ).first()
        
        if attendance:
            return AttendanceInfo.model_validate(attendance)
        return None
    
    @staticmethod
    def get_leave_balance(user: User) -> LeaveBalanceInfo:
        """Get leave balance for a user"""
        return LeaveBalanceInfo(
            casual_leave=user.casual_leave_balance or 0,
            sick_leave=user.sick_leave_balance or 0,
            annual_leave=user.annual_leave_balance or 0,
            wfh_balance=user.wfh_balance or 0
        )
    
    @staticmethod
    def calculate_learner_rank(db: Session, employee_id: int) -> Optional[int]:
        """Calculate employee's rank based on modules completed"""
        # Get all employees with their module counts
        module_counts = db.query(
            SkillModuleEnrollment.employee_id,
            func.count(SkillModuleEnrollment.id).label('completed_count')
        ).filter(
            SkillModuleEnrollment.status == ModuleStatus.COMPLETED
        ).group_by(
            SkillModuleEnrollment.employee_id
        ).subquery()
        
        # Get employee's count
        employee_count = db.query(module_counts.c.completed_count).filter(
            module_counts.c.employee_id == employee_id
        ).scalar()
        
        if employee_count is None:
            return None
        
        # Count how many employees have more completed modules
        rank = db.query(func.count()).select_from(module_counts).filter(
            module_counts.c.completed_count > employee_count
        ).scalar()
        
        return rank + 1 if rank is not None else 1
    
    # ==================== HR Dashboard Methods ====================
    
    @staticmethod
    def get_hr_dashboard_data(db: Session) -> HRDashboardResponse:
        """Get complete HR dashboard data"""
        
        # Get department employee counts
        departments = DashboardService._get_department_employee_counts(db)
        
        # Get department attendance statistics
        department_attendance = DashboardService._get_department_attendance_stats(db)
        
        # Get department modules completion
        department_modules = DashboardService._get_department_modules_stats(db)
        
        # Get active applications
        active_applications = DashboardService._get_active_applications(db)
        
        # Get totals
        total_employees = db.query(func.count(User.id)).filter(
            User.is_active == True,
            User.role != UserRole.ADMIN
        ).scalar() or 0
        
        total_departments = db.query(func.count(Department.id)).filter(
            Department.is_active == True
        ).scalar() or 0
        
        total_active_applications = db.query(func.count(Application.id)).filter(
            Application.status.in_([ApplicationStatus.PENDING, ApplicationStatus.REVIEWED])
        ).scalar() or 0
        
        return HRDashboardResponse(
            departments=departments,
            department_attendance=department_attendance,
            department_modules=department_modules,
            active_applications=active_applications,
            total_employees=total_employees,
            total_departments=total_departments,
            total_active_applications=total_active_applications
        )
    
    @staticmethod
    def _get_department_employee_counts(db: Session) -> List[DepartmentEmployeeCount]:
        """Get employee count per department"""
        results = db.query(
            Department.id,
            Department.name,
            func.count(User.id).label('employee_count')
        ).outerjoin(
            User, and_(User.department_id == Department.id, User.is_active == True)
        ).filter(
            Department.is_active == True
        ).group_by(
            Department.id, Department.name
        ).all()
        
        return [
            DepartmentEmployeeCount(
                department_id=dept_id,
                department_name=dept_name,
                employee_count=count
            )
            for dept_id, dept_name, count in results
        ]
    
    @staticmethod
    def _get_department_attendance_stats(db: Session, days: int = 30) -> List[DepartmentAttendance]:
        """Get department-wise attendance statistics for last N days"""
        start_date = date.today() - timedelta(days=days)
        
        # Get attendance stats per department
        results = db.query(
            Department.id,
            Department.name,
            func.count(Attendance.id).label('total_records'),
            func.sum(
                case(
                    (Attendance.status.in_([AttendanceStatus.PRESENT, AttendanceStatus.WFH]), 1),
                    else_=0
                )
            ).label('present_count'),
            func.sum(
                case(
                    (Attendance.status.in_([AttendanceStatus.ABSENT, AttendanceStatus.LEAVE]), 1),
                    else_=0
                )
            ).label('absent_count')
        ).join(
            User, User.department_id == Department.id
        ).join(
            Attendance, Attendance.employee_id == User.id
        ).filter(
            Department.is_active == True,
            Attendance.date >= start_date
        ).group_by(
            Department.id, Department.name
        ).all()
        
        attendance_stats = []
        for dept_id, dept_name, total, present, absent in results:
            if total > 0:
                present_pct = (present / total) * 100 if present else 0
                absent_pct = (absent / total) * 100 if absent else 0
            else:
                present_pct = 0
                absent_pct = 0
            
            attendance_stats.append(
                DepartmentAttendance(
                    department_id=dept_id,
                    department_name=dept_name,
                    present_percentage=round(present_pct, 2),
                    absent_percentage=round(absent_pct, 2)
                )
            )
        
        return attendance_stats
    
    @staticmethod
    def _get_department_modules_stats(db: Session) -> List[DepartmentModulesCompleted]:
        """Get department-wise skill modules completion statistics"""
        results = db.query(
            Department.id,
            Department.name,
            func.count(SkillModuleEnrollment.id).label('modules_completed')
        ).join(
            User, User.department_id == Department.id
        ).join(
            SkillModuleEnrollment, SkillModuleEnrollment.employee_id == User.id
        ).filter(
            Department.is_active == True,
            SkillModuleEnrollment.status == ModuleStatus.COMPLETED
        ).group_by(
            Department.id, Department.name
        ).all()
        
        return [
            DepartmentModulesCompleted(
                department_id=dept_id,
                department_name=dept_name,
                modules_completed=count
            )
            for dept_id, dept_name, count in results
        ]
    
    @staticmethod
    def _get_active_applications(db: Session, limit: int = 10) -> List[ActiveApplicationInfo]:
        """Get recent active job applications"""
        applications = db.query(Application).join(
            JobListing := Application.job
        ).filter(
            Application.status.in_([ApplicationStatus.PENDING, ApplicationStatus.REVIEWED])
        ).order_by(
            desc(Application.applied_date)
        ).limit(limit).all()
        
        result = []
        for app in applications:
            result.append(ActiveApplicationInfo(
                application_id=app.id,
                applicant_name=app.applicant_name or (app.applicant.name if app.applicant else "Unknown"),
                applied_role=app.job.position if app.job else "Unknown",
                applied_date=app.applied_date,
                status=app.status.value,
                source=app.source
            ))
        
        return result
    
    # ==================== Manager Dashboard Methods ====================
    
    @staticmethod
    def get_manager_dashboard_data(db: Session, manager: User) -> ManagerDashboardResponse:
        """Get complete Manager dashboard data"""
        
        # Personal info
        leave_balance = DashboardService.get_leave_balance(manager)
        today_attendance = DashboardService.get_today_attendance(db, manager.id)
        upcoming_holidays = DashboardService.get_upcoming_holidays(db, limit=5)
        learner_rank = DashboardService.calculate_learner_rank(db, manager.id)
        
        # Team info
        team_stats = None
        team_goals = TeamGoalsStats(
            total_goals=0,
            completed_goals=0,
            in_progress_goals=0,
            not_started_goals=0,
            completion_percentage=0.0
        )
        team_attendance = []
        team_modules_leaderboard = []
        
        # Get manager's team
        managed_team = db.query(Team).filter(Team.manager_id == manager.id).first()
        
        if managed_team:
            team_stats = DashboardService._get_team_stats(db, managed_team.id)
            team_goals = DashboardService._get_team_goals_stats(db, managed_team.id)
            team_attendance = DashboardService._get_team_attendance_stats(db, managed_team.id)
            team_modules_leaderboard = DashboardService._get_team_modules_leaderboard(db, managed_team.id)
        
        return ManagerDashboardResponse(
            personal_info=leave_balance,
            today_attendance=today_attendance,
            upcoming_holidays=upcoming_holidays,
            team_stats=team_stats,
            team_goals=team_goals,
            team_attendance=team_attendance,
            team_modules_leaderboard=team_modules_leaderboard,
            learner_rank=learner_rank
        )
    
    @staticmethod
    def _get_team_stats(db: Session, team_id: int) -> Optional[TeamStats]:
        """Get team statistics"""
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            return None
        
        # Get team member count
        member_count = db.query(func.count(User.id)).filter(
            User.team_id == team_id,
            User.is_active == True
        ).scalar() or 0
        
        # Calculate team training hours (from skill enrollments)
        training_hours = db.query(
            func.sum(SkillModule.duration_hours)
        ).join(
            SkillModuleEnrollment, SkillModuleEnrollment.module_id == SkillModule.id
        ).join(
            User, User.id == SkillModuleEnrollment.employee_id
        ).filter(
            User.team_id == team_id,
            SkillModuleEnrollment.status == ModuleStatus.COMPLETED
        ).scalar() or 0.0
        
        # Calculate team performance score (average of recent performance reports)
        performance_score = db.query(
            func.avg(PerformanceReport.overall_rating)
        ).join(
            User, User.id == PerformanceReport.employee_id
        ).filter(
            User.team_id == team_id,
            PerformanceReport.report_period_end >= date.today() - timedelta(days=90)
        ).scalar() or 0.0
        
        return TeamStats(
            team_id=team.id,
            team_name=team.name,
            total_members=member_count,
            team_training_hours=round(training_hours, 1),
            team_performance_score=round(performance_score, 2)
        )
    
    @staticmethod
    def _get_team_goals_stats(db: Session, team_id: int) -> TeamGoalsStats:
        """Get team goals statistics"""
        # Get all goals for team members
        results = db.query(
            func.count(Goal.id).label('total'),
            func.sum(case((Goal.status == GoalStatus.COMPLETED, 1), else_=0)).label('completed'),
            func.sum(case((Goal.status == GoalStatus.IN_PROGRESS, 1), else_=0)).label('in_progress'),
            func.sum(case((Goal.status == GoalStatus.NOT_STARTED, 1), else_=0)).label('not_started')
        ).join(
            User, User.id == Goal.employee_id
        ).filter(
            User.team_id == team_id
        ).first()
        
        total = results.total or 0
        completed = results.completed or 0
        in_progress = results.in_progress or 0
        not_started = results.not_started or 0
        
        completion_pct = (completed / total * 100) if total > 0 else 0.0
        
        return TeamGoalsStats(
            total_goals=total,
            completed_goals=completed,
            in_progress_goals=in_progress,
            not_started_goals=not_started,
            completion_percentage=round(completion_pct, 2)
        )
    
    @staticmethod
    def _get_team_attendance_stats(db: Session, team_id: int, days: int = 30) -> List[TeamMemberAttendance]:
        """Get team member attendance statistics"""
        start_date = date.today() - timedelta(days=days)
        
        results = db.query(
            User.id,
            User.name,
            func.count(Attendance.id).label('total_records'),
            func.sum(
                case(
                    (Attendance.status.in_([AttendanceStatus.PRESENT, AttendanceStatus.WFH]), 1),
                    else_=0
                )
            ).label('present_count'),
            func.sum(
                case(
                    (Attendance.status.in_([AttendanceStatus.ABSENT, AttendanceStatus.LEAVE]), 1),
                    else_=0
                )
            ).label('absent_count')
        ).outerjoin(
            Attendance, and_(
                Attendance.employee_id == User.id,
                Attendance.date >= start_date
            )
        ).filter(
            User.team_id == team_id,
            User.is_active == True
        ).group_by(
            User.id, User.name
        ).all()
        
        attendance_stats = []
        for emp_id, emp_name, total, present, absent in results:
            if total > 0:
                present_pct = (present / total) * 100 if present else 0
                absent_pct = (absent / total) * 100 if absent else 0
            else:
                present_pct = 0
                absent_pct = 0
            
            attendance_stats.append(
                TeamMemberAttendance(
                    employee_id=emp_id,
                    employee_name=emp_name,
                    present_percentage=round(present_pct, 2),
                    absent_percentage=round(absent_pct, 2)
                )
            )
        
        return attendance_stats
    
    @staticmethod
    def _get_team_modules_leaderboard(db: Session, team_id: int, limit: int = 10) -> List[TeamMemberModules]:
        """Get team member modules completion leaderboard"""
        results = db.query(
            User.id,
            User.name,
            func.count(SkillModuleEnrollment.id).label('modules_completed')
        ).outerjoin(
            SkillModuleEnrollment, and_(
                SkillModuleEnrollment.employee_id == User.id,
                SkillModuleEnrollment.status == ModuleStatus.COMPLETED
            )
        ).filter(
            User.team_id == team_id,
            User.is_active == True
        ).group_by(
            User.id, User.name
        ).order_by(
            desc('modules_completed')
        ).limit(limit).all()
        
        return [
            TeamMemberModules(
                employee_id=emp_id,
                employee_name=emp_name,
                modules_completed=count
            )
            for emp_id, emp_name, count in results
        ]
    
    # ==================== Employee Dashboard Methods ====================
    
    @staticmethod
    def get_employee_dashboard_data(db: Session, employee: User) -> EmployeeDashboardResponse:
        """Get complete Employee dashboard data"""
        
        leave_balance = DashboardService.get_leave_balance(employee)
        today_attendance = DashboardService.get_today_attendance(db, employee.id)
        upcoming_holidays = DashboardService.get_upcoming_holidays(db, limit=5)
        learning_goals = DashboardService._get_employee_goal_stats(db, employee.id)
        learner_rank = DashboardService.calculate_learner_rank(db, employee.id)
        
        return EmployeeDashboardResponse(
            employee_name=employee.name,
            leave_balance=leave_balance,
            today_attendance=today_attendance,
            upcoming_holidays=upcoming_holidays,
            learning_goals=learning_goals,
            learner_rank=learner_rank
        )
    
    @staticmethod
    def _get_employee_goal_stats(db: Session, employee_id: int) -> GoalStats:
        """Get employee goals statistics"""
        results = db.query(
            func.count(Goal.id).label('total'),
            func.sum(case((Goal.status == GoalStatus.COMPLETED, 1), else_=0)).label('completed')
        ).filter(
            Goal.employee_id == employee_id
        ).first()
        
        total = results.total or 0
        completed = results.completed or 0
        pending = total - completed
        
        completion_pct = (completed / total * 100) if total > 0 else 0.0
        
        return GoalStats(
            total_goals=total,
            completed_goals=completed,
            pending_goals=pending,
            completion_percentage=round(completion_pct, 2)
        )
    
    # ==================== Performance/Analytics Methods ====================
    
    @staticmethod
    def get_employee_performance_metrics(
        db: Session, 
        employee_id: int, 
        months: int = 12
    ) -> PerformanceMetrics:
        """Get employee performance metrics including monthly module completion"""
        
        employee = db.query(User).filter(User.id == employee_id).first()
        if not employee:
            raise ValueError("Employee not found")
        
        # Get monthly module completion
        start_date = date.today() - timedelta(days=months * 30)
        
        monthly_data = db.query(
            func.strftime('%Y-%m', SkillModuleEnrollment.completed_date).label('month'),
            func.count(SkillModuleEnrollment.id).label('count')
        ).filter(
            SkillModuleEnrollment.employee_id == employee_id,
            SkillModuleEnrollment.status == ModuleStatus.COMPLETED,
            SkillModuleEnrollment.completed_date >= start_date
        ).group_by('month').order_by('month').all()
        
        monthly_modules = [
            MonthlyModulesCompleted(
                month=month_str,
                modules_completed=count
            )
            for month_str, count in monthly_data
        ]
        
        # Total modules completed
        total_modules = db.query(func.count(SkillModuleEnrollment.id)).filter(
            SkillModuleEnrollment.employee_id == employee_id,
            SkillModuleEnrollment.status == ModuleStatus.COMPLETED
        ).scalar() or 0
        
        # Attendance rate (last 90 days)
        attendance_start = date.today() - timedelta(days=90)
        attendance_results = db.query(
            func.count(Attendance.id).label('total'),
            func.sum(
                case(
                    (Attendance.status.in_([AttendanceStatus.PRESENT, AttendanceStatus.WFH]), 1),
                    else_=0
                )
            ).label('present')
        ).filter(
            Attendance.employee_id == employee_id,
            Attendance.date >= attendance_start
        ).first()
        
        total_att = attendance_results.total or 0
        present_att = attendance_results.present or 0
        attendance_rate = (present_att / total_att * 100) if total_att > 0 else 0.0
        
        # Goals completion rate
        goals_results = db.query(
            func.count(Goal.id).label('total'),
            func.sum(case((Goal.status == GoalStatus.COMPLETED, 1), else_=0)).label('completed')
        ).filter(
            Goal.employee_id == employee_id
        ).first()
        
        total_goals = goals_results.total or 0
        completed_goals = goals_results.completed or 0
        goals_completion_rate = (completed_goals / total_goals * 100) if total_goals > 0 else 0.0
        
        return PerformanceMetrics(
            employee_id=employee.id,
            employee_name=employee.name,
            monthly_modules=monthly_modules,
            total_modules_completed=total_modules,
            attendance_rate=round(attendance_rate, 2),
            goals_completion_rate=round(goals_completion_rate, 2)
        )


# Import SkillModule model
from models import SkillModule, JobListing


