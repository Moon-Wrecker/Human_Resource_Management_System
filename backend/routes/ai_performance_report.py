"""
API Routes for AI-Powered Performance Reports
Comprehensive endpoints for individual, team, and organization-wide performance reports
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from datetime import date

from database import get_db
from models import User, UserRole
from utils.dependencies import (
    get_current_active_user,
    require_hr,
    require_manager,
    require_hr_or_manager
)
from schemas.ai_performance_schemas import (
    AIReportGenerateRequest,
    AIReportResponse,
    TeamReportRequest,
    TeamReportResponse,
    OrganizationReportRequest,
    OrganizationReportResponse,
    HealthCheckResponse,
    MessageResponse,
    TimePeriodEnum,
    ReportTemplateEnum,
    ReportScopeEnum
)
from services.ai_performance_report_service import AIPerformanceReportService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai/performance-report", tags=["AI Performance Reports"])

# Initialize service
ai_report_service = AIPerformanceReportService()


# ==================== Health Check ====================

@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Check AI Report Service Health",
    description="Check if AI performance report service and providers are available"
)
async def health_check():
    """
    Check health status of AI performance report service.
    Returns provider availability status.
    """
    try:
        provider_status = ai_report_service.ai_provider.health_check()
        
        return HealthCheckResponse(
            service="AI Performance Report",
            status="healthy" if provider_status["available_providers"] > 0 else "degraded",
            ai_provider_status=provider_status,
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service health check failed: {str(e)}"
        )


# ==================== Individual Employee Reports ====================

@router.post(
    "/individual",
    response_model=AIReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Individual Performance Report",
    description="Generate AI-powered performance report for a specific employee"
)
async def generate_individual_report(
    request: AIReportGenerateRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Generate Individual Performance Report
    
    Generate a comprehensive AI-powered performance report for an employee.
    
    ### Access Control:
    - **Employee**: Can only generate for themselves (employee_id must match their ID)
    - **Manager**: Can generate for themselves and their direct reports
    - **HR**: Can generate for any employee
    
    ### Features:
    - Multiple time periods (30/90/180/365 days, quarters, custom)
    - Multiple templates (quick, standard, comprehensive, leadership, technical)
    - Optional team comparison
    - Optional period-over-period comparison
    - Custom metrics (HR only with custom template)
    - Weekly auto-save on Tuesdays (txt format)
    
    ### Report Includes:
    - Executive Summary
    - Strengths & Continue Doing
    - Areas for Development
    - Actionable Recommendations
    - Immediate Actions (if critical)
    - Performance Snapshot
    - Forward-Looking Focus
    
    ### Data Sources:
    - Goals & checkpoints
    - Feedback received
    - Attendance records
    - Training completion
    - Collaboration metrics
    """
    try:
        # Access control validation
        if current_user.role == UserRole.EMPLOYEE:
            if request.employee_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Employees can only generate reports for themselves"
                )
        
        elif current_user.role == UserRole.MANAGER:
            # Check if employee is a direct report
            employee = db.query(User).filter(User.id == request.employee_id).first()
            if not employee:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Employee with ID {request.employee_id} not found"
                )
            
            if employee.manager_id != current_user.id and request.employee_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Managers can only generate reports for themselves or their direct reports"
                )
        
        # HR can generate for anyone (no additional check needed)
        
        # Validate custom metrics (HR only)
        if request.template == ReportTemplateEnum.CUSTOM:
            if current_user.role != UserRole.HR:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Custom metric selection is only available to HR"
                )
            if not request.custom_metrics or len(request.custom_metrics) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Custom metrics must be specified for custom template"
                )
        
        # Generate report
        logger.info(f"User {current_user.id} generating report for employee {request.employee_id}")
        
        report = await ai_report_service.generate_individual_report(
            db=db,
            employee_id=request.employee_id,
            time_period=request.time_period,
            start_date=request.start_date,
            end_date=request.end_date,
            template=request.template,
            custom_metrics=[m.value for m in request.custom_metrics] if request.custom_metrics else None,
            include_team_comparison=request.include_team_comparison,
            include_period_comparison=request.include_period_comparison
        )
        
        return report
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating individual report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate report: {str(e)}"
        )


