"""
Policy service - Business logic for policy operations
"""
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime
from fastapi import UploadFile
import os
import uuid
from models import Policy, PolicyAcknowledgment, User, UserRole
from schemas.policy_schemas import PolicyCreate, PolicyUpdate, PolicyResponse
from config import settings


class PolicyService:
    """Policy service class"""
    
    @staticmethod
    def create_policy(
        db: Session,
        policy_data: PolicyCreate,
        created_by_user: User
    ) -> Policy:
        """
        Create a new policy
        
        Args:
            db: Database session
            policy_data: Policy data from request
            created_by_user: User creating the policy
            
        Returns:
            Policy: Created policy object
        """
        # Create policy
        new_policy = Policy(
            title=policy_data.title,
            description=policy_data.description,
            content=policy_data.content,
            category=policy_data.category,
            version=policy_data.version,
            effective_date=policy_data.effective_date,
            review_date=policy_data.review_date,
            created_by=created_by_user.id,
            created_at=datetime.utcnow(),
            is_active=True
        )
        
        db.add(new_policy)
        db.commit()
        db.refresh(new_policy)
        
        return new_policy
    
    @staticmethod
    def get_policies(
        db: Session,
        current_user: User,
        include_inactive: bool = False,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Policy], int, int]:
        """
        Get all policies
        
        Args:
            db: Database session
            current_user: Current user
            include_inactive: Include inactive policies
            category: Filter by category
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (policies, total_count, active_count)
        """
        # Build query
        query = db.query(Policy)
        
        # Filter by active status (unless including inactive)
        if not include_inactive:
            query = query.filter(Policy.is_active == True)
        
        # Filter by category
        if category:
            query = query.filter(Policy.category == category)
        
        # Order by effective date (newest first)
        query = query.order_by(Policy.effective_date.desc())
        
        # Get total count
        total_count = query.count()
        
        # Get active count
        active_count = db.query(Policy).filter(Policy.is_active == True).count()
        
        # Apply pagination
        policies = query.offset(skip).limit(limit).all()
        
        return policies, total_count, active_count
    
    @staticmethod
    def get_policy_by_id(
        db: Session,
        policy_id: int
    ) -> Optional[Policy]:
        """
        Get policy by ID
        
        Args:
            db: Database session
            policy_id: Policy ID
            
        Returns:
            Policy or None if not found
        """
        return db.query(Policy).filter(Policy.id == policy_id).first()
    
    @staticmethod
    def update_policy(
        db: Session,
        policy_id: int,
        update_data: PolicyUpdate
    ) -> Optional[Policy]:
        """
        Update policy
        
        Args:
            db: Database session
            policy_id: Policy ID
            update_data: Update data
            
        Returns:
            Updated policy or None if not found
        """
        policy = db.query(Policy).filter(Policy.id == policy_id).first()
        
        if not policy:
            return None
        
        # Update fields that are provided
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(policy, field, value)
        
        policy.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(policy)
        
        return policy
    
    @staticmethod
    def delete_policy(
        db: Session,
        policy_id: int,
        soft_delete: bool = True
    ) -> bool:
        """
        Delete policy (soft delete by default)
        
        Args:
            db: Database session
            policy_id: Policy ID
            soft_delete: If True, set is_active to False; if False, actually delete
            
        Returns:
            True if deleted, False if not found
        """
        policy = db.query(Policy).filter(Policy.id == policy_id).first()
        
        if not policy:
            return False
        
        if soft_delete:
            # Soft delete: set is_active to False
            policy.is_active = False
            policy.updated_at = datetime.utcnow()
            db.commit()
        else:
            # Hard delete: remove from database (also deletes file if exists)
            if policy.document_path and os.path.exists(policy.document_path):
                os.remove(policy.document_path)
            db.delete(policy)
            db.commit()
        
        return True
    
    @staticmethod
    async def upload_policy_document(
        db: Session,
        policy_id: int,
        file: UploadFile
    ) -> Tuple[Optional[Policy], Optional[str], Optional[int]]:
        """
        Upload policy document (PDF)
        
        Args:
            db: Database session
            policy_id: Policy ID
            file: Uploaded file
            
        Returns:
            Tuple of (policy, file_path, file_size) or (None, error_message, None)
        """
        # Get policy
        policy = db.query(Policy).filter(Policy.id == policy_id).first()
        
        if not policy:
            return None, "Policy not found", None
        
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            return None, "Only PDF files are allowed", None
        
        # Create unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{policy_id}_{uuid.uuid4().hex[:8]}_{file.filename}"
        file_path = os.path.join(settings.UPLOAD_DIR, "policies", unique_filename)
        
        # Read file content and check size
        file_content = await file.read()
        file_size = len(file_content)
        
        if file_size > settings.MAX_FILE_SIZE:
            return None, f"File size exceeds maximum allowed ({settings.MAX_FILE_SIZE_MB}MB)", None
        
        # Delete old file if exists
        if policy.document_path and os.path.exists(policy.document_path):
            os.remove(policy.document_path)
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Update policy with file path
        policy.document_path = file_path
        policy.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(policy)
        
        # Auto-index policy for RAG (async, non-blocking)
        try:
            from ai_services.policy_rag_service import PolicyRAGService
            rag_service = PolicyRAGService()
            rag_service.index_policy_document(file_path, policy.title)
        except Exception as e:
            # Log error but don't fail the upload
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to index policy {policy.id} for RAG: {e}")
        
        return policy, file_path, file_size
    
    @staticmethod
    def get_policy_document_path(
        db: Session,
        policy_id: int
    ) -> Optional[str]:
        """
        Get policy document file path
        
        Args:
            db: Database session
            policy_id: Policy ID
            
        Returns:
            File path or None if not found
        """
        policy = db.query(Policy).filter(Policy.id == policy_id).first()
        
        if not policy or not policy.document_path:
            return None
        
        if not os.path.exists(policy.document_path):
            return None
        
        return policy.document_path
    
    @staticmethod
    def acknowledge_policy(
        db: Session,
        policy_id: int,
        user: User
    ) -> Optional[PolicyAcknowledgment]:
        """
        Acknowledge policy by user
        
        Args:
            db: Database session
            policy_id: Policy ID
            user: User acknowledging the policy
            
        Returns:
            PolicyAcknowledgment or None if already acknowledged
        """
        # Check if policy exists
        policy = db.query(Policy).filter(Policy.id == policy_id).first()
        if not policy:
            return None
        
        # Check if already acknowledged
        existing = db.query(PolicyAcknowledgment).filter(
            and_(
                PolicyAcknowledgment.policy_id == policy_id,
                PolicyAcknowledgment.user_id == user.id
            )
        ).first()
        
        if existing:
            return existing  # Already acknowledged
        
        # Create acknowledgment
        acknowledgment = PolicyAcknowledgment(
            policy_id=policy_id,
            user_id=user.id,
            acknowledged_date=datetime.utcnow()
        )
        
        db.add(acknowledgment)
        db.commit()
        db.refresh(acknowledgment)
        
        return acknowledgment
    
    @staticmethod
    def get_policy_acknowledgments(
        db: Session,
        policy_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[PolicyAcknowledgment], int]:
        """
        Get all acknowledgments for a policy
        
        Args:
            db: Database session
            policy_id: Policy ID
            skip: Pagination offset
            limit: Maximum results
            
        Returns:
            Tuple of (acknowledgments, total_count)
        """
        query = db.query(PolicyAcknowledgment).filter(
            PolicyAcknowledgment.policy_id == policy_id
        ).order_by(PolicyAcknowledgment.acknowledged_date.desc())
        
        total_count = query.count()
        acknowledgments = query.offset(skip).limit(limit).all()
        
        return acknowledgments, total_count
    
    @staticmethod
    def get_user_acknowledgments(
        db: Session,
        user_id: int
    ) -> List[PolicyAcknowledgment]:
        """
        Get all policies acknowledged by a user
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            List of acknowledgments
        """
        return db.query(PolicyAcknowledgment).filter(
            PolicyAcknowledgment.user_id == user_id
        ).order_by(PolicyAcknowledgment.acknowledged_date.desc()).all()
    
    @staticmethod
    def has_user_acknowledged_policy(
        db: Session,
        policy_id: int,
        user_id: int
    ) -> bool:
        """
        Check if user has acknowledged a policy
        
        Args:
            db: Database session
            policy_id: Policy ID
            user_id: User ID
            
        Returns:
            True if acknowledged, False otherwise
        """
        count = db.query(PolicyAcknowledgment).filter(
            and_(
                PolicyAcknowledgment.policy_id == policy_id,
                PolicyAcknowledgment.user_id == user_id
            )
        ).count()
        
        return count > 0
    
    @staticmethod
    def format_policy_response(
        policy: Policy,
        db: Session,
        current_user: Optional[User] = None
    ) -> PolicyResponse:
        """
        Format policy for response with additional fields
        
        Args:
            policy: Policy object
            db: Database session (to fetch creator name, acknowledgments)
            current_user: Current user (to check acknowledgment status)
            
        Returns:
            PolicyResponse with formatted data
        """
        # Get creator name
        creator = db.query(User).filter(User.id == policy.created_by).first()
        creator_name = creator.name if creator else "Unknown"
        
        # Check if has document
        has_document = bool(policy.document_path and os.path.exists(policy.document_path))
        
        # Generate document URL
        document_url = None
        if has_document:
            # Convert absolute path to relative URL
            document_url = f"/api/v1/policies/{policy.id}/download"
        
        # Get acknowledgment count
        acknowledgment_count = db.query(PolicyAcknowledgment).filter(
            PolicyAcknowledgment.policy_id == policy.id
        ).count()
        
        # Check if current user has acknowledged
        is_acknowledged_by_user = False
        if current_user:
            is_acknowledged_by_user = PolicyService.has_user_acknowledged_policy(
                db, policy.id, current_user.id
            )
        
        return PolicyResponse(
            id=policy.id,
            title=policy.title,
            description=policy.description,
            content=policy.content,
            category=policy.category,
            version=policy.version,
            is_active=policy.is_active,
            effective_date=policy.effective_date,
            review_date=policy.review_date,
            document_path=policy.document_path,
            created_by=policy.created_by,
            created_by_name=creator_name,
            created_at=policy.created_at,
            updated_at=policy.updated_at,
            has_document=has_document,
            document_url=document_url,
            acknowledgment_count=acknowledgment_count,
            is_acknowledged_by_user=is_acknowledged_by_user
        )
    
    @staticmethod
    def get_stats(db: Session) -> dict:
        """
        Get policy statistics
        
        Args:
            db: Database session
            
        Returns:
            Dictionary with statistics
        """
        total = db.query(Policy).count()
        active = db.query(Policy).filter(Policy.is_active == True).count()
        inactive = db.query(Policy).filter(Policy.is_active == False).count()
        
        # Policies with documents
        with_documents = db.query(Policy).filter(
            and_(
                Policy.is_active == True,
                Policy.document_path != None
            )
        ).count()
        
        # Total acknowledgments
        total_acknowledgments = db.query(PolicyAcknowledgment).count()
        
        # Get category breakdown
        categories = db.query(
            Policy.category,
            func.count(Policy.id).label('count')
        ).filter(
            Policy.is_active == True
        ).group_by(Policy.category).all()
        
        category_stats = {cat: count for cat, count in categories if cat}
        
        return {
            "total": total,
            "active": active,
            "inactive": inactive,
            "with_documents": with_documents,
            "total_acknowledgments": total_acknowledgments,
            "categories": category_stats
        }

