"""
AI Performance Report Service
Handles data aggregation, report generation, and storage for AI-powered performance reports
"""

import os
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, extract
from fastapi import HTTPException, status

from models import (
    User,
    UserRole,
    Goal,
    GoalStatus,
    GoalCheckpoint,
    GoalComment,
    GoalHistory,
    Feedback,
    Attendance,
    AttendanceStatus,
    SkillModuleEnrollment,
    ModuleStatus,
    PerformanceReport,
    Department,
    Team,
)
from schemas.ai_performance_schemas import (
    TimePeriodEnum,
    ReportTemplateEnum,
    MetricEnum,
    DataSummary,
    AIReportResponse,
    TeamMemberReport,
    TeamReportResponse,
    OrganizationReportResponse,
)
from services.ai_provider_manager import AIProviderManager
from utils.performance_prompt_templates import PerformancePromptTemplates
import time

logger = logging.getLogger(__name__)


class AIPerformanceReportService:
    """
    Core service for AI-powered performance report generation.
    Handles data aggregation, AI prompt generation, and report formatting.
    """

    def __init__(self):
        """Initialize service with AI provider"""
        self.ai_provider = AIProviderManager()
        self.prompt_templates = PerformancePromptTemplates()
        self.reports_dir = os.path.join("storage", "ai_reports")
        os.makedirs(self.reports_dir, exist_ok=True)

    # ==================== Time Period Calculation ====================

    @staticmethod
    def calculate_time_period(
        time_period: TimePeriodEnum,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Tuple[date, date, str]:
        """
        Calculate start and end dates based on time period enum.

        Returns:
            (start_date, end_date, period_label)
        """
        today = date.today()

        if time_period == TimePeriodEnum.CUSTOM:
            if not start_date or not end_date:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="start_date and end_date required for custom period",
                )
            label = f"{start_date.strftime('%b %d, %Y')} to {end_date.strftime('%b %d, %Y')}"
            return start_date, end_date, label

        elif time_period == TimePeriodEnum.LAST_30_DAYS:
            start = today - timedelta(days=30)
            label = "Last 30 Days"

        elif time_period == TimePeriodEnum.LAST_90_DAYS:
            start = today - timedelta(days=90)
            label = "Last 90 Days"

        elif time_period == TimePeriodEnum.LAST_180_DAYS:
            start = today - timedelta(days=180)
            label = "Last 180 Days"

        elif time_period == TimePeriodEnum.LAST_365_DAYS:
            start = today - timedelta(days=365)
            label = "Last 365 Days (1 Year)"

        elif time_period == TimePeriodEnum.CURRENT_QUARTER:
            quarter = (today.month - 1) // 3
            start = date(today.year, quarter * 3 + 1, 1)
            label = f"Q{quarter + 1} {today.year}"

        elif time_period == TimePeriodEnum.LAST_QUARTER:
            current_quarter = (today.month - 1) // 3
            if current_quarter == 0:
                quarter = 3
                year = today.year - 1
            else:
                quarter = current_quarter - 1
                year = today.year
            start = date(year, quarter * 3 + 1, 1)
            if quarter == 3:
                end_date = date(year, 12, 31)
            else:
                end_date = date(year, (quarter + 1) * 3 + 1, 1) - timedelta(days=1)
            label = f"Q{quarter + 1} {year}"
            return start, end_date, label

        elif time_period == TimePeriodEnum.CURRENT_YEAR:
            start = date(today.year, 1, 1)
            label = f"Year {today.year}"

        else:
            # Default to last 90 days
            start = today - timedelta(days=90)
            label = "Last 90 Days"

        return start, today, label

    # ==================== Data Aggregation ====================

    def aggregate_employee_performance_data(
        self,
        db: Session,
        employee_id: int,
        start_date: date,
        end_date: date,
        selected_metrics: List[str],
        include_team_comparison: bool = False,
        include_period_comparison: bool = False,
    ) -> Dict[str, Any]:
        """
        Aggregate all performance data for an employee for the specified period.
        This is the core data collection method.
        """
        # Get employee
        employee = db.query(User).filter(User.id == employee_id).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found",
            )

        # Employee basic info
        employee_data = {
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "position": employee.job_role,
            "department": employee.department_obj.name
            if employee.department_obj
            else "Not assigned",
            "team": employee.team_obj.name if employee.team_obj else "Not assigned",
            "manager_name": employee.manager.name
            if employee.manager
            else "Not assigned",
        }

        # Calculate period duration
        period_days = (end_date - start_date).days + 1

        # Initialize metrics data
        metrics_data = {
            "period_days": period_days,
            "start_date": start_date,
            "end_date": end_date,
        }

        # Aggregate goals data
        if (
            "goal_completion" in selected_metrics
            or "overdue_goals" in selected_metrics
            or not selected_metrics
        ):
            metrics_data.update(
                self._aggregate_goals_data(db, employee_id, start_date, end_date)
            )

        # Aggregate feedback data
        if (
            "feedback_ratings" in selected_metrics
            or "feedback_sentiment" in selected_metrics
            or not selected_metrics
        ):
            metrics_data.update(
                self._aggregate_feedback_data(db, employee_id, start_date, end_date)
            )

        # Aggregate attendance data
        if "attendance_rate" in selected_metrics or not selected_metrics:
            metrics_data.update(
                self._aggregate_attendance_data(db, employee_id, start_date, end_date)
            )

        # Aggregate training data
        if (
            "training_completion" in selected_metrics
            or "skills_development" in selected_metrics
            or not selected_metrics
        ):
            metrics_data.update(
                self._aggregate_training_data(db, employee_id, start_date, end_date)
            )

        # Aggregate collaboration data
        if "peer_collaboration" in selected_metrics or not selected_metrics:
            metrics_data.update(
                self._aggregate_collaboration_data(
                    db, employee_id, start_date, end_date
                )
            )

        # Add team comparison if requested
        if include_team_comparison and employee.team_id:
            metrics_data.update(
                self._add_team_comparison(
                    db, employee, start_date, end_date, metrics_data
                )
            )

        # Add period comparison if requested
        if include_period_comparison:
            metrics_data.update(
                self._add_period_comparison(
                    db, employee_id, start_date, end_date, metrics_data
                )
            )

        # Assess data sufficiency
        data_summary = self._assess_data_sufficiency(metrics_data)

        return {
            "employee": employee_data,
            "metrics": metrics_data,
            "data_summary": data_summary,
        }

    def _aggregate_goals_data(
        self, db: Session, employee_id: int, start_date: date, end_date: date
    ) -> Dict[str, Any]:
        """Aggregate goal-related metrics"""

        # Get all goals for the period
        goals = (
            db.query(Goal)
            .filter(
                Goal.employee_id == employee_id,
                Goal.is_deleted == False,
                or_(
                    and_(Goal.start_date >= start_date, Goal.start_date <= end_date),
                    and_(Goal.target_date >= start_date, Goal.target_date <= end_date),
                    and_(Goal.start_date <= start_date, Goal.target_date >= end_date),
                ),
            )
            .all()
        )

        total_goals = len(goals)
        completed_goals = sum(1 for g in goals if g.status == GoalStatus.COMPLETED)
        in_progress_goals = sum(1 for g in goals if g.status == GoalStatus.IN_PROGRESS)
        overdue_goals = sum(
            1
            for g in goals
            if g.target_date < date.today() and g.status != GoalStatus.COMPLETED
        )

        # Calculate completion rate
        goal_completion_rate = (
            (completed_goals / total_goals * 100) if total_goals > 0 else 0
        )

        # Calculate average completion time for completed goals
        completed_with_dates = [
            g for g in goals if g.status == GoalStatus.COMPLETED and g.completion_date
        ]
        if completed_with_dates:
            completion_times = [
                (g.completion_date - g.start_date).days for g in completed_with_dates
            ]
            avg_completion_days = sum(completion_times) / len(completion_times)

            # On-time completion rate
            on_time_completed = sum(
                1 for g in completed_with_dates if g.completion_date <= g.target_date
            )
            on_time_rate = on_time_completed / len(completed_with_dates) * 100
        else:
            avg_completion_days = 0
            on_time_rate = 0

        # Goals by priority
        goals_by_priority = {}
        for priority in ["low", "medium", "high", "critical"]:
            count = sum(1 for g in goals if g.priority == priority)
            if count > 0:
                completed = sum(
                    1
                    for g in goals
                    if g.priority == priority and g.status == GoalStatus.COMPLETED
                )
                goals_by_priority[priority.title()] = (
                    f"{completed}/{count} ({completed / count * 100:.1f}%)"
                )

        # Goals by category
        goals_by_category = {}
        category_ids = set(g.category_id for g in goals if g.category_id)
        for cat_id in category_ids:
            cat_goals = [g for g in goals if g.category_id == cat_id]
            if cat_goals:
                cat_name = (
                    cat_goals[0].category.name
                    if cat_goals[0].category
                    else f"Category {cat_id}"
                )
                completed = sum(
                    1 for g in cat_goals if g.status == GoalStatus.COMPLETED
                )
                goals_by_category[cat_name] = (
                    f"{completed}/{len(cat_goals)} ({completed / len(cat_goals) * 100:.1f}%)"
                )

        # Get completed goal examples (recent)
        completed_goal_examples = [
            f"{g.title} (Completed {g.completion_date.strftime('%b %d')} - Priority: {g.priority})"
            for g in sorted(
                [
                    g
                    for g in goals
                    if g.status == GoalStatus.COMPLETED and g.completion_date
                ],
                key=lambda x: x.completion_date,
                reverse=True,
            )[:5]
        ]

        # Get overdue goal examples
        overdue_goal_examples = [
            f"{g.title} (Due {g.target_date.strftime('%b %d')} - {(date.today() - g.target_date).days} days overdue - Priority: {g.priority})"
            for g in sorted(
                [
                    g
                    for g in goals
                    if g.target_date < date.today() and g.status != GoalStatus.COMPLETED
                ],
                key=lambda x: x.target_date,
            )[:5]
        ]

        # Checkpoints data
        total_checkpoints = 0
        completed_checkpoints = 0
        for goal in goals:
            checkpoints = goal.checkpoints
            total_checkpoints += len(checkpoints)
            completed_checkpoints += sum(1 for cp in checkpoints if cp.is_completed)

        checkpoint_completion_rate = (
            (completed_checkpoints / total_checkpoints * 100)
            if total_checkpoints > 0
            else 0
        )

        return {
            "total_goals": total_goals,
            "completed_goals": completed_goals,
            "in_progress_goals": in_progress_goals,
            "overdue_goals": overdue_goals,
            "goal_completion_rate": goal_completion_rate,
            "avg_completion_days": avg_completion_days,
            "on_time_rate": on_time_rate,
            "goals_by_priority": goals_by_priority,
            "goals_by_category": goals_by_category,
            "completed_goal_examples": completed_goal_examples,
            "overdue_goal_examples": overdue_goal_examples,
            "total_checkpoints": total_checkpoints,
            "completed_checkpoints": completed_checkpoints,
            "checkpoint_completion_rate": checkpoint_completion_rate,
        }

    def _aggregate_feedback_data(
        self, db: Session, employee_id: int, start_date: date, end_date: date
    ) -> Dict[str, Any]:
        """Aggregate feedback-related metrics"""

        feedbacks = (
            db.query(Feedback)
            .filter(
                Feedback.employee_id == employee_id,
                Feedback.given_on >= datetime.combine(start_date, datetime.min.time()),
                Feedback.given_on <= datetime.combine(end_date, datetime.max.time()),
            )
            .all()
        )

        total_feedback = len(feedbacks)

        if total_feedback == 0:
            return {
                "total_feedback": 0,
                "avg_feedback_rating": 0,
                "positive_feedback_count": 0,
                "constructive_feedback_count": 0,
                "performance_feedback_count": 0,
                "feedback_examples": [],
            }

        # Calculate average rating
        rated_feedback = [f for f in feedbacks if f.rating is not None]
        avg_rating = (
            sum(f.rating for f in rated_feedback) / len(rated_feedback)
            if rated_feedback
            else 0
        )

        # Count by type
        positive_count = sum(1 for f in feedbacks if f.feedback_type == "positive")
        constructive_count = sum(
            1 for f in feedbacks if f.feedback_type == "constructive"
        )
        performance_count = sum(
            1 for f in feedbacks if f.feedback_type == "performance"
        )

        # Get examples
        feedback_examples = [
            {
                "subject": f.subject,
                "description": f.description,
                "rating": f.rating,
                "feedback_type": f.feedback_type or "general",
                "given_by": f.given_by_user.name if f.given_by_user else "Unknown",
                "given_on": f.given_on.strftime("%b %d, %Y"),
            }
            for f in sorted(feedbacks, key=lambda x: x.given_on, reverse=True)[:5]
        ]

        return {
            "total_feedback": total_feedback,
            "avg_feedback_rating": avg_rating,
            "positive_feedback_count": positive_count,
            "constructive_feedback_count": constructive_count,
            "performance_feedback_count": performance_count,
            "feedback_examples": feedback_examples,
        }

    def _aggregate_attendance_data(
        self, db: Session, employee_id: int, start_date: date, end_date: date
    ) -> Dict[str, Any]:
        """Aggregate attendance-related metrics"""

        attendance_records = (
            db.query(Attendance)
            .filter(
                Attendance.employee_id == employee_id,
                Attendance.date >= start_date,
                Attendance.date <= end_date,
            )
            .all()
        )

        total_days = len(attendance_records)

        if total_days == 0:
            return {
                "attendance_rate": 0,
                "days_present": 0,
                "days_absent": 0,
                "wfh_days": 0,
                "total_attendance_records": 0,
            }

        days_present = sum(
            1 for a in attendance_records if a.status == AttendanceStatus.PRESENT
        )
        days_absent = sum(
            1 for a in attendance_records if a.status == AttendanceStatus.ABSENT
        )
        wfh_days = sum(
            1 for a in attendance_records if a.status == AttendanceStatus.WFH
        )

        # Calculate attendance rate (present + wfh as attended)
        attendance_rate = (
            ((days_present + wfh_days) / total_days * 100) if total_days > 0 else 0
        )

        return {
            "attendance_rate": attendance_rate,
            "days_present": days_present,
            "days_absent": days_absent,
            "wfh_days": wfh_days,
            "total_attendance_records": total_days,
        }

    def _aggregate_training_data(
        self, db: Session, employee_id: int, start_date: date, end_date: date
    ) -> Dict[str, Any]:
        """Aggregate training/skills development metrics"""

        # Get enrollments completed in this period
        completed_enrollments = (
            db.query(SkillModuleEnrollment)
            .filter(
                SkillModuleEnrollment.employee_id == employee_id,
                SkillModuleEnrollment.status == ModuleStatus.COMPLETED,
                SkillModuleEnrollment.completed_date
                >= datetime.combine(start_date, datetime.min.time()),
                SkillModuleEnrollment.completed_date
                <= datetime.combine(end_date, datetime.max.time()),
            )
            .all()
        )

        # Get all enrollments (for completion rate)
        all_enrollments = (
            db.query(SkillModuleEnrollment)
            .filter(
                SkillModuleEnrollment.employee_id == employee_id,
                SkillModuleEnrollment.enrolled_date
                >= datetime.combine(start_date, datetime.min.time()),
            )
            .all()
        )

        modules_completed = len(completed_enrollments)
        modules_in_progress = sum(
            1 for e in all_enrollments if e.status == ModuleStatus.PENDING
        )
        total_enrolled = len(all_enrollments)

        training_completion_rate = (
            (modules_completed / total_enrolled * 100) if total_enrolled > 0 else 0
        )

        # Get skills acquired (from completed modules)
        skills_acquired = list(
            set(
                skill.strip()
                for e in completed_enrollments
                if e.module and e.module.skill_areas
                for skill in e.module.skill_areas.split(",")
            )
        )

        return {
            "modules_completed": modules_completed,
            "modules_in_progress": modules_in_progress,
            "training_completion_rate": training_completion_rate,
            "skills_acquired": skills_acquired,
        }

    def _aggregate_collaboration_data(
        self, db: Session, employee_id: int, start_date: date, end_date: date
    ) -> Dict[str, Any]:
        """Aggregate collaboration/engagement metrics"""

        # Get goal comments by this employee
        comments = (
            db.query(GoalComment)
            .join(Goal)
            .filter(
                GoalComment.user_id == employee_id,
                GoalComment.created_at
                >= datetime.combine(start_date, datetime.min.time()),
                GoalComment.created_at
                <= datetime.combine(end_date, datetime.max.time()),
                GoalComment.is_deleted == False,
            )
            .all()
        )

        total_comments = len(comments)
        question_comments = sum(1 for c in comments if c.comment_type == "question")
        blocker_comments = sum(1 for c in comments if c.comment_type == "blocker")
        milestone_comments = sum(1 for c in comments if c.comment_type == "milestone")
        update_comments = sum(1 for c in comments if c.comment_type == "update")

        return {
            "total_comments": total_comments,
            "question_comments": question_comments,
            "blocker_comments": blocker_comments,
            "milestone_comments": milestone_comments,
            "update_comments": update_comments,
        }

    def _add_team_comparison(
        self,
        db: Session,
        employee: User,
        start_date: date,
        end_date: date,
        employee_metrics: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Add team average comparison data"""

        if not employee.team_id:
            return {}

        # Get all team members
        team_members = (
            db.query(User)
            .filter(
                User.team_id == employee.team_id,
                User.id != employee.id,
                User.is_active == True,
            )
            .all()
        )

        if not team_members:
            return {}

        # Calculate team averages
        team_completion_rates = []
        team_ratings = []
        team_attendance_rates = []

        for member in team_members:
            # Goal completion
            member_goals = (
                db.query(Goal)
                .filter(
                    Goal.employee_id == member.id,
                    Goal.start_date >= start_date,
                    Goal.start_date <= end_date,
                )
                .all()
            )

            if member_goals:
                completed = sum(
                    1 for g in member_goals if g.status == GoalStatus.COMPLETED
                )
                team_completion_rates.append(completed / len(member_goals) * 100)

            # Feedback rating
            member_feedback = (
                db.query(Feedback)
                .filter(
                    Feedback.employee_id == member.id,
                    Feedback.given_on
                    >= datetime.combine(start_date, datetime.min.time()),
                    Feedback.given_on
                    <= datetime.combine(end_date, datetime.max.time()),
                    Feedback.rating.isnot(None),
                )
                .all()
            )

            if member_feedback:
                team_ratings.append(
                    sum(f.rating for f in member_feedback) / len(member_feedback)
                )

            # Attendance
            member_attendance = (
                db.query(Attendance)
                .filter(
                    Attendance.employee_id == member.id,
                    Attendance.date >= start_date,
                    Attendance.date <= end_date,
                )
                .all()
            )

            if member_attendance:
                present = sum(
                    1
                    for a in member_attendance
                    if a.status in [AttendanceStatus.PRESENT, AttendanceStatus.WFH]
                )
                team_attendance_rates.append(present / len(member_attendance) * 100)

        team_avg_completion = (
            sum(team_completion_rates) / len(team_completion_rates)
            if team_completion_rates
            else 0
        )
        team_avg_rating = sum(team_ratings) / len(team_ratings) if team_ratings else 0
        team_avg_attendance = (
            sum(team_attendance_rates) / len(team_attendance_rates)
            if team_attendance_rates
            else 0
        )

        return {
            "team_average": True,
            "team_avg_completion": team_avg_completion,
            "team_avg_rating": team_avg_rating,
            "team_avg_attendance": team_avg_attendance,
            "vs_team": employee_metrics.get("goal_completion_rate", 0)
            - team_avg_completion,
        }

    def _add_period_comparison(
        self,
        db: Session,
        employee_id: int,
        start_date: date,
        end_date: date,
        current_metrics: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Add previous period comparison data"""

        # Calculate previous period (same duration)
        period_duration = (end_date - start_date).days
        prev_end_date = start_date - timedelta(days=1)
        prev_start_date = prev_end_date - timedelta(days=period_duration)

        # Get previous period metrics (simplified)
        prev_goals = (
            db.query(Goal)
            .filter(
                Goal.employee_id == employee_id,
                Goal.start_date >= prev_start_date,
                Goal.start_date <= prev_end_date,
            )
            .all()
        )

        prev_total = len(prev_goals)
        prev_completed = sum(1 for g in prev_goals if g.status == GoalStatus.COMPLETED)
        prev_completion_rate = (
            (prev_completed / prev_total * 100) if prev_total > 0 else 0
        )

        prev_feedback = (
            db.query(Feedback)
            .filter(
                Feedback.employee_id == employee_id,
                Feedback.given_on
                >= datetime.combine(prev_start_date, datetime.min.time()),
                Feedback.given_on
                <= datetime.combine(prev_end_date, datetime.max.time()),
                Feedback.rating.isnot(None),
            )
            .all()
        )

        prev_rating = (
            sum(f.rating for f in prev_feedback) / len(prev_feedback)
            if prev_feedback
            else 0
        )

        return {
            "previous_period": True,
            "prev_completion_rate": prev_completion_rate,
            "prev_rating": prev_rating,
            "period_trend": current_metrics.get("goal_completion_rate", 0)
            - prev_completion_rate,
        }

    def _assess_data_sufficiency(self, metrics: Dict[str, Any]) -> DataSummary:
        """Assess if there's sufficient data for meaningful report generation"""

        warnings = []

        total_goals = metrics.get("total_goals", 0)
        total_feedback = metrics.get("total_feedback", 0)
        total_attendance = metrics.get("total_attendance_records", 0)

        # Determine sufficiency
        data_points = total_goals + total_feedback + total_attendance

        if data_points >= 50:
            sufficiency = "sufficient"
        elif data_points >= 20:
            sufficiency = "limited"
            warnings.append(
                "Limited data available. Report may not capture full performance picture."
            )
        else:
            sufficiency = "insufficient"
            warnings.append(
                "Insufficient data for comprehensive analysis. Consider longer time period or accumulate more data."
            )

        if total_goals < 3:
            warnings.append("Very few goals recorded in this period.")

        if total_feedback < 2:
            warnings.append(
                "Limited feedback available. Encourage more regular feedback."
            )

        if total_attendance < 10:
            warnings.append("Limited attendance data.")

        return DataSummary(
            total_goals=total_goals,
            completed_goals=metrics.get("completed_goals", 0),
            in_progress_goals=metrics.get("in_progress_goals", 0),
            overdue_goals=metrics.get("overdue_goals", 0),
            total_feedback=total_feedback,
            average_feedback_rating=metrics.get("avg_feedback_rating"),
            attendance_rate=metrics.get("attendance_rate"),
            training_completion_rate=metrics.get("training_completion_rate"),
            total_checkpoints=metrics.get("total_checkpoints", 0),
            completed_checkpoints=metrics.get("completed_checkpoints", 0),
            data_sufficiency=sufficiency,
            warnings=warnings,
        )

    # ==================== Report Generation ====================

    async def generate_individual_report(
        self,
        db: Session,
        employee_id: int,
        time_period: TimePeriodEnum,
        start_date: Optional[date],
        end_date: Optional[date],
        template: ReportTemplateEnum,
        custom_metrics: Optional[List[str]],
        include_team_comparison: bool,
        include_period_comparison: bool,
    ) -> AIReportResponse:
        """Generate AI-powered individual performance report"""

        start_time = time.time()

        # Calculate time period
        period_start, period_end, period_label = self.calculate_time_period(
            time_period, start_date, end_date
        )

        # Determine metrics to use
        if template == ReportTemplateEnum.CUSTOM and custom_metrics:
            selected_metrics = custom_metrics
        else:
            selected_metrics = self._get_template_metrics(template)

        # Aggregate data
        aggregated_data = self.aggregate_employee_performance_data(
            db,
            employee_id,
            period_start,
            period_end,
            selected_metrics,
            include_team_comparison,
            include_period_comparison,
        )

        # Check data sufficiency
        if aggregated_data["data_summary"].data_sufficiency == "insufficient":
            logger.warning(f"Insufficient data for employee {employee_id}")
            # Still generate but with warning

        # Build prompt
        prompt = self.prompt_templates.get_individual_report_prompt(
            employee_data=aggregated_data["employee"],
            metrics_data=aggregated_data["metrics"],
            time_period=period_label,
            template=template.value,
            include_comparisons=(include_team_comparison or include_period_comparison),
        )

        # Generate report using AI
        logger.info(f"Generating AI report for employee {employee_id}")
        report_markdown = await self.ai_provider.generate_report(prompt)

        generation_time = time.time() - start_time

        # Build response
        response = AIReportResponse(
            report_id=self._generate_report_id(),
            employee_id=employee_id,
            employee_name=aggregated_data["employee"]["name"],
            employee_email=aggregated_data["employee"]["email"],
            report_type="individual",
            generated_at=datetime.now(),
            time_period_start=period_start,
            time_period_end=period_end,
            time_period_label=period_label,
            template_used=template.value,
            metrics_used=[
                m.value if isinstance(m, MetricEnum) else m for m in selected_metrics
            ],
            report_markdown=report_markdown,
            data_summary=aggregated_data["data_summary"],
            generation_time_seconds=round(generation_time, 2),
        )

        # Save if Tuesday (day 1 = Tuesday in Python)
        if datetime.now().weekday() == 1:
            self._save_weekly_report(response)

        logger.info(
            f"Report generated successfully for employee {employee_id} in {generation_time:.2f}s"
        )

        return response

    @staticmethod
    def _get_template_metrics(template: ReportTemplateEnum) -> List[str]:
        """Get metrics for predefined templates"""

        if template == ReportTemplateEnum.QUICK_SUMMARY:
            return ["goal_completion", "feedback_ratings", "attendance_rate"]

        elif template == ReportTemplateEnum.STANDARD_REVIEW:
            return [
                "goal_completion",
                "feedback_ratings",
                "attendance_rate",
                "training_completion",
                "overdue_goals",
            ]

        elif template == ReportTemplateEnum.COMPREHENSIVE_REVIEW:
            return [
                "goal_completion",
                "attendance_rate",
                "training_completion",
                "feedback_ratings",
                "overdue_goals",
                "checkpoint_progress",
                "feedback_sentiment",
                "skills_development",
                "peer_collaboration",
                "category_goal_success",
                "priority_goal_handling",
            ]

        elif template == ReportTemplateEnum.LEADERSHIP_FOCUS:
            return [
                "goal_completion",
                "feedback_ratings",
                "peer_collaboration",
                "category_goal_success",
                "training_completion",
            ]

        elif template == ReportTemplateEnum.TECHNICAL_FOCUS:
            return [
                "goal_completion",
                "skills_development",
                "training_completion",
                "checkpoint_progress",
                "category_goal_success",
            ]

        else:
            # Default to standard
            return [
                "goal_completion",
                "feedback_ratings",
                "attendance_rate",
                "training_completion",
                "overdue_goals",
            ]

    @staticmethod
    def _generate_report_id() -> str:
        """Generate unique report ID"""
        return f"RPT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{os.urandom(4).hex()}"

    def _save_weekly_report(self, report: AIReportResponse):
        """Save report as txt file (weekly on Tuesday)"""
        try:
            filename = (
                f"report_{report.employee_id}_{datetime.now().strftime('%Y%m%d')}.txt"
            )
            filepath = os.path.join(self.reports_dir, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"AI PERFORMANCE REPORT\n")
                f.write(f"{'=' * 60}\n\n")
                f.write(f"Employee: {report.employee_name}\n")
                f.write(f"Email: {report.employee_email}\n")
                f.write(f"Period: {report.time_period_label}\n")
                f.write(
                    f"Generated: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
                f.write(f"Template: {report.template_used}\n\n")
                f.write(f"{'=' * 60}\n\n")
                f.write(report.report_markdown)

            report.is_saved = True
            report.saved_path = filepath
            report.saved_on = datetime.now()

            logger.info(f"Weekly report saved: {filepath}")

        except Exception as e:
            logger.error(f"Failed to save weekly report: {str(e)}")

    # ==================== Team Report Generation ====================

    async def generate_team_summary_report(
        self,
        db: Session,
        team_id: int,
        time_period: TimePeriodEnum,
        start_date: Optional[date],
        end_date: Optional[date],
        template: ReportTemplateEnum,
    ) -> TeamReportResponse:
        """Generate team summary report for manager"""

        start_time = time.time()

        # Calculate time period
        period_start, period_end, period_label = self.calculate_time_period(
            time_period, start_date, end_date
        )

        # Get team info
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Team with ID {team_id} not found",
            )

        # Get all team members
        team_members = (
            db.query(User).filter(User.team_id == team_id, User.is_active == True).all()
        )

        if not team_members:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active team members found",
            )

        # Aggregate team-level data
        team_data = self._aggregate_team_data(
            db, team, team_members, period_start, period_end
        )

        # Get individual member summaries
        member_summaries = []
        for member in team_members:
            member_data = self._get_member_summary(db, member, period_start, period_end)
            member_summaries.append(member_data)

        # Build prompt
        prompt = self.prompt_templates.get_team_summary_prompt(
            team_data=team_data,
            member_summaries=member_summaries,
            time_period=period_label,
        )

        # Generate report
        logger.info(f"Generating team summary report for team {team_id}")
        team_summary_markdown = await self.ai_provider.generate_report(prompt)

        generation_time = time.time() - start_time

        # Convert member summaries to TeamMemberReport format
        member_reports = [
            TeamMemberReport(
                employee_id=m["id"],
                employee_name=m["name"],
                report_summary=m.get("summary", "No summary available"),
                key_metrics={
                    "goal_completion": m.get("completion_rate", 0),
                    "feedback_rating": m.get("avg_feedback_rating", 0),
                    "attendance": m.get("attendance_rate", 0),
                },
                overall_status=self._determine_status(m),
            )
            for m in member_summaries
        ]

        response = TeamReportResponse(
            report_id=self._generate_report_id(),
            team_id=team_id,
            team_name=team.name,
            report_type="team_summary",
            generated_at=datetime.now(),
            time_period_start=period_start,
            time_period_end=period_end,
            template_used=template.value,
            team_summary_markdown=team_summary_markdown,
            member_reports=member_reports,
            team_data_summary=team_data,
            generation_time_seconds=round(generation_time, 2),
        )

        logger.info(f"Team summary generated in {generation_time:.2f}s")
        return response

    async def generate_team_comparative_report(
        self,
        db: Session,
        team_id: int,
        time_period: TimePeriodEnum,
        start_date: Optional[date],
        end_date: Optional[date],
        template: ReportTemplateEnum,
    ) -> TeamReportResponse:
        """Generate comparative/leaderboard report for team"""

        start_time = time.time()

        # Calculate time period
        period_start, period_end, period_label = self.calculate_time_period(
            time_period, start_date, end_date
        )

        # Get team info
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Team with ID {team_id} not found",
            )

        # Get all team members
        team_members = (
            db.query(User).filter(User.team_id == team_id, User.is_active == True).all()
        )

        # Aggregate team data
        team_data = self._aggregate_team_data(
            db, team, team_members, period_start, period_end
        )

        # Get member summaries
        member_summaries = []
        for member in team_members:
            member_data = self._get_member_summary(db, member, period_start, period_end)
            member_summaries.append(member_data)

        # Sort by performance (goal completion rate)
        member_summaries.sort(key=lambda x: x.get("completion_rate", 0), reverse=True)

        # Build prompt
        prompt = self.prompt_templates.get_team_comparative_prompt(
            team_data=team_data,
            member_summaries=member_summaries,
            time_period=period_label,
        )

        # Generate report
        logger.info(f"Generating comparative report for team {team_id}")
        comparative_markdown = await self.ai_provider.generate_report(prompt)

        generation_time = time.time() - start_time

        # Build member reports
        member_reports = [
            TeamMemberReport(
                employee_id=m["id"],
                employee_name=m["name"],
                report_summary=f"Rank #{i + 1}: {m.get('completion_rate', 0):.1f}% completion",
                key_metrics={
                    "goal_completion": m.get("completion_rate", 0),
                    "feedback_rating": m.get("avg_feedback_rating", 0),
                    "attendance": m.get("attendance_rate", 0),
                    "rank": i + 1,
                },
                overall_status=self._determine_status(m),
            )
            for i, m in enumerate(member_summaries)
        ]

        response = TeamReportResponse(
            report_id=self._generate_report_id(),
            team_id=team_id,
            team_name=team.name,
            report_type="team_comparative",
            generated_at=datetime.now(),
            time_period_start=period_start,
            time_period_end=period_end,
            template_used=template.value,
            team_comparative_markdown=comparative_markdown,
            member_reports=member_reports,
            team_data_summary=team_data,
            generation_time_seconds=round(generation_time, 2),
        )

        logger.info(f"Comparative report generated in {generation_time:.2f}s")
        return response

    def _aggregate_team_data(
        self,
        db: Session,
        team: Team,
        members: List[User],
        start_date: date,
        end_date: date,
    ) -> Dict[str, Any]:
        """Aggregate team-level performance data"""

        member_ids = [m.id for m in members]

        # Team goals
        team_goals = (
            db.query(Goal)
            .filter(
                Goal.employee_id.in_(member_ids),
                Goal.start_date >= start_date,
                Goal.start_date <= end_date,
                Goal.is_deleted == False,
            )
            .all()
        )

        total_goals = len(team_goals)
        completed_goals = sum(1 for g in team_goals if g.status == GoalStatus.COMPLETED)
        in_progress_goals = sum(
            1 for g in team_goals if g.status == GoalStatus.IN_PROGRESS
        )
        overdue_goals = sum(
            1
            for g in team_goals
            if g.target_date < date.today() and g.status != GoalStatus.COMPLETED
        )

        goal_completion_rate = (
            (completed_goals / total_goals * 100) if total_goals > 0 else 0
        )

        # On-time rate
        completed_with_dates = [
            g
            for g in team_goals
            if g.status == GoalStatus.COMPLETED and g.completion_date
        ]
        on_time = sum(
            1 for g in completed_with_dates if g.completion_date <= g.target_date
        )
        on_time_rate = (
            (on_time / len(completed_with_dates) * 100) if completed_with_dates else 0
        )

        # Team feedback
        team_feedback = (
            db.query(Feedback)
            .filter(
                Feedback.employee_id.in_(member_ids),
                Feedback.given_on >= datetime.combine(start_date, datetime.min.time()),
                Feedback.given_on <= datetime.combine(end_date, datetime.max.time()),
            )
            .all()
        )

        total_feedback = len(team_feedback)
        rated_feedback = [f for f in team_feedback if f.rating is not None]
        avg_rating = (
            sum(f.rating for f in rated_feedback) / len(rated_feedback)
            if rated_feedback
            else 0
        )
        positive_feedback = sum(
            1 for f in team_feedback if f.feedback_type == "positive"
        )
        positive_feedback_pct = (
            (positive_feedback / total_feedback * 100) if total_feedback > 0 else 0
        )

        # Team attendance
        team_attendance = (
            db.query(Attendance)
            .filter(
                Attendance.employee_id.in_(member_ids),
                Attendance.date >= start_date,
                Attendance.date <= end_date,
            )
            .all()
        )

        total_records = len(team_attendance)
        present_records = sum(
            1
            for a in team_attendance
            if a.status in [AttendanceStatus.PRESENT, AttendanceStatus.WFH]
        )
        avg_attendance = (
            (present_records / total_records * 100) if total_records > 0 else 0
        )

        # Team training
        team_training = (
            db.query(SkillModuleEnrollment)
            .filter(
                SkillModuleEnrollment.employee_id.in_(member_ids),
                SkillModuleEnrollment.status == ModuleStatus.COMPLETED,
                SkillModuleEnrollment.completed_date
                >= datetime.combine(start_date, datetime.min.time()),
                SkillModuleEnrollment.completed_date
                <= datetime.combine(end_date, datetime.max.time()),
            )
            .count()
        )

        # Team collaboration
        team_comments = (
            db.query(GoalComment)
            .join(Goal)
            .filter(
                GoalComment.user_id.in_(member_ids),
                GoalComment.created_at
                >= datetime.combine(start_date, datetime.min.time()),
                GoalComment.created_at
                <= datetime.combine(end_date, datetime.max.time()),
            )
            .count()
        )

        blockers = (
            db.query(GoalComment)
            .join(Goal)
            .filter(
                GoalComment.user_id.in_(member_ids),
                GoalComment.comment_type == "blocker",
                GoalComment.created_at
                >= datetime.combine(start_date, datetime.min.time()),
                GoalComment.created_at
                <= datetime.combine(end_date, datetime.max.time()),
            )
            .count()
        )

        return {
            "team_name": team.name,
            "department_name": team.department.name
            if team.department
            else "Not assigned",
            "manager_name": team.manager.name if team.manager else "Not assigned",
            "team_size": len(members),
            "total_goals": total_goals,
            "completed_goals": completed_goals,
            "in_progress_goals": in_progress_goals,
            "overdue_goals": overdue_goals,
            "goal_completion_rate": goal_completion_rate,
            "avg_completion_rate": goal_completion_rate,  # Same as team rate
            "on_time_rate": on_time_rate,
            "total_feedback": total_feedback,
            "avg_rating": avg_rating,
            "positive_feedback_pct": positive_feedback_pct,
            "avg_attendance": avg_attendance,
            "avg_training_completion": team_training,
            "total_comments": team_comments,
            "total_blockers": blockers,
            "collaboration_score": "High"
            if team_comments > len(members) * 5
            else "Moderate"
            if team_comments > len(members) * 2
            else "Low",
        }

    def _get_member_summary(
        self, db: Session, member: User, start_date: date, end_date: date
    ) -> Dict[str, Any]:
        """Get performance summary for a team member"""

        # Goals
        member_goals = (
            db.query(Goal)
            .filter(
                Goal.employee_id == member.id,
                Goal.start_date >= start_date,
                Goal.start_date <= end_date,
                Goal.is_deleted == False,
            )
            .all()
        )

        total_goals = len(member_goals)
        completed = sum(1 for g in member_goals if g.status == GoalStatus.COMPLETED)
        overdue = sum(
            1
            for g in member_goals
            if g.target_date < date.today() and g.status != GoalStatus.COMPLETED
        )
        completion_rate = (completed / total_goals * 100) if total_goals > 0 else 0

        # Feedback
        member_feedback = (
            db.query(Feedback)
            .filter(
                Feedback.employee_id == member.id,
                Feedback.given_on >= datetime.combine(start_date, datetime.min.time()),
                Feedback.given_on <= datetime.combine(end_date, datetime.max.time()),
            )
            .all()
        )

        feedback_count = len(member_feedback)
        rated = [f for f in member_feedback if f.rating is not None]
        avg_rating = sum(f.rating for f in rated) / len(rated) if rated else 0

        # Attendance
        member_attendance = (
            db.query(Attendance)
            .filter(
                Attendance.employee_id == member.id,
                Attendance.date >= start_date,
                Attendance.date <= end_date,
            )
            .all()
        )

        total_att = len(member_attendance)
        present = sum(
            1
            for a in member_attendance
            if a.status in [AttendanceStatus.PRESENT, AttendanceStatus.WFH]
        )
        attendance_rate = (present / total_att * 100) if total_att > 0 else 0

        # Training
        training_completed = (
            db.query(SkillModuleEnrollment)
            .filter(
                SkillModuleEnrollment.employee_id == member.id,
                SkillModuleEnrollment.status == ModuleStatus.COMPLETED,
                SkillModuleEnrollment.completed_date
                >= datetime.combine(start_date, datetime.min.time()),
                SkillModuleEnrollment.completed_date
                <= datetime.combine(end_date, datetime.max.time()),
            )
            .count()
        )

        # Determine highlight and challenge
        highlight = ""
        if completion_rate >= 80:
            highlight = f"High goal completion rate ({completion_rate:.1f}%)"
        elif avg_rating >= 4.0:
            highlight = f"Excellent feedback ratings ({avg_rating:.1f}/5.0)"
        elif training_completed >= 3:
            highlight = (
                f"Strong learning commitment ({training_completed} modules completed)"
            )
        else:
            highlight = "Consistent performance"

        challenge = ""
        if overdue >= 3:
            challenge = f"{overdue} overdue goals requiring attention"
        elif completion_rate < 50:
            challenge = "Goal completion rate below expectations"
        elif avg_rating < 3.5 and feedback_count > 0:
            challenge = "Feedback ratings suggest areas for improvement"
        elif attendance_rate < 80:
            challenge = "Attendance consistency needs attention"
        else:
            challenge = "No major challenges identified"

        return {
            "id": member.id,
            "name": member.name,
            "position": member.job_role or "Employee",
            "total_goals": total_goals,
            "completed_goals": completed,
            "overdue_goals": overdue,
            "completion_rate": completion_rate,
            "feedback_count": feedback_count,
            "avg_feedback_rating": avg_rating,
            "attendance_rate": attendance_rate,
            "training_completion": training_completed,
            "highlight": highlight,
            "challenge": challenge,
            "summary": f"{member.name} achieved {completion_rate:.1f}% goal completion with {avg_rating:.1f}/5.0 average feedback rating.",
        }

    @staticmethod
    def _determine_status(member_data: Dict[str, Any]) -> str:
        """Determine overall performance status"""
        completion_rate = member_data.get("completion_rate", 0)
        avg_rating = member_data.get("avg_feedback_rating", 0)
        overdue = member_data.get("overdue_goals", 0)

        # Excellent: High completion, high rating, few overdue
        if completion_rate >= 80 and avg_rating >= 4.0 and overdue <= 1:
            return "excellent"

        # Good: Above average
        elif completion_rate >= 60 and avg_rating >= 3.5 and overdue <= 2:
            return "good"

        # Needs attention: Below average
        elif completion_rate < 50 or avg_rating < 3.0 or overdue >= 3:
            return "needs_attention"

        # Critical: Multiple red flags
        elif completion_rate < 30 or overdue >= 5:
            return "critical"

        else:
            return "good"

    # ==================== Organization Report Generation ====================

    async def generate_organization_report(
        self,
        db: Session,
        scope: str,
        department_id: Optional[int],
        time_period: TimePeriodEnum,
        start_date: Optional[date],
        end_date: Optional[date],
        template: ReportTemplateEnum,
    ) -> OrganizationReportResponse:
        """Generate organization-wide or department-level report (HR only)"""

        start_time = time.time()

        # Calculate time period
        period_start, period_end, period_label = self.calculate_time_period(
            time_period, start_date, end_date
        )

        # Determine scope
        if scope == "department" and department_id:
            department = (
                db.query(Department).filter(Department.id == department_id).first()
            )
            if not department:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Department with ID {department_id} not found",
                )
            departments = [department]
            dept_name = department.name
        else:
            # Organization-wide
            departments = (
                db.query(Department).filter(Department.is_active == True).all()
            )
            dept_name = None

        # Aggregate organization data
        org_data = self._aggregate_organization_data(
            db, departments, period_start, period_end
        )

        # Get department summaries
        department_summaries = []
        for dept in departments:
            dept_summary = self._get_department_summary(
                db, dept, period_start, period_end
            )
            department_summaries.append(dept_summary)

        # Build prompt
        prompt = self.prompt_templates.get_organization_report_prompt(
            org_data=org_data,
            department_summaries=department_summaries,
            time_period=period_label,
            scope=scope,
        )

        # Generate report
        logger.info(f"Generating organization report, scope: {scope}")
        report_markdown = await self.ai_provider.generate_report(
            prompt, max_tokens=3000
        )

        generation_time = time.time() - start_time

        response = OrganizationReportResponse(
            report_id=self._generate_report_id(),
            scope=scope,
            department_id=department_id,
            department_name=dept_name,
            generated_at=datetime.now(),
            time_period_start=period_start,
            time_period_end=period_end,
            report_markdown=report_markdown,
            organization_data_summary=org_data,
            department_summaries=department_summaries,
            generation_time_seconds=round(generation_time, 2),
        )

        logger.info(f"Organization report generated in {generation_time:.2f}s")
        return response

    def _aggregate_organization_data(
        self,
        db: Session,
        departments: List[Department],
        start_date: date,
        end_date: date,
    ) -> Dict[str, Any]:
        """Aggregate organization-level data"""

        # Get all active employees in these departments
        dept_ids = [d.id for d in departments]
        all_employees = (
            db.query(User)
            .filter(User.department_id.in_(dept_ids), User.is_active == True)
            .all()
        )

        employee_ids = [e.id for e in all_employees]

        # Organization goals
        org_goals = (
            db.query(Goal)
            .filter(
                Goal.employee_id.in_(employee_ids),
                Goal.start_date >= start_date,
                Goal.start_date <= end_date,
                Goal.is_deleted == False,
            )
            .all()
        )

        total_goals = len(org_goals)
        completed = sum(1 for g in org_goals if g.status == GoalStatus.COMPLETED)
        completion_rate = (completed / total_goals * 100) if total_goals > 0 else 0

        # On-time rate
        completed_with_dates = [
            g
            for g in org_goals
            if g.status == GoalStatus.COMPLETED and g.completion_date
        ]
        on_time = sum(
            1 for g in completed_with_dates if g.completion_date <= g.target_date
        )
        on_time_rate = (
            (on_time / len(completed_with_dates) * 100) if completed_with_dates else 0
        )

        # Average overdue per employee
        overdue_goals = [
            g
            for g in org_goals
            if g.target_date < date.today() and g.status != GoalStatus.COMPLETED
        ]
        avg_overdue = len(overdue_goals) / len(all_employees) if all_employees else 0

        # Organization feedback
        org_feedback = (
            db.query(Feedback)
            .filter(
                Feedback.employee_id.in_(employee_ids),
                Feedback.given_on >= datetime.combine(start_date, datetime.min.time()),
                Feedback.given_on <= datetime.combine(end_date, datetime.max.time()),
            )
            .all()
        )

        total_feedback = len(org_feedback)
        rated = [f for f in org_feedback if f.rating is not None]
        avg_rating = sum(f.rating for f in rated) / len(rated) if rated else 0

        # Feedback frequency
        feedback_per_employee = (
            total_feedback / len(all_employees) if all_employees else 0
        )
        if feedback_per_employee >= 3:
            freq = "High"
        elif feedback_per_employee >= 1:
            freq = "Moderate"
        else:
            freq = "Low"

        # Organization attendance
        org_attendance = (
            db.query(Attendance)
            .filter(
                Attendance.employee_id.in_(employee_ids),
                Attendance.date >= start_date,
                Attendance.date <= end_date,
            )
            .all()
        )

        total_att = len(org_attendance)
        present = sum(
            1
            for a in org_attendance
            if a.status in [AttendanceStatus.PRESENT, AttendanceStatus.WFH]
        )
        attendance_rate = (present / total_att * 100) if total_att > 0 else 0

        # Training completion
        training = (
            db.query(SkillModuleEnrollment)
            .filter(
                SkillModuleEnrollment.employee_id.in_(employee_ids),
                SkillModuleEnrollment.status == ModuleStatus.COMPLETED,
                SkillModuleEnrollment.completed_date
                >= datetime.combine(start_date, datetime.min.time()),
                SkillModuleEnrollment.completed_date
                <= datetime.combine(end_date, datetime.max.time()),
            )
            .count()
        )

        training_per_employee = training / len(all_employees) if all_employees else 0
        training_completion_pct = training_per_employee * 10  # Rough estimate

        return {
            "org_name": "Company",  # Can be made dynamic
            "total_employees": len(all_employees),
            "total_departments": len(departments),
            "total_goals": total_goals,
            "completion_rate": completion_rate,
            "on_time_rate": on_time_rate,
            "avg_overdue": avg_overdue,
            "total_feedback": total_feedback,
            "avg_rating": avg_rating,
            "feedback_frequency": freq,
            "attendance_rate": attendance_rate,
            "training_completion": min(training_completion_pct, 100),
        }

    def _get_department_summary(
        self, db: Session, department: Department, start_date: date, end_date: date
    ) -> Dict[str, Any]:
        """Get summary for a department"""

        # Get department employees
        dept_employees = (
            db.query(User)
            .filter(User.department_id == department.id, User.is_active == True)
            .all()
        )

        employee_ids = [e.id for e in dept_employees]

        if not employee_ids:
            return {
                "name": department.name,
                "employee_count": 0,
                "completion_rate": 0,
                "avg_rating": 0,
                "attendance_rate": 0,
                "training_completion": 0,
                "status": "no_data",
            }

        # Department goals
        dept_goals = (
            db.query(Goal)
            .filter(
                Goal.employee_id.in_(employee_ids),
                Goal.start_date >= start_date,
                Goal.start_date <= end_date,
                Goal.is_deleted == False,
            )
            .all()
        )

        total = len(dept_goals)
        completed = sum(1 for g in dept_goals if g.status == GoalStatus.COMPLETED)
        completion_rate = (completed / total * 100) if total > 0 else 0

        # Department feedback
        dept_feedback = (
            db.query(Feedback)
            .filter(
                Feedback.employee_id.in_(employee_ids),
                Feedback.given_on >= datetime.combine(start_date, datetime.min.time()),
                Feedback.given_on <= datetime.combine(end_date, datetime.max.time()),
                Feedback.rating.isnot(None),
            )
            .all()
        )

        avg_rating = (
            sum(f.rating for f in dept_feedback) / len(dept_feedback)
            if dept_feedback
            else 0
        )

        # Department attendance
        dept_attendance = (
            db.query(Attendance)
            .filter(
                Attendance.employee_id.in_(employee_ids),
                Attendance.date >= start_date,
                Attendance.date <= end_date,
            )
            .all()
        )

        total_att = len(dept_attendance)
        present = sum(
            1
            for a in dept_attendance
            if a.status in [AttendanceStatus.PRESENT, AttendanceStatus.WFH]
        )
        attendance_rate = (present / total_att * 100) if total_att > 0 else 0

        # Training
        training = (
            db.query(SkillModuleEnrollment)
            .filter(
                SkillModuleEnrollment.employee_id.in_(employee_ids),
                SkillModuleEnrollment.status == ModuleStatus.COMPLETED,
                SkillModuleEnrollment.completed_date
                >= datetime.combine(start_date, datetime.min.time()),
            )
            .count()
        )

        training_pct = (training / len(employee_ids) * 10) if employee_ids else 0

        # Determine status
        if completion_rate >= 75 and avg_rating >= 4.0:
            status = "high_performing"
        elif completion_rate >= 50 and avg_rating >= 3.5:
            status = "performing_well"
        elif completion_rate < 40 or avg_rating < 3.0:
            status = "needs_support"
        else:
            status = "average"

        return {
            "name": department.name,
            "employee_count": len(dept_employees),
            "completion_rate": completion_rate,
            "avg_rating": avg_rating,
            "attendance_rate": attendance_rate,
            "training_completion": min(training_pct, 100),
            "status": status,
        }