@router.get(
    "/individual/me",
    response_model=AIReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate My Performance Report",
    description="Generate performance report for the currently authenticated user"
)
async def generate_my_report(
    time_period: TimePeriodEnum = Query(default=TimePeriodEnum.LAST_90_DAYS),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    template: ReportTemplateEnum = Query(default=ReportTemplateEnum.STANDARD_REVIEW),
    include_team_comparison: bool = Query(default=False),
    include_period_comparison: bool = Query(default=False),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """
    ## Generate My Performance Report (Shortcut)
    
    Quick endpoint for users to generate their own performance report.
    
    **Access**: All authenticated users
    """
    try:
        report = await ai_report_service.generate_individual_report(
            db=db,
            employee_id=current_user.id,
            time_period=time_period,
            start_date=start_date,
            end_date=end_date,
            template=template,
            custom_metrics=None,  # Not allowed in this endpoint
            include_team_comparison=include_team_comparison,
            include_period_comparison=include_period_comparison
        )
        
        return report
    
    except Exception as e:
        logger.error(f"Error generating my report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate report: {str(e)}"
        )


# ==================== Team Reports (Manager) ====================

@router.post(
    "/team/summary",
    response_model=TeamReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Team Summary Report",
    description="Generate summary report for entire team (Manager/HR only)"
)
async def generate_team_summary(
    request: TeamReportRequest,
    current_user: Annotated[User, Depends(require_hr_or_manager)],
    db: Session = Depends(get_db)
):
    """
    ## Generate Team Summary Report
    
    Generate a comprehensive summary of team performance for managers.
    
    ### Report Includes:
    - Team Executive Summary
    - Team Strengths & Wins
    - Top Performers & Recognition
    - Team Members Needing Support
    - Team Trends & Patterns
    - Manager Action Items
    - Urgent Attention Required (if any)
    - Team Performance Snapshot
    
    ### Access Control:
    - **Manager**: Can only generate for their own team (team_id must match)
    - **HR**: Can generate for any team
    
    **Note**: For individual team member reports, see `/team/individual` endpoint.
    """
    try:
        # Determine team_id
        if request.team_id:
            team_id = request.team_id
            # If manager, validate it's their team
            if current_user.role == UserRole.MANAGER:
                if current_user.team_id != team_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Managers can only generate reports for their own team"
                    )
        else:
            # Default to current user's team
            if not current_user.team_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User is not assigned to any team"
                )
            team_id = current_user.team_id
        
        # Generate report based on scope
        if request.scope == ReportScopeEnum.TEAM_SUMMARY:
            report = await ai_report_service.generate_team_summary_report(
                db=db,
                team_id=team_id,
                time_period=request.time_period,
                start_date=request.start_date,
                end_date=request.end_date,
                template=request.template
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Use appropriate endpoint for this scope"
            )
        
        return report
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating team summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate team report: {str(e)}"
        )


@router.post(
    "/team/comparative",
    response_model=TeamReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Team Comparative Report",
    description="Generate comparative/leaderboard report for team (Manager/HR only)"
)
async def generate_team_comparative(
    request: TeamReportRequest,
    current_user: Annotated[User, Depends(require_hr_or_manager)],
    db: Session = Depends(get_db)
):
    """
    ## Generate Team Comparative Report
    
    Generate a comparative analysis/leaderboard of team member performance.
    
    ### Report Includes:
    - Performance Distribution Overview
    - Performance Leaderboard (ranked table)
    - Comparative Insights
    - Recommended Actions by Performance Tier
      - High Performers (recognition, stretch assignments)
      - Core Performers (development opportunities)
      - Developing Performers (support plans)
    - Fairness & Context Notes
    
    ### Access Control:
    - **Manager**: Only their own team
    - **HR**: Any team
    
    **Use Case**: Performance reviews, recognition decisions, identifying support needs
    """
    try:
        # Determine team_id
        if request.team_id:
            team_id = request.team_id
            if current_user.role == UserRole.MANAGER:
                if current_user.team_id != team_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Managers can only generate reports for their own team"
                    )
        else:
            if not current_user.team_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User is not assigned to any team"
                )
            team_id = current_user.team_id
        
        # Generate comparative report
        report = await ai_report_service.generate_team_comparative_report(
            db=db,
            team_id=team_id,
            time_period=request.time_period,
            start_date=request.start_date,
            end_date=request.end_date,
            template=request.template
        )
        
        return report
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating comparative report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate comparative report: {str(e)}"
        )


