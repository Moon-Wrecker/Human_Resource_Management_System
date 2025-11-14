"""
Goal Management Routes
Comprehensive API endpoints for goal tracking, task management, and performance monitoring
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from datetime import datetime, date

from database import get_db
from models import User, UserRole
from utils.dependencies import get_current_active_user, require_manager, require_hr_or_manager
from services.goal_service import GoalService
from schemas.goal_schemas import (
    GoalCreate,
    GoalUpdate,
    GoalStatusUpdate,
    GoalResponse,
    GoalListResponse,
    GoalStatsResponse,
    TeamGoalStatsResponse,
    CheckpointCreate,
    CheckpointUpdate,
    CheckpointResponse,
    GoalCommentCreate,
    GoalCommentUpdate,
    GoalCommentResponse,
    GoalCategoryCreate,
    GoalCategoryUpdate,
    GoalCategoryResponse,
    GoalTemplateCreate,
    GoalTemplateUpdate,
    GoalTemplateResponse,
    MessageResponse,
    GoalStatusEnum,
    GoalPriorityEnum
)

router = APIRouter(prefix="/goals", tags=["Goals & Task Management"])


# ==================== Goal CRUD Endpoints ====================

@router.post(
    "",
    response_model=GoalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Goal",
    description="Create a new goal (Manager assigns to team member OR Employee creates personal goal)"
)
async def create_goal(
    goal_data: GoalCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Create Goal
    
    **Two modes:**
    1. **Manager-Assigned Goal**: Manager assigns goal to team member
       - `is_personal`: false
       - `employee_id`: Team member's ID
       - Manager must be the direct manager of the employee
    
    2. **Personal Goal**: Employee creates goal for themselves
       - `is_personal`: true
       - `employee_id`: Must match current user ID
    
    **Features:**
    - Auto-calculates progress from checkpoints
    - Sends notifications to relevant parties
    - Creates audit trail
    - Supports goal templates
    
    **Access:**
    - Managers: Can assign to direct reports
    - Employees: Can create personal goals
    - HR: Cannot assign goals
    """
    goal_dict = goal_data.model_dump()
    return GoalService.create_goal(db, goal_dict, current_user)


