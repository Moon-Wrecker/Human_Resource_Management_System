#!/usr/bin/env python3
"""
AI Services Setup Test Script
Tests all AI services and dependencies
"""
import sys
import os
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text.center(60)}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ️  {text}{RESET}")

# Test 1: Python Version
print_header("TEST 1: Python Version")
print(f"Python version: {sys.version}")
if sys.version_info >= (3, 9):
    print_success("Python version is compatible (3.9+)")
else:
    print_error("Python 3.9+ is required")
    sys.exit(1)

# Test 2: Core Dependencies
print_header("TEST 2: Core Dependencies")
core_deps = [
    ('fastapi', 'FastAPI'),
    ('pydantic', 'Pydantic'),
    ('sqlalchemy', 'SQLAlchemy'),
    ('uvicorn', 'Uvicorn'),
]

missing_core = []
for module, name in core_deps:
    try:
        __import__(module)
        print_success(f"{name} installed")
    except ImportError:
        print_error(f"{name} NOT installed")
        missing_core.append(module)

if missing_core:
    print_error(f"\nMissing core dependencies: {', '.join(missing_core)}")
    print_info("Install with: pip install -r requirements.txt")

# Test 3: AI Dependencies
print_header("TEST 3: AI Dependencies")
ai_deps = [
    ('langchain', 'LangChain'),
    ('langchain_google_genai', 'LangChain Google GenAI'),
    ('langchain_community', 'LangChain Community'),
    ('langchain_text_splitters', 'LangChain Text Splitters'),
    ('faiss', 'FAISS (vectorstore)'),
    ('PyPDF2', 'PyPDF2 (PDF parsing)'),
    ('google.generativeai', 'Google Generative AI'),
]

missing_ai = []
for module, name in ai_deps:
    try:
        __import__(module)
        print_success(f"{name} installed")
    except ImportError:
        print_warning(f"{name} NOT installed")
        missing_ai.append(module)

if missing_ai:
    print_warning(f"\nMissing AI dependencies: {', '.join(missing_ai)}")
    print_info("Install with: pip install -r requirements_ai.txt")

# Test 4: Environment Configuration
print_header("TEST 4: Environment Configuration")

# Check for .env file
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    print_success(f".env file exists at {env_path}")
    
    # Try to load config
    try:
        from config import settings
        print_success("Configuration loaded successfully")
        
        # Check Google API Key
        if settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY != "":
            if settings.GOOGLE_API_KEY.startswith("AIza"):
                print_success(f"Google API Key configured (starts with: {settings.GOOGLE_API_KEY[:10]}...)")
            else:
                print_warning("Google API Key set but format looks unusual")
        else:
            print_error("Google API Key NOT configured")
            print_info("Add GOOGLE_API_KEY=your_key_here to .env file")
            
    except Exception as e:
        print_error(f"Error loading configuration: {e}")
else:
    print_error(f".env file NOT found at {env_path}")
    print_info("Create .env file from .env.template")

# Test 5: Directory Structure
print_header("TEST 5: Directory Structure")
required_dirs = [
    'ai_services',
    'routes',
    'schemas',
    'services',
    'uploads',
]

for dir_name in required_dirs:
    dir_path = Path(__file__).parent / dir_name
    if dir_path.exists():
        print_success(f"{dir_name}/ directory exists")
    else:
        print_error(f"{dir_name}/ directory NOT found")

# Test 6: AI Service Files
print_header("TEST 6: AI Service Files")
ai_files = [
    'ai_services/__init__.py',
    'ai_services/policy_rag_service.py',
    'ai_services/resume_screener_service.py',
    'ai_services/job_description_generator_service.py',
    'routes/ai_policy_rag.py',
    'routes/ai_resume_screener.py',
    'routes/ai_job_description.py',
    'schemas/ai_schemas.py',
]

for file_path in ai_files:
    full_path = Path(__file__).parent / file_path
    if full_path.exists():
        print_success(f"{file_path} exists")
    else:
        print_error(f"{file_path} NOT found")