@router.get(
    "/team/my-team",
    response_model=TeamReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Report for My Team",
    description="Quick endpoint for managers to generate report for their team"
)
async def generate_my_team_report(
    scope: ReportScopeEnum = Query(default=ReportScopeEnum.TEAM_SUMMARY),
    time_period: TimePeriodEnum = Query(default=TimePeriodEnum.LAST_90_DAYS),
    template: ReportTemplateEnum = Query(default=ReportTemplateEnum.STANDARD_REVIEW),
    current_user: Annotated[User, Depends(require_manager)] = None,
    db: Session = Depends(get_db)
):
    """
    ## Generate My Team Report (Manager Shortcut)
    
    Quick endpoint for managers to generate reports for their own team.
    
    **Access**: Managers only
    **Query Parameters**:
    - `scope`: team_summary or team_comparative
    - `time_period`: Time period for analysis
    - `template`: Report template
    """
    try:
        if not current_user.team_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Manager is not assigned to any team"
            )
        
        if scope == ReportScopeEnum.TEAM_SUMMARY:
            report = await ai_report_service.generate_team_summary_report(
                db=db,
                team_id=current_user.team_id,
                time_period=time_period,
                start_date=None,
                end_date=None,
                template=template
            )
        elif scope == ReportScopeEnum.TEAM_COMPARATIVE:
            report = await ai_report_service.generate_team_comparative_report(
                db=db,
                team_id=current_user.team_id,
                time_period=time_period,
                start_date=None,
                end_date=None,
                template=template
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Scope {scope} not supported for this endpoint"
            )
        
        return report
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating my team report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate team report: {str(e)}"
        )


# ==================== Organization Reports (HR Only) ====================

@router.post(
    "/organization",
    response_model=OrganizationReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Organization/Department Report",
    description="Generate organization-wide or department-level report (HR only)"
)
async def generate_organization_report(
    request: OrganizationReportRequest,
    current_user: Annotated[User, Depends(require_hr)],
    db: Session = Depends(get_db)
):
    """
    ## Generate Organization/Department Report (HR Only)
    
    Generate strategic performance analysis at organization or department level.
    
    ### Report Includes:
    - Executive Summary for HR Leadership
    - Organizational Performance Overview
    - Department Performance Analysis
      - High-Performing Departments
      - Departments Needing Support
      - Department Comparison Matrix
    - Organization-Wide Trends & Insights
    - Strategic HR Recommendations
    - Talent Management Insights
    - Critical Organizational Risks (if any)
    - Strategic Focus Areas
    
    ### Scopes:
    - **organization**: All departments, company-wide analysis
    - **department**: Single department deep-dive (requires department_id)
    
    ### Use Cases:
    - Executive reporting
    - Strategic HR planning
    - Resource allocation decisions
    - Policy and process improvements
    - Talent management and succession planning
    
    **Access**: HR only
    """
    try:
        # Validate scope
        if request.scope == ReportScopeEnum.DEPARTMENT:
            if not request.department_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="department_id required for department scope"
                )
        
        # Generate report
        logger.info(f"HR user {current_user.id} generating {request.scope} report")
        
        report = await ai_report_service.generate_organization_report(
            db=db,
            scope=request.scope.value,
            department_id=request.department_id,
            time_period=request.time_period,
            start_date=request.start_date,
            end_date=request.end_date,
            template=request.template
        )
        
        return report
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating organization report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate organization report: {str(e)}"
        )


