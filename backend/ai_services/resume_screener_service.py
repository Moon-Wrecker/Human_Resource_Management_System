"""
Resume Screener Service - AI-powered resume analysis
Screens resumes against job descriptions with permanent storage
"""
import os
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import uuid

# Check if required libraries are available
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    import PyPDF2
    try:
        import docx2txt
        DOCX_AVAILABLE = True
    except ImportError:
        DOCX_AVAILABLE = False
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

from config import settings

logger = logging.getLogger("resume_screener_service")


class ResumeScreenerService:
    """
    Resume Screener Service
    
    AI-powered resume analysis against job descriptions
    Stores results permanently for future reference
    """
    
    def __init__(self):
        """Initialize the Resume Screener service"""
        if not LANGCHAIN_AVAILABLE:
            logger.error("LangChain libraries not installed. Install with: pip install -r requirements_ai.txt")
            raise ImportError("LangChain libraries required for Resume Screener service")
        
        if not settings.GOOGLE_API_KEY:
            logger.error("GOOGLE_API_KEY not set in environment variables")
            raise ValueError("GOOGLE_API_KEY is required for Resume Screener service")
        
        self.api_key = settings.GOOGLE_API_KEY
        self.storage_dir = settings.RESUME_SCREENER_STORAGE_DIR
        
        # Create storage directory
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # Initialize LLM
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                temperature=0.2,  # Lower for more consistent analysis
                google_api_key=self.api_key
            )
            
            logger.info("Resume Screener Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Resume Screener Service: {e}")
            raise
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {e}")
            raise
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        if not DOCX_AVAILABLE:
            raise ImportError("docx2txt not installed. Install with: pip install docx2txt")
        
        try:
            text = docx2txt.process(file_path)
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from DOCX {file_path}: {e}")
            raise
    
    def extract_resume_text(self, file_path: str) -> str:
        """Extract text from resume (PDF or DOCX)"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_ext in ['.docx', '.doc']:
            return self.extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    def analyze_resume(
        self,
        resume_text: str,
        job_description: str,
        candidate_name: str = "Unknown"
    ) -> Dict[str, Any]:
        """
        Analyze a single resume against job description
        
        Args:
            resume_text: Resume content as text
            job_description: Job description text
            candidate_name: Name of the candidate
            
        Returns:
            dict: Analysis results with scores and insights
        """
        try:
            # Create analysis prompt
            prompt = f"""
You are an expert HR recruiter and talent acquisition specialist. Analyze the following resume against the job description and provide a detailed assessment.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Provide your analysis in the following JSON format (respond with ONLY valid JSON, no additional text):
{{
    "candidate_name": "{candidate_name}",
    "overall_fit_score": <number 0-100>,
    "skill_matches": [
        {{
            "skill_name": "Python",
            "present_in_resume": true,
            "importance_level": 5,
            "proficiency_level": 4,
            "context": "3 years experience with Django and Flask"
        }}
    ],
    "experience_matches": [
        {{
            "area": "Backend Development",
            "years_required": 3,
            "years_present": 4,
            "relevance_score": 5,
            "context": "4 years as Python backend developer"
        }}
    ],
    "education_match": {{
        "requirement": "Bachelor's in Computer Science",
        "has_match": true,
        "details": "B.Tech in Computer Science from XYZ University"
    }},
    "strengths": [
        "Strong Python expertise",
        "Proven leadership experience",
        "Excellent problem-solving skills"
    ],
    "gaps": [
        "Limited AWS experience",
        "No mention of CI/CD"
    ],
    "summary": "Strong candidate with excellent technical skills. Good fit for senior role with minor gaps in cloud technologies."
}}