# Test 7: Import AI Services
print_header("TEST 7: Import AI Services")

if not missing_ai:
    try:
        from ai_services.policy_rag_service import PolicyRAGService
        print_success("PolicyRAGService can be imported")
    except Exception as e:
        print_error(f"PolicyRAGService import failed: {e}")
    
    try:
        from ai_services.resume_screener_service import ResumeScreenerService
        print_success("ResumeScreenerService can be imported")
    except Exception as e:
        print_error(f"ResumeScreenerService import failed: {e}")
    
    try:
        from ai_services.job_description_generator_service import JobDescriptionGeneratorService
        print_success("JobDescriptionGeneratorService can be imported")
    except Exception as e:
        print_error(f"JobDescriptionGeneratorService import failed: {e}")
else:
    print_warning("Skipping service imports (AI dependencies not installed)")

# Test 8: Initialize AI Services (if possible)
print_header("TEST 8: Initialize AI Services")

if not missing_ai:
    try:
        from config import settings
        if settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY != "":
            try:
                from ai_services.policy_rag_service import PolicyRAGService
                service = PolicyRAGService()
                print_success("Policy RAG Service initialized successfully")
            except Exception as e:
                print_error(f"Policy RAG Service initialization failed: {e}")
            
            try:
                from ai_services.resume_screener_service import ResumeScreenerService
                service = ResumeScreenerService()
                print_success("Resume Screener Service initialized successfully")
            except Exception as e:
                print_error(f"Resume Screener Service initialization failed: {e}")
            
            try:
                from ai_services.job_description_generator_service import JobDescriptionGeneratorService
                service = JobDescriptionGeneratorService()
                print_success("Job Description Generator Service initialized successfully")
            except Exception as e:
                print_error(f"Job Description Generator Service initialization failed: {e}")
        else:
            print_warning("Skipping service initialization (Google API Key not configured)")
    except Exception as e:
        print_error(f"Error during service initialization: {e}")
else:
    print_warning("Skipping service initialization (AI dependencies not installed)")

# Test 9: Check AI Data Directories
print_header("TEST 9: AI Data Directories")

ai_data_dirs = [
    'ai_data',
    'ai_data/policy_index',
    'ai_data/resume_analysis',
    'ai_data/temp',
]

for dir_name in ai_data_dirs:
    dir_path = Path(__file__).parent.parent / dir_name
    if dir_path.exists():
        print_success(f"{dir_name}/ exists")
    else:
        print_warning(f"{dir_name}/ will be created on first use")

# Final Summary
print_header("SUMMARY")

all_issues = []

if missing_core:
    all_issues.append("Core dependencies missing")
if missing_ai:
    all_issues.append("AI dependencies missing")
if not env_path.exists():
    all_issues.append(".env file not found")
else:
    try:
        from config import settings
        if not settings.GOOGLE_API_KEY or settings.GOOGLE_API_KEY == "":
            all_issues.append("Google API Key not configured")
    except:
        all_issues.append("Configuration error")

if not all_issues:
    print_success("🎉 ALL TESTS PASSED! AI Services are ready to use!")
    print_info("\nNext steps:")
    print_info("1. Start the backend: python3 main.py")
    print_info("2. Visit API docs: http://localhost:8000/api/docs")
    print_info("3. Test AI endpoints in the docs")
else:
    print_error(f"❌ Found {len(all_issues)} issue(s):")
    for issue in all_issues:
        print(f"   - {issue}")
    
    print_info("\n📋 Setup Instructions:")
    if missing_core:
        print_info("1. Install core dependencies:")
        print_info("   pip install -r requirements.txt")
    if missing_ai:
        print_info("2. Install AI dependencies:")
        print_info("   pip install -r requirements_ai.txt")
    if not env_path.exists():
        print_info("3. Create .env file:")
        print_info("   cp .env.template .env")
    print_info("4. Get Google API Key from: https://makersuite.google.com/app/apikey")
    print_info("5. Add to .env: GOOGLE_API_KEY=your_key_here")
    print_info("6. Run this test again: python3 test_ai_setup.py")

print()

