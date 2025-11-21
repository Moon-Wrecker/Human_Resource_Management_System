import os
import json
import time
import tempfile
import logging
import shutil
import traceback
from pathlib import Path
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

import uvicorn
from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Import updated resume screener
from resume_screener import ResumeScreener, ResumeAnalysis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler("resume_api.log")  # Also log to file
    ]
)
logger = logging.getLogger("resume_screener_api")

# Initialize FastAPI app
app = FastAPI(
    title="Resume Screener API",
    description="API for screening resumes against job descriptions using Gemini multimodal models",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Create upload and results directories
UPLOAD_DIR = Path("./uploads")
RESULTS_DIR = Path("./results")
FRONTEND_DIR = Path("./frontend")

# Ensure directories exist
UPLOAD_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)
FRONTEND_DIR.mkdir(exist_ok=True)

# Initialize screener
API_KEY = os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    # Use the key from your original file as fallback
    API_KEY = "AIzaSyDV1Wvu-i1vXOAbfCzDdjvCp4ap722z13E"
    logger.warning("Using hardcoded API key since GOOGLE_API_KEY environment variable is not set")

MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-2.5-flash")  # Using model with vision capabilities

try:
    logger.info(f"Initializing screener with model: {MODEL_NAME}")
    screener = ResumeScreener(
        model_name=MODEL_NAME,
        api_key=API_KEY,
        max_workers=4
    )
    logger.info("Screener initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize screener: {str(e)}")
    logger.error(traceback.format_exc())
    # Continue running the app, but the endpoints will fail

# Define request/response models
class SingleScreenRequest(BaseModel):
    job_description: str
    
class BatchScreenRequest(BaseModel):
    job_description: str
    output_format: str = "excel"

class ScreeningResponse(BaseModel):
    status: str
    message: str
    result: Optional[Dict[str, Any]] = None
    result_file: Optional[str] = None

class JobDescriptionRequest(BaseModel):
    title: str
    company: str
    description: str

# Background task for batch processing
def process_batch_resumes(
    resume_files: List[str],
    job_description: str,
    output_format: str,
    task_id: str
):
    """Process batch of resumes in background
    
    Args:
        resume_files: List of resume file paths
        job_description: Job description text
        output_format: Output format (csv, excel, json)
        task_id: Unique ID for this task
    """
    try:
        logger.info(f"Starting batch processing task: {task_id}")
        
        # Create output file path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if output_format == "csv":
            output_file = RESULTS_DIR / f"resume_analysis_{task_id}_{timestamp}.csv"
        elif output_format == "excel":
            output_file = RESULTS_DIR / f"resume_analysis_{task_id}_{timestamp}.xlsx"
        else:
            output_file = RESULTS_DIR / f"resume_analysis_{task_id}_{timestamp}.json"
        
        # Process resumes
        summary = screener.screen_multiple_resumes(
            resume_dir_or_paths=resume_files,
            job_description=job_description,
            output_format=output_format,
            output_path=str(output_file)
        )
        
        # Save task result
        task_result = {
            "status": "completed",
            "summary": summary,
            "output_file": str(output_file.name)
        }
        
        # Save task result to file
        with open(RESULTS_DIR / f"{task_id}_result.json", "w") as f:
            json.dump(task_result, f)
        
        logger.info(f"Batch processing completed for task: {task_id}")
        
    except Exception as e:
        logger.error(f"Error in background task {task_id}: {str(e)}")
        logger.error(traceback.format_exc())
        
        # Save error to file
        error_result = {
            "status": "error",
            "error": str(e)
        }
        with open(RESULTS_DIR / f"{task_id}_result.json", "w") as f:
            json.dump(error_result, f)

# Endpoints
@app.get("/", tags=["Status"])
async def root():
    """Root endpoint to check if API is running"""
    return {"status": "success", "message": "Resume Screener API is running with Gemini multimodal support"}

@app.get("/health", tags=["Status"])
async def health_check():
    """Health check endpoint"""
    # Check if API key is set
    if not API_KEY:
        return {"status": "warning", "message": "GOOGLE_API_KEY not set. API will not function correctly."}
    
    # Test connection to Gemini API
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            temperature=0.1,
            google_api_key=API_KEY
        )
        response = llm.invoke("Respond with 'OK' if you can receive this message.")
        if "OK" in response.content:
            return {"status": "healthy", "message": "API is healthy and Gemini connection is working"}
        else:
            return {"status": "warning", "message": f"Gemini API connection test received unexpected response: {response.content[:50]}..."}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "error", "message": f"API health check failed: {str(e)}"}

