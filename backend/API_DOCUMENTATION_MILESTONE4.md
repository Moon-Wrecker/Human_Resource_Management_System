# API Documentation - Milestone 4
## PulseTrack HRMS API Endpoints

**Team 11, IIT Madras**  
**Course:** Software Engineering (SEP 2025)  
**Milestone:** 4 - API Endpoints

---

## Table of Contents
1. [Overview](#overview)
2. [GenAI APIs Integrated](#genai-apis-integrated)
3. [APIs Created by Dev Team](#apis-created-by-dev-team)
4. [API-to-User-Story Mapping](#api-to-user-story-mapping)
5. [Error Handling](#error-handling)
6. [Authentication](#authentication)

---

## Overview

PulseTrack HRMS provides a comprehensive RESTful API built with FastAPI, featuring:
- **Total API Endpoints:** 80+
- **GenAI Integrations:** 3 major services
- **User Stories Covered:** 16/16 (100%)
- **Authentication:** JWT-based
- **Documentation:** Auto-generated Swagger/OpenAPI
- **Response Format:** JSON
- **Base URL:** `http://localhost:8000/api/v1`

---

## GenAI APIs Integrated

### 1. Google Gemini API (Google AI)
**Purpose:** Natural language processing, content generation, and intelligent analysis

**Integration Details:**
- **Model Used:** `gemini-1.5-flash`
- **Library:** `google-generativeai` (Python SDK)
- **API Key:** Configured via environment variable `GEMINI_API_KEY`
- **Rate Limits:** Handled with exponential backoff
- **Cost:** Pay-per-use based on tokens

**Used In:**
1. **Policy RAG Service** - Natural language understanding for policy Q&A
2. **Resume Screener Service** - Resume analysis and candidate matching
3. **Job Description Generator** - Professional JD content generation

**Key Features:**
- Text generation with structured output
- Embedding generation for semantic search
- Multi-turn conversation support
- JSON mode for structured responses

**Example API Call (Internal):**
```python
import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(prompt)
```

---

### 2. ChromaDB (Vector Database)
**Purpose:** Vector embeddings storage and semantic similarity search

**Integration Details:**
- **Library:** `chromadb` (Python SDK)
- **Storage:** Local persistent storage (`./chroma_db`)
- **Embedding Model:** Google Gemini Embeddings
- **Collection:** `policy_documents`
- **Distance Metric:** Cosine similarity

**Used In:**
- **Policy RAG Service** - Store and retrieve policy document embeddings

**Key Features:**
- Persistent vector storage
- Metadata filtering
- Fast similarity search (< 100ms)
- Auto-indexing on document upload

**Example API Call (Internal):**
```python
import chromadb
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("policy_documents")
results = collection.query(query_embeddings=[embedding], n_results=5)
```

---

### 3. Langchain Framework
**Purpose:** RAG (Retrieval Augmented Generation) pipeline orchestration

**Integration Details:**
- **Library:** `langchain`, `langchain-google-genai`
- **Components Used:**
  - `PyPDFLoader` - PDF document loading
  - `RecursiveCharacterTextSplitter` - Text chunking
  - `GoogleGenerativeAIEmbeddings` - Embedding generation
  - `Chroma` - Vector store integration
  - `ConversationalRetrievalChain` - RAG pipeline

**Used In:**
- **Policy RAG Service** - End-to-end RAG implementation

**Key Features:**
- Document loading and preprocessing
- Smart text chunking with overlap
- Conversational context management
- Source tracking and citation

**Example Pipeline:**
```python
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = Chroma(embedding_function=embeddings)
qa_chain = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())
```

---

### 4. PyPDF2 (PDF Processing)
**Purpose:** Extract text content from PDF documents

**Integration Details:**
- **Library:** `PyPDF2` (Python SDK)
- **Used For:** Resume parsing, policy document processing
- **Features:** Text extraction, page iteration

**Used In:**
1. **Resume Screener Service** - Extract text from uploaded resumes
2. **Policy RAG Service** - Extract text from policy PDFs

**Example API Call (Internal):**
```python
import PyPDF2
with open(pdf_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
```

---

## APIs Created by Dev Team

### Category 1: AI-Powered APIs (GenAI Integration)

#### 1.1 Policy RAG APIs
**Base Path:** `/api/v1/ai/policy-rag`

| Method | Endpoint | Description | User Story |
|--------|----------|-------------|------------|
| POST | `/ask` | Ask policy question using AI | #6, #10 |
| GET | `/suggestions` | Get suggested policy questions | #6, #10 |
| GET | `/status` | Get policy index status | #6, #10 |
| POST | `/index/rebuild` | Rebuild policy index | #6 (Admin) |

**Key Features:**
- 24/7 AI chatbot for policy queries
- RAG-based accurate answers with source citation
- Conversational context support
- Auto-indexing of uploaded policies

**Error Handling:**
- 400: Invalid question format
- 503: AI service unavailable
- 500: AI processing error

---

#### 1.2 Resume Screener APIs
**Base Path:** `/api/v1/ai/resume-screener`

| Method | Endpoint | Description | User Story |
|--------|----------|-------------|------------|
| POST | `/screen` | Screen resumes with AI | #5 |
| GET | `/results/{analysis_id}` | Get saved screening results | #5 |
| GET | `/history` | Get screening history | #5 |
| POST | `/screen/stream` | Screen with real-time progress (SSE) | #5 |

**Key Features:**
- AI-powered candidate matching
- Skill detection and proficiency estimation
- 0-100 scoring system
- Batch processing support
- Permanent results storage
- Real-time progress updates (SSE)

**Response Example:**
```json
{
  "success": true,
  "job_id": 5,
  "total_analyzed": 15,
  "average_score": 78.5,
  "top_candidate": "Jane Smith",
  "analysis_id": "abc123",
  "results": [
    {
      "candidate_name": "Jane Smith",
      "overall_fit_score": 92,
      "skills_match": ["Python (Expert)", "React (Advanced)"],
      "strengths": ["Technical leadership", "Cloud architecture"],
      "gaps": ["Limited DevOps experience"]
    }
  ]
}
```

---

#### 1.3 Job Description Generator APIs
**Base Path:** `/api/v1/ai/job-description`

| Method | Endpoint | Description | User Story |
|--------|----------|-------------|------------|
| POST | `/generate` | Generate JD with AI | #2 |
| POST | `/improve` | Improve existing JD | #2 |
| POST | `/extract-keywords` | Extract SEO keywords | #2 |
| GET | `/status` | Get service status | #2 |

**Key Features:**
- Professional JD generation
- Dual mode: Preview or Save as draft
- Company culture integration
- ATS optimization
- SEO-friendly content

**Request Example:**
```json
{
  "job_title": "Senior Software Engineer",
  "job_level": "Senior",
  "department": "Engineering",
  "location": "Remote",
  "employment_type": "Full-time",
  "responsibilities": [
    "Design scalable systems",
    "Lead technical decisions"
  ],
  "save_as_draft": true
}
```

---

### Category 2: Dashboard APIs

#### 2.1 Dashboard Endpoints
**Base Path:** `/api/v1/dashboard`

| Method | Endpoint | Description | User Story | Access |
|--------|----------|-------------|------------|--------|
| GET | `/hr` | HR dashboard data | #1 | HR |
| GET | `/manager` | Manager dashboard data | #13 | Manager |
| GET | `/employee` | Employee dashboard data | #7 | Employee |
| GET | `/me` | Auto-route to role dashboard | All | All |
| GET | `/performance/{employee_id}` | Employee performance metrics | #7, #14 | HR/Manager/Self |
| GET | `/performance/me` | My performance metrics | #7 | All |

**Features:**
- Role-specific dashboards
- Real-time statistics
- Department-wise analytics
- Team performance tracking
- Learning progress monitoring

---

### Category 3: Employee Management APIs

#### 3.1 Employee CRUD
**Base Path:** `/api/v1/employees`

| Method | Endpoint | Description | User Story | Access |
|--------|----------|-------------|------------|--------|
| GET | `/` | List all employees (paginated) | #4 | HR |
| POST | `/` | Create new employee | #4 | HR |
| GET | `/{id}` | Get employee details | #4 | HR |
| PUT | `/{id}` | Update employee | #4 | HR |
| DELETE | `/{id}` | Deactivate employee | #4 | HR |
| GET | `/stats` | Get employee statistics | #4, #15 | HR |

**Features:**
- Pagination and filtering
- Search by name, email, employee ID
- Department, team, role filters
- Statistics and analytics
- Soft delete (deactivation)

---

### Category 4: Recruitment APIs

#### 4.1 Job Listings
**Base Path:** `/api/v1/jobs`

| Method | Endpoint | Description | User Story | Access |
|--------|----------|-------------|------------|--------|
| GET | `/` | List job postings | #3 | All |
| POST | `/` | Create job posting | #2, #3 | HR |
| GET | `/{id}` | Get job details | #3 | All |
| PUT | `/{id}` | Update job posting | #3 | HR |
| DELETE | `/{id}` | Close job posting | #3 | HR |
| GET | `/stats` | Get job statistics | #3 | HR |

---

#### 4.2 Applications
**Base Path:** `/api/v1/applications`

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/` | List applications | HR |
| POST | `/` | Submit application | Public |
| GET | `/{id}` | Get application details | HR |
| PUT | `/{id}/status` | Update application status | HR |
| GET | `/job/{job_id}` | Get applications for job | HR |

---

### Category 5: Performance Management APIs

#### 5.1 Feedback
**Base Path:** `/api/v1/feedback`

| Method | Endpoint | Description | User Story | Access |
|--------|----------|-------------|------------|--------|
| POST | `/` | Create feedback | #14 | Manager/HR |
| GET | `/me` | Get my feedback | #7 | All |
| GET | `/employee/{id}` | Get employee feedback | #7, #14 | Manager/HR |
| GET | `/given` | Feedback I gave | #14 | Manager/HR |
| PUT | `/{id}` | Update feedback | #14 | Giver |
| DELETE | `/{id}` | Delete feedback | #14 | Giver/HR |
| GET | `/stats/summary` | Feedback statistics | #7, #14 | Manager/HR |

**Features:**
- Multiple feedback types (positive, constructive, goal-related)
- Rating system (1-5)
- Date range filtering
- Statistics and trends

---

#### 5.2 Goals
**Base Path:** `/api/v1/goals`

| Method | Endpoint | Description | User Story | Access |
|--------|----------|-------------|------------|--------|
| POST | `/` | Create goal | #12 | Manager/HR |
| GET | `/me` | Get my goals | #12 | All |
| GET | `/team` | Get team goals | #12, #13 | Manager |
| GET | `/{id}` | Get goal details | #12 | All |
| PUT | `/{id}` | Update goal | #12 | Manager/HR |
| DELETE | `/{id}` | Delete goal | #12 | Manager/HR |
| PUT | `/{id}/progress` | Update progress | #12 | All |

---

#### 5.3 Skills
**Base Path:** `/api/v1/skills`

| Method | Endpoint | Description | User Story | Access |
|--------|----------|-------------|------------|--------|
| GET | `/modules` | List skill modules | #11 | All |
| GET | `/me` | My skill progress | #11 | All |
| GET | `/team` | Team skills progress | #11, #13 | Manager |
| POST | `/assign` | Assign module to employee | #11 | Manager/HR |
| PUT | `/progress/{id}` | Update module progress | #11 | All |
| GET | `/leaderboard` | Skills leaderboard | #11, #13 | All |

---

### Category 6: Leave & Attendance APIs

#### 6.1 Leave Management
**Base Path:** `/api/v1/leaves`

| Method | Endpoint | Description | User Story | Access |
|--------|----------|-------------|------------|--------|
| POST | `/` | Create leave request | #9 | All |
| GET | `/me` | My leave requests | #9 | All |
| GET | `/team` | Team leave requests | #9 | Manager |
| GET | `/{id}` | Get leave details | #9 | All |
| PUT | `/{id}/approve` | Approve leave | #9 | Manager/HR |
| PUT | `/{id}/reject` | Reject leave | #9 | Manager/HR |
| GET | `/balance` | Get leave balance | #9 | All |

**Features:**
- Multiple leave types (casual, sick, annual, maternity, paternity)
- Balance checking
- Approval workflow
- Notifications on status change

---

#### 6.2 Attendance
**Base Path:** `/api/v1/attendance`

| Method | Endpoint | Description | User Story | Access |
|--------|----------|-------------|------------|--------|
| POST | `/checkin` | Check in | #1 | All |
| POST | `/checkout` | Check out | #1 | All |
| GET | `/me` | My attendance | #1 | All |
| GET | `/team` | Team attendance | #1, #13 | Manager |
| GET | `/summary` | Attendance summary | #1, #15 | HR |
| GET | `/today` | Today's attendance | #1 | All |

---

### Category 7: Payslip APIs

**Base Path:** `/api/v1/payslips`

| Method | Endpoint | Description | User Story | Access |
|--------|----------|-------------|------------|--------|
| GET | `/me` | My payslips | #8 | All |
| GET | `/{id}` | Get payslip details | #8 | Self/HR |
| GET | `/{id}/download` | Download payslip PDF | #8 | Self/HR |
| POST | `/` | Generate payslip | #8 | HR |
| GET | `/employee/{id}` | Employee's payslips | #8 | HR |

**Features:**
- PDF generation
- Earnings and deductions breakdown
- Tax calculations
- Year/month filtering
- Secure access control

---

### Category 8: Policy & Announcements

#### 8.1 Policies
**Base Path:** `/api/v1/policies`

| Method | Endpoint | Description | User Story | Access |
|--------|----------|-------------|------------|--------|
| GET | `/` | List policies | #6 | All |
| POST | `/` | Upload policy | #6 | HR |
| GET | `/{id}` | Get policy details | #6 | All |
| GET | `/{id}/download` | Download policy | #6 | All |
| DELETE | `/{id}` | Delete policy | #6 | HR |

**Features:**
- PDF upload and storage
- Auto-indexing for RAG
- Category organization
- Version control

---

#### 8.2 Announcements
**Base Path:** `/api/v1/announcements`

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/` | List announcements | All |
| POST | `/` | Create announcement | HR |
| GET | `/{id}` | Get announcement details | All |
| PUT | `/{id}` | Update announcement | HR |
| DELETE | `/{id}` | Delete announcement | HR |
| GET | `/recent` | Get recent announcements | All |

---

### Category 9: Organization Structure

#### 9.1 Departments
**Base Path:** `/api/v1/departments`

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/` | List departments | All |
| POST | `/` | Create department | HR |
| GET | `/{id}` | Get department details | All |
| PUT | `/{id}` | Update department | HR |

---

#### 9.2 Organization
**Base Path:** `/api/v1/organization`

| Method | Endpoint | Description | User Story | Access |
|--------|----------|-------------|------------|--------|
| GET | `/structure` | Get org hierarchy | #16 | HR/Admin |
| GET | `/info` | Get company info | #16 | All |
| PUT | `/info` | Update company info | #16 | Admin |

---

### Category 10: User Profile & Authentication

#### 10.1 Authentication
**Base Path:** `/api/v1/auth`

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/login` | User login | Public |
| POST | `/logout` | User logout | All |
| POST | `/refresh` | Refresh token | All |
| GET | `/me` | Get current user | All |

**Features:**
- JWT authentication
- Refresh tokens
- Role-based access control
- Secure password hashing

---

#### 10.2 Profile
**Base Path:** `/api/v1/profile`

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/me` | Get my profile | All |
| PUT | `/me` | Update my profile | All |
| PUT | `/password` | Change password | All |
| POST | `/photo` | Upload profile photo | All |

---

### Category 11: Miscellaneous

#### 11.1 Holidays
**Base Path:** `/api/v1/holidays`

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/` | List holidays | All |
| POST | `/` | Create holiday | HR |
| GET | `/upcoming` | Get upcoming holidays | All |

---

#### 11.2 Requests
**Base Path:** `/api/v1/requests`

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/` | List requests | All |
| POST | `/` | Create request (WFH, equipment, etc.) | All |
| PUT | `/{id}/approve` | Approve request | Manager/HR |
| PUT | `/{id}/reject` | Reject request | Manager/HR |

---

## API-to-User-Story Mapping

### Complete Mapping Table

| User Story # | User Story Name | APIs Implementing It |
|--------------|-----------------|----------------------|
| #1 | Dashboard Monitoring (HR) | `GET /dashboard/hr`, `GET /attendance/summary` |
| #2 | Job Description Management | `POST /ai/job-description/generate`, `POST /jobs` |
| #3 | Job Posting Management | `GET /jobs`, `POST /jobs`, `PUT /jobs/{id}`, `DELETE /jobs/{id}` |
| #4 | Employee Database | `GET /employees`, `POST /employees`, `PUT /employees/{id}`, `GET /employees/stats` |
| #5 | Resume Screening | `POST /ai/resume-screener/screen`, `GET /ai/resume-screener/results/{id}` |
| #6 | Policy Access (HR) | `POST /ai/policy-rag/ask`, `GET /policies`, `POST /policies` |
| #7 | Performance Tracking | `GET /dashboard/performance/me`, `GET /feedback/me` |
| #8 | Payslip Access | `GET /payslips/me`, `GET /payslips/{id}/download` |
| #9 | Leave Notifications | `GET /leaves/me`, `POST /leaves`, `PUT /leaves/{id}/approve` |
| #10 | Policy Queries (Employee) | `POST /ai/policy-rag/ask`, `GET /ai/policy-rag/suggestions` |
| #11 | Skill Development | `GET /skills/team`, `POST /skills/assign`, `GET /skills/modules` |
| #12 | Goal Setting | `POST /goals`, `PUT /goals/{id}`, `GET /goals/team` |
| #13 | Team Performance Dashboard | `GET /dashboard/manager`, `GET /feedback/employee/{id}` |
| #14 | Employee Reviews | `POST /feedback`, `GET /feedback/employee/{id}` |
| #15 | Strategic Analytics | `GET /dashboard/hr`, `GET /employees/stats`, `GET /attendance/summary` |
| #16 | System Administration | `GET /employees`, `PUT /employees/{id}`, `GET /organization/structure` |

---

## Error Handling

All APIs follow consistent error response format:

### Standard Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": []
  }
}
```

### Common HTTP Status Codes
- **200 OK:** Successful GET/PUT/DELETE
- **201 Created:** Successful POST (resource created)
- **400 Bad Request:** Invalid input data, validation errors
- **401 Unauthorized:** Missing or invalid authentication token
- **403 Forbidden:** Authenticated but insufficient permissions
- **404 Not Found:** Resource not found
- **422 Unprocessable Entity:** Validation errors with details
- **500 Internal Server Error:** Server-side error
- **503 Service Unavailable:** External service (AI) unavailable

### Error Code Categories

#### Validation Errors (400, 422)
- `VALIDATION_ERROR` - Input validation failed
- `MISSING_FIELD` - Required field missing
- `INVALID_FORMAT` - Invalid data format

#### Authentication/Authorization Errors (401, 403)
- `UNAUTHORIZED` - Not authenticated
- `FORBIDDEN` - Insufficient permissions
- `INVALID_TOKEN` - JWT token invalid or expired
- `TOKEN_EXPIRED` - JWT token expired

#### Resource Errors (404)
- `NOT_FOUND` - Resource not found
- `EMPLOYEE_NOT_FOUND` - Employee not found
- `JOB_NOT_FOUND` - Job listing not found

#### Business Logic Errors (400)
- `INSUFFICIENT_BALANCE` - Insufficient leave balance
- `DUPLICATE_ENTRY` - Duplicate record (email, employee ID)
- `CANNOT_DELETE` - Cannot delete (has dependencies)

#### AI Service Errors (500, 503)
- `AI_SERVICE_UNAVAILABLE` - GenAI service not available
- `AI_PROCESSING_ERROR` - Error during AI processing
- `GENERATION_FAILED` - Content generation failed

### Example Error Responses

#### 401 Unauthorized
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

#### 403 Forbidden
```json
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "Only HR can access this endpoint"
  }
}
```

#### 422 Validation Error
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": [
      {
        "loc": ["body", "email"],
        "msg": "Invalid email format",
        "type": "value_error"
      }
    ]
  }
}
```

#### 503 AI Service Unavailable
```json
{
  "success": false,
  "error": {
    "code": "AI_SERVICE_UNAVAILABLE",
    "message": "Policy RAG service unavailable: Gemini API key not configured"
  }
}
```

---

## Authentication

### JWT-Based Authentication

All endpoints (except `/auth/login` and public endpoints) require JWT authentication.

### Getting a Token

**Endpoint:** `POST /api/v1/auth/login`

**Request:**
```json
{
  "email": "hr@pulsetrack.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "hr@pulsetrack.com",
    "name": "HR Manager",
    "role": "hr"
  }
}
```

### Using the Token

Include the token in the `Authorization` header for all authenticated requests:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Expiration

- **Access Token:** Expires in 24 hours
- **Refresh Token:** Available for renewing access tokens

### Role-Based Access Control (RBAC)

| Role | Access Level | Permissions |
|------|-------------|-------------|
| **Employee** | Basic | Own data, submit requests, view public info |
| **Manager** | Team-level | Team member data, approvals, feedback, goals |
| **HR** | Organization-wide | All employee data, recruitment, policies, payroll |
| **Admin** | System-level | User management, system configuration |

---

## Testing the APIs

### Using Swagger UI
Interactive API documentation available at:
```
http://localhost:8000/api/docs
```

### Using ReDoc
Alternative documentation at:
```
http://localhost:8000/api/redoc
```

### Using cURL

**Example: Login**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "hr@pulsetrack.com", "password": "password123"}'
```

**Example: Get HR Dashboard (with token)**
```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/hr" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Example: Ask Policy Question (GenAI)**
```bash
curl -X POST "http://localhost:8000/api/v1/ai/policy-rag/ask" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the leave policy?"}'
```

---

## API Performance

### Response Times (Average)

| API Category | Avg Response Time |
|-------------|-------------------|
| Authentication | 100-200ms |
| Dashboard APIs | 200-500ms |
| CRUD Operations | 50-150ms |
| Policy RAG (GenAI) | 2-5 seconds |
| Resume Screener (GenAI) | 3-5 seconds per resume |
| JD Generator (GenAI) | 5-10 seconds |

### Rate Limiting

Currently no rate limiting implemented. Recommended for production:
- **General APIs:** 100 requests/minute per user
- **GenAI APIs:** 10 requests/minute per user (to manage costs)

---

## Summary

### Statistics
- **Total APIs Created:** 80+
- **GenAI Integrations:** 4 (Gemini, ChromaDB, Langchain, PyPDF2)
- **User Stories Covered:** 16/16 (100%)
- **API Categories:** 11
- **Error Codes Defined:** 15+
- **Authentication:** JWT-based with RBAC
- **Documentation:** Auto-generated Swagger/OpenAPI

### Key Achievements
✅ All 16 user stories implemented with APIs  
✅ 3 major GenAI services integrated  
✅ Comprehensive error handling  
✅ Role-based access control  
✅ Auto-generated API documentation  
✅ Consistent REST API design  
✅ Proper HTTP status codes  
✅ Request/response validation  

---

## Contact
**Team 11, IIT Madras**  
**Project:** PulseTrack HRMS  
**Documentation Date:** November 2025

