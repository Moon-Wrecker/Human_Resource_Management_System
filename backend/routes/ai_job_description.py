"""
Job Description Generator AI Routes - GenAI Integration
AI-powered job description generation with dual modes (preview/save)

**User Story Implemented:**
- HR Manager: Job Description Management - Efficiently create and manage job descriptions with 
  structured approach to save time and maintain up-to-date role definitions

**GenAI Integration:**
- Uses Google Gemini API for professional JD generation
- Template-based structured output
- Context-aware content generation
- SEO and ATS optimization

**Key Features:**
- Dual mode: Generate for review OR Save as draft
- Professional, compelling content generation
- Structured sections (summary, responsibilities, qualifications, benefits)
- Company culture integration
- SEO keyword extraction
- Improvement suggestions for existing JDs
- ATS-friendly formatting
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User, UserRole, JobListing
from utils.dependencies import get_current_user
from schemas.ai_schemas import (
    JobDescriptionGenerateRequest,
    JobDescriptionGenerateResponse,
    JobDescriptionContent
)
from ai_services.job_description_generator_service import JobDescriptionGeneratorService
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/ai/job-description",
    tags=["AI - Job Description Generator"],
    responses={
        503: {"description": "Service Unavailable - AI service not configured"},
        500: {"description": "Internal Server Error - Generation failed"}
    }
)

# Singleton instance
_jd_generator_service = None


def get_jd_generator_service() -> JobDescriptionGeneratorService:
    """Get or create JD Generator service instance"""
    global _jd_generator_service
    if _jd_generator_service is None:
        try:
            _jd_generator_service = JobDescriptionGeneratorService()
        except Exception as e:
            logger.error(f"Failed to initialize JD Generator Service: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Job Description Generator service unavailable: {str(e)}"
            )
    return _jd_generator_service


@router.post(
    "/generate",
    response_model=JobDescriptionGenerateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate Job Description with AI (GenAI)",
    description="Create professional, ATS-optimized job descriptions using Google Gemini",
    responses={
        201: {
            "description": "Job description generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "title": "Senior Software Engineer",
                            "summary": "We are seeking an experienced Senior Software Engineer...",
                            "key_responsibilities": [
                                "Design and develop scalable backend systems",
                                "Lead technical architecture decisions",
                                "Mentor junior developers"
                            ],
                            "required_qualifications": [
                                "5+ years of software development experience",
                                "Strong proficiency in Python and JavaScript",
                                "Experience with cloud platforms (AWS/GCP)"
                            ],
                            "preferred_qualifications": [
                                "Experience with microservices architecture",
                                "Knowledge of DevOps practices"
                            ],
                            "benefits": ["Competitive salary", "Health insurance", "Remote work"],
                            "full_description": "Complete formatted JD..."
                        },
                        "job_listing_id": 42,
                        "message": "Job description saved as draft"
                    }
                }
            }
        },
        400: {"description": "Bad Request - Invalid input data"},
        403: {"description": "Forbidden - HR access required"}
    }
)
async def generate_job_description(
    request: JobDescriptionGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    ## Generate Job Description with AI - Automated JD Creation
    
    **User Story:**
    - **HR Manager - Job Description Management**: Saves time creating professional job descriptions
      with AI-powered generation that maintains consistency and quality
    
    **Two Modes:**
    1. **Preview Mode** (`save_as_draft=False`): Generate and review before saving
    2. **Draft Mode** (`save_as_draft=True`): Automatically save as job listing draft
    
    **Features:**
    - **Professional Content**: AI generates compelling, clear job descriptions
    - **Structured Output**: Summary, responsibilities, qualifications, benefits
    - **Company Culture Integration**: Incorporates company values and culture
    - **ATS Optimization**: Formatted for Applicant Tracking Systems
    - **SEO Friendly**: Includes relevant keywords
    - **Customizable**: Accepts detailed requirements and preferences
    
    **How it Works:**
    1. Accepts job details, requirements, and company info
    2. Gemini AI generates structured, professional content
    3. Returns formatted JD with all required sections
    4. Optionally saves as draft job listing in database
    
    **Request Body:**
    - `job_title` (required): Job title
    - `job_level` (required): Entry/Mid/Senior/Lead
    - `department` (optional): Department name
    - `location` (optional): Job location or "Remote"
    - `employment_type` (optional): Full-time/Part-time/Contract
    - `responsibilities` (optional): List of key responsibilities
    - `requirements` (optional): List of qualifications with required/preferred flag
    - `company_info` (optional): Company name, description, industry, values
    - `salary_range` (optional): Salary range
    - `benefits` (optional): List of benefits
    - `save_as_draft` (optional): Whether to save as job listing draft
    
    **Response:**
    - Generated JD content with all sections
    - Job listing ID if saved as draft
    - Success message
    
    **Error Handling:**
    - Validates HR permission
    - Handles AI generation failures gracefully
    - Returns detailed error messages
    
    **Access**: HR only
    **Performance**: Typically 5-10 seconds for generation
    """
    # Check HR permission
    if current_user.role != UserRole.HR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can generate job descriptions"
        )
    
    try:
        # Prepare company info
        company_info = None
        if request.company_info:
            company_info = {
                "name": request.company_info.name,
                "description": request.company_info.description,
                "industry": request.company_info.industry,
                "values": request.company_info.values
            }
        
        # Prepare requirements
        requirements = [
            {
                "requirement": req.requirement,
                "is_required": req.is_required
            }
            for req in request.requirements
        ]
        
        # Generate job description
        service = get_jd_generator_service()
        result = service.generate_job_description(
            job_title=request.job_title,
            job_level=request.job_level,
            department=request.department,
            location=request.location,
            employment_type=request.employment_type,
            responsibilities=request.responsibilities,
            requirements=requirements,
            company_info=company_info,
            salary_range=request.salary_range,
            benefits=request.benefits
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Failed to generate job description")
            )
        
        jd_data = result["data"]
        
        # If save_as_draft is True, create job listing
        job_listing_id = None
        if request.save_as_draft:
            # Create job listing draft
            new_job = JobListing(
                title=jd_data["title"],
                department=request.department,
                location=request.location,
                job_type=request.employment_type,
                description=jd_data["full_description"],
                responsibilities="\n".join(jd_data["key_responsibilities"]),
                qualifications="\n".join(
                    jd_data["required_qualifications"] + jd_data.get("preferred_qualifications", [])
                ),
                salary_range=request.salary_range or "Competitive",
                experience_required=request.job_level,
                created_by=current_user.id,
                status="draft",  # Save as draft
                created_at=datetime.utcnow(),
                is_active=False  # Draft is not active
            )
            
            db.add(new_job)
            db.commit()
            db.refresh(new_job)
            
            job_listing_id = new_job.id
            logger.info(f"Created job listing draft #{job_listing_id} from AI generation")
        
        # Return response
        return JobDescriptionGenerateResponse(
            success=True,
            data=JobDescriptionContent(**jd_data),
            job_listing_id=job_listing_id,
            message="Job description saved as draft" if request.save_as_draft else "Job description generated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating job description: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/improve")