@app.post("/screen/single", response_model=ScreeningResponse, tags=["Screening"])
async def screen_single_resume(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...),
):
    """Screen a single resume against a job description"""
    
    if not API_KEY:
        logger.error("API key not set")
        raise HTTPException(
            status_code=500,
            detail="GOOGLE_API_KEY not set. API will not function correctly."
        )
    
    try:
        # Log received information
        logger.info(f"Received resume: {resume_file.filename}, content type: {resume_file.content_type}")
        logger.info(f"Job description length: {len(job_description)} characters")
        
        # Create temp directory for file
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = Path(temp_dir) / resume_file.filename
            
            # Save uploaded file
            try:
                with open(temp_file_path, "wb") as f:
                    content = await resume_file.read()
                    f.write(content)
                logger.info(f"Resume saved to temporary path: {temp_file_path}, size: {os.path.getsize(temp_file_path)} bytes")
            except Exception as e:
                logger.error(f"Error saving file: {str(e)}")
                logger.error(traceback.format_exc())
                raise HTTPException(
                    status_code=500,
                    detail=f"Error saving uploaded file: {str(e)}"
                )
            
            # Process resume
            try:
                logger.info("Starting resume analysis...")
                analysis = screener.screen_single_resume(str(temp_file_path), job_description)
                
                # Generate explanation
                explanation = screener.explain_analysis(analysis)
                logger.info(f"Analysis completed successfully. Fit score: {analysis['overall_fit_score']}")
            except Exception as e:
                logger.error(f"Error in resume analysis: {str(e)}")
                logger.error(traceback.format_exc())
                raise HTTPException(
                    status_code=500,
                    detail=f"Error analyzing resume: {str(e)}"
                )
        
        # Return results
        return {
            "status": "success",
            "message": "Resume screened successfully",
            "result": {
                "analysis": analysis,
                "explanation": explanation
            },
            "result_file": None
        }
    
    except Exception as e:
        if not isinstance(e, HTTPException):
            logger.error(f"Unexpected error screening resume: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"Error screening resume: {str(e)}"
            )
        else:
            raise

@app.post("/screen/batch", response_model=ScreeningResponse, tags=["Screening"])
async def screen_batch_resumes(
    background_tasks: BackgroundTasks,
    job_description: str = Form(...),
    resume_files: List[UploadFile] = File(...),
    output_format: str = Form("excel")
):
    """Screen multiple resumes against a job description (async batch process)"""
    
    if not API_KEY:
        logger.error("API key not set for batch processing")
        raise HTTPException(
            status_code=500,
            detail="GOOGLE_API_KEY not set. API will not function correctly."
        )
    
    try:
        # Validate output format
        if output_format not in ["csv", "excel", "json"]:
            logger.error(f"Invalid output format: {output_format}")
            raise HTTPException(
                status_code=400,
                detail="Invalid output format. Must be 'csv', 'excel', or 'json'."
            )
        
        # Create task ID
        task_id = f"task_{int(time.time())}"
        task_dir = UPLOAD_DIR / task_id
        task_dir.mkdir(exist_ok=True)
        
        # Log files received
        logger.info(f"Received {len(resume_files)} files for batch processing")
        for i, file in enumerate(resume_files):
            logger.info(f"  File {i+1}: {file.filename}, content type: {file.content_type}")
        
        # Save uploaded files
        saved_files = []
        for resume_file in resume_files:
            try:
                file_path = task_dir / resume_file.filename
                with open(file_path, "wb") as f:
                    content = await resume_file.read()
                    f.write(content)
                saved_files.append(str(file_path))
                logger.info(f"Saved {resume_file.filename} to {file_path}")
            except Exception as e:
                logger.error(f"Error saving file {resume_file.filename}: {str(e)}")
                logger.error(traceback.format_exc())
                raise HTTPException(
                    status_code=500,
                    detail=f"Error saving uploaded file {resume_file.filename}: {str(e)}"
                )
        
        # Start background task
        logger.info(f"Starting batch task {task_id} with {len(saved_files)} files")
        background_tasks.add_task(
            process_batch_resumes,
            saved_files,
            job_description,
            output_format,
            task_id
        )
        
        # Return task ID
        return {
            "status": "processing",
            "message": f"Batch processing started. Task ID: {task_id}",
            "result": {"task_id": task_id},
            "result_file": None
        }
    
    except Exception as e:
        if not isinstance(e, HTTPException):
            logger.error(f"Unexpected error in batch process: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"Error starting batch process: {str(e)}"
            )
        else:
            raise

@app.get("/task/{task_id}/status", response_model=ScreeningResponse, tags=["Tasks"])
async def check_task_status(task_id: str):
    """Check status of a batch processing task"""
    
    # Check if result file exists
    result_file = RESULTS_DIR / f"{task_id}_result.json"
    
    if not result_file.exists():
        logger.info(f"Task {task_id} is still processing")
        return {
            "status": "processing",
            "message": "Task is still processing",
            "result": {"task_id": task_id},
            "result_file": None
        }
    
    # Read result file
    try:
        with open(result_file, "r") as f:
            result = json.load(f)
        
        if result["status"] == "error":
            logger.warning(f"Task {task_id} failed: {result.get('error', 'Unknown error')}")
            return {
                "status": "error",
                "message": f"Task failed: {result.get('error', 'Unknown error')}",
                "result": {"task_id": task_id, "error": result.get("error", "Unknown error")},
                "result_file": None
            }
        
        # Task completed successfully
        logger.info(f"Task {task_id} completed successfully")
        return {
            "status": "completed",
            "message": "Task completed successfully",
            "result": {"task_id": task_id, "summary": result["summary"]},
            "result_file": result["output_file"]
        }
    except Exception as e:
        logger.error(f"Error reading task result file: {str(e)}")
        return {
            "status": "error",
            "message": f"Error reading task result: {str(e)}",
            "result": {"task_id": task_id, "error": str(e)},
            "result_file": None
        }

