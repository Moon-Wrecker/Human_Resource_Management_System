"""
Profile API Routes
Endpoints for user profile management, documents, and team information
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Annotated

from database import get_db
from models import User, UserRole
from utils.dependencies import get_current_active_user, require_manager, require_hr_or_manager
from services.profile_service import ProfileService
from pydantic_models import (
    ProfileResponse,
    UpdateProfileRequest,
    DocumentUploadResponse,
    UserDocumentsResponse,
    ManagerInfoResponse,
    TeamResponse,
    ProfileStatsResponse,
    MessageResponse
)

router = APIRouter(prefix="/profile", tags=["Profile"])


# ==================== Profile Information Endpoints ====================

@router.get(
    "/me",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get My Profile",
    description="Get complete profile information for the currently authenticated user",
    responses={
        200: {
            "description": "Profile retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 3,
                        "name": "John Doe",
                        "email": "john.doe@company.com",
                        "phone": "+91 9876543210",
                        "employee_id": "EMP003",
                        "role": "employee",
                        "job_role": "Software Developer",
                        "department_name": "Engineering",
                        "team_name": "Backend Team",
                        "manager_name": "Michael Chen",
                        "casual_leave_balance": 8,
                        "sick_leave_balance": 10,
                        "annual_leave_balance": 12,
                        "wfh_balance": 20
                    }
                }
            }
        },
        401: {"description": "Not authenticated"}
    }
)
async def get_my_profile(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Get My Profile
    
    Retrieve complete profile information for the currently logged-in user including:
    - Basic information (name, email, phone, employee ID)
    - Job details (role, level, department, team)
    - Manager information
    - Leave balances
    - Uploaded documents (profile image, Aadhar, PAN)
    - Account metadata
    
    **Access:** All authenticated users
    
    **Use Case:** Display user profile page, account settings
    """
    profile = ProfileService.get_user_profile(db, current_user.id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return profile


@router.get(
    "/{user_id}",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get User Profile by ID",
    description="Get profile information for a specific user (HR/Manager only)",
    responses={
        200: {"description": "Profile retrieved successfully"},
        403: {"description": "Insufficient permissions"},
        404: {"description": "User not found"}
    }
)
async def get_user_profile(
    user_id: int,
    current_user: Annotated[User, Depends(require_hr_or_manager)],
    db: Session = Depends(get_db)
):
    """
    ## Get User Profile by ID
    
    Retrieve profile information for a specific user.
    
    **Access Control:**
    - HR can view any user's profile
    - Manager can view their team members' profiles
    
    **Use Case:** HR/Manager viewing employee details, team management
    """
    # Additional access control for managers
    if current_user.role == UserRole.MANAGER:
        target_user = db.query(User).filter(User.id == user_id).first()
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if target_user.manager_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view profiles of your team members"
            )
    
    profile = ProfileService.get_user_profile(db, user_id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return profile


@router.put(
    "/me",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Update My Profile",
    description="Update current user's profile information",
    responses={
        200: {"description": "Profile updated successfully"},
        400: {"description": "Invalid input data"},
        401: {"description": "Not authenticated"}
    }
)
async def update_my_profile(
    profile_data: UpdateProfileRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Update My Profile
    
    Update current user's profile information.
    
    **Editable Fields:**
    - name: Full name
    - phone: Phone number
    
    **Note:** Other fields like email, employee_id, role, department, etc. 
    can only be changed by HR through employee management.
    
    **Access:** All authenticated users
    
    **Use Case:** User updating their contact information
    """
    update_data = profile_data.model_dump(exclude_unset=True)
    
    updated_profile = ProfileService.update_user_profile(
        db, current_user.id, update_data
    )
    
    if not updated_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return updated_profile


# ==================== Document Management Endpoints ====================

@router.post(
    "/upload-image",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload Profile Image",
    description="Upload or update profile image",
    responses={
        201: {"description": "Profile image uploaded successfully"},
        400: {"description": "Invalid file type or size"},
        401: {"description": "Not authenticated"}
    }
)
async def upload_profile_image(
    file: UploadFile = File(..., description="Profile image file (JPG, PNG, GIF)"),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """
    ## Upload Profile Image
    
    Upload or update the user's profile image.
    
    **File Requirements:**
    - **Formats:** JPG, JPEG, PNG, GIF
    - **Max Size:** 10 MB
    
    **Note:** Uploading a new image will replace the existing one.
    
    **Access:** All authenticated users
    
    **Use Case:** User updating their profile picture
    """
    result = ProfileService.upload_profile_image(db, current_user.id, file)
    return result


@router.post(
    "/upload-document",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload Document",
    description="Upload identification documents (Aadhar, PAN)",
    responses={
        201: {"description": "Document uploaded successfully"},
        400: {"description": "Invalid file type or document type"},
        401: {"description": "Not authenticated"}
    }
)
async def upload_document(
    document_type: str = Form(..., description="Document type: 'aadhar' or 'pan'"),
    file: UploadFile = File(..., description="Document file (PDF, DOC, DOCX)"),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """
    ## Upload Document
    
    Upload identification documents like Aadhar card or PAN card.
    
    **Document Types:**
    - `aadhar`: Aadhar card
    - `pan`: PAN card
    
    **File Requirements:**
    - **Formats:** PDF, DOC, DOCX
    - **Max Size:** 10 MB
    
    **Note:** Uploading a new document will replace the existing one.
    
    **Access:** All authenticated users
    
    **Use Case:** Employee document submission for HR records
    """
    result = ProfileService.upload_document(
        db, current_user.id, document_type, file
    )
    return result


@router.get(
    "/documents",
    response_model=UserDocumentsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get My Documents",
    description="Get all uploaded documents for current user",
    responses={
        200: {"description": "Documents retrieved successfully"},
        401: {"description": "Not authenticated"}
    }
)
async def get_my_documents(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Get My Documents
    
    Retrieve all uploaded documents for the current user including:
    - Profile image
    - Aadhar card
    - PAN card
    
    **Access:** All authenticated users
    
    **Use Case:** Display uploaded documents on profile page
    """
    documents = ProfileService.get_user_documents(db, current_user.id)
    return documents


@router.delete(
    "/documents/{document_type}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete Document",
    description="Delete a specific document",
    responses={
        200: {"description": "Document deleted successfully"},
        400: {"description": "Invalid document type"},
        404: {"description": "Document not found"},
        401: {"description": "Not authenticated"}
    }
)
async def delete_document(
    document_type: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Delete Document
    
    Delete a specific document from the user's profile.
    
    **Document Types:**
    - `profile_image`: Profile image
    - `aadhar`: Aadhar card
    - `pan`: PAN card
    
    **Access:** All authenticated users
    
    **Use Case:** User removing an outdated or incorrect document
    """
    result = ProfileService.delete_document(db, current_user.id, document_type)
    return result


# ==================== Team & Manager Endpoints ====================

@router.get(
    "/manager",
    response_model=ManagerInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Get My Manager",
    description="Get information about current user's manager",
    responses={
        200: {"description": "Manager information retrieved"},
        404: {"description": "Manager not assigned"},
        401: {"description": "Not authenticated"}
    }
)
async def get_my_manager(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Get My Manager
    
    Retrieve information about the current user's manager including:
    - Name, email, phone
    - Employee ID
    - Job role and department
    - Profile image
    
    **Access:** All authenticated users
    
    **Use Case:** Display manager contact information, org hierarchy
    """
    manager = ProfileService.get_manager_info(db, current_user.id)
    
    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manager not assigned"
        )
    
    return manager


@router.get(
    "/team",
    response_model=TeamResponse,
    status_code=status.HTTP_200_OK,
    summary="Get My Team",
    description="Get team members for current user (for managers)",
    responses={
        200: {"description": "Team information retrieved"},
        401: {"description": "Not authenticated"}
    }
)
async def get_my_team(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Get My Team
    
    Get list of team members who report to the current user.
    
    **Returns:**
    - Team information (team name, department)
    - List of team members with basic details
    - Total member count
    
    **Access:** All authenticated users (useful for managers)
    
    **Use Case:** Display team roster, team management
    """
    team = ProfileService.get_team_members(db, current_user.id)
    return team


@router.get(
    "/team/{manager_id}",
    response_model=TeamResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Team by Manager ID",
    description="Get team members for a specific manager (HR only)",
    responses={
        200: {"description": "Team information retrieved"},
        403: {"description": "Insufficient permissions"},
        404: {"description": "Manager not found"}
    }
)
async def get_team_by_manager(
    manager_id: int,
    current_user: Annotated[User, Depends(require_hr_or_manager)],
    db: Session = Depends(get_db)
):
    """
    ## Get Team by Manager ID
    
    Get team members for a specific manager.
    
    **Access:** HR and Managers only
    
    **Use Case:** HR viewing team structures, cross-team collaboration
    """
    team = ProfileService.get_team_members(db, manager_id)
    return team


# ==================== Statistics & Analytics Endpoints ====================

@router.get(
    "/stats",
    response_model=ProfileStatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get My Profile Statistics",
    description="Get statistics and analytics for current user",
    responses={
        200: {"description": "Statistics retrieved successfully"},
        401: {"description": "Not authenticated"}
    }
)
async def get_my_profile_stats(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Get My Profile Statistics
    
    Get comprehensive statistics and analytics for the current user including:
    - Goals (total, completed, in progress)
    - Skill modules (total, completed)
    - Training hours
    - Attendance percentage
    - Leaves taken this year
    
    **Access:** All authenticated users
    
    **Use Case:** Display performance metrics on profile/dashboard
    """
    stats = ProfileService.get_profile_stats(db, current_user.id)
    return stats


@router.get(
    "/stats/{user_id}",
    response_model=ProfileStatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get User Profile Statistics",
    description="Get statistics for a specific user (HR/Manager only)",
    responses={
        200: {"description": "Statistics retrieved successfully"},
        403: {"description": "Insufficient permissions"},
        404: {"description": "User not found"}
    }
)
async def get_user_profile_stats(
    user_id: int,
    current_user: Annotated[User, Depends(require_hr_or_manager)],
    db: Session = Depends(get_db)
):
    """
    ## Get User Profile Statistics
    
    Get statistics and analytics for a specific user.
    
    **Access Control:**
    - HR can view any user's statistics
    - Manager can view their team members' statistics
    
    **Use Case:** Performance reviews, team analytics
    """
    # Additional access control for managers
    if current_user.role == UserRole.MANAGER:
        target_user = db.query(User).filter(User.id == user_id).first()
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if target_user.manager_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view statistics of your team members"
            )
    
    stats = ProfileService.get_profile_stats(db, user_id)
    return stats