async def improve_job_description(
    job_listing_id: int,
    improvements: list[str],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Improve an existing job description based on feedback
    
    Takes an existing job listing and applies AI-powered improvements
    based on specific feedback points.
    
    **Access**: HR only
    """
    # Check HR permission
    if current_user.role != UserRole.HR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can improve job descriptions"
        )
    
    try:
        # Get job listing
        job = db.query(JobListing).filter(JobListing.id == job_listing_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job listing {job_listing_id} not found"
            )
        
        # Improve description
        service = get_jd_generator_service()
        improved_description = service.improve_existing_jd(
            existing_jd=job.description,
            improvements=improvements
        )
        
        # Update job listing
        job.description = improved_description
        job.updated_at = datetime.utcnow()
        db.commit()
        
        return {
            "success": True,
            "message": "Job description improved successfully",
            "improved_description": improved_description
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error improving job description: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/extract-keywords")
async def extract_keywords(
    job_description: str,
    current_user: User = Depends(get_current_user)
):
    """
    Extract SEO/ATS keywords from a job description
    
    Useful for optimizing job postings for search engines and applicant tracking systems.
    
    **Access**: HR only
    """
    # Check HR permission
    if current_user.role != UserRole.HR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can extract keywords"
        )
    
    try:
        service = get_jd_generator_service()
        keywords = service.extract_keywords(job_description)
        
        return {
            "success": True,
            "keywords": keywords,
            "total": len(keywords)
        }
        
    except Exception as e:
        logger.error(f"Error extracting keywords: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/status")
async def get_jd_generator_status(
    current_user: User = Depends(get_current_user)
):
    """
    Get status of Job Description Generator service
    
    **Access**: All authenticated users
    """
    try:
        # Try to get service (will initialize if not already)
        service = get_jd_generator_service()
        
        return {
            "available": True,
            "model": settings.GEMINI_MODEL,
            "features": [
                "Generate professional job descriptions",
                "Save as draft or preview only",
                "Improve existing descriptions",
                "Extract SEO keywords",
                "Dual mode support"
            ]
        }
        
    except Exception as e:
        return {
            "available": False,
            "error": str(e)
        }