@router.get(
    "/organization/company-wide",
    response_model=OrganizationReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Company-Wide Report",
    description="Quick endpoint for company-wide performance analysis (HR only)"
)
async def generate_company_wide_report(
    time_period: TimePeriodEnum = Query(default=TimePeriodEnum.CURRENT_QUARTER),
    template: ReportTemplateEnum = Query(default=ReportTemplateEnum.COMPREHENSIVE_REVIEW),
    current_user: Annotated[User, Depends(require_hr)] = None,
    db: Session = Depends(get_db)
):
    """
    ## Generate Company-Wide Performance Report (HR Shortcut)
    
    Quick endpoint for generating organization-wide performance analysis.
    
    **Access**: HR only
    **Default**: Current quarter, comprehensive review
    """
    try:
        report = await ai_report_service.generate_organization_report(
            db=db,
            scope="organization",
            department_id=None,
            time_period=time_period,
            start_date=None,
            end_date=None,
            template=template
        )
        
        return report
    
    except Exception as e:
        logger.error(f"Error generating company-wide report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate company-wide report: {str(e)}"
        )


# ==================== Utility Endpoints ====================

@router.get(
    "/templates",
    response_model=dict,
    summary="Get Available Report Templates",
    description="List all available report templates with descriptions"
)
async def get_templates(
    current_user: Annotated[User, Depends(get_current_active_user)] = None
):
    """
    ## Get Available Report Templates
    
    Returns list of available templates with descriptions and recommended use cases.
    
    **Access**: All authenticated users
    """
    templates = {
        "quick_summary": {
            "name": "Quick Summary",
            "description": "Brief report with 3 key metrics",
            "metrics_count": 3,
            "recommended_for": "Quick check-ins, weekly reviews",
            "available_to": ["employee", "manager", "hr"]
        },
        "standard_review": {
            "name": "Standard Review",
            "description": "Balanced report with 5-7 key metrics",
            "metrics_count": 5,
            "recommended_for": "Monthly reviews, regular 1-on-1s",
            "available_to": ["employee", "manager", "hr"]
        },
        "comprehensive_review": {
            "name": "Comprehensive Review",
            "description": "Detailed analysis with all available metrics",
            "metrics_count": 11,
            "recommended_for": "Quarterly reviews, annual performance reviews",
            "available_to": ["employee", "manager", "hr"]
        },
        "leadership_focus": {
            "name": "Leadership Focus",
            "description": "Focus on leadership, collaboration, and team impact",
            "metrics_count": 5,
            "recommended_for": "Manager evaluations, promotion decisions",
            "available_to": ["manager", "hr"]
        },
        "technical_focus": {
            "name": "Technical Focus",
            "description": "Focus on technical skills, training, and goal execution",
            "metrics_count": 5,
            "recommended_for": "Technical role evaluations, skill assessments",
            "available_to": ["manager", "hr"]
        },
        "custom": {
            "name": "Custom Selection",
            "description": "Select specific metrics for tailored analysis",
            "metrics_count": "variable",
            "recommended_for": "Specific evaluation needs, targeted feedback",
            "available_to": ["hr"]
        }
    }
    
    return {
        "templates": templates,
        "user_role": current_user.role.value,
        "note": "Custom template with metric selection is available to HR only"
    }


@router.get(
    "/metrics",
    response_model=dict,
    summary="Get Available Metrics",
    description="List all available metrics for custom reports (HR only)"
)
async def get_metrics(
    current_user: Annotated[User, Depends(require_hr)] = None
):
    """
    ## Get Available Metrics (HR Only)
    
    Returns list of all metrics available for custom report generation.
    
    **Access**: HR only
    """
    metrics = {
        "goal_completion": "Goal Completion Rate - % of goals completed",
        "attendance_rate": "Attendance Rate - % of days present",
        "training_completion": "Training Completion - Modules completed",
        "feedback_ratings": "Feedback Ratings - Average rating received",
        "overdue_goals": "Overdue Goals - Number and analysis",
        "checkpoint_progress": "Checkpoint Progress - Sub-task completion",
        "feedback_sentiment": "Feedback Sentiment - Positive vs constructive",
        "skills_development": "Skills Development - New skills acquired",
        "peer_collaboration": "Peer Collaboration - Comments, interactions",
        "category_goal_success": "Category-wise Goal Success - By goal type",
        "priority_goal_handling": "Priority Goal Handling - By goal priority",
        "team_comparison": "Team Comparison - vs team average",
        "period_comparison": "Period Comparison - vs previous period"
    }
    
    return {
        "available_metrics": metrics,
        "note": "Select metrics for custom template reports",
        "recommendation": "Choose 5-7 metrics for balanced analysis"
    }


# Import datetime for health check
from datetime import datetime

