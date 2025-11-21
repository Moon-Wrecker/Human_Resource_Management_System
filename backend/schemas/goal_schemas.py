"""
Goal Management Schemas
Pydantic models for goal tracking, task management, and performance monitoring
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


# ==================== Enums ====================

class GoalStatusEnum(str, Enum):
    """Goal status enumeration"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"


class GoalPriorityEnum(str, Enum):
    """Goal priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CommentTypeEnum(str, Enum):
    """Comment type enumeration"""
    UPDATE = "update"
    FEEDBACK = "feedback"
    QUESTION = "question"
    BLOCKER = "blocker"
    MILESTONE = "milestone"


# ==================== Goal Checkpoint Schemas ====================

class CheckpointBase(BaseModel):
    """Base checkpoint schema"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    sequence_number: int = Field(..., ge=1)


class CheckpointCreate(CheckpointBase):
    """Create checkpoint request"""
    pass


class CheckpointUpdate(BaseModel):
    """Update checkpoint request"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class CheckpointResponse(CheckpointBase):
    """Checkpoint response"""
    id: int
    goal_id: int
    is_completed: bool
    completed_date: Optional[datetime] = None
    completed_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================== Goal Category Schemas ====================

class GoalCategoryBase(BaseModel):
    """Base goal category schema"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    color_code: Optional[str] = Field(None, max_length=20)
    icon: Optional[str] = Field(None, max_length=50)


class GoalCategoryCreate(GoalCategoryBase):
    """Create goal category request"""
    pass


class GoalCategoryUpdate(BaseModel):
    """Update goal category request"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    color_code: Optional[str] = None
    icon: Optional[str] = None
    is_active: Optional[bool] = None


class GoalCategoryResponse(GoalCategoryBase):
    """Goal category response"""
    id: int
    is_active: bool
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    goal_count: Optional[int] = 0  # Number of goals in this category
    
    class Config:
        from_attributes = True


# ==================== Goal Template Schemas ====================

class GoalTemplateBase(BaseModel):
    """Base goal template schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = None
    priority: GoalPriorityEnum = GoalPriorityEnum.MEDIUM
    default_duration_days: Optional[int] = Field(None, ge=1, le=365)


class GoalTemplateCreate(GoalTemplateBase):
    """Create goal template request"""
    checkpoint_template: Optional[List[dict]] = []  # List of {title, description}


class GoalTemplateUpdate(BaseModel):
    """Update goal template request"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = None
    priority: Optional[GoalPriorityEnum] = None
    default_duration_days: Optional[int] = Field(None, ge=1, le=365)
    checkpoint_template: Optional[List[dict]] = None
    is_active: Optional[bool] = None


class GoalTemplateResponse(GoalTemplateBase):
    """Goal template response"""
    id: int
    checkpoint_template: Optional[List[dict]] = []
    is_active: bool
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    usage_count: int = 0
    
    class Config:
        from_attributes = True


# ==================== Goal Schemas ====================

class GoalBase(BaseModel):
    """Base goal schema"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = None
    priority: GoalPriorityEnum = GoalPriorityEnum.MEDIUM
    start_date: date
    target_date: date
    
    @field_validator('target_date')
    @classmethod
    def validate_target_date(cls, v, info):
        if 'start_date' in info.data and v < info.data['start_date']:
            raise ValueError('target_date must be after start_date')
        return v


class GoalCreate(GoalBase):
    """Create goal request"""
    employee_id: int  # Who this goal is for
    is_personal: bool = False  # True if self-created, False if assigned by manager
    template_id: Optional[int] = None
    checkpoints: Optional[List[CheckpointCreate]] = []


