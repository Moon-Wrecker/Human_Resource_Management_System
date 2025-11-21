"""
Policy RAG (AI Q&A) Routes - GenAI Integration
AI-powered policy question answering with auto-indexing using RAG (Retrieval Augmented Generation)

**User Stories Implemented:**
- HR Manager: Policy Access - Make company policies accessible 24/7 through employee self-service portal
- Employee: Policy Queries - Quickly find answers to company policy questions without waiting for HR

**GenAI Integration:**
- Uses Google Gemini API for natural language understanding
- ChromaDB for vector embeddings and semantic search
- Langchain for RAG pipeline orchestration
- Automatic policy document indexing on upload

**Key Features:**
- 24/7 policy chatbot availability
- Context-aware responses using RAG
- Multi-document search and synthesis
- Conversational chat history support
- Auto-indexing of uploaded policy documents
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
router = APIRouter(
    prefix="/ai/policy-rag", 
    tags=["AI - Policy RAG"],
    responses={
        503: {"description": "Service Unavailable - AI service not configured"},
        500: {"description": "Internal Server Error - AI service error"}
    }
)

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


@router.post(
    "/ask",
    response_model=PolicyAnswerResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask Policy Question (GenAI)",
    description="AI-powered policy question answering using RAG with Google Gemini",
    responses={
        200: {
            "description": "Question answered successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "answer": "According to our leave policy, employees are entitled to 12 days of casual leave per year...",
                        "sources": ["leave_policy.pdf", "hr_handbook.pdf"],
                        "confidence": 0.92,
                        "related_topics": ["Annual Leave", "Sick Leave", "WFH Policy"]
                    }
                }
            }
        },
        400: {"description": "Bad Request - Invalid question format"},
        503: {"description": "Service Unavailable - AI service not ready"}
    }
)
async def ask_policy_question(
    request: PolicyQuestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    ## Ask Policy Question - 24/7 AI Policy Chatbot
    
    **User Stories:**
    - **HR Manager - Policy Access**: Provides 24/7 policy access without HR intervention
    - **Employee - Policy Queries**: Instant answers to policy questions
    
    **Features:**
    - Natural language question processing using Google Gemini
    - Retrieval Augmented Generation (RAG) for accurate, source-backed answers
    - Conversational context support (chat history)
    - Source citation and confidence scoring
    - Related topic suggestions
    
    **How it Works:**
    1. Question is embedded using AI
    2. Similar policy sections retrieved from vector database
    3. Gemini generates contextualized answer
    4. Sources and confidence returned
    
    **Request Body:**
    - `question` (required): Policy question in natural language
    - `chat_history` (optional): Previous conversation for context
    
    **Error Handling:**
    - Returns error details if service unavailable
    - Handles malformed questions gracefully
    - Logs all questions for audit
    
    **Access**: All authenticated users (Employees, HR, Managers)
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