@app.get("/download/{filename}", tags=["Results"])
async def download_result(filename: str):
    """Download a result file"""
    
    file_path = RESULTS_DIR / filename
    
    if not file_path.exists():
        logger.error(f"Download requested for non-existent file: {filename}")
        raise HTTPException(
            status_code=404,
            detail=f"File not found: {filename}"
        )
    
    # Determine content type
    if filename.endswith(".csv"):
        media_type = "text/csv"
    elif filename.endswith(".xlsx"):
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    else:  # json
        media_type = "application/json"
    
    logger.info(f"Serving download for: {filename}, media type: {media_type}")
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=media_type
    )

@app.post("/job-description/generate", tags=["Job Description"])
async def generate_job_description(request: JobDescriptionRequest):
    """Generate a more detailed job description based on basic information"""
    
    if not API_KEY:
        logger.error("API key not set for job description generation")
        raise HTTPException(
            status_code=500,
            detail="GOOGLE_API_KEY not set. API will not function correctly."
        )
    
    try:
        # Set up prompt and LLM
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.output_parsers import StrOutputParser
        
        logger.info(f"Generating job description for: {request.title} at {request.company}")
        
        prompt = ChatPromptTemplate.from_template("""
            You are an expert HR professional. Create a comprehensive job description for the following position:
            
            Job Title: {title}
            Company: {company}
            Basic Description: {description}
            
            Please expand this into a full job description including:
            - A detailed overview of the role
            - Key responsibilities
            - Required qualifications and experience
            - Preferred qualifications
            - Benefits and perks (use standard benefits if not specified)
            
            Format the description with proper sections and bullet points for clarity.
        """)
        
        llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            temperature=0.3,
            google_api_key=API_KEY
        )
        
        chain = prompt | llm | StrOutputParser()
        
        # Generate job description
        job_description = chain.invoke({
            "title": request.title,
            "company": request.company,
            "description": request.description
        })
        
        logger.info(f"Job description generated successfully ({len(job_description)} chars)")
        
        return {
            "status": "success",
            "message": "Job description generated successfully",
            "result": {"job_description": job_description},
            "result_file": None
        }
    
    except Exception as e:
        logger.error(f"Error generating job description: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error generating job description: {str(e)}"
        )

# Setup frontend
@app.get("/setup-frontend", tags=["Admin"])
async def setup_frontend():
    """Setup the frontend by copying template to index.html"""
    try:
        # Create the frontend directory if it doesn't exist
        FRONTEND_DIR.mkdir(exist_ok=True)
        
        # Copy the template file if it exists
        src_html = Path("./frontend_template.html")
        dest_html = FRONTEND_DIR / "index.html"
        
        if not src_html.exists():
            return {
                "status": "error", 
                "message": "frontend_template.html not found in current directory"
            }
        
        shutil.copy(src_html, dest_html)
        return {
            "status": "success",
            "message": f"Frontend setup successful. Template copied to {dest_html}"
        }
    except Exception as e:
        logger.error(f"Error setting up frontend: {str(e)}")
        return {"status": "error", "message": f"Error setting up frontend: {str(e)}"}

# Serve static files
try:
    # Mount the frontend static directory
    app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")
    logger.info("Static files mounted successfully at /frontend")
except Exception as e:
    logger.error(f"Could not set up static files: {str(e)}")
    logger.error(traceback.format_exc())

# Main function
def main():
    """Main function to start the API server"""
    # Get port from environment or use default
    port = int(os.environ.get("PORT", "8000"))
    
    # Check if API key is set
    if not API_KEY:
        logger.warning("GOOGLE_API_KEY environment variable not set. Using hardcoded key.")
    
    # Check if frontend is set up
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        # Try to copy template automatically
        template_path = Path("./frontend_template.html")
        if template_path.exists():
            logger.info("Automatically copying frontend template to frontend/index.html")
            shutil.copy(template_path, index_path)
        else:
            logger.warning("Frontend index.html does not exist and template not found. Frontend will not work.")
    
    # Print startup message with model information
    print(f"\n🚀 Starting Resume Screener API using {MODEL_NAME} on http://localhost:{port}")
    print("📊 This version uses Gemini multimodal capabilities for both text analysis and image processing")
    print(f"📚 API documentation available at http://localhost:{port}/docs")
    print(f"💻 Frontend available at http://localhost:{port}/frontend")
    print("\nPress Ctrl+C to stop the server\n")
    
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
