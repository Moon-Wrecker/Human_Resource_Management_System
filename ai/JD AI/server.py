
import os
import logging
from typing import List, Optional, Dict, Any

import uvicorn
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
load_dotenv()
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("job_description_api")

# Initialize FastAPI app
app = FastAPI(
    title="Job Description Generator API",
    description="API for generating professional job descriptions using LangChain and Gemini models",
    version="1.0.0",
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Models for the API -----

class CompanyInfoRequest(BaseModel):
    """Information about the company"""
    name: str = Field(..., description="Company name")
    description: str = Field(..., description="Brief description of the company")
    industry: str = Field(..., description="Industry the company operates in")
    values: Optional[List[str]] = Field(None, description="Company values or culture points")

class JobRequirementRequest(BaseModel):
    """Requirement for a job position"""
    requirement: str = Field(..., description="Specific job requirement")
    is_required: bool = Field(..., description="Whether this requirement is mandatory or preferred")

class JobDescriptionRequest(BaseModel):
    """Request model for job description generation"""
    job_title: str = Field(..., description="Title of the job position")
    job_level: str = Field(..., description="Level of the position (entry, mid, senior, etc.)")
    department: str = Field(..., description="Department the role belongs to")
    location: str = Field(..., description="Job location, can be remote, hybrid or specific location")
    employment_type: str = Field(..., description="Type of employment (full-time, part-time, contract)")
    company_info: CompanyInfoRequest = Field(..., description="Information about the company")
    responsibilities: List[str] = Field(..., description="List of job responsibilities")
    requirements: List[JobRequirementRequest] = Field(..., description="List of job requirements with is_required flag")
    salary_range: Optional[str] = Field(None, description="Optional salary range")
    benefits: Optional[List[str]] = Field(None, description="List of benefits offered")
    application_process: Optional[str] = Field(None, description="Description of the application process")

class JobDescriptionResponseContent(BaseModel):
    """Content of the job description response"""
    title: str = Field(..., description="Job title with level")
    company_overview: str = Field(..., description="Brief overview of the company")
    job_summary: str = Field(..., description="Summary of the job position")
    key_responsibilities: List[str] = Field(..., description="List of key responsibilities")
    required_qualifications: List[str] = Field(..., description="List of required qualifications")
    preferred_qualifications: List[str] = Field(..., description="List of preferred qualifications")
    benefits_section: Optional[str] = Field(None, description="Benefits section if provided")
    how_to_apply: Optional[str] = Field(None, description="Application instructions if provided")
    full_description: str = Field(..., description="Complete formatted job description text")

class JobDescriptionResponse(BaseModel):
    """Response model for job description generation"""
    status: str = Field(..., description="Status of the request (success or error)")
    data: Optional[JobDescriptionResponseContent] = Field(None, description="Generated job description data")
    error: Optional[str] = Field(None, description="Error message if status is error")

# ----- Job Description Generator -----

class JobDescriptionGenerator:
    """Generator class for creating job descriptions using LangChain and Gemini"""
    
    def __init__(self, model_name: str, api_key: str, temperature: float = 0.2):
        """Initialize the generator with the specified Gemini model"""
        self.model = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=api_key
        )
        
        # Define output structure
        class JobDescriptionOutput(BaseModel):
            """Structure for the generated job description"""
            title: str = Field(description="Job title with level")
            company_overview: str = Field(description="Brief overview of the company")
            job_summary: str = Field(description="Summary of the job position")
            key_responsibilities: List[str] = Field(description="List of key responsibilities")
            required_qualifications: List[str] = Field(description="List of required qualifications")
            preferred_qualifications: List[str] = Field(description="List of preferred qualifications")
            benefits_section: Optional[str] = Field(None, description="Benefits section if provided")
            how_to_apply: Optional[str] = Field(None, description="Application instructions if provided")
            full_description: str = Field(description="Complete formatted job description text")
        
        self.output_class = JobDescriptionOutput
        
        # Create parser
        self.parser = PydanticOutputParser(pydantic_object=self.output_class)
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_template("""
            You are an expert HR professional and job description writer. Create a professional job description based on the following information:

            Job Title: {job_title}
            Job Level: {job_level}
            Department: {department}
            Location: {location}
            Employment Type: {employment_type}
            
            Company Information:
            Company Name: {company_name}
            Company Description: {company_description}
            Industry: {company_industry}
            Company Values: {company_values}
            
            Responsibilities:
            {responsibilities}
            
            Requirements:
            {requirements}
            
            Salary Range (if provided): {salary_range}
            Benefits (if provided): {benefits}
            Application Process (if provided): {application_process}
            
            Create a professional, well-structured job description that will attract qualified candidates. Use clear headings and bullet points where appropriate. 
            Ensure the language is inclusive and engaging. The job description should include a compelling summary, detailed responsibilities, clear qualifications 
            (separated into required and preferred), benefits information, and application instructions.
            
            {format_instructions}
        """)
        
        # Create the chain
        self.chain = self.prompt | self.model | self.parser
    
    def _format_responsibilities(self, responsibilities: List[str]) -> str:
        """Format the responsibilities list for the prompt"""
        return "\n".join([f"- {r}" for r in responsibilities])
    
    def _format_requirements(self, requirements: List[Dict[str, Any]]) -> str:
        """Format the requirements list for the prompt"""
        req_list = []
        for req in requirements:
            prefix = "Required: " if req.get("is_required", True) else "Preferred: "
            req_list.append(f"- {prefix}{req['requirement']}")
        return "\n".join(req_list)
    
    def _format_company_values(self, values: Optional[List[str]]) -> str:
        """Format company values if provided"""
        if not values:
            return "N/A"
        return ", ".join(values)
    
    def _format_benefits(self, benefits: Optional[List[str]]) -> str:
        """Format benefits if provided"""
        if not benefits:
            return "N/A"
        return "\n".join([f"- {b}" for b in benefits])
    
    def generate(self, job_request: JobDescriptionRequest) -> Dict[str, Any]:
        """Generate a job description based on the provided request"""
        # Prepare requirements list in the format expected by the formatter
        requirements = [
            {"requirement": req.requirement, "is_required": req.is_required}
            for req in job_request.requirements
        ]
        
        # Prepare inputs for the prompt
        inputs = {
            "job_title": job_request.job_title,
            "job_level": job_request.job_level,
            "department": job_request.department,
            "location": job_request.location,
            "employment_type": job_request.employment_type,
            "company_name": job_request.company_info.name,
            "company_description": job_request.company_info.description,
            "company_industry": job_request.company_info.industry,
            "company_values": self._format_company_values(job_request.company_info.values),
            "responsibilities": self._format_responsibilities(job_request.responsibilities),
            "requirements": self._format_requirements(requirements),
            "salary_range": job_request.salary_range if job_request.salary_range else "N/A",
            "benefits": self._format_benefits(job_request.benefits),
            "application_process": job_request.application_process if job_request.application_process else "N/A",
            "format_instructions": self.parser.get_format_instructions()
        }
        
        # Generate job description using the chain
        return self.chain.invoke(inputs).dict()

