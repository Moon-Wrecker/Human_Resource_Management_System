"""
Announcements routes - API endpoints for announcements management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from database import get_db
from models import User
from utils.dependencies import get_current_active_user, require_hr_or_manager
from services.announcement_service import AnnouncementService
from schemas.announcement_schemas import (
    AnnouncementCreate,
    AnnouncementUpdate,
    AnnouncementResponse,
    AnnouncementListResponse,
    MessageResponse
)

router = APIRouter(prefix="/announcements", tags=["Announcements"])


@router.get(
    "",
    response_model=AnnouncementListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get All Announcements",
    description="Get all active announcements (accessible to all authenticated users)",
    responses={
        200: {
            "description": "List of announcements retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "announcements": [
                            {
                                "id": 1,
                                "title": "Office Closed for Diwali",
                                "message": "All branches will remain closed from November 14–16",
                                "link": "https://intranet.company.com/holiday-calendar",
                                "is_urgent": False,
                                "created_by": 1,
                                "created_by_name": "Sarah Johnson",
                                "created_at": "2025-11-02T10:00:00",
                                "published_date": "2025-11-02T10:00:00",
                                "is_active": True,
                                "is_expired": False
                            }
                        ],
                        "total": 10,
                        "active": 8,
                        "urgent": 2
                    }
                }
            }
        },
        401: {"description": "Not authenticated"}
    }
)
async def get_announcements(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
    include_expired: bool = Query(False, description="Include expired announcements"),
    include_inactive: bool = Query(False, description="Include inactive announcements (HR only)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return")
):
    """
    ## Get All Announcements
    
    Get all announcements visible to the current user.
    
    **Requires**: Valid access token in Authorization header
    
    ### Query Parameters:
    - **include_expired**: Include expired announcements (default: false)
    - **include_inactive**: Include inactive announcements (default: false, HR only)
    - **skip**: Pagination offset (default: 0)
    - **limit**: Maximum results (default: 100, max: 500)
    
    ### Response:
    - **announcements**: List of announcement objects
    - **total**: Total number of announcements
    - **active**: Number of active announcements
    - **urgent**: Number of urgent announcements
    
    ### Notes:
    - Announcements are ordered by urgency, then by publish date (newest first)
    - Non-expired and active announcements shown by default
    - HR/Admin can see inactive announcements if requested
    """
    # Get announcements
    announcements, total, active, urgent = AnnouncementService.get_announcements(
        db=db,
        current_user=current_user,
        include_expired=include_expired,
        include_inactive=include_inactive,
        skip=skip,
        limit=limit
    )
    
    # Format responses
    formatted_announcements = [
        AnnouncementService.format_announcement_response(announcement, db)
        for announcement in announcements
    ]
    
    return AnnouncementListResponse(
        announcements=formatted_announcements,
        total=total,
        active=active,
        urgent=urgent
    )


@router.get(
    "/{announcement_id}",
    response_model=AnnouncementResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Announcement by ID",
    description="Get a specific announcement by its ID",
    responses={
        200: {"description": "Announcement retrieved successfully"},
        404: {"description": "Announcement not found"},
        401: {"description": "Not authenticated"}
    }
)
async def get_announcement(
    announcement_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Get Announcement by ID
    
    Get detailed information about a specific announcement.
    
    **Requires**: Valid access token in Authorization header
    
    ### Path Parameters:
    - **announcement_id**: ID of the announcement to retrieve
    
    ### Response:
    Returns the announcement object with all details.
    """
    announcement = AnnouncementService.get_announcement_by_id(db, announcement_id)
    
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )
    
    return AnnouncementService.format_announcement_response(announcement, db)