@router.get(
    "/me",
    response_model=GoalListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get My Goals",
    description="Get all goals for the current user with filtering and pagination"
)
async def get_my_goals(
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(100, ge=1, le=500, description="Page size"),
    status: Optional[GoalStatusEnum] = Query(None, description="Filter by status"),
    priority: Optional[GoalPriorityEnum] = Query(None, description="Filter by priority"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    is_overdue: Optional[bool] = Query(None, description="Filter overdue goals only"),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """
    ## Get My Goals
    
    Retrieve all goals assigned to or created by the current user.
    
    **Filters:**
    - `status`: Filter by goal status (not_started, in_progress, completed, etc.)
    - `priority`: Filter by priority (low, medium, high, critical)
    - `category_id`: Filter by goal category
    - `is_overdue`: Show only overdue goals
    
    **Response includes:**
    - Goal details with progress percentage
    - All checkpoints and completion status
    - Days remaining and overdue status
    - Manager/assignee information
    
    **Access:** All authenticated users
    """
    goals, total = GoalService.get_my_goals(
        db=db,
        current_user=current_user,
        skip=skip,
        limit=limit,
        status=status.value if status else None,
        priority=priority.value if priority else None,
        category_id=category_id,
        is_overdue=is_overdue
    )
    
    total_pages = (total + limit - 1) // limit
    
    return GoalListResponse(
        goals=goals,
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        total_pages=total_pages
    )


@router.get(
    "/team",
    response_model=GoalListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Team Goals",
    description="Get goals for all team members (Manager/HR only)"
)
async def get_team_goals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    status: Optional[GoalStatusEnum] = Query(None),
    priority: Optional[GoalPriorityEnum] = Query(None),
    is_overdue: Optional[bool] = Query(None),
    current_user: Annotated[User, Depends(require_manager)] = None,
    db: Session = Depends(get_db)
):
    """
    ## Get Team Goals
    
    Retrieve goals for all team members.
    
    **Access:**
    - Managers: See goals for their direct reports
    - HR/Admin: See all goals in the organization
    
    **Use Cases:**
    - Team performance monitoring
    - Identifying blockers and overdue goals
    - Performance review preparation
    """
    goals, total = GoalService.get_team_goals(
        db=db,
        current_user=current_user,
        skip=skip,
        limit=limit,
        employee_id=employee_id,
        status=status.value if status else None,
        priority=priority.value if priority else None,
        is_overdue=is_overdue
    )
    
    total_pages = (total + limit - 1) // limit
    
    return GoalListResponse(
        goals=goals,
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        total_pages=total_pages
    )


@router.get(
    "/{goal_id}",
    response_model=GoalResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Goal by ID",
    description="Get detailed information about a specific goal"
)
async def get_goal(
    goal_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Get Goal by ID
    
    Retrieve complete details of a specific goal.
    
    **Access Control:**
    - Employee: Can view their own goals
    - Manager: Can view team member goals
    - HR/Admin: Can view all goals
    
    **Returns:**
    - Complete goal details
    - All checkpoints with completion status
    - Progress tracking information
    - Audit trail metadata
    """
    return GoalService.get_goal_by_id(db, goal_id, current_user)


@router.put(
    "/{goal_id}",
    response_model=GoalResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Goal",
    description="Update goal details (title, description, dates, priority, etc.)"
)
async def update_goal(
    goal_id: int,
    update_data: GoalUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Update Goal
    
    Update goal information.
    
    **Editable Fields:**
    - title, description
    - category_id, priority
    - start_date, target_date
    - status
    
    **Access:**
    - Personal goals: Employee can update
    - Assigned goals: Manager can update
    - Both parties can update status
    
    **Features:**
    - Creates audit trail for all changes
    - Sends notifications on status changes
    - Auto-completes when status set to completed
    """
    update_dict = update_data.model_dump(exclude_unset=True)
    return GoalService.update_goal(db, goal_id, update_dict, current_user)


@router.patch(
    "/{goal_id}/status",
    response_model=GoalResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Goal Status",
    description="Update only the goal status (quick status change)"
)
async def update_goal_status(
    goal_id: int,
    status_data: GoalStatusUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Update Goal Status
    
    Quick endpoint to update only the goal status.
    
    **Status Options:**
    - not_started
    - in_progress
    - completed
    - on_hold
    - cancelled
    
    **Features:**
    - Auto-sets completion_date when status is completed
    - Notifies relevant parties
    - Updates audit trail
    """
    update_dict = {"status": status_data.status}
    return GoalService.update_goal(db, goal_id, update_dict, current_user)


@router.delete(
    "/{goal_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete Goal",
    description="Soft delete a goal (archived, not permanently deleted)"
)
async def delete_goal(
    goal_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Delete Goal
    
    Soft delete a goal (marks as deleted, doesn't remove from database).
    
    **Access:**
    - Personal goals: Employee can delete
    - Assigned goals: Manager can delete
    
    **Note:** Deleted goals are hidden from normal views but preserved for audit trails
    """
    result = GoalService.delete_goal(db, goal_id, current_user)
    return MessageResponse(message=result["message"])


# ==================== Checkpoint Management Endpoints ====================

@router.post(
    "/{goal_id}/checkpoints",
    response_model=CheckpointResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Checkpoint",
    description="Add a new checkpoint/task to a goal"
)
async def create_checkpoint(
    goal_id: int,
    checkpoint_data: CheckpointCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Add Checkpoint
    
    Add a new checkpoint (sub-task/milestone) to a goal.
    
    **Features:**
    - Auto-sequences checkpoints
    - Recalculates goal progress automatically
    - Creates audit trail
    
    **Access:** Employee (goal owner) or Manager (goal creator) can add checkpoints
    """
    checkpoint_dict = checkpoint_data.model_dump()
    return GoalService.create_checkpoint(db, goal_id, checkpoint_dict, current_user)


@router.put(
    "/checkpoints/{checkpoint_id}",
    response_model=CheckpointResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Checkpoint",
    description="Update checkpoint details or mark as complete/incomplete"
)
async def update_checkpoint(
    checkpoint_id: int,
    update_data: CheckpointUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Update Checkpoint
    
    Update checkpoint information or completion status.
    
    **Key Feature:**
    - Marking checkpoint as complete auto-recalculates goal progress
    - Sends notification to manager when employee completes checkpoint
    - Updates audit trail
    
    **Access:** Employee or Manager can update checkpoints
    """
    update_dict = update_data.model_dump(exclude_unset=True)
    return GoalService.update_checkpoint(db, checkpoint_id, update_dict, current_user)


@router.delete(
    "/checkpoints/{checkpoint_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete Checkpoint",
    description="Remove a checkpoint from a goal"
)
async def delete_checkpoint(
    checkpoint_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Delete Checkpoint
    
    Remove a checkpoint from a goal.
    
    **Note:** Recalculates goal progress after deletion
    """
    result = GoalService.delete_checkpoint(db, checkpoint_id, current_user)
    return MessageResponse(message=result["message"])


# ==================== Comments & Collaboration Endpoints ====================

@router.post(
    "/{goal_id}/comments",
    response_model=GoalCommentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Comment",
    description="Add a comment/update to a goal"
)
async def add_comment(
    goal_id: int,
    comment_data: GoalCommentCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Add Comment
    
    Add a comment or update to a goal for collaboration.
    
    **Comment Types:**
    - update: Progress update
    - feedback: Manager feedback
    - question: Employee question
    - blocker: Issue/blocker report
    - milestone: Milestone achievement
    
    **Features:**
    - Notifies the other party (manager ↔ employee)
    - Creates communication thread
    - Supports progress tracking
    
    **Access:** Employee (goal owner) or Manager (goal creator) can comment
    """
    comment_dict = comment_data.model_dump()
    return GoalService.add_comment(db, goal_id, comment_dict, current_user)


@router.get(
    "/{goal_id}/comments",
    response_model=list[GoalCommentResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Comments",
    description="Get all comments/updates for a goal"
)
async def get_comments(
    goal_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Get Comments
    
    Retrieve all comments and updates for a goal.
    
    **Returns:** Comments in reverse chronological order (newest first)
    
    **Access:** Employee or Manager involved in the goal
    """
    return GoalService.get_goal_comments(db, goal_id, current_user)


# ==================== Statistics & Analytics Endpoints ====================

@router.get(
    "/stats/me",
    response_model=GoalStatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get My Goal Statistics",
    description="Get comprehensive statistics about my goals"
)
async def get_my_goal_stats(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Get My Goal Statistics
    
    Comprehensive statistics for the current user's goals.
    
    **Metrics:**
    - Total goals, active goals, completed goals
    - Overdue goals count
    - Completion rate
    - Average completion time
    - Goals breakdown by priority, category, status
    
    **Use Cases:**
    - Dashboard widgets
    - Performance self-assessment
    - Progress tracking
    """
    return GoalService.get_my_goal_stats(db, current_user)


@router.get(
    "/stats/team",
    response_model=TeamGoalStatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Team Goal Statistics",
    description="Get team-wide goal statistics (Manager only)"
)
async def get_team_goal_stats(
    current_user: Annotated[User, Depends(require_manager)],
    db: Session = Depends(get_db)
):
    """
    ## Get Team Goal Statistics
    
    Team-wide goal statistics for managers.
    
    **Metrics:**
    - Total team goals, completed, in progress, overdue
    - Team completion rate
    - Per-member statistics
    - Top performers (by completion rate)
    - Team members needing attention (high overdue count)
    
    **Use Cases:**
    - Manager dashboard
    - Team performance monitoring
    - Performance review preparation
    - Identifying struggling team members
    
    **Access:** Managers and HR only
    """
    return GoalService.get_team_goal_stats(db, current_user)


# ==================== Goal Categories Endpoints ====================

@router.post(
    "/categories",
    response_model=GoalCategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Goal Category",
    description="Create a new goal category (Manager/HR only)"
)
async def create_category(
    category_data: GoalCategoryCreate,
    current_user: Annotated[User, Depends(require_manager)],
    db: Session = Depends(get_db)
):
    """
    ## Create Goal Category
    
    Create a new goal category for organizing goals.
    
    **Examples:**
    - Learning & Development
    - Performance Improvement
    - Project Delivery
    - Innovation
    - Leadership
    
    **Features:**
    - Color coding for UI
    - Icon support
    - Active/inactive status
    
    **Access:** Managers and HR only
    """
    category_dict = category_data.model_dump()
    return GoalService.create_category(db, category_dict, current_user)


@router.get(
    "/categories",
    response_model=list[GoalCategoryResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Goal Categories",
    description="Get all goal categories"
)
async def get_categories(
    include_inactive: bool = Query(False, description="Include inactive categories"),
    db: Session = Depends(get_db)
):
    """
    ## Get Goal Categories
    
    Retrieve all goal categories.
    
    **Use Cases:**
    - Category selection dropdown
    - Goal filtering
    - Dashboard breakdown by category
    
    **Access:** All authenticated users
    """
    return GoalService.get_categories(db, include_inactive)


@router.put(
    "/categories/{category_id}",
    response_model=GoalCategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Goal Category",
    description="Update goal category details (Manager/HR only)"
)
async def update_category(
    category_id: int,
    update_data: GoalCategoryUpdate,
    current_user: Annotated[User, Depends(require_manager)],
    db: Session = Depends(get_db)
):
    """
    ## Update Goal Category
    
    Update goal category information.
    
    **Editable Fields:**
    - name, description
    - color_code, icon
    - is_active (to deactivate)
    
    **Access:** Managers and HR only
    """
    update_dict = update_data.model_dump(exclude_unset=True)
    return GoalService.update_category(db, category_id, update_dict, current_user)


# ==================== Goal Templates Endpoints ====================

@router.post(
    "/templates",
    response_model=GoalTemplateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Goal Template",
    description="Create a reusable goal template (Manager/HR only)"
)
async def create_template(
    template_data: GoalTemplateCreate,
    current_user: Annotated[User, Depends(require_manager)],
    db: Session = Depends(get_db)
):
    """
    ## Create Goal Template
    
    Create a reusable goal template for common goals.
    
    **Use Cases:**
    - Onboarding goals for new employees
    - Quarterly performance goals
    - Skill development paths
    - Project completion templates
    
    **Features:**
    - Pre-defined checkpoints
    - Default duration
    - Priority and category suggestions
    - Usage tracking
    
    **Access:** Managers and HR only
    """
    template_dict = template_data.model_dump()
    return GoalService.create_template(db, template_dict, current_user)


@router.get(
    "/templates",
    response_model=list[GoalTemplateResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Goal Templates",
    description="Get all goal templates"
)
async def get_templates(
    include_inactive: bool = Query(False, description="Include inactive templates"),
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Get Goal Templates
    
    Retrieve all available goal templates.
    
    **Ordering:** By usage count (most used first)
    
    **Use Cases:**
    - Quick goal creation
    - Standardized goal setting
    - Best practices sharing
    
    **Access:** All authenticated users
    """
    return GoalService.get_templates(db, include_inactive)


@router.get(
    "/templates/{template_id}",
    response_model=GoalTemplateResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Goal Template",
    description="Get a specific goal template by ID"
)
async def get_template(
    template_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Get Goal Template
    
    Retrieve a specific goal template.
    
    **Returns:** Complete template with checkpoint structure
    
    **Access:** All authenticated users
    """
    from models import GoalTemplate
    template = db.query(GoalTemplate).filter(GoalTemplate.id == template_id).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    return GoalService._format_template_response(template)