class GoalUpdate(BaseModel):
    """Update goal request"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = None
    priority: Optional[GoalPriorityEnum] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    status: Optional[GoalStatusEnum] = None


class GoalStatusUpdate(BaseModel):
    """Update goal status"""
    status: GoalStatusEnum


class GoalResponse(GoalBase):
    """Complete goal response"""
    id: int
    employee_id: int
    employee_name: Optional[str] = None
    employee_email: Optional[str] = None
    
    # Status and progress
    status: GoalStatusEnum
    progress_percentage: float
    completion_date: Optional[date] = None
    
    # Type and template
    is_personal: bool
    template_id: Optional[int] = None
    
    # Assignment
    assigned_by: Optional[int] = None
    assigned_by_name: Optional[str] = None
    
    # Category
    category_name: Optional[str] = None
    category_color: Optional[str] = None
    
    # Checkpoints
    checkpoints: List[CheckpointResponse] = []
    total_checkpoints: int = 0
    completed_checkpoints: int = 0
    
    # Metadata
    is_deleted: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Computed fields
    days_remaining: Optional[int] = None
    is_overdue: bool = False
    
    class Config:
        from_attributes = True


class GoalListResponse(BaseModel):
    """Paginated list of goals"""
    goals: List[GoalResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# ==================== Goal Comment Schemas ====================

class GoalCommentCreate(BaseModel):
    """Create goal comment request"""
    comment: str = Field(..., min_length=1)
    comment_type: CommentTypeEnum = CommentTypeEnum.UPDATE


class GoalCommentUpdate(BaseModel):
    """Update goal comment request"""
    comment: str = Field(..., min_length=1)
    comment_type: Optional[CommentTypeEnum] = None


class GoalCommentResponse(BaseModel):
    """Goal comment response"""
    id: int
    goal_id: int
    user_id: int
    user_name: Optional[str] = None
    user_role: Optional[str] = None
    comment: str
    comment_type: str
    attachment_path: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_deleted: bool = False
    
    class Config:
        from_attributes = True


# ==================== Goal History Schemas ====================

class GoalHistoryResponse(BaseModel):
    """Goal history/audit trail response"""
    id: int
    goal_id: int
    user_id: int
    user_name: Optional[str] = None
    action: str
    field_name: Optional[str] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Goal Statistics Schemas ====================

class GoalStatsResponse(BaseModel):
    """Goal statistics for an employee"""
    total_goals: int = 0
    active_goals: int = 0
    completed_goals: int = 0
    overdue_goals: int = 0
    completion_rate: float = 0.0
    average_completion_days: Optional[float] = None
    goals_by_priority: dict = {}
    goals_by_category: dict = {}
    goals_by_status: dict = {}


class TeamGoalStatsResponse(BaseModel):
    """Team goal statistics for managers"""
    total_team_goals: int = 0
    completed_team_goals: int = 0
    in_progress_team_goals: int = 0
    overdue_team_goals: int = 0
    team_completion_rate: float = 0.0
    team_members_stats: List[dict] = []  # Per-member statistics
    top_performers: List[dict] = []
    needs_attention: List[dict] = []


# ==================== Progress Report Schemas ====================

class GoalProgressReport(BaseModel):
    """Detailed progress report for performance reviews"""
    employee_id: int
    employee_name: str
    report_period_start: date
    report_period_end: date
    
    # Goal metrics
    total_goals_assigned: int = 0
    total_goals_completed: int = 0
    total_goals_in_progress: int = 0
    total_goals_overdue: int = 0
    completion_rate: float = 0.0
    
    # Detailed breakdown
    completed_goals: List[GoalResponse] = []
    in_progress_goals: List[GoalResponse] = []
    overdue_goals: List[GoalResponse] = []
    
    # Performance indicators
    average_completion_time: Optional[float] = None
    on_time_completion_rate: float = 0.0
    quality_score: Optional[float] = None  # Based on manager feedback
    
    # Category breakdown
    goals_by_category: dict = {}
    goals_by_priority: dict = {}


# ==================== Utility Schemas ====================

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True


class BulkOperationResponse(BaseModel):
    """Response for bulk operations"""
    success_count: int
    failure_count: int
    total: int
    messages: List[str] = []


# ==================== Filter Schemas ====================

class GoalFilterParams(BaseModel):
    """Goal filtering parameters"""
    employee_id: Optional[int] = None
    status: Optional[GoalStatusEnum] = None
    priority: Optional[GoalPriorityEnum] = None
    category_id: Optional[int] = None
    is_personal: Optional[bool] = None
    is_overdue: Optional[bool] = None
    assigned_by: Optional[int] = None
    start_date_from: Optional[date] = None
    start_date_to: Optional[date] = None
    target_date_from: Optional[date] = None
    target_date_to: Optional[date] = None
    search: Optional[str] = None  # Search in title/description

