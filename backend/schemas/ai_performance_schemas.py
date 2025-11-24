"""
Pydantic Schemas for AI Performance Report System
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from enum import Enum


# ==================== Enums ====================

class TimePeriodEnum(str, Enum):
    """Predefined time periods"""
    LAST_30_DAYS = "last_30_days"
    LAST_90_DAYS = "last_90_days"
    LAST_180_DAYS = "last_180_days"
    LAST_365_DAYS = "last_365_days"
    CURRENT_QUARTER = "current_quarter"
    LAST_QUARTER = "last_quarter"
    CURRENT_YEAR = "current_year"
    CUSTOM = "custom"


class ReportTemplateEnum(str, Enum):
    """Report templates with different detail levels"""
    QUICK_SUMMARY = "quick_summary"  # Brief, 3 key metrics
    STANDARD_REVIEW = "standard_review"  # Moderate, 5-7 metrics
    COMPREHENSIVE_REVIEW = "comprehensive_review"  # Detailed, all metrics
    LEADERSHIP_FOCUS = "leadership_focus"  # Leadership & management focus
    TECHNICAL_FOCUS = "technical_focus"  # Technical & skills focus
    CUSTOM = "custom"  # Custom metric selection (HR only)


class MetricEnum(str, Enum):
    """Available metrics for custom reports"""
    GOAL_COMPLETION = "goal_completion"
    ATTENDANCE_RATE = "attendance_rate"
    TRAINING_COMPLETION = "training_completion"
    FEEDBACK_RATINGS = "feedback_ratings"
    OVERDUE_GOALS = "overdue_goals"
    CHECKPOINT_PROGRESS = "checkpoint_progress"
    FEEDBACK_SENTIMENT = "feedback_sentiment"
    SKILLS_DEVELOPMENT = "skills_development"
    PEER_COLLABORATION = "peer_collaboration"
    CATEGORY_GOAL_SUCCESS = "category_goal_success"
    PRIORITY_GOAL_HANDLING = "priority_goal_handling"
    TEAM_COMPARISON = "team_comparison"
    PERIOD_COMPARISON = "period_comparison"


class ReportScopeEnum(str, Enum):
    """Scope of report generation"""
    INDIVIDUAL = "individual"  # Single employee
    TEAM_INDIVIDUAL = "team_individual"  # Each team member separately
    TEAM_SUMMARY = "team_summary"  # Entire team summary
    TEAM_COMPARATIVE = "team_comparative"  # Team comparison report
    DEPARTMENT = "department"  # Department-wide (HR only)
    ORGANIZATION = "organization"  # Organization-wide (HR only)


# ==================== Request Schemas ====================

class AIReportGenerateRequest(BaseModel):
    """Request schema for generating AI performance report"""
    employee_id: int = Field(..., description="Employee ID for report generation", gt=0)
    time_period: TimePeriodEnum = Field(
        default=TimePeriodEnum.LAST_90_DAYS,
        description="Predefined time period or custom"
    )
    start_date: Optional[date] = Field(None, description="Start date for custom period")
    end_date: Optional[date] = Field(None, description="End date for custom period")
    template: ReportTemplateEnum = Field(
        default=ReportTemplateEnum.STANDARD_REVIEW,
        description="Report template to use"
    )
    custom_metrics: Optional[List[MetricEnum]] = Field(
        None,
        description="Custom metrics (only for HR with custom template)"
    )
    include_team_comparison: bool = Field(
        default=False,
        description="Include comparison with team average"
    )
    include_period_comparison: bool = Field(
        default=False,
        description="Include comparison with previous period"
    )
    
    @field_validator('end_date')
    @classmethod
    def validate_dates(cls, v, info):
        """Validate custom date range"""
        if info.data.get('time_period') == TimePeriodEnum.CUSTOM:
            if not v or not info.data.get('start_date'):
                raise ValueError('start_date and end_date required for custom period')
            if v < info.data.get('start_date'):
                raise ValueError('end_date must be after start_date')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": 5,
                "time_period": "last_90_days",
                "template": "standard_review",
                "include_team_comparison": True,
                "include_period_comparison": True
            }
        }


class TeamReportRequest(BaseModel):
    """Request schema for team-wide report generation"""
    team_id: Optional[int] = Field(None, description="Team ID (optional, defaults to manager's team)")
    scope: ReportScopeEnum = Field(
        default=ReportScopeEnum.TEAM_SUMMARY,
        description="Type of team report"
    )
    time_period: TimePeriodEnum = Field(default=TimePeriodEnum.LAST_90_DAYS)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    template: ReportTemplateEnum = Field(default=ReportTemplateEnum.STANDARD_REVIEW)
    
    class Config:
        json_schema_extra = {
            "example": {
                "scope": "team_summary",
                "time_period": "last_90_days",
                "template": "standard_review"
            }
        }


class OrganizationReportRequest(BaseModel):
    """Request schema for organization-wide reports (HR only)"""
    scope: ReportScopeEnum = Field(description="Organization or department scope")
    department_id: Optional[int] = Field(None, description="Specific department ID")
    time_period: TimePeriodEnum = Field(default=TimePeriodEnum.LAST_90_DAYS)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    template: ReportTemplateEnum = Field(default=ReportTemplateEnum.STANDARD_REVIEW)
    custom_metrics: Optional[List[MetricEnum]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "scope": "department",
                "department_id": 1,
                "time_period": "current_quarter",
                "template": "comprehensive_review"
            }
        }


# ==================== Response Schemas ====================

class DataSummary(BaseModel):
    """Summary of data used in report generation"""
    total_goals: int = 0
    completed_goals: int = 0
    in_progress_goals: int = 0
    overdue_goals: int = 0
    total_feedback: int = 0
    average_feedback_rating: Optional[float] = None
    attendance_rate: Optional[float] = None
    training_completion_rate: Optional[float] = None
    total_checkpoints: int = 0
    completed_checkpoints: int = 0
    data_sufficiency: str = Field(
        ...,
        description="sufficient, limited, insufficient"
    )
    warnings: List[str] = []


class AIReportResponse(BaseModel):
    """Response schema for generated AI report"""
    report_id: Optional[str] = Field(None, description="Unique report identifier")
    employee_id: int
    employee_name: str
    employee_email: str
    report_type: str = Field(..., description="individual, team_summary, etc.")
    generated_at: datetime
    time_period_start: date
    time_period_end: date
    time_period_label: str
    template_used: str
    metrics_used: List[str]
    
    # The actual AI-generated content
    report_markdown: str = Field(..., description="AI-generated report in markdown format")
    
    # Data summary
    data_summary: DataSummary
    
    # Metadata
    ai_model: str = "gemini-2.0-flash-exp"
    generation_time_seconds: Optional[float] = None
    
    # Storage info (for weekly saved reports)
    is_saved: bool = False
    saved_path: Optional[str] = None
    saved_on: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "RPT-20250116-001",
                "employee_id": 5,
                "employee_name": "John Doe",
                "employee_email": "john.doe@company.com",
                "report_type": "individual",
                "generated_at": "2025-01-16T10:30:00",
                "time_period_start": "2024-10-16",
                "time_period_end": "2025-01-16",
                "time_period_label": "Last 90 Days",
                "template_used": "standard_review",
                "metrics_used": ["goal_completion", "attendance_rate", "feedback_ratings"],
                "report_markdown": "# Performance Report\n\n## Strengths...",
                "data_summary": {
                    "total_goals": 10,
                    "completed_goals": 7,
                    "data_sufficiency": "sufficient"
                },
                "is_saved": False
            }
        }


class TeamMemberReport(BaseModel):
    """Individual team member's report summary"""
    employee_id: int
    employee_name: str
    report_summary: str = Field(..., description="Brief summary for team view")
    key_metrics: Dict[str, Any]
    overall_status: str = Field(..., description="excellent, good, needs_attention, critical")