Instructions:
- Be objective and thorough
- Base scores on actual evidence from the resume
- importance_level and relevance_score: 1 (low) to 5 (high)
- proficiency_level: 1 (beginner) to 5 (expert)
- overall_fit_score: 0-100 considering all factors
- Include specific context from the resume where applicable
"""
            
            # Get analysis from LLM
            response = self.llm.invoke(prompt)
            response_text = response.content.strip()
            
            # Extract JSON from response (handle cases where LLM adds extra text)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in LLM response")
            
            json_text = response_text[start_idx:end_idx]
            analysis = json.loads(json_text)
            
            # Add timestamp
            analysis['analysis_date'] = datetime.utcnow().isoformat()
            
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON from LLM response: {e}")
            logger.error(f"Response text: {response_text}")
            # Return a default analysis structure
            return {
                "candidate_name": candidate_name,
                "overall_fit_score": 50,
                "skill_matches": [],
                "experience_matches": [],
                "education_match": {
                    "requirement": "Unknown",
                    "has_match": False,
                    "details": "Analysis failed - please try again"
                },
                "strengths": ["Unable to analyze"],
                "gaps": ["Analysis error occurred"],
                "summary": "Analysis could not be completed due to technical error.",
                "analysis_date": datetime.utcnow().isoformat(),
                "error": str(e)
            }
        except Exception as e:
            logger.error(f"Error analyzing resume: {e}")
            raise
    
    def screen_resumes(
        self,
        resume_files: List[Dict[str, Any]],
        job_description: str,
        job_id: int,
        job_title: str = ""
    ) -> Dict[str, Any]:
        """
        Screen multiple resumes against a job description
        
        Args:
            resume_files: List of dicts with 'path' and 'candidate_name'
            job_description: Job description text
            job_id: Job listing ID
            job_title: Job title (optional)
            
        Returns:
            dict: Screening results with analysis for all resumes
        """
        try:
            logger.info(f"Screening {len(resume_files)} resumes for job {job_id}")
            
            results = []
            total_score = 0
            
            for resume_file in resume_files:
                try:
                    # Extract resume text
                    resume_text = self.extract_resume_text(resume_file['path'])
                    
                    # Analyze resume
                    analysis = self.analyze_resume(
                        resume_text=resume_text,
                        job_description=job_description,
                        candidate_name=resume_file.get('candidate_name', 'Unknown')
                    )
                    
                    # Add application_id if provided
                    if 'application_id' in resume_file:
                        analysis['application_id'] = resume_file['application_id']
                    
                    results.append(analysis)
                    total_score += analysis.get('overall_fit_score', 0)
                    
                except Exception as e:
                    logger.error(f"Error screening resume {resume_file.get('candidate_name')}: {e}")
                    # Add error result
                    results.append({
                        "candidate_name": resume_file.get('candidate_name', 'Unknown'),
                        "application_id": resume_file.get('application_id'),
                        "overall_fit_score": 0,
                        "skill_matches": [],
                        "experience_matches": [],
                        "education_match": {"requirement": "", "has_match": False, "details": ""},
                        "strengths": [],
                        "gaps": ["Analysis failed"],
                        "summary": f"Error analyzing resume: {str(e)}",
                        "analysis_date": datetime.utcnow().isoformat(),
                        "error": str(e)
                    })
            
            # Calculate average score
            average_score = total_score / len(results) if results else 0
            
            # Find top candidate
            top_candidate = None
            if results:
                top_result = max(results, key=lambda x: x.get('overall_fit_score', 0))
                top_candidate = top_result.get('candidate_name')
            
            # Generate analysis ID
            analysis_id = uuid.uuid4().hex[:12]
            
            # Save results to storage
            screening_data = {
                "analysis_id": analysis_id,
                "job_id": job_id,
                "job_title": job_title,
                "timestamp": datetime.utcnow().isoformat(),
                "total_analyzed": len(results),
                "average_score": average_score,
                "top_candidate": top_candidate,
                "results": results
            }
            
            self._save_screening_results(analysis_id, screening_data)
            
            return {
                "success": True,
                "analysis_id": analysis_id,
                "job_id": job_id,
                "job_title": job_title,
                "results": results,
                "total_analyzed": len(results),
                "average_score": round(average_score, 2),
                "top_candidate": top_candidate
            }
            
        except Exception as e:
            logger.error(f"Error in batch resume screening: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _save_screening_results(self, analysis_id: str, data: Dict[str, Any]):
        """Save screening results to storage"""
        try:
            file_path = os.path.join(self.storage_dir, f"{analysis_id}.json")
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved screening results to {file_path}")
        except Exception as e:
            logger.error(f"Error saving screening results: {e}")
            raise
    
    def get_screening_results(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve saved screening results"""
        try:
            file_path = os.path.join(self.storage_dir, f"{analysis_id}.json")
            
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            return data
            
        except Exception as e:
            logger.error(f"Error retrieving screening results: {e}")
            return None
    
    def list_screening_history(self, job_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """List all screening analyses, optionally filtered by job_id"""
        try:
            history = []
            
            # Get all JSON files in storage directory
            for file_path in Path(self.storage_dir).glob("*.json"):
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    
                    # Filter by job_id if provided
                    if job_id is None or data.get('job_id') == job_id:
                        # Add summary to history
                        history.append({
                            "analysis_id": data['analysis_id'],
                            "job_id": data['job_id'],
                            "job_title": data.get('job_title', ''),
                            "timestamp": data['timestamp'],
                            "total_analyzed": data['total_analyzed'],
                            "average_score": data['average_score'],
                            "top_candidate": data.get('top_candidate')
                        })
                except Exception as e:
                    logger.warning(f"Error reading screening file {file_path}: {e}")
                    continue
            
            # Sort by timestamp (newest first)
            history.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return history
            
        except Exception as e:
            logger.error(f"Error listing screening history: {e}")
            return []

