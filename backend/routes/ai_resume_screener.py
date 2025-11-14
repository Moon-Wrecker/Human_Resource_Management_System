"""
Resume Screener AI Routes
AI-powered resume analysis with permanent storage
"""
import logging
import asyncio
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from database import get_db
from models import User, UserRole, JobListing, Application
from utils.dependencies import get_current_user
from schemas.ai_schemas import (
    ResumeScreeningRequest,
    ResumeScreeningResultResponse,
    MessageResponse
)
from ai_services.resume_screener_service import ResumeScreenerService
from config import settings
from datetime import datetime
import os

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai/resume-screener", tags=["AI - Resume Screener"])

# Singleton instance
_resume_screener_service = None


def get_resume_screener_service() -> ResumeScreenerService:
    """Get or create Resume Screener service instance"""
    global _resume_screener_service
    if _resume_screener_service is None:
        try:
            _resume_screener_service = ResumeScreenerService()
        except Exception as e:
            logger.error(f"Failed to initialize Resume Screener Service: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Resume Screener service unavailable: {str(e)}"
            )
    return _resume_screener_service


@router.post("/screen", response_model=ResumeScreeningResultResponse)
async def screen_resumes(
    request: ResumeScreeningRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Screen resumes against a job description using AI
    
    Analyzes multiple resumes and provides:
    - Overall fit score (0-100)
    - Skill matching with proficiency levels
    - Experience matching
    - Education verification
    - Strengths and gaps
    - Detailed summary
    
    Results are stored permanently for future reference.
    
    **Access**: HR only
    **Note**: This is a long-running operation. Use background tasks for large batches.
    """
    # Check HR permission
    if current_user.role != UserRole.HR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can screen resumes"
        )
    
    try:
        # Get job listing
        job = db.query(JobListing).filter(JobListing.id == request.job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job listing {request.job_id} not found"
            )
        
        # Use provided JD or get from job listing
        job_description = request.job_description or job.description
        
        if not job_description:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Job description not available"
            )
        
        # Get applications to screen
        if request.resume_ids:
            # Screen specific applications
            applications = db.query(Application).filter(
                Application.id.in_(request.resume_ids),
                Application.job_id == request.job_id
            ).all()
        else:
            # Screen all applications for this job
            applications = db.query(Application).filter(
                Application.job_id == request.job_id
            ).all()
        
        if not applications:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No applications found to screen"
            )
        
        logger.info(f"Screening {len(applications)} resumes for job {request.job_id}")
        
        # Prepare resume files for screening
        resume_files = []
        for app in applications:
            if not app.resume_path or not os.path.exists(app.resume_path):
                logger.warning(f"Resume file not found for application {app.id}")
                continue
            
            resume_files.append({
                "path": app.resume_path,
                "candidate_name": app.full_name,
                "application_id": app.id
            })
        
        if not resume_files:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid resume files found for screening"
            )
        
        # Screen resumes
        service = get_resume_screener_service()
        result = service.screen_resumes(
            resume_files=resume_files,
            job_description=job_description,
            job_id=request.job_id,
            job_title=job.title
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Screening failed")
            )
        
        # Return results
        return ResumeScreeningResultResponse(
            success=True,
            job_id=result["job_id"],
            job_title=result.get("job_title"),
            results=result["results"],
            total_analyzed=result["total_analyzed"],
            average_score=result["average_score"],
            top_candidate=result.get("top_candidate"),
            analysis_id=result.get("analysis_id")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error screening resumes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/results/{analysis_id}", response_model=ResumeScreeningResultResponse)
async def get_screening_results(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve saved screening results by analysis ID
    
    **Access**: HR only
    """
    # Check HR permission
    if current_user.role != UserRole.HR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can view screening results"
        )
    
    try:
        service = get_resume_screener_service()
        results = service.get_screening_results(analysis_id)
        
        if not results:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Screening results not found for analysis ID: {analysis_id}"
            )
        
        return ResumeScreeningResultResponse(
            success=True,
            job_id=results["job_id"],
            job_title=results.get("job_title"),
            results=results["results"],
            total_analyzed=results["total_analyzed"],
            average_score=results["average_score"],
            top_candidate=results.get("top_candidate"),
            analysis_id=results["analysis_id"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving screening results: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/history")
async def get_screening_history(
    job_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get history of all resume screening analyses
    
    Optionally filter by job_id to see screening history for a specific job.
    
    **Access**: HR only
    """
    # Check HR permission
    if current_user.role != UserRole.HR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can view screening history"
        )
    
    try:
        service = get_resume_screener_service()
        history = service.list_screening_history(job_id=job_id)
        
        return {
            "success": True,
            "total": len(history),
            "history": history
        }
        
    except Exception as e:
        logger.error(f"Error retrieving screening history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/screen/stream")
async def screen_resumes_stream(
    request: ResumeScreeningRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Screen resumes with real-time progress updates (Server-Sent Events)
    
    Returns a stream of progress updates as resumes are analyzed.
    This provides better UX for long-running operations.
    
    **Stream Format**: Server-Sent Events (SSE)
    - `event: progress` - Progress update (% complete)
    - `event: result` - Individual resume analysis complete
    - `event: complete` - All resumes analyzed
    - `event: error` - Error occurred
    
    **Access**: HR only
    """
    # Check HR permission
    if current_user.role != UserRole.HR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can screen resumes"
        )
    
    async def event_generator():
        """Generate SSE events for resume screening progress"""
        try:
            # Get job listing
            job = db.query(JobListing).filter(JobListing.id == request.job_id).first()
            if not job:
                yield f"event: error\ndata: {json.dumps({'error': 'Job listing not found'})}\n\n"
                return
            
            # Use provided JD or get from job listing
            job_description = request.job_description or job.description
            
            if not job_description:
                yield f"event: error\ndata: {json.dumps({'error': 'Job description not available'})}\n\n"
                return
            
            # Get applications to screen
            if request.resume_ids:
                applications = db.query(Application).filter(
                    Application.id.in_(request.resume_ids),
                    Application.job_id == request.job_id
                ).all()
            else:
                applications = db.query(Application).filter(
                    Application.job_id == request.job_id
                ).all()
            
            if not applications:
                yield f"event: error\ndata: {json.dumps({'error': 'No applications found'})}\n\n"
                return
            
            # Prepare resume files
            resume_files = []
            for app in applications:
                if not app.resume_path or not os.path.exists(app.resume_path):
                    continue
                resume_files.append({
                    "path": app.resume_path,
                    "candidate_name": app.full_name,
                    "application_id": app.id
                })
            
            if not resume_files:
                yield f"event: error\ndata: {json.dumps({'error': 'No valid resume files found'})}\n\n"
                return
            
            total = len(resume_files)
            yield f"event: start\ndata: {json.dumps({'total': total, 'job_title': job.title})}\n\n"
            
            # Screen resumes one by one with progress updates
            service = get_resume_screener_service()
            results = []
            total_score = 0
            
            for idx, resume_file in enumerate(resume_files):
                try:
                    # Extract and analyze
                    resume_text = service.extract_resume_text(resume_file['path'])
                    analysis = service.analyze_resume(
                        resume_text=resume_text,
                        job_description=job_description,
                        candidate_name=resume_file.get('candidate_name', 'Unknown')
                    )
                    
                    if 'application_id' in resume_file:
                        analysis['application_id'] = resume_file['application_id']
                    
                    results.append(analysis)
                    total_score += analysis.get('overall_fit_score', 0)
                    
                    # Send individual result
                    yield f"event: result\ndata: {json.dumps({
                        'candidate': analysis['candidate_name'],
                        'score': analysis['overall_fit_score'],
                        'progress': int((idx + 1) / total * 100)
                    })}\n\n"
                    
                    # Small delay for better UX
                    await asyncio.sleep(0.1)
                    
                except Exception as e:
                    logger.error(f"Error screening {resume_file.get('candidate_name')}: {e}")
                    yield f"event: error\ndata: {json.dumps({
                        'candidate': resume_file.get('candidate_name'),
                        'error': str(e)
                    })}\n\n"
            
            # Calculate final stats
            average_score = total_score / len(results) if results else 0
            top_candidate = None
            if results:
                top_result = max(results, key=lambda x: x.get('overall_fit_score', 0))
                top_candidate = top_result.get('candidate_name')
            
            # Save results
            import uuid
            analysis_id = uuid.uuid4().hex[:12]
            screening_data = {
                "analysis_id": analysis_id,
                "job_id": request.job_id,
                "job_title": job.title,
                "timestamp": datetime.utcnow().isoformat(),
                "total_analyzed": len(results),
                "average_score": average_score,
                "top_candidate": top_candidate,
                "results": results
            }
            service._save_screening_results(analysis_id, screening_data)
            
            # Send completion event
            yield f"event: complete\ndata: {json.dumps({
                'analysis_id': analysis_id,
                'total_analyzed': len(results),
                'average_score': round(average_score, 2),
                'top_candidate': top_candidate
            })}\n\n"
            
        except Exception as e:
            logger.error(f"Error in streaming resume screening: {e}")
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