class TeamReportResponse(BaseModel):
    """Response schema for team-wide reports"""
    report_id: Optional[str] = None
    team_id: int
    team_name: str
    report_type: str
    generated_at: datetime
    time_period_start: date
    time_period_end: date
    template_used: str
    
    # For team summary
    team_summary_markdown: Optional[str] = None
    
    # For team comparative
    team_comparative_markdown: Optional[str] = None
    
    # For individual reports
    member_reports: List[TeamMemberReport] = []
    
    # Team-level data
    team_data_summary: Dict[str, Any]
    
    generation_time_seconds: Optional[float] = None


class OrganizationReportResponse(BaseModel):
    """Response schema for organization-wide reports"""
    report_id: Optional[str] = None
    scope: str
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    generated_at: datetime
    time_period_start: date
    time_period_end: date
    
    report_markdown: str
    
    organization_data_summary: Dict[str, Any]
    department_summaries: List[Dict[str, Any]] = []
    
    generation_time_seconds: Optional[float] = None


class ReportHistoryItem(BaseModel):
    """Historical report item"""
    report_id: str
    employee_id: int
    employee_name: str
    generated_at: datetime
    time_period_label: str
    template_used: str
    saved_path: Optional[str] = None


class ReportHistoryResponse(BaseModel):
    """Response for report history listing"""
    reports: List[ReportHistoryItem]
    total: int
    page: int
    page_size: int


# ==================== Utility Schemas ====================

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True


class HealthCheckResponse(BaseModel):
    """AI service health check response"""
    service: str = "AI Performance Report"
    status: str
    ai_provider_status: Dict[str, Any]
    timestamp: datetime