# ----- API Configuration -----
# Get API key from environment variable
GOOGLE_API_KEY = "AIzaSyDV1Wvu-i1vXOAbfCzDdjvCp4ap722z13E"
print(GOOGLE_API_KEY,"this is the key")
MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-2.5-flash-lite")
TEMPERATURE = float(os.environ.get("GEMINI_TEMPERATURE", "0.2"))

# ----- API Endpoints -----

@app.get("/", tags=["Status"])
async def root():
    """Root endpoint - check if API is running"""
    return {"status": "success", "message": "Job Description Generator API is running"}

@app.get("/health", tags=["Status"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/generate", response_model=JobDescriptionResponse, tags=["Generation"])
async def generate_job_description(request: JobDescriptionRequest):
    """
    Generate a job description based on the provided information
    
    This endpoint takes job details and company information and generates
    a professional job description using LangChain and Google's Gemini models.
    """
    try:
        # Check if API key is available
        if not GOOGLE_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Google API key is not configured. Set the GOOGLE_API_KEY environment variable."
            )
        
        # Initialize generator
        generator = JobDescriptionGenerator(
            model_name=MODEL_NAME,
            api_key=GOOGLE_API_KEY,
            temperature=TEMPERATURE
        )
        
        # Generate job description
        job_description = generator.generate(request)
        
        # Return successful response
        return {
            "status": "success",
            "data": job_description,
            "error": None
        }
    except ValueError as e:
        # Handle validation errors
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Error generating job description: {str(e)}")
        return {
            "status": "error",
            "data": None,
            "error": f"Error generating job description: {str(e)}"
        }

# ----- Error Handling -----

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions and return structured response"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "data": None,
            "error": exc.detail
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions and return structured response"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "data": None,
            "error": f"An unexpected error occurred: {str(exc)}"
        }
    )

# ----- Main Function -----

if __name__ == "__main__":
    # Check if API key is set
    if not GOOGLE_API_KEY:
        logger.warning("GOOGLE_API_KEY environment variable is not set. API will not function correctly.")
        print("\n⚠️  WARNING: GOOGLE_API_KEY environment variable is not set!")
        print("Please set it with: export GOOGLE_API_KEY=your_api_key_here\n")
    
    # Get port from environment or use default
    port = int(os.environ.get("PORT", "8000"))
    
    # Print startup message
    print(f"\n🚀 Starting Job Description Generator API on http://localhost:{port}")
    print(f"📚 API documentation will be available at http://localhost:{port}/docs")
    print("\nPress Ctrl+C to stop the server\n")
    
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=port)
