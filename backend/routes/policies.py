"""
Policies routes - API endpoints for policies management with file upload/download
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from datetime import date
from database import get_db
from models import User
from utils.dependencies import get_current_active_user, require_hr_or_manager
from services.policy_service import PolicyService
from schemas.policy_schemas import (
    PolicyCreate,
    PolicyUpdate,
    PolicyResponse,
    PolicyListResponse,
    PolicyAcknowledgmentResponse,
    PolicyAcknowledgmentListResponse,
    PolicyUploadResponse,
    MessageResponse
)
import os

router = APIRouter(prefix="/policies", tags=["Policies"])


@router.get(
    "",
    response_model=PolicyListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get All Policies",
    description="Get all active policies (accessible to all authenticated users)",
    responses={
        200: {"description": "List of policies retrieved successfully"},
        401: {"description": "Not authenticated"}
    }
)
async def get_policies(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
    include_inactive: bool = Query(False, description="Include inactive policies (HR only)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return")
):
    """
    ## Get All Policies
    
    Get all policies visible to the current user.
    
    **Requires**: Valid access token in Authorization header
    
    ### Query Parameters:
    - **include_inactive**: Include inactive policies (default: false, HR only)
    - **category**: Filter by category (HR, IT, Finance, etc.)
    - **skip**: Pagination offset (default: 0)
    - **limit**: Maximum results (default: 100, max: 500)
    
    ### Response:
    - **policies**: List of policy objects
    - **total**: Total number of policies
    - **active**: Number of active policies
    
    ### Notes:
    - Policies are ordered by effective date (newest first)
    - Each policy includes document status and acknowledgment info
    """
    # Get policies
    policies, total, active = PolicyService.get_policies(
        db=db,
        current_user=current_user,
        include_inactive=include_inactive,
        category=category,
        skip=skip,
        limit=limit
    )
    
    # Format responses
    formatted_policies = [
        PolicyService.format_policy_response(policy, db, current_user)
        for policy in policies
    ]
    
    return PolicyListResponse(
        policies=formatted_policies,
        total=total,
        active=active
    )


@router.get(
    "/{policy_id}",
    response_model=PolicyResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Policy by ID",
    description="Get a specific policy by its ID",
    responses={
        200: {"description": "Policy retrieved successfully"},
        404: {"description": "Policy not found"},
        401: {"description": "Not authenticated"}
    }
)
async def get_policy(
    policy_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Get Policy by ID
    
    Get detailed information about a specific policy.
    
    **Requires**: Valid access token in Authorization header
    
    ### Path Parameters:
    - **policy_id**: ID of the policy to retrieve
    
    ### Response:
    Returns the policy object with all details including document status.
    """
    policy = PolicyService.get_policy_by_id(db, policy_id)
    
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    return PolicyService.format_policy_response(policy, db, current_user)


@router.post(
    "",
    response_model=PolicyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Policy (HR Only)",
    description="Create a new policy (requires HR role)",
    responses={
        201: {"description": "Policy created successfully"},
        400: {"description": "Invalid input data"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions (not HR)"}
    }
)
async def create_policy(
    policy_data: PolicyCreate,
    current_user: Annotated[User, Depends(require_hr_or_manager)],
    db: Session = Depends(get_db)
):
    """
    ## Create Policy
    
    Create a new policy. Only HR can create policies.
    Document can be uploaded separately using the upload endpoint.
    
    **Requires**:
    - Valid access token in Authorization header
    - User role must be HR or MANAGER
    
    ### Request Body:
    - **title**: Policy title (required, max 200 chars)
    - **description**: Policy description (optional)
    - **content**: Policy content/text (required)
    - **category**: Policy category (optional, e.g., HR, IT, Finance)
    - **version**: Policy version (default: "1.0")
    - **effective_date**: Policy effective date (required, ISO format)
    - **review_date**: Policy review date (optional, ISO format)
    - **require_acknowledgment**: Require employee acknowledgment (default: false)
    
    ### Response:
    Returns the created policy object.
    
    ### Notes:
    - After creating the policy, upload the PDF document using POST /{policy_id}/upload
    - Version increments automatically when policy is updated
    """
    # Create policy
    policy = PolicyService.create_policy(
        db=db,
        policy_data=policy_data,
        created_by_user=current_user
    )
    
    return PolicyService.format_policy_response(policy, db, current_user)


@router.post(
    "/{policy_id}/upload",
    response_model=PolicyUploadResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload Policy Document (HR Only)",
    description="Upload PDF document for a policy",
    responses={
        200: {"description": "Document uploaded successfully"},
        400: {"description": "Invalid file type or size"},
        404: {"description": "Policy not found"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions (not HR)"}
    }
)
async def upload_policy_document(
    policy_id: int,
    file: UploadFile = File(..., description="PDF document to upload"),
    current_user: Annotated[User, Depends(require_hr_or_manager)] = None,
    db: Session = Depends(get_db)
):
    """
    ## Upload Policy Document
    
    Upload a PDF document for a policy. Only HR can upload.
    
    **Requires**:
    - Valid access token in Authorization header
    - User role must be HR or MANAGER
    
    ### Path Parameters:
    - **policy_id**: ID of the policy to upload document for
    
    ### Form Data:
    - **file**: PDF file (multipart/form-data)
    
    ### Response:
    Returns upload confirmation with file details.
    
    ### Notes:
    - Only PDF files are allowed
    - Maximum file size: 10MB (configurable)
    - Replaces existing document if present
    - File is stored in uploads/policies/
    """
    # Upload document
    policy, result, file_size = await PolicyService.upload_policy_document(
        db=db,
        policy_id=policy_id,
        file=file
    )
    
    if not policy:
        # result contains error message
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST if "not found" not in result else status.HTTP_404_NOT_FOUND,
            detail=result
        )
    
    return PolicyUploadResponse(
        policy_id=policy.id,
        file_name=file.filename,
        file_path=result,
        file_size=file_size,
        message="Policy document uploaded successfully"
    )


@router.get(
    "/{policy_id}/download",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
    summary="Download Policy Document",
    description="Download the PDF document for a policy",
    responses={
        200: {"description": "Document downloaded successfully"},
        404: {"description": "Policy or document not found"},
        401: {"description": "Not authenticated"}
    }
)
async def download_policy_document(
    policy_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Download Policy Document
    
    Download the PDF document associated with a policy.
    
    **Requires**: Valid access token in Authorization header
    
    ### Path Parameters:
    - **policy_id**: ID of the policy to download document for
    
    ### Response:
    Returns the PDF file for download.
    
    ### Notes:
    - File is returned as application/pdf
    - Filename is preserved from original upload
    - Returns 404 if policy has no document attached
    """
    # Get document path
    file_path = PolicyService.get_policy_document_path(db, policy_id)
    
    if not file_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy document not found"
        )
    
    # Get original filename
    filename = os.path.basename(file_path)
    
    # Return file
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=filename
    )


@router.put(
    "/{policy_id}",
    response_model=PolicyResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Policy (HR Only)",
    description="Update an existing policy (requires HR role)",
    responses={
        200: {"description": "Policy updated successfully"},
        404: {"description": "Policy not found"},
        400: {"description": "Invalid input data"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions (not HR)"}
    }
)
async def update_policy(
    policy_id: int,
    update_data: PolicyUpdate,
    current_user: Annotated[User, Depends(require_hr_or_manager)],
    db: Session = Depends(get_db)
):
    """
    ## Update Policy
    
    Update an existing policy. Only HR can update policies.
    
    **Requires**:
    - Valid access token in Authorization header
    - User role must be HR or MANAGER
    
    ### Path Parameters:
    - **policy_id**: ID of the policy to update
    
    ### Request Body:
    All fields are optional. Only provided fields will be updated:
    - **title**: Updated title
    - **description**: Updated description
    - **content**: Updated content
    - **category**: Updated category
    - **version**: Updated version
    - **effective_date**: Updated effective date
    - **review_date**: Updated review date
    - **is_active**: Updated active status
    
    ### Response:
    Returns the updated policy object.
    
    ### Notes:
    - When content is updated, consider incrementing the version
    - Updating resets all acknowledgments (users must re-acknowledge)
    - To update the PDF document, use PUT /{policy_id}/upload
    """
    # Update policy
    policy = PolicyService.update_policy(
        db=db,
        policy_id=policy_id,
        update_data=update_data
    )
    
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    return PolicyService.format_policy_response(policy, db, current_user)


@router.delete(
    "/{policy_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete Policy (HR Only)",
    description="Delete a policy (soft delete by default)",
    responses={
        200: {"description": "Policy deleted successfully"},
        404: {"description": "Policy not found"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions (not HR)"}
    }
)
async def delete_policy(
    policy_id: int,
    current_user: Annotated[User, Depends(require_hr_or_manager)],
    db: Session = Depends(get_db),
    hard_delete: bool = Query(False, description="Permanently delete (default: soft delete)")
):
    """
    ## Delete Policy
    
    Delete a policy. Only HR can delete policies.
    By default, performs a soft delete (sets is_active to false).
    
    **Requires**:
    - Valid access token in Authorization header
    - User role must be HR or MANAGER
    
    ### Path Parameters:
    - **policy_id**: ID of the policy to delete
    
    ### Query Parameters:
    - **hard_delete**: If true, permanently delete; if false, soft delete (default: false)
    
    ### Response:
    Returns success message.
    
    ### Notes:
    - Soft delete: Sets is_active to false (recommended, keeps audit trail)
    - Hard delete: Permanently removes from database AND deletes PDF file
    - Hard delete also removes all acknowledgment records
    """
    # Delete policy
    success = PolicyService.delete_policy(
        db=db,
        policy_id=policy_id,
        soft_delete=not hard_delete
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    delete_type = "permanently deleted" if hard_delete else "deactivated"
    return MessageResponse(
        message=f"Policy {delete_type} successfully"
    )


@router.post(
    "/{policy_id}/acknowledge",
    response_model=PolicyAcknowledgmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Acknowledge Policy",
    description="Acknowledge that you have read and understood a policy",
    responses={
        201: {"description": "Policy acknowledged successfully"},
        404: {"description": "Policy not found"},
        401: {"description": "Not authenticated"}
    }
)
async def acknowledge_policy(
    policy_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    ## Acknowledge Policy
    
    Acknowledge that you have read and understood a policy.
    
    **Requires**: Valid access token in Authorization header
    
    ### Path Parameters:
    - **policy_id**: ID of the policy to acknowledge
    
    ### Response:
    Returns acknowledgment record.
    
    ### Notes:
    - Can only acknowledge once per policy
    - If already acknowledged, returns existing acknowledgment
    - Acknowledgment is tracked with timestamp
    - HR can see who has acknowledged via /policies/{id}/acknowledgments
    """
    # Acknowledge policy
    acknowledgment = PolicyService.acknowledge_policy(
        db=db,
        policy_id=policy_id,
        user=current_user
    )
    
    if not acknowledgment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    # Get policy and user details for response
    policy = PolicyService.get_policy_by_id(db, policy_id)
    
    return PolicyAcknowledgmentResponse(
        id=acknowledgment.id,
        policy_id=acknowledgment.policy_id,
        user_id=acknowledgment.user_id,
        acknowledged_date=acknowledgment.acknowledged_date,
        policy_title=policy.title if policy else None,
        user_name=current_user.name
    )


@router.get(
    "/{policy_id}/acknowledgments",
    response_model=PolicyAcknowledgmentListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Policy Acknowledgments (HR Only)",
    description="Get all users who have acknowledged a policy",
    responses={
        200: {"description": "Acknowledgments retrieved successfully"},
        404: {"description": "Policy not found"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions (not HR)"}
    }
)
async def get_policy_acknowledgments(
    policy_id: int,
    current_user: Annotated[User, Depends(require_hr_or_manager)],
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(100, ge=1, le=500, description="Maximum results")
):
    """
    ## Get Policy Acknowledgments
    
    Get all users who have acknowledged a specific policy.
    Only HR or Manager can access this endpoint.
    
    **Requires**:
    - Valid access token in Authorization header
    - User role must be HR or MANAGER
    
    ### Path Parameters:
    - **policy_id**: ID of the policy
    
    ### Query Parameters:
    - **skip**: Pagination offset
    - **limit**: Maximum results
    
    ### Response:
    Returns list of acknowledgments with user details.
    """
    # Check if policy exists
    policy = PolicyService.get_policy_by_id(db, policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    # Get acknowledgments
    acknowledgments, total = PolicyService.get_policy_acknowledgments(
        db=db,
        policy_id=policy_id,
        skip=skip,
        limit=limit
    )
    
    # Format responses
    formatted_acknowledgments = []
    for ack in acknowledgments:
        user = db.query(User).filter(User.id == ack.user_id).first()
        formatted_acknowledgments.append(PolicyAcknowledgmentResponse(
            id=ack.id,
            policy_id=ack.policy_id,
            user_id=ack.user_id,
            acknowledged_date=ack.acknowledged_date,
            policy_title=policy.title,
            user_name=user.name if user else "Unknown"
        ))
    
    return PolicyAcknowledgmentListResponse(
        acknowledgments=formatted_acknowledgments,
        total=total
    )


@router.get(
    "/stats/summary",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Get Policy Statistics (HR Only)",
    description="Get statistics about policies",
    responses={
        200: {"description": "Statistics retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions (not HR)"}
    }
)
async def get_policy_stats(
    current_user: Annotated[User, Depends(require_hr_or_manager)],
    db: Session = Depends(get_db)
):
    """
    ## Get Policy Statistics
    
    Get statistics about policies in the system.
    Only HR or Manager can access this endpoint.
    
    **Requires**:
    - Valid access token in Authorization header
    - User role must be HR or MANAGER
    
    ### Response:
    Returns statistics including:
    - **total**: Total number of policies
    - **active**: Number of active policies
    - **inactive**: Number of inactive policies
    - **with_documents**: Policies with PDF documents
    - **total_acknowledgments**: Total policy acknowledgments
    - **categories**: Breakdown by category
    """
    stats = PolicyService.get_stats(db)
    return stats

