"""
Goal Service - Business logic for goal and task management
Comprehensive goal tracking system with progress monitoring, notifications, and audit trails
"""
import json
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_, desc, asc, extract
from fastapi import HTTPException, status

from models import (
    User, UserRole, Goal, GoalCheckpoint, GoalCategory, GoalTemplate,
    GoalComment, GoalHistory, GoalStatus, Notification
)


class GoalService:
    """Service for goal management operations"""
    
    # ==================== Goal CRUD Operations ====================
    
    @staticmethod
    def create_goal(
        db: Session,
        goal_data: Dict[str, Any],
        current_user: User
    ) -> Dict[str, Any]:
        """
        Create a new goal
        
        Args:
            db: Database session
            goal_data: Goal creation data
            current_user: User creating the goal
            
        Returns:
            Created goal dictionary
        """
        # Validate employee exists
        employee = db.query(User).filter(User.id == goal_data['employee_id']).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )
        
        # Access control
        is_personal = goal_data.get('is_personal', False)
        
        if is_personal:
            # Personal goals: employee can only create for themselves
            if current_user.id != goal_data['employee_id']:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only create personal goals for yourself"
                )
            assigned_by = current_user.id
        else:
            # Assigned goals: only managers can assign to their team members
            if current_user.role == UserRole.HR:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="HR cannot assign goals. Only managers can assign goals to their team members."
                )
            
            if current_user.role != UserRole.MANAGER:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only managers can assign goals to team members"
                )
            
            # Verify employee reports to this manager
            if employee.manager_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only assign goals to your direct reports"
                )
            
            assigned_by = current_user.id
        
        # If using template, load checkpoint template
        checkpoints_data = goal_data.pop('checkpoints', [])
        template_id = goal_data.get('template_id')
        
        if template_id:
            template = db.query(GoalTemplate).filter(
                GoalTemplate.id == template_id,
                GoalTemplate.is_active == True
            ).first()
            
            if template:
                # Parse checkpoint template
                if template.checkpoint_template:
                    try:
                        template_checkpoints = json.loads(template.checkpoint_template)
                        if not checkpoints_data:
                            checkpoints_data = template_checkpoints
                    except:
                        pass
                
                # Update template usage count
                template.usage_count += 1
        
        # Create goal
        goal = Goal(
            employee_id=goal_data['employee_id'],
            title=goal_data['title'],
            description=goal_data.get('description'),
            category_id=goal_data.get('category_id'),
            priority=goal_data.get('priority', 'medium'),
            start_date=goal_data['start_date'],
            target_date=goal_data['target_date'],
            is_personal=is_personal,
            template_id=template_id,
            assigned_by=assigned_by,
            status=GoalStatus.NOT_STARTED,
            progress_percentage=0.0
        )
        
        db.add(goal)
        db.flush()  # Get goal.id
        
        # Create checkpoints
        for idx, checkpoint_data in enumerate(checkpoints_data, start=1):
            checkpoint = GoalCheckpoint(
                goal_id=goal.id,
                title=checkpoint_data.get('title', checkpoint_data) if isinstance(checkpoint_data, dict) else checkpoint_data,
                description=checkpoint_data.get('description') if isinstance(checkpoint_data, dict) else None,
                sequence_number=idx,
                is_completed=False
            )
            db.add(checkpoint)
        
        # Create history entry
        GoalService._create_history_entry(
            db=db,
            goal_id=goal.id,
            user_id=current_user.id,
            action="created",
            field_name="goal",
            new_value=json.dumps({
                "title": goal.title,
                "employee_id": goal.employee_id,
                "is_personal": goal.is_personal
            })
        )
        
        db.commit()
        db.refresh(goal)
        
        # Send notification to employee (if not personal goal)
        if not is_personal:
            GoalService._create_notification(
                db=db,
                user_id=goal.employee_id,
                title="New Goal Assigned",
                message=f"Your manager has assigned you a new goal: {goal.title}",
                notification_type="goal_assigned",
                resource_type="goal",
                resource_id=goal.id
            )
        
        return GoalService.get_goal_by_id(db, goal.id, current_user)
    
    @staticmethod
    def get_goal_by_id(
        db: Session,
        goal_id: int,
        current_user: User
    ) -> Dict[str, Any]:
        """
        Get goal by ID with access control
        
        Args:
            db: Database session
            goal_id: Goal ID
            current_user: Current user
            
        Returns:
            Goal dictionary with all details
        """
        goal = db.query(Goal).options(
            joinedload(Goal.employee),
            joinedload(Goal.assigned_by_user),
            joinedload(Goal.category),
            joinedload(Goal.checkpoints)
        ).filter(
            Goal.id == goal_id,
            Goal.is_deleted == False
        ).first()
        
        if not goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Goal not found"
            )
        
        # Access control
        if current_user.role not in [UserRole.HR, UserRole.ADMIN]:
            if goal.employee_id != current_user.id and goal.assigned_by != current_user.id:
                # Check if user is manager of the employee
                if not (current_user.role == UserRole.MANAGER and goal.employee.manager_id == current_user.id):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="You don't have permission to view this goal"
                    )
        
        return GoalService._format_goal_response(goal)
    
    @staticmethod
    def update_goal(
        db: Session,
        goal_id: int,
        update_data: Dict[str, Any],
        current_user: User
    ) -> Dict[str, Any]:
        """
        Update goal
        
        Args:
            db: Database session
            goal_id: Goal ID
            update_data: Fields to update
            current_user: Current user
            
        Returns:
            Updated goal dictionary
        """
        goal = db.query(Goal).filter(
            Goal.id == goal_id,
            Goal.is_deleted == False
        ).first()
        
        if not goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Goal not found"
            )
        
        # Access control: Only assigned_by (manager) or employee can update
        can_update = False
        if current_user.role in [UserRole.HR, UserRole.ADMIN]:
            can_update = True
        elif goal.is_personal and goal.employee_id == current_user.id:
            can_update = True
        elif not goal.is_personal and goal.assigned_by == current_user.id:
            can_update = True
        
        if not can_update:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this goal"
            )
        
        # Track changes for history
        changes = []
        
        # Update fields
        allowed_fields = ['title', 'description', 'category_id', 'priority', 
                         'start_date', 'target_date', 'status']
        
        for field, value in update_data.items():
            if field in allowed_fields and value is not None:
                # Convert status enum from schema to model enum
                if field == 'status':
                    # Handle GoalStatusEnum from schema or string value
                    if hasattr(value, 'value'):
                        # It's an enum, get its value
                        status_value = value.value
                    else:
                        # It's a string
                        status_value = value
                    # Convert to model's GoalStatus enum
                    value = GoalStatus(status_value)
                
                old_value = getattr(goal, field)
                if old_value != value:
                    changes.append({
                        'field': field,
                        'old': str(old_value),
                        'new': str(value)
                    })
                    setattr(goal, field, value)
        
        # Auto-complete if status changed to completed
        if update_data.get('status') == GoalStatus.COMPLETED and goal.completion_date is None:
            goal.completion_date = date.today()
            goal.progress_percentage = 100.0
            changes.append({
                'field': 'completion_date',
                'old': None,
                'new': str(date.today())
            })
        
        goal.updated_at = datetime.utcnow()
        
        # Create history entries for changes
        for change in changes:
            GoalService._create_history_entry(
                db=db,
                goal_id=goal.id,
                user_id=current_user.id,
                action="updated",
                field_name=change['field'],
                old_value=change['old'],
                new_value=change['new']
            )
        
        db.commit()
        db.refresh(goal)
        
        # Notify if status changed
        if update_data.get('status') and goal.assigned_by and goal.assigned_by != current_user.id:
            GoalService._create_notification(
                db=db,
                user_id=goal.assigned_by,
                title="Goal Status Updated",
                message=f"Goal '{goal.title}' status changed to {goal.status.value}",
                notification_type="goal_status_changed",
                resource_type="goal",
                resource_id=goal.id
            )
        
        return GoalService.get_goal_by_id(db, goal.id, current_user)
    
    @staticmethod
    def delete_goal(
        db: Session,
        goal_id: int,
        current_user: User
    ) -> Dict[str, str]:
        """
        Soft delete goal
        
        Args:
            db: Database session
            goal_id: Goal ID
            current_user: Current user
            
        Returns:
            Success message
        """
        goal = db.query(Goal).filter(
            Goal.id == goal_id,
            Goal.is_deleted == False
        ).first()
        
        if not goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Goal not found"
            )
        
        # Access control: Only assigned_by (manager) can delete assigned goals
        # Employee can delete their personal goals
        can_delete = False
        if current_user.role in [UserRole.HR, UserRole.ADMIN]:
            can_delete = True
        elif goal.is_personal and goal.employee_id == current_user.id:
            can_delete = True
        elif not goal.is_personal and goal.assigned_by == current_user.id:
            can_delete = True
        
        if not can_delete:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this goal"
            )
        
        # Soft delete
        goal.is_deleted = True
        goal.updated_at = datetime.utcnow()
        
        # Create history entry
        GoalService._create_history_entry(
            db=db,
            goal_id=goal.id,
            user_id=current_user.id,
            action="deleted",
            field_name="is_deleted",
            old_value="False",
            new_value="True"
        )
        
        db.commit()
        
        return {"message": "Goal deleted successfully"}
    
    # ==================== Goal Listing & Filtering ====================
    
    @staticmethod
    def get_my_goals(
        db: Session,
        current_user: User,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category_id: Optional[int] = None,
        is_overdue: Optional[bool] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get goals for current user
        
        Args:
            db: Database session
            current_user: Current user
            skip: Pagination offset
            limit: Page size
            status: Filter by status
            priority: Filter by priority
            category_id: Filter by category
            is_overdue: Filter overdue goals
            
        Returns:
            Tuple of (goals list, total count)
        """
        query = db.query(Goal).filter(
            Goal.employee_id == current_user.id,
            Goal.is_deleted == False
        )
        
        # Apply filters
        if status:
            query = query.filter(Goal.status == status)
        if priority:
            query = query.filter(Goal.priority == priority)
        if category_id:
            query = query.filter(Goal.category_id == category_id)
        if is_overdue:
            today = date.today()
            query = query.filter(
                Goal.target_date < today,
                Goal.status != GoalStatus.COMPLETED
            )
        
        total = query.count()
        
        goals = query.options(
            joinedload(Goal.employee),
            joinedload(Goal.assigned_by_user),
            joinedload(Goal.category),
            joinedload(Goal.checkpoints)
        ).order_by(desc(Goal.created_at)).offset(skip).limit(limit).all()
        
        return [GoalService._format_goal_response(goal) for goal in goals], total
    
    @staticmethod
    def get_team_goals(
        db: Session,
        current_user: User,
        skip: int = 0,
        limit: int = 100,
        employee_id: Optional[int] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        is_overdue: Optional[bool] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get goals for team members (Manager only)
        
        Args:
            db: Database session
            current_user: Current user (must be manager)
            skip: Pagination offset
            limit: Page size
            employee_id: Filter by specific employee
            status: Filter by status
            priority: Filter by priority
            is_overdue: Filter overdue goals
            
        Returns:
            Tuple of (goals list, total count)
        """
        if current_user.role not in [UserRole.MANAGER, UserRole.HR, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only managers and HR can view team goals"
            )
        
        # Get team member IDs
        if current_user.role == UserRole.MANAGER:
            team_members = db.query(User.id).filter(
                User.manager_id == current_user.id,
                User.is_active == True
            ).all()
            team_member_ids = [member[0] for member in team_members]
            
            query = db.query(Goal).filter(
                Goal.employee_id.in_(team_member_ids),
                Goal.is_deleted == False
            )
        else:
            # HR/Admin can see all goals
            query = db.query(Goal).filter(Goal.is_deleted == False)
        
        # Apply filters
        if employee_id:
            query = query.filter(Goal.employee_id == employee_id)
        if status:
            query = query.filter(Goal.status == status)
        if priority:
            query = query.filter(Goal.priority == priority)
        if is_overdue:
            today = date.today()
            query = query.filter(
                Goal.target_date < today,
                Goal.status != GoalStatus.COMPLETED
            )
        
        total = query.count()
        
        goals = query.options(
            joinedload(Goal.employee),
            joinedload(Goal.assigned_by_user),
            joinedload(Goal.category),
            joinedload(Goal.checkpoints)
        ).order_by(desc(Goal.created_at)).offset(skip).limit(limit).all()
        
        return [GoalService._format_goal_response(goal) for goal in goals], total
    
    # ==================== Checkpoint Management ====================
    
    @staticmethod
    def create_checkpoint(
        db: Session,
        goal_id: int,
        checkpoint_data: Dict[str, Any],
        current_user: User
    ) -> Dict[str, Any]:
        """Create new checkpoint for a goal"""
        goal = db.query(Goal).filter(
            Goal.id == goal_id,
            Goal.is_deleted == False
        ).first()
        
        if not goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Goal not found"
            )
        
        # Access control
        if goal.employee_id != current_user.id and goal.assigned_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to modify this goal"
            )
        
        # Get next sequence number
        max_seq = db.query(func.max(GoalCheckpoint.sequence_number)).filter(
            GoalCheckpoint.goal_id == goal_id
        ).scalar() or 0
        
        checkpoint = GoalCheckpoint(
            goal_id=goal_id,
            title=checkpoint_data['title'],
            description=checkpoint_data.get('description'),
            sequence_number=checkpoint_data.get('sequence_number', max_seq + 1),
            is_completed=False
        )
        
        db.add(checkpoint)
        
        # Create history
        GoalService._create_history_entry(
            db=db,
            goal_id=goal_id,
            user_id=current_user.id,
            action="checkpoint_added",
            field_name="checkpoint",
            new_value=checkpoint_data['title']
        )
        
        db.commit()
        db.refresh(checkpoint)
        
        # Recalculate progress
        GoalService._recalculate_progress(db, goal_id)
        
        return GoalService._format_checkpoint_response(checkpoint)
    
    @staticmethod
    def update_checkpoint(
        db: Session,
        checkpoint_id: int,
        update_data: Dict[str, Any],
        current_user: User
    ) -> Dict[str, Any]:
        """Update checkpoint"""
        checkpoint = db.query(GoalCheckpoint).filter(
            GoalCheckpoint.id == checkpoint_id
        ).first()
        
        if not checkpoint:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Checkpoint not found"
            )
        
        goal = db.query(Goal).filter(Goal.id == checkpoint.goal_id).first()
        
        # Access control
        if goal.employee_id != current_user.id and goal.assigned_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to modify this checkpoint"
            )
        
        # Track changes
        was_completed = checkpoint.is_completed
        
        # Update fields
        if 'title' in update_data:
            checkpoint.title = update_data['title']
        if 'description' in update_data:
            checkpoint.description = update_data['description']
        if 'is_completed' in update_data:
            checkpoint.is_completed = update_data['is_completed']
            if update_data['is_completed'] and not was_completed:
                checkpoint.completed_date = datetime.utcnow()
                checkpoint.completed_by = current_user.id
                
                # Create history
                GoalService._create_history_entry(
                    db=db,
                    goal_id=goal.id,
                    user_id=current_user.id,
                    action="checkpoint_completed",
                    field_name="checkpoint",
                    new_value=checkpoint.title
                )
                
                # Notify manager if employee completed checkpoint
                if goal.assigned_by and current_user.id == goal.employee_id:
                    GoalService._create_notification(
                        db=db,
                        user_id=goal.assigned_by,
                        title="Checkpoint Completed",
                        message=f"{current_user.name} completed checkpoint '{checkpoint.title}' for goal '{goal.title}'",
                        notification_type="checkpoint_completed",
                        resource_type="goal",
                        resource_id=goal.id
                    )
            elif not update_data['is_completed'] and was_completed:
                checkpoint.completed_date = None
                checkpoint.completed_by = None
        
        checkpoint.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(checkpoint)
        
        # Recalculate progress
        GoalService._recalculate_progress(db, goal.id)
        
        return GoalService._format_checkpoint_response(checkpoint)
    
    @staticmethod
    def delete_checkpoint(
        db: Session,
        checkpoint_id: int,
        current_user: User
    ) -> Dict[str, str]:
        """Delete checkpoint"""
        checkpoint = db.query(GoalCheckpoint).filter(
            GoalCheckpoint.id == checkpoint_id
        ).first()
        
        if not checkpoint:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Checkpoint not found"
            )
        
        goal = db.query(Goal).filter(Goal.id == checkpoint.goal_id).first()
        
        # Access control
        if goal.employee_id != current_user.id and goal.assigned_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this checkpoint"
            )
        
        # Create history before deleting
        GoalService._create_history_entry(
            db=db,
            goal_id=goal.id,
            user_id=current_user.id,
            action="checkpoint_deleted",
            field_name="checkpoint",
            old_value=checkpoint.title
        )
        
        db.delete(checkpoint)
        db.commit()
        
        # Recalculate progress
        GoalService._recalculate_progress(db, goal.id)
        
        return {"message": "Checkpoint deleted successfully"}
    
    # ==================== Comment Management ====================
    
    @staticmethod
    def add_comment(
        db: Session,
        goal_id: int,
        comment_data: Dict[str, Any],
        current_user: User
    ) -> Dict[str, Any]:
        """Add comment to goal"""
        goal = db.query(Goal).filter(
            Goal.id == goal_id,
            Goal.is_deleted == False
        ).first()
        
        if not goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Goal not found"
            )
        
        # Access control
        if goal.employee_id != current_user.id and goal.assigned_by != current_user.id:
            if current_user.role not in [UserRole.HR, UserRole.ADMIN]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to comment on this goal"
                )
        
        comment = GoalComment(
            goal_id=goal_id,
            user_id=current_user.id,
            comment=comment_data['comment'],
            comment_type=comment_data.get('comment_type', 'update')
        )
        
        db.add(comment)
        db.commit()
        db.refresh(comment)
        
        # Notify the other party (employee notifies manager, manager notifies employee)
        notify_user_id = None
        if current_user.id == goal.employee_id and goal.assigned_by:
            notify_user_id = goal.assigned_by
        elif current_user.id == goal.assigned_by:
            notify_user_id = goal.employee_id
        
        if notify_user_id:
            GoalService._create_notification(
                db=db,
                user_id=notify_user_id,
                title="New Goal Comment",
                message=f"{current_user.name} commented on goal '{goal.title}'",
                notification_type="goal_comment",
                resource_type="goal",
                resource_id=goal.id
            )
        
        return GoalService._format_comment_response(db, comment)
    
    @staticmethod
    def get_goal_comments(
        db: Session,
        goal_id: int,
        current_user: User
    ) -> List[Dict[str, Any]]:
        """Get all comments for a goal"""
        goal = db.query(Goal).filter(Goal.id == goal_id).first()
        
        if not goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Goal not found"
            )
        
        # Access control
        if goal.employee_id != current_user.id and goal.assigned_by != current_user.id:
            if current_user.role not in [UserRole.HR, UserRole.ADMIN]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to view comments on this goal"
                )
        
        comments = db.query(GoalComment).filter(
            GoalComment.goal_id == goal_id,
            GoalComment.is_deleted == False
        ).order_by(desc(GoalComment.created_at)).all()
        
        return [GoalService._format_comment_response(db, comment) for comment in comments]
    
    # ==================== Goal Statistics ====================
    
    @staticmethod
    def get_my_goal_stats(
        db: Session,
        current_user: User
    ) -> Dict[str, Any]:
        """Get goal statistics for current user"""
        today = date.today()
        
        # Total goals
        total_goals = db.query(func.count(Goal.id)).filter(
            Goal.employee_id == current_user.id,
            Goal.is_deleted == False
        ).scalar() or 0
        
        # Active goals (not completed, not cancelled)
        active_goals = db.query(func.count(Goal.id)).filter(
            Goal.employee_id == current_user.id,
            Goal.is_deleted == False,
            Goal.status.in_([GoalStatus.NOT_STARTED, GoalStatus.IN_PROGRESS])
        ).scalar() or 0
        
        # Completed goals
        completed_goals = db.query(func.count(Goal.id)).filter(
            Goal.employee_id == current_user.id,
            Goal.is_deleted == False,
            Goal.status == GoalStatus.COMPLETED
        ).scalar() or 0
        
        # Overdue goals
        overdue_goals = db.query(func.count(Goal.id)).filter(
            Goal.employee_id == current_user.id,
            Goal.is_deleted == False,
            Goal.target_date < today,
            Goal.status != GoalStatus.COMPLETED
        ).scalar() or 0
        
        # Completion rate
        completion_rate = (completed_goals / total_goals * 100) if total_goals > 0 else 0.0
        
        # Average completion days
        avg_days = db.query(
            func.avg(
                func.julianday(Goal.completion_date) - func.julianday(Goal.start_date)
            )
        ).filter(
            Goal.employee_id == current_user.id,
            Goal.is_deleted == False,
            Goal.status == GoalStatus.COMPLETED,
            Goal.completion_date.isnot(None)
        ).scalar()
        
        # Goals by priority
        priority_stats = db.query(
            Goal.priority,
            func.count(Goal.id)
        ).filter(
            Goal.employee_id == current_user.id,
            Goal.is_deleted == False
        ).group_by(Goal.priority).all()
        
        goals_by_priority = {priority: count for priority, count in priority_stats}
        
        # Goals by category
        category_stats = db.query(
            GoalCategory.name,
            func.count(Goal.id)
        ).join(
            Goal, Goal.category_id == GoalCategory.id
        ).filter(
            Goal.employee_id == current_user.id,
            Goal.is_deleted == False
        ).group_by(GoalCategory.name).all()
        
        goals_by_category = {category: count for category, count in category_stats}
        
        # Goals by status
        status_stats = db.query(
            Goal.status,
            func.count(Goal.id)
        ).filter(
            Goal.employee_id == current_user.id,
            Goal.is_deleted == False
        ).group_by(Goal.status).all()
        
        goals_by_status = {str(status.value): count for status, count in status_stats}
        
        return {
            "total_goals": total_goals,
            "active_goals": active_goals,
            "completed_goals": completed_goals,
            "overdue_goals": overdue_goals,
            "completion_rate": round(completion_rate, 1),
            "average_completion_days": round(avg_days, 1) if avg_days else None,
            "goals_by_priority": goals_by_priority,
            "goals_by_category": goals_by_category,
            "goals_by_status": goals_by_status
        }
    
    @staticmethod
    def get_team_goal_stats(
        db: Session,
        current_user: User
    ) -> Dict[str, Any]:
        """Get team goal statistics (Manager only)"""
        if current_user.role not in [UserRole.MANAGER, UserRole.HR, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only managers and HR can view team statistics"
            )
        
        # Get team member IDs
        team_members = db.query(User).filter(
            User.manager_id == current_user.id,
            User.is_active == True
        ).all()
        team_member_ids = [member.id for member in team_members]
        
        today = date.today()
        
        # Total team goals
        total_team_goals = db.query(func.count(Goal.id)).filter(
            Goal.employee_id.in_(team_member_ids),
            Goal.is_deleted == False
        ).scalar() or 0
        
        # Completed team goals
        completed_team_goals = db.query(func.count(Goal.id)).filter(
            Goal.employee_id.in_(team_member_ids),
            Goal.is_deleted == False,
            Goal.status == GoalStatus.COMPLETED
        ).scalar() or 0
        
        # In progress team goals
        in_progress_team_goals = db.query(func.count(Goal.id)).filter(
            Goal.employee_id.in_(team_member_ids),
            Goal.is_deleted == False,
            Goal.status == GoalStatus.IN_PROGRESS
        ).scalar() or 0
        
        # Overdue team goals
        overdue_team_goals = db.query(func.count(Goal.id)).filter(
            Goal.employee_id.in_(team_member_ids),
            Goal.is_deleted == False,
            Goal.target_date < today,
            Goal.status != GoalStatus.COMPLETED
        ).scalar() or 0
        
        # Team completion rate
        team_completion_rate = (completed_team_goals / total_team_goals * 100) if total_team_goals > 0 else 0.0
        
        # Per-member statistics
        team_members_stats = []
        for member in team_members:
            member_total = db.query(func.count(Goal.id)).filter(
                Goal.employee_id == member.id,
                Goal.is_deleted == False
            ).scalar() or 0
            
            member_completed = db.query(func.count(Goal.id)).filter(
                Goal.employee_id == member.id,
                Goal.is_deleted == False,
                Goal.status == GoalStatus.COMPLETED
            ).scalar() or 0
            
            member_overdue = db.query(func.count(Goal.id)).filter(
                Goal.employee_id == member.id,
                Goal.is_deleted == False,
                Goal.target_date < today,
                Goal.status != GoalStatus.COMPLETED
            ).scalar() or 0
            
            team_members_stats.append({
                "employee_id": member.id,
                "employee_name": member.name,
                "total_goals": member_total,
                "completed_goals": member_completed,
                "overdue_goals": member_overdue,
                "completion_rate": round((member_completed / member_total * 100), 1) if member_total > 0 else 0.0
            })
        
        # Top performers (by completion rate)
        top_performers = sorted(
            [m for m in team_members_stats if m['total_goals'] > 0],
            key=lambda x: x['completion_rate'],
            reverse=True
        )[:5]
        
        # Needs attention (high overdue count or low completion rate)
        needs_attention = sorted(
            [m for m in team_members_stats if m['overdue_goals'] > 0],
            key=lambda x: x['overdue_goals'],
            reverse=True
        )[:5]
        
        return {
            "total_team_goals": total_team_goals,
            "completed_team_goals": completed_team_goals,
            "in_progress_team_goals": in_progress_team_goals,
            "overdue_team_goals": overdue_team_goals,
            "team_completion_rate": round(team_completion_rate, 1),
            "team_members_stats": team_members_stats,
            "top_performers": top_performers,
            "needs_attention": needs_attention
        }
    
    # ==================== Goal Categories ====================
    
    @staticmethod
    def create_category(
        db: Session,
        category_data: Dict[str, Any],
        current_user: User
    ) -> Dict[str, Any]:
        """Create goal category (Manager/HR only)"""
        if current_user.role not in [UserRole.MANAGER, UserRole.HR, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only managers and HR can create goal categories"
            )
        
        # Check if category already exists
        existing = db.query(GoalCategory).filter(
            GoalCategory.name == category_data['name']
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )
        
        category = GoalCategory(
            name=category_data['name'],
            description=category_data.get('description'),
            color_code=category_data.get('color_code'),
            icon=category_data.get('icon'),
            created_by=current_user.id
        )
        
        db.add(category)
        db.commit()
        db.refresh(category)
        
        return GoalService._format_category_response(db, category)
    
    @staticmethod
    def get_categories(
        db: Session,
        include_inactive: bool = False
    ) -> List[Dict[str, Any]]:
        """Get all goal categories"""
        query = db.query(GoalCategory)
        
        if not include_inactive:
            query = query.filter(GoalCategory.is_active == True)
        
        categories = query.order_by(GoalCategory.name).all()
        
        return [GoalService._format_category_response(db, cat) for cat in categories]
    
    @staticmethod
    def update_category(
        db: Session,
        category_id: int,
        update_data: Dict[str, Any],
        current_user: User
    ) -> Dict[str, Any]:
        """Update goal category"""
        if current_user.role not in [UserRole.MANAGER, UserRole.HR, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only managers and HR can update goal categories"
            )
        
        category = db.query(GoalCategory).filter(GoalCategory.id == category_id).first()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        # Update fields
        for field in ['name', 'description', 'color_code', 'icon', 'is_active']:
            if field in update_data and update_data[field] is not None:
                setattr(category, field, update_data[field])
        
        category.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(category)
        
        return GoalService._format_category_response(db, category)
    
    # ==================== Goal Templates ====================
    
    @staticmethod
    def create_template(
        db: Session,
        template_data: Dict[str, Any],
        current_user: User
    ) -> Dict[str, Any]:
        """Create goal template (Manager/HR only)"""
        if current_user.role not in [UserRole.MANAGER, UserRole.HR, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only managers and HR can create goal templates"
            )
        
        checkpoint_template = template_data.pop('checkpoint_template', [])
        
        template = GoalTemplate(
            name=template_data['name'],
            description=template_data.get('description'),
            category_id=template_data.get('category_id'),
            priority=template_data.get('priority', 'medium'),
            default_duration_days=template_data.get('default_duration_days'),
            checkpoint_template=json.dumps(checkpoint_template) if checkpoint_template else None,
            created_by=current_user.id
        )
        
        db.add(template)
        db.commit()
        db.refresh(template)
        
        return GoalService._format_template_response(template)
    
    @staticmethod
    def get_templates(
        db: Session,
        include_inactive: bool = False
    ) -> List[Dict[str, Any]]:
        """Get all goal templates"""
        query = db.query(GoalTemplate)
        
        if not include_inactive:
            query = query.filter(GoalTemplate.is_active == True)
        
        templates = query.order_by(desc(GoalTemplate.usage_count)).all()
        
        return [GoalService._format_template_response(template) for template in templates]
    
    # ==================== Helper Methods ====================
    
    @staticmethod
    def _recalculate_progress(db: Session, goal_id: int):
        """Recalculate goal progress based on checkpoint completion"""
        goal = db.query(Goal).filter(Goal.id == goal_id).first()
        
        if not goal:
            return
        
        checkpoints = db.query(GoalCheckpoint).filter(
            GoalCheckpoint.goal_id == goal_id
        ).all()
        
        if not checkpoints:
            return
        
        total_checkpoints = len(checkpoints)
        completed_checkpoints = sum(1 for c in checkpoints if c.is_completed)
        
        progress = (completed_checkpoints / total_checkpoints * 100) if total_checkpoints > 0 else 0.0
        goal.progress_percentage = round(progress, 1)
        
        # Auto-update status based on progress
        if progress == 0 and goal.status == GoalStatus.NOT_STARTED:
            pass
        elif 0 < progress < 100 and goal.status == GoalStatus.NOT_STARTED:
            goal.status = GoalStatus.IN_PROGRESS
        elif progress == 100:
            goal.status = GoalStatus.COMPLETED
            if not goal.completion_date:
                goal.completion_date = date.today()
        
        db.commit()
    
    @staticmethod
    def _format_goal_response(goal: Goal) -> Dict[str, Any]:
        """Format goal for response"""
        today = date.today()
        days_remaining = (goal.target_date - today).days if goal.target_date else None
        is_overdue = (goal.target_date < today and goal.status != GoalStatus.COMPLETED) if goal.target_date else False
        
        checkpoints = sorted(goal.checkpoints, key=lambda x: x.sequence_number)
        total_checkpoints = len(checkpoints)
        completed_checkpoints = sum(1 for c in checkpoints if c.is_completed)
        
        return {
            "id": goal.id,
            "title": goal.title,
            "description": goal.description,
            "category_id": goal.category_id,
            "category_name": goal.category.name if goal.category else None,
            "category_color": goal.category.color_code if goal.category else None,
            "priority": goal.priority,
            "start_date": goal.start_date,
            "target_date": goal.target_date,
            "completion_date": goal.completion_date,
            "status": goal.status.value if isinstance(goal.status, GoalStatus) else goal.status,
            "progress_percentage": goal.progress_percentage,
            "is_personal": goal.is_personal,
            "template_id": goal.template_id,
            "employee_id": goal.employee_id,
            "employee_name": goal.employee.name if goal.employee else None,
            "employee_email": goal.employee.email if goal.employee else None,
            "assigned_by": goal.assigned_by,
            "assigned_by_name": goal.assigned_by_user.name if goal.assigned_by_user else None,
            "checkpoints": [GoalService._format_checkpoint_response(c) for c in checkpoints],
            "total_checkpoints": total_checkpoints,
            "completed_checkpoints": completed_checkpoints,
            "days_remaining": days_remaining,
            "is_overdue": is_overdue,
            "is_deleted": goal.is_deleted,
            "created_at": goal.created_at,
            "updated_at": goal.updated_at
        }
    
    @staticmethod
    def _format_checkpoint_response(checkpoint: GoalCheckpoint) -> Dict[str, Any]:
        """Format checkpoint for response"""
        return {
            "id": checkpoint.id,
            "goal_id": checkpoint.goal_id,
            "title": checkpoint.title,
            "description": checkpoint.description,
            "sequence_number": checkpoint.sequence_number,
            "is_completed": checkpoint.is_completed,
            "completed_date": checkpoint.completed_date,
            "completed_by": checkpoint.completed_by,
            "created_at": checkpoint.created_at,
            "updated_at": checkpoint.updated_at
        }
    
    @staticmethod
    def _format_category_response(db: Session, category: GoalCategory) -> Dict[str, Any]:
        """Format category for response"""
        goal_count = db.query(func.count(Goal.id)).filter(
            Goal.category_id == category.id,
            Goal.is_deleted == False
        ).scalar() or 0
        
        return {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "color_code": category.color_code,
            "icon": category.icon,
            "is_active": category.is_active,
            "created_by": category.created_by,
            "created_at": category.created_at,
            "updated_at": category.updated_at,
            "goal_count": goal_count
        }
    
    @staticmethod
    def _format_template_response(template: GoalTemplate) -> Dict[str, Any]:
        """Format template for response"""
        checkpoint_template = []
        if template.checkpoint_template:
            try:
                checkpoint_template = json.loads(template.checkpoint_template)
            except:
                pass
        
        return {
            "id": template.id,
            "name": template.name,
            "description": template.description,
            "category_id": template.category_id,
            "priority": template.priority,
            "default_duration_days": template.default_duration_days,
            "checkpoint_template": checkpoint_template,
            "is_active": template.is_active,
            "created_by": template.created_by,
            "created_at": template.created_at,
            "updated_at": template.updated_at,
            "usage_count": template.usage_count
        }
    
    @staticmethod
    def _format_comment_response(db: Session, comment: GoalComment) -> Dict[str, Any]:
        """Format comment for response"""
        user = db.query(User).filter(User.id == comment.user_id).first()
        
        return {
            "id": comment.id,
            "goal_id": comment.goal_id,
            "user_id": comment.user_id,
            "user_name": user.name if user else None,
            "user_role": user.role.value if user and user.role else None,
            "comment": comment.comment,
            "comment_type": comment.comment_type,
            "attachment_path": comment.attachment_path,
            "created_at": comment.created_at,
            "updated_at": comment.updated_at,
            "is_deleted": comment.is_deleted
        }
    
    @staticmethod
    def _create_history_entry(
        db: Session,
        goal_id: int,
        user_id: int,
        action: str,
        field_name: Optional[str] = None,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None
    ):
        """Create history entry for audit trail"""
        history = GoalHistory(
            goal_id=goal_id,
            user_id=user_id,
            action=action,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value
        )
        db.add(history)
    
    @staticmethod
    def _create_notification(
        db: Session,
        user_id: int,
        title: str,
        message: str,
        notification_type: str,
        resource_type: str,
        resource_id: int
    ):
        """Create notification for user"""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            resource_type=resource_type,
            resource_id=resource_id,
            is_read=False
        )
        db.add(notification)
        db.commit()

