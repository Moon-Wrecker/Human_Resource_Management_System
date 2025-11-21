"""
Job Description Generator Service
AI-powered job description generation with dual modes
"""
import logging
import json
from typing import Dict, Any, List, Optional

# Check if required libraries are available
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

from config import settings

logger = logging.getLogger("jd_generator_service")


class JobDescriptionGeneratorService:
    """
    Job Description Generator Service
    
    Generates professional job descriptions using AI
    Supports two modes:
    1. Generate only - returns JD for review
    2. Save as draft - creates job listing draft in database
    """
    
    def __init__(self):
        """Initialize the JD Generator service"""
        if not LANGCHAIN_AVAILABLE:
            logger.error("LangChain libraries not installed. Install with: pip install -r requirements_ai.txt")
            raise ImportError("LangChain libraries required for JD Generator service")
        
        if not settings.GOOGLE_API_KEY:
            logger.error("GOOGLE_API_KEY not set in environment variables")
            raise ValueError("GOOGLE_API_KEY is required for JD Generator service")
        
        self.api_key = settings.GOOGLE_API_KEY
        
        # Initialize LLM with slightly higher temperature for creative writing
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                temperature=0.4,  # Slightly higher for more creative output
                google_api_key=self.api_key
            )
            
            logger.info("Job Description Generator Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize JD Generator Service: {e}")
            raise
    
    def generate_job_description(
        self,
        job_title: str,
        job_level: str,
        department: str,
        location: str,
        employment_type: str,
        responsibilities: List[str],
        requirements: List[Dict[str, Any]],
        company_info: Optional[Dict[str, Any]] = None,
        salary_range: Optional[str] = None,
        benefits: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate a professional job description
        
        Args:
            job_title: Job title (e.g., "Senior Python Developer")
            job_level: Job level (entry, mid, senior, lead, principal)
            department: Department name
            location: Job location (e.g., "Remote", "Bangalore", "Hybrid")
            employment_type: Type of employment (full-time, part-time, contract)
            responsibilities: List of key responsibilities
            requirements: List of requirements with is_required flag
            company_info: Optional company information
            salary_range: Optional salary range
            benefits: Optional list of benefits
            
        Returns:
            dict: Generated job description with structured content
        """
        try:
            # Prepare requirements sections
            required_qualifications = [
                req['requirement'] for req in requirements if req.get('is_required', True)
            ]
            preferred_qualifications = [
                req['requirement'] for req in requirements if not req.get('is_required', True)
            ]
            
            # Build company section
            company_section = ""
            if company_info:
                company_section = f"""
COMPANY INFORMATION:
- Name: {company_info.get('name', 'Our Company')}
- Description: {company_info.get('description', 'A leading organization')}
- Industry: {company_info.get('industry', 'Technology')}
- Values: {', '.join(company_info.get('values', ['Innovation', 'Excellence']))}
"""
            
            # Build benefits section
            benefits_section = ""
            if benefits:
                benefits_section = f"""
BENEFITS:
{chr(10).join(f'- {benefit}' for benefit in benefits)}
"""
            
            # Build salary section
            salary_section = ""
            if salary_range:
                salary_section = f"\nSALARY RANGE: {salary_range}"
            
            # Create prompt
            prompt = f"""
You are an expert HR professional and technical recruiter. Generate a compelling, professional job description that will attract top talent.

JOB DETAILS:
- Title: {job_title}
- Level: {job_level}
- Department: {department}
- Location: {location}
- Employment Type: {employment_type}
{salary_section}

{company_section}

KEY RESPONSIBILITIES:
{chr(10).join(f'- {resp}' for resp in responsibilities)}

REQUIRED QUALIFICATIONS:
{chr(10).join(f'- {req}' for req in required_qualifications)}

PREFERRED QUALIFICATIONS:
{chr(10).join(f'- {pref}' for pref in preferred_qualifications) if preferred_qualifications else '(None specified)'}

{benefits_section}

Generate a comprehensive job description in the following JSON format (respond with ONLY valid JSON, no additional text):
{{
    "title": "{job_title}",
    "company_overview": "A compelling 2-3 sentence overview about the company and its mission (if company info provided, otherwise omit)",
    "job_summary": "An engaging 2-3 sentence summary that captures the essence of the role and its impact",
    "key_responsibilities": [
        "Detailed responsibility 1",
        "Detailed responsibility 2",
        "..."
    ],
    "required_qualifications": [
        "Clear, specific required qualification 1",
        "Clear, specific required qualification 2",
        "..."
    ],
    "preferred_qualifications": [
        "Desirable qualification 1",
        "Desirable qualification 2",
        "..."
    ],
    "benefits_section": "A well-formatted benefits section (if benefits provided)",
    "how_to_apply": "Instructions on how to apply (use standard text if not specified)",
    "full_description": "A complete, well-formatted job description combining all sections in a professional manner"
}}

Guidelines:
- Make the description engaging and authentic
- Use action-oriented language
- Be specific about expectations
- Highlight what makes this opportunity unique
- Maintain professional tone throughout
- Ensure inclusivity in language
- Make it ATS-friendly with relevant keywords
- Format the full_description as a polished, ready-to-publish job posting
"""
            
            # Get response from LLM
            response = self.llm.invoke(prompt)
            response_text = response.content.strip()
            
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in LLM response")
            
            json_text = response_text[start_idx:end_idx]
            jd_content = json.loads(json_text)
            
            logger.info(f"Successfully generated job description for: {job_title}")
            
            return {
                "success": True,
                "data": jd_content
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON from LLM response: {e}")
            logger.error(f"Response text: {response_text}")
            return {
                "success": False,
                "error": "Failed to parse job description from AI response"
            }
        except Exception as e:
            logger.error(f"Error generating job description: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_section(self, section_type: str, context: Dict[str, Any]) -> str:
        """
        Generate a specific section of a job description
        
        Useful for regenerating individual sections without redoing the entire JD
        
        Args:
            section_type: Type of section (e.g., "summary", "responsibilities", "qualifications")
            context: Context information for generation
            
        Returns:
            str: Generated section content
        """
        try:
            if section_type == "summary":
                prompt = f"""
Generate a compelling job summary for:
- Title: {context.get('title')}
- Level: {context.get('level')}
- Department: {context.get('department')}

Make it engaging and highlight the impact of the role. Return only the summary text (2-3 sentences).
"""
            elif section_type == "responsibilities":
                prompt = f"""
Expand and improve these job responsibilities:
{chr(10).join(f'- {r}' for r in context.get('responsibilities', []))}

Make them more detailed, specific, and action-oriented. Return as a bullet list.
"""
            elif section_type == "qualifications":
                prompt = f"""
Refine and expand these qualifications for a {context.get('title')} role:
{chr(10).join(f'- {q}' for q in context.get('qualifications', []))}

Make them clear, specific, and comprehensive. Return as a bullet list.
"""
            else:
                return "Unknown section type"
            
            response = self.llm.invoke(prompt)
            return response.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating section {section_type}: {e}")
            return f"Error: {str(e)}"
    
    def improve_existing_jd(self, existing_jd: str, improvements: List[str]) -> str:
        """
        Improve an existing job description based on feedback
        
        Args:
            existing_jd: Current job description text
            improvements: List of specific improvements to make
            
        Returns:
            str: Improved job description
        """
        try:
            prompt = f"""
Improve the following job description based on these requirements:

CURRENT JOB DESCRIPTION:
{existing_jd}

IMPROVEMENTS NEEDED:
{chr(10).join(f'- {imp}' for imp in improvements)}

Return the improved job description maintaining the same structure but incorporating all requested improvements.
"""
            
            response = self.llm.invoke(prompt)
            return response.content.strip()
            
        except Exception as e:
            logger.error(f"Error improving job description: {e}")
            return existing_jd
    
    def extract_keywords(self, job_description: str) -> List[str]:
        """
        Extract relevant keywords from a job description for SEO/ATS optimization
        
        Args:
            job_description: Job description text
            
        Returns:
            List[str]: Extracted keywords
        """
        try:
            prompt = f"""
Extract the most important keywords from this job description for ATS and SEO optimization:

{job_description}

Return ONLY a JSON array of keywords (15-20 keywords max), no additional text:
["keyword1", "keyword2", ...]
"""
            
            response = self.llm.invoke(prompt)
            response_text = response.content.strip()
            
            # Extract JSON array
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx != -1 and end_idx > 0:
                keywords = json.loads(response_text[start_idx:end_idx])
                return keywords
            
            return []
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []

