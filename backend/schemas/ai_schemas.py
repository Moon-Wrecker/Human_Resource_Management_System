"""
Pydantic schemas for AI services
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime


# ==================== Policy RAG Schemas ====================


class PolicyQuestionRequest(BaseModel):
    """Request to ask a question about policies"""

    question: str = Field(
        ..., min_length=3, description="Question about company policies"
    )
    chat_history: Optional[List[Dict[str, str]]] = Field(
        None, description="Previous chat messages"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "question": "How many casual leaves am I allowed per year?",
                "chat_history": [
                    {"role": "user", "content": "What is the leave policy?"},
                    {"role": "assistant", "content": "The leave policy includes..."},
                ],
            }
        }


class PolicyAnswerResponse(BaseModel):
    """Response with policy answer"""

    success: bool
    answer: Optional[str] = None
    sources: Optional[List[Dict[str, str]]] = None
    question: Optional[str] = None
    error: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "answer": "Employees are entitled to 12 casual leaves per year...",
                "sources": [
                    {
                        "policy_title": "Leave Policy 2025",
                        "content": "Casual Leave: 12 days per calendar year...",
                    }
                ],
                "question": "How many casual leaves am I allowed per year?",
            }
        }


class PolicySuggestionsResponse(BaseModel):
    """Response with suggested questions"""

    suggestions: List[str]


class PolicyIndexStatusResponse(BaseModel):
    """Response with index status"""

    indexed: bool
    total_vectors: Optional[int] = None
    index_location: Optional[str] = None
    model: Optional[str] = None
    embedding_model: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None


# ==================== Resume Screener Schemas ====================


class ResumeScreeningRequest(BaseModel):
    """Request to screen resumes against a job description"""

    job_id: int = Field(..., description="ID of the job listing")
    job_description: Optional[str] = Field(
        None, description="Job description text (if not using job_id)"
    )
    resume_ids: Optional[List[int]] = Field(
        None, description="Application IDs to screen"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "job_id": 1,
                "job_description": "Looking for Python developer with 3+ years experience...",
                "resume_ids": [1, 2, 3],
            }
        }


class SkillMatchResponse(BaseModel):
    """Skill match details"""

    skill_name: str
    present_in_resume: bool
    importance_level: int = Field(ge=0, le=5)
    proficiency_level: Optional[int] = Field(None, ge=0, le=5)
    context: Optional[str] = None


class ExperienceMatchResponse(BaseModel):
    """Experience match details"""

    area: str
    years_required: Optional[float | str] = None
    years_present: float
    relevance_score: int = Field(ge=0, le=5)
    context: Optional[str] = None


class EducationMatchResponse(BaseModel):
    """Education match details"""

    requirement: str
    has_match: bool
    details: str


class ResumeAnalysisResponse(BaseModel):
    """Resume analysis result"""

    candidate_name: str
    application_id: Optional[int] = None
    overall_fit_score: int = Field(ge=0, le=100)
    skill_matches: List[SkillMatchResponse]
    experience_matches: List[ExperienceMatchResponse]
    education_match: EducationMatchResponse
    strengths: List[str]
    gaps: List[str]
    summary: str
    analysis_date: datetime


class ResumeScreeningResultResponse(BaseModel):
    """Response with screening results"""

    success: bool
    job_id: int
    job_title: Optional[str] = None
    results: List[ResumeAnalysisResponse]
    total_analyzed: int
    average_score: float
    top_candidate: Optional[str] = None
    analysis_id: Optional[int] = None
    error: Optional[str] = None


# ==================== Job Description Generator Schemas ====================


class CompanyInfoInput(BaseModel):
    """Company information for JD generation"""

    name: Optional[str] = Field(None, description="Company name")
    description: Optional[str] = Field(None, description="Brief company description")
    industry: Optional[str] = Field(None, description="Industry")
    values: Optional[List[str]] = Field(None, description="Company values")


class JobRequirementInput(BaseModel):
    """Job requirement input"""

    requirement: str
    is_required: bool = True


class JobDescriptionGenerateRequest(BaseModel):
    """Request to generate job description"""

    job_title: str = Field(..., description="Job title")
    job_level: str = Field(..., description="Job level (entry, mid, senior)")
    department: str = Field(..., description="Department")
    location: str = Field(..., description="Job location")
    employment_type: str = Field(default="full-time", description="Employment type")
    company_info: Optional[CompanyInfoInput] = None
    responsibilities: List[str] = Field(..., description="Key responsibilities")
    requirements: List[JobRequirementInput] = Field(..., description="Job requirements")
    salary_range: Optional[str] = None
    benefits: Optional[List[str]] = None
    save_as_draft: bool = Field(default=False, description="Save as job listing draft")

    class Config:
        json_schema_extra = {
            "example": {
                "job_title": "Senior Python Developer",
                "job_level": "Senior",
                "department": "Engineering",
                "location": "Remote/Bangalore",
                "employment_type": "full-time",
                "responsibilities": [
                    "Design and develop scalable backend services",
                    "Mentor junior developers",
                    "Review code and ensure quality",
                ],
                "requirements": [
                    {"requirement": "5+ years Python experience", "is_required": True},
                    {
                        "requirement": "Experience with Django/FastAPI",
                        "is_required": True,
                    },
                    {"requirement": "AWS experience", "is_required": False},
                ],
                "salary_range": "$120,000 - $150,000",
                "save_as_draft": False,
            }
        }


class JobDescriptionContent(BaseModel):
    """Generated job description content"""

    title: str
    company_overview: Optional[str] = None
    job_summary: str
    key_responsibilities: List[str]
    required_qualifications: List[str]
    preferred_qualifications: List[str]
    benefits_section: Optional[str] = None
    how_to_apply: Optional[str] = None
    full_description: str


class JobDescriptionGenerateResponse(BaseModel):
    """Response with generated job description"""

    success: bool
    data: Optional[JobDescriptionContent] = None
    job_listing_id: Optional[int] = None
    message: Optional[str] = None
    error: Optional[str] = None


# ==================== Common Schemas ====================


class MessageResponse(BaseModel):
    """Generic message response"""

    message: str

    class Config:
        json_schema_extra = {"example": {"message": "Operation completed successfully"}}


class AIStatusResponse(BaseModel):
    """AI services status"""

    policy_rag: Dict[str, Any]
    resume_screener: Dict[str, Any]
    jd_generator: Dict[str, Any]