@router.post(
    "",
    response_model=AnnouncementResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Announcement (HR/Manager Only)",
    description="Create a new announcement (requires HR or Manager role)",
    responses={
        201: {"description": "Announcement created successfully"},
        400: {"description": "Invalid input data"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions (not HR or Manager)"}
    }
)
async def create_announcement(
    announcement_data: AnnouncementCreate,
    current_user: Annotated[User, Depends(require_hr_or_manager)],
    db: Session = Depends(get_db)
):
    """
    ## Create Announcement
    
    Create a new announcement. Only HR or Manager can create announcements.
    
    **Requires**:
    - Valid access token in Authorization header
    - User role must be HR or MANAGER
    
    ### Request Body:
    - **title**: Announcement title (required, max 200 chars)
    - **message**: Announcement message/description (required)
    - **link**: Optional link for more details (max 500 chars)
    - **target_departments**: Optional comma-separated department IDs
    - **target_roles**: Optional comma-separated roles to target
    - **is_urgent**: Mark as urgent (default: false)
    - **expiry_date**: Optional expiry date (ISO format)
    
    ### Response:
    Returns the created announcement object.
    
    ### Notes:
    - Announcement is active and published immediately
    - All users can see it unless specific targets are set
    - Urgent announcements appear first in the list
    """
    # Create announcement
    announcement = AnnouncementService.create_announcement(
        db=db,
        announcement_data=announcement_data,
        created_by_user=current_user
    )
    
    return AnnouncementService.format_announcement_response(announcement, db)


@router.put(
    "/{announcement_id}",
    response_model=AnnouncementResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Announcement (HR/Manager Only)",
    description="Update an existing announcement (requires HR or Manager role)",
    responses={
        200: {"description": "Announcement updated successfully"},
        404: {"description": "Announcement not found"},
        400: {"description": "Invalid input data"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions (not HR or Manager)"}
    }
)
async def update_announcement(
    announcement_id: int,
    update_data: AnnouncementUpdate,
    current_user: Annotated[User, Depends(require_hr_or_manager)],
    db: Session = Depends(get_db)
):
    """
    ## Update Announcement
    
    Update an existing announcement. Only HR or Manager can update announcements.
    
    **Requires**:
    - Valid access token in Authorization header
    - User role must be HR or MANAGER
    
    ### Path Parameters:
    - **announcement_id**: ID of the announcement to update
    
    ### Request Body:
    All fields are optional. Only provided fields will be updated:
    - **title**: Updated title
    - **message**: Updated message
    - **link**: Updated link
    - **target_departments**: Updated target departments
    - **target_roles**: Updated target roles
    - **is_urgent**: Updated urgency flag
    - **expiry_date**: Updated expiry date
    - **is_active**: Updated active status
    
    ### Response:
    Returns the updated announcement object.
    """
    # Update announcement
    announcement = AnnouncementService.update_announcement(
        db=db,
        announcement_id=announcement_id,
        update_data=update_data
    )
    
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )
    
    return AnnouncementService.format_announcement_response(announcement, db)


@router.delete(
    "/{announcement_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete Announcement (HR/Manager Only)",
    description="Delete an announcement (soft delete by default)",
    responses={
        200: {"description": "Announcement deleted successfully"},
        404: {"description": "Announcement not found"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions (not HR or Manager)"}
    }
)
async def delete_announcement(
    announcement_id: int,
    current_user: Annotated[User, Depends(require_hr_or_manager)],
    db: Session = Depends(get_db),
    hard_delete: bool = Query(False, description="Permanently delete (default: soft delete)")
):
    """
    ## Delete Announcement
    
    Delete an announcement. Only HR or Manager can delete announcements.
    By default, performs a soft delete (sets is_active to false).
    
    **Requires**:
    - Valid access token in Authorization header
    - User role must be HR or MANAGER
    
    ### Path Parameters:
    - **announcement_id**: ID of the announcement to delete
    
    ### Query Parameters:
    - **hard_delete**: If true, permanently delete; if false, soft delete (default: false)
    
    ### Response:
    Returns success message.
    
    ### Notes:
    - Soft delete: Sets is_active to false (recommended, keeps audit trail)
    - Hard delete: Permanently removes from database (use with caution)
    """
    # Delete announcement
    success = AnnouncementService.delete_announcement(
        db=db,
        announcement_id=announcement_id,
        soft_delete=not hard_delete
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )
    
    delete_type = "permanently deleted" if hard_delete else "deactivated"
    return MessageResponse(
        message=f"Announcement {delete_type} successfully"
    )


@router.get(
    "/stats/summary",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Get Announcement Statistics (HR/Manager Only)",
    description="Get statistics about announcements",
    responses={
        200: {"description": "Statistics retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions (not HR or Manager)"}
    }
)
async def get_announcement_stats(
    current_user: Annotated[User, Depends(require_hr_or_manager)],
    db: Session = Depends(get_db)
):
    """
    ## Get Announcement Statistics
    
    Get statistics about announcements in the system.
    Only HR or Manager can access this endpoint.
    
    **Requires**:
    - Valid access token in Authorization header
    - User role must be HR or MANAGER
    
    ### Response:
    Returns statistics including:
    - **total**: Total number of announcements
    - **active**: Number of active announcements
    - **urgent**: Number of urgent announcements
    - **expired**: Number of expired announcements
    - **inactive**: Number of inactive announcements
    """
    stats = AnnouncementService.get_stats(db)
    return stats

