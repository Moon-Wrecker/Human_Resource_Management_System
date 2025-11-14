"""
Policy RAG (AI Q&A) Routes
AI-powered policy question answering with auto-indexing
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User
from utils.dependencies import get_current_user
from schemas.ai_schemas import (
    PolicyQuestionRequest,
    PolicyAnswerResponse,
    PolicySuggestionsResponse,
    PolicyIndexStatusResponse,
    MessageResponse
)
from ai_services.policy_rag_service import PolicyRAGService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai/policy-rag", tags=["AI - Policy RAG"])

# Singleton instance
_policy_rag_service = None


def get_policy_rag_service() -> PolicyRAGService:
    """Get or create Policy RAG service instance"""
    global _policy_rag_service
    if _policy_rag_service is None:
        try:
            _policy_rag_service = PolicyRAGService()
            # Try to load existing index
            _policy_rag_service.load_index()
        except Exception as e:
            logger.error(f"Failed to initialize Policy RAG Service: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Policy RAG service unavailable: {str(e)}"
            )
    return _policy_rag_service


@router.post("/ask", response_model=PolicyAnswerResponse)
async def ask_policy_question(
    request: PolicyQuestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Ask a question about company policies
    
    The AI will answer based on indexed policy documents.
    Supports conversational context through chat history.
    
    **Access**: All authenticated users
    """
    try:
        logger.info(f"User {current_user.email} asked: {request.question}")
        
        service = get_policy_rag_service()
        result = service.ask_question(
            question=request.question,
            chat_history=request.chat_history
        )
        
        return PolicyAnswerResponse(**result)
        
    except Exception as e:
        logger.error(f"Error processing policy question: {e}")
        return PolicyAnswerResponse(
            success=False,
            error=str(e)
        )


@router.get("/suggestions", response_model=PolicySuggestionsResponse)
async def get_policy_suggestions(
    current_user: User = Depends(get_current_user)
):
    """
    Get suggested policy questions
    
    Returns a list of common questions that users can ask
    to get started with the policy Q&A feature.
    
    **Access**: All authenticated users
    """
    try:
        service = get_policy_rag_service()
        suggestions = service.get_suggestions()
        
        return PolicySuggestionsResponse(suggestions=suggestions)
        
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/status", response_model=PolicyIndexStatusResponse)
async def get_index_status(
    current_user: User = Depends(get_current_user)
):
    """
    Get status of the policy index
    
    Returns information about whether policies are indexed and ready for Q&A.
    
    **Access**: All authenticated users
    """
    try:
        service = get_policy_rag_service()
        status_info = service.get_index_status()
        
        return PolicyIndexStatusResponse(**status_info)
        
    except Exception as e:
        logger.error(f"Error getting index status: {e}")
        return PolicyIndexStatusResponse(
            indexed=False,
            error=str(e)
        )


@router.post("/index/rebuild", response_model=MessageResponse)
async def rebuild_index(
    current_user: User = Depends(get_current_user)
):
    """
    Rebuild the policy index from all uploaded policies
    
    This endpoint triggers a full re-indexing of all policy documents
    in the uploads/policies directory. Use this if the index gets corrupted
    or when policies are manually added to the directory.
    
    **Access**: All authenticated users (auto-indexes on policy upload)
    **Note**: Usually not needed as policies are auto-indexed when uploaded
    """
    try:
        from config import settings
        import os
        
        policy_dir = os.path.join(settings.UPLOAD_DIR, "policies")
        
        service = get_policy_rag_service()
        result = service.index_all_policies(policy_dir)
        
        if result.get("success"):
            indexed = result.get("indexed", 0)
            total = result.get("total", 0)
            message = f"Successfully indexed {indexed} out of {total} policies"
            
            if result.get("failed"):
                message += f". Failed: {', '.join(result['failed'])}"
            
            return MessageResponse(message=message)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Failed to rebuild index")
            )
        
    except Exception as e:
        logger.error(f"Error rebuilding index: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

