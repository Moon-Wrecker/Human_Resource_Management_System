"""
Main FastAPI Application
GenAI HRMS Backend API
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import SQLAlchemyError
import time
import logging
import os

from config import settings, create_upload_directories
from database import engine, create_tables

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app with comprehensive metadata
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
# PulseTrack HRMS - GenAI-Powered Human Resource Management System

## Overview
PulseTrack HRMS is a comprehensive, AI-powered Human Resource Management System designed to revolutionize 
workforce management by making HR processes smarter, faster, and more human-centric.

## Key Features
- 🤖 **AI-Powered**: Integrated GenAI services (Policy RAG, Resume Screening, JD Generation)
- 👥 **Multi-Role Support**: HR, Managers, Employees, Executives, IT Admins
- 📊 **Real-time Dashboards**: Role-specific dashboards with analytics
- 🎯 **Performance Tracking**: Goals, feedback, and skill development
- 📋 **Leave Management**: Comprehensive leave and attendance tracking
- 💼 **Recruitment**: Job posting, applications, AI resume screening
- 📄 **Policy Management**: 24/7 AI chatbot for policy queries

## GenAI Integrations
- **Google Gemini API**: For natural language processing and content generation
- **ChromaDB**: Vector database for semantic search
- **Langchain**: RAG pipeline orchestration
- **PyPDF2**: Document processing

## User Stories Implemented (16 Total)
### HR Manager (6)
1. Dashboard Monitoring - Real-time workforce analytics
2. Job Description Management - AI-powered JD generation
3. Job Posting Management - Centralized job portal
4. Employee Database - Complete employee information system
5. Resume Screening - AI-powered candidate matching
6. Policy Access - 24/7 self-service policy portal

### Employee (4)
7. Performance Tracking - View metrics and feedback
8. Payslip Access - Download monthly payslips
9. Leave Notifications - Timely approval notifications
10. Policy Queries - AI chatbot for instant answers

### Team Lead (4)
11. Skill Development - Team skill module access
12. Goal Setting - Set and track employee goals
13. Team Performance Dashboard - Monitor team progress
14. Employee Reviews - Provide continuous feedback

### Executive (1)
15. Strategic Analytics - High-level HR insights

### IT Administrator (1)
16. System Administration - User roles and permissions

## Authentication
All endpoints require JWT authentication unless specified otherwise.
Include the JWT token in the Authorization header: `Bearer <token>`

## Error Handling
All endpoints follow consistent error response format with proper HTTP status codes.

## Documentation
- Interactive API Docs: /api/docs (Swagger UI)
- Alternative Docs: /api/redoc (ReDoc)
- OpenAPI JSON: /api/openapi.json
- OpenAPI YAML: /api/openapi.yaml (downloadable)
    """,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    contact={
        "name": "PulseTrack HRMS Team 11",
        "email": "support@pulsetrack-hrms.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=[
        {"name": "Root", "description": "Root and health check endpoints"},
        {"name": "Health", "description": "Health check endpoints"},
        {"name": "API", "description": "API information endpoints"},
        {"name": "Authentication", "description": "User authentication and authorization"},
        {"name": "Dashboard", "description": "Role-specific dashboard endpoints - **User Stories: Dashboard Monitoring, Team Performance Dashboard, Strategic Analytics**"},
        {"name": "Employee Management", "description": "Employee CRUD operations (HR only) - **User Story: Employee Database**"},
        {"name": "Profile", "description": "User profile management"},
        {"name": "Attendance", "description": "Attendance tracking and management"},
        {"name": "Leave Management", "description": "Leave requests and approvals - **User Story: Leave Notifications**"},
        {"name": "Job Listings", "description": "Job listings management - **User Story: Job Posting Management**"},
        {"name": "Applications", "description": "Job applications management"},
        {"name": "Feedback", "description": "Performance feedback system - **User Stories: Performance Tracking, Employee Reviews**"},
        {"name": "Payslips", "description": "Payslip management and access - **User Story: Payslip Access**"},
        {"name": "Goals & Task Management", "description": "Goal setting and tracking - **User Story: Goal Setting**"},
        {"name": "Skills/Modules Management", "description": "Skill development and modules - **User Story: Skill Development**"},
        {"name": "Policies", "description": "Company policy management"},
        {"name": "Announcements", "description": "Company announcements"},
        {"name": "Holidays", "description": "Holiday calendar management"},
        {"name": "Departments", "description": "Department management"},
        {"name": "Organization/Hierarchy", "description": "Organization structure"},
        {"name": "Team Requests", "description": "Various employee requests (WFH, equipment, etc.)"},
        {"name": "AI - Policy RAG", "description": "**[GenAI]** AI-powered policy Q&A chatbot - **User Stories: Policy Access, Policy Queries**"},
        {"name": "AI - Resume Screener", "description": "**[GenAI]** AI-powered resume screening - **User Story: Resume Screening**"},
        {"name": "AI - Job Description Generator", "description": "**[GenAI]** AI-powered JD generation - **User Story: Job Description Management**"},
        {"name": "AI Performance Reports", "description": "**[GenAI]** AI-powered performance reports - Individual, team, and organization-wide analysis"}
    ]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request data",
                "details": exc.errors()
            }
        }
    )

@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors"""
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "DATABASE_ERROR",
                "message": "A database error occurred"
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    logger.error(f"Unhandled error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal server error occurred"
            }
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Database: {settings.DATABASE_URL}")
    
    # Create upload directories
    create_upload_directories()
    
    # Create database tables
    try:
        create_tables()
        logger.info("Database tables created/verified")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info(f"Shutting down {settings.APP_NAME}")

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information"""
    return {
        "success": True,
        "data": {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "docs": "/api/docs",
            "status": "running"
        }
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
            "version": settings.APP_VERSION
        }
    }

# OpenAPI YAML endpoint
@app.get("/api/openapi.yaml", tags=["API"], include_in_schema=False)
async def get_openapi_yaml():
    """
    Download OpenAPI specification as YAML
    
    Provides the complete API specification in YAML format, compatible with Swagger and other tools.
    """
    from fastapi.responses import Response
    import yaml
    
    openapi_schema = app.openapi()
    yaml_content = yaml.dump(openapi_schema, sort_keys=False, default_flow_style=False, allow_unicode=True)
    
    return Response(
        content=yaml_content,
        media_type="application/x-yaml",
        headers={
            "Content-Disposition": "attachment; filename=openapi.yaml"
        }
    )

# API v1 Router placeholder
@app.get("/api/v1", tags=["API"])
async def api_v1_root():
    """API v1 root endpoint"""
    return {
        "success": True,
        "data": {
            "version": "1.0",
            "message": "GenAI HRMS API v1",
            "endpoints": {
                "auth": "/api/v1/auth",
                "profile": "/api/v1/profile",
                "dashboard": "/api/v1/dashboard",
                "users": "/api/v1/users",
                "jobs": "/api/v1/jobs",
                "applications": "/api/v1/applications",
                "feedback": "/api/v1/feedback",
                "payslips": "/api/v1/payslips",
                "employees": "/api/v1/employees",
                "attendance": "/api/v1/attendance",
                "leaves": "/api/v1/leaves",
                "goals": "/api/v1/goals",
                "skills": "/api/v1/skills",
                "requests": "/api/v1/requests",
                "announcements": "/api/v1/announcements",
                "policies": "/api/v1/policies",
                "holidays": "/api/v1/holidays",
                "departments": "/api/v1/departments",
                "organization": "/api/v1/organization",
                "ai_policy_rag": "/api/v1/ai/policy-rag",
                "ai_resume_screener": "/api/v1/ai/resume-screener",
                "ai_job_description": "/api/v1/ai/job-description",
                "ai_performance_report": "/api/v1/ai/performance-report"
            },
            "documentation": {
                "swagger_ui": "/api/docs",
                "redoc": "/api/redoc",
                "openapi_json": "/api/openapi.json",
                "openapi_yaml": "/api/openapi.yaml"
            }
        }
    }

# Import and include routers
from routes.auth import router as auth_router
from routes.dashboard import router as dashboard_router
from routes.profile import router as profile_router
from routes.attendance import router as attendance_router
from routes.jobs import router as jobs_router
from routes.applications import router as applications_router
from routes.announcements import router as announcements_router
from routes.policies import router as policies_router
from routes.feedback import router as feedback_router
from routes.payslips import router as payslips_router
from routes.holidays import router as holidays_router
from routes.departments import router as departments_router
from routes.organization import router as organization_router
from routes.employees import router as employees_router
from routes.leaves import router as leaves_router
from routes.skills import router as skills_router
from routes.requests import router as requests_router
from routes.goals import router as goals_router

# Import AI routers (optional - will load if dependencies available)
try:
    from routes.ai_policy_rag import router as ai_policy_rag_router
    from routes.ai_resume_screener import router as ai_resume_screener_router
    from routes.ai_job_description import router as ai_job_description_router
    from routes.ai_performance_report import router as ai_performance_report_router
    AI_ROUTES_AVAILABLE = True
    logger.info("AI services routes loaded successfully")
except ImportError as e:
    AI_ROUTES_AVAILABLE = False
    logger.warning(f"AI services not available: {e}")
    logger.warning("Install AI dependencies with: pip install -r requirements_ai.txt")

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(profile_router, prefix="/api/v1")
app.include_router(attendance_router, prefix="/api/v1")
app.include_router(jobs_router, prefix="/api/v1")
app.include_router(applications_router, prefix="/api/v1")
app.include_router(announcements_router, prefix="/api/v1")
app.include_router(policies_router, prefix="/api/v1")
app.include_router(feedback_router, prefix="/api/v1")
app.include_router(payslips_router, prefix="/api/v1")
app.include_router(holidays_router, prefix="/api/v1")
app.include_router(departments_router, prefix="/api/v1")
app.include_router(organization_router, prefix="/api/v1")
app.include_router(employees_router, prefix="/api/v1")
app.include_router(leaves_router, prefix="/api/v1")
app.include_router(skills_router, prefix="/api/v1")
app.include_router(requests_router, prefix="/api/v1")
app.include_router(goals_router, prefix="/api/v1")

# Include AI routers if available
if AI_ROUTES_AVAILABLE:
    app.include_router(ai_policy_rag_router, prefix="/api/v1")
    app.include_router(ai_resume_screener_router, prefix="/api/v1")
    app.include_router(ai_job_description_router, prefix="/api/v1")
    app.include_router(ai_performance_report_router, prefix="/api/v1")
    logger.info("AI routes registered: Policy RAG, Resume Screener, JD Generator, Performance Reports")

# Mount static files for uploads (must be after routers)
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# More routers will be added as we build them
# from routes.users import router as users_router
# app.include_router(users_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )

