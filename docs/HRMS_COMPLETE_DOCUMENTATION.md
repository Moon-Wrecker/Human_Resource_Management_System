# GenAI HRMS - Complete Documentation

**Last Updated**: November 14, 2025  
**Version**: 1.0.0  
**Status**: ✅ **80% Complete** - 11 Core Modules + AI Features Implemented | 🚀 Final Phase: Goals, Skills, Leaves

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Status & Progress](#project-status--progress)
3. [Quick Start Guide](#quick-start-guide)
4. [Project Structure](#project-structure)
5. [Database Schema](#database-schema)
6. [Implemented APIs](#implemented-apis)
   - [Authentication System](#authentication-system)
   - [Dashboard APIs](#dashboard-apis)
   - [Profile Management](#profile-management)
   - [Attendance Management](#attendance-management)
   - [Job Listings](#job-listings)
   - [Applications](#applications)
   - [Announcements](#announcements)
   - [Policies](#policies)
   - [Feedback](#feedback)
   - [Payslips](#payslips)
7. [AI Features](#ai-features)
8. [Role-Based Access Control](#role-based-access-control)
9. [Future Implementation Roadmap](#future-implementation-roadmap)
10. [Test Credentials](#test-credentials)
11. [Troubleshooting](#troubleshooting)

---

## Project Overview

### What is GenAI HRMS?

A full-stack Human Resource Management System with AI-powered features including resume screening and job description generation. The system supports three user roles with distinct permissions and interfaces.

### Technology Stack

**Backend**:
- **Framework**: FastAPI (Python)
- **Database**: SQLite (dev) / PostgreSQL (production)
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens
- **API Documentation**: Swagger/OpenAPI
- **Port**: 8000

**Frontend**:
- **Framework**: React 19.2.0 with TypeScript
- **Build Tool**: Vite 7.1.7
- **Routing**: React Router DOM v7
- **Styling**: Tailwind CSS v4
- **UI Components**: Radix UI
- **Charts**: Recharts 2.15.4
- **Port**: 5173 (default)

**AI Services**:
- **Framework**: FastAPI (Python)
- **AI Models**: Google Gemini (via LangChain)
- **Vector Store**: FAISS (for Policy RAG)
- **Ports**: 8001 (JD AI), 8002 (Policy RAG), 8003 (Resume Screener)

### System Roles

1. **HR** - Full access to recruitment, employee management, and system configuration
2. **MANAGER** - Access to team management, approvals, and team analytics
3. **EMPLOYEE** - Access to personal data, goals, skills, and self-service features

---

## Quick Start Guide

### Backend Setup

#### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Linux/Mac)
source venv/bin/activate
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and update:
# - SECRET_KEY (32+ characters)
# - JWT_SECRET_KEY (32+ characters)
# - CORS_ORIGINS (add your frontend URL)
```

#### 4. Initialize Database

```bash
python database.py
```

#### 5. Start Backend Server

```bash
# Using main.py
python main.py

# Or using uvicorn
uvicorn main:app --reload --port 8000
```

**Access Points**:
- API Root: http://localhost:8000
- Health Check: http://localhost:8000/health
- Swagger Docs: http://localhost:8000/api/docs

### Frontend Setup

#### 1. Install Dependencies

```bash
cd frontend
pnpm install  # or npm install
```

#### 2. Configure Environment

```bash
# Create .env from template
cp env.template .env

# Content should be:
VITE_API_BASE_URL=http://localhost:8000
VITE_ENV=development
```

#### 3. Start Development Server

```bash
pnpm run dev  # or npm run dev
```

**Access**: http://localhost:5173

### Clear Cache (if needed)

```bash
cd frontend
pnpm run clear-cache  # or npm run clear-cache
pnpm run dev
```

---

## Project Structure

### Backend Structure

```
backend/
├── main.py                 # FastAPI entry point (200+ lines)
├── config.py              # Configuration management
├── database.py            # Database connection & session
├── models.py              # SQLAlchemy models (15+ tables)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── hr_system.db          # SQLite database
│
├── routes/               # ✅ API route handlers
│   ├── auth.py          # ✅ Authentication (6 endpoints)
│   ├── dashboard.py     # ✅ Dashboards (6 endpoints)
│   ├── profile.py       # ✅ Profile Management (12 endpoints)
│   ├── attendance.py    # ✅ Attendance Management (9 endpoints)
│   ├── jobs.py          # ✅ Job Listings Management (7 endpoints)
│   ├── applications.py  # ⏳ Applications
│   ├── users.py         # ⏳ User management
│   ├── leaves.py        # ⏳ Leave management
│   ├── goals.py         # ⏳ Goals
│   ├── skills.py        # ⏳ Skill development
│   ├── feedback.py      # ⏳ Feedback
│   └── ...              # ⏳ More routes
│
├── services/            # Business logic layer
│   ├── auth_service.py
│   ├── dashboard_service.py
│   ├── profile_service.py
│   ├── attendance_service.py
│   ├── job_service.py
│   └── ...
│
├── utils/               # Utility functions
│   ├── security.py      # JWT & password hashing
│   ├── dependencies.py  # FastAPI dependencies
│   └── ...
│
└── uploads/             # File storage
    ├── resumes/
    ├── documents/
    ├── profiles/
    ├── policies/
    └── payslips/
```

### Frontend Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── ui/             # 20+ Radix-based primitives
│   │   ├── *-sidebar.tsx   # Role-specific sidebars
│   │   ├── *-header.tsx    # Headers
│   │   └── charts/         # Chart components
│   │
│   ├── constants/          # Navigation & config
│   │   ├── EmployeeSidebarItems.ts
│   │   ├── HRSidebaritems.ts
│   │   └── ManagerSidebarItems.ts
│   │
│   ├── layouts/            # Role-based layouts
│   │   ├── Employee.tsx    # Employee layout
│   │   ├── HR.tsx         # HR layout
│   │   └── Manager.tsx    # Manager layout
│   │
│   ├── pages/             # Application pages
│   │   ├── Common/        # Shared pages (Attendance, Payslips, etc.)
│   │   ├── Employee/      # Employee-specific (10 pages)
│   │   ├── HR/           # HR-specific (10 pages)
│   │   ├── Manager/      # Manager-specific (4 pages)
│   │   ├── Home.tsx
│   │   └── Login.tsx
│   │
│   ├── services/          # API service layer
│   │   ├── api.ts              # Axios instance & interceptors
│   │   ├── authService.ts      # Auth API calls
│   │   ├── dashboardService.ts # Dashboard API calls
│   │   ├── profileService.ts   # Profile API calls
│   │   ├── attendanceService.ts # Attendance API calls
│   │   └── jobService.ts       # Job listings API calls
│   │
│   ├── App.tsx           # Root component
│   ├── main.tsx          # Entry point
│   └── router.tsx        # Route configuration
│
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
└── .env
```

### AI Services Structure

```
ai/
├── JD AI/                 # Job Description Generator
│   ├── server.py         # FastAPI server (Port 8001)
│   ├── example.html      # Demo frontend
│   └── requirements.txt  # Python dependencies
│
├── policy rag/           # Policy Q&A System (RAG)
│   ├── policy_api.py     # FastAPI server (Port 8002)
│   ├── policy_rag.py     # RAG implementation with FAISS
│   ├── frontend.html     # Demo frontend
│   ├── text.txt          # Sample policy document
│   ├── readme.md         # Setup instructions
│   ├── faiss_index/      # FAISS vector database (auto-generated)
│   └── requirements.txt  # Python dependencies
│
└── Resume Screener/      # AI Resume Screening
    ├── server.py         # FastAPI server (Port 8003)
    ├── resume_screener.py # Core screening logic
    ├── frontend/
    │   └── index.html    # Demo frontend
    ├── uploads/          # Resume uploads directory
    ├── results/          # Screening results storage
    ├── resume_screener.log # Application logs
    └── requirements.txt  # Python dependencies
```

**Note**: All three AI services are standalone and can run independently or alongside the main HRMS backend.

---

## Database Schema

### Core Tables (15+ tables)

#### 1. **users** - User accounts and employee data

```sql
- id, employee_id, name, email, password_hash
- role (EMPLOYEE, HR, MANAGER)
- department_id, team_id, manager_id
- position, phone, date_of_birth, join_date
- hierarchy_level (1-7)
- salary, is_active, emergency_contact
- aadhar_document_path, pan_document_path
- leave balances (casual, sick, annual, wfh)
```

#### 2. **departments** - Department organization

```sql
- id, name, description, head_id
- budget, employee_count
```

#### 3. **teams** - Team structure

```sql
- id, name, description, department_id
- manager_id, member_count
```

#### 4. **job_listings** - Job postings

```sql
- id, title, description, department
- location, job_type, experience_required
- skills_required, salary_range
- posted_by_id, posted_at, is_active
```

#### 5. **applications** - Job applications

```sql
- id, job_listing_id, applicant_name
- email, phone, resume_path
- cover_letter, status, applied_at
- reviewed_by_id, reviewed_at
```

#### 6. **announcements** - Company announcements

```sql
- id, title, description, posted_by_id
- posted_at, expires_at, priority
- target_audience, is_urgent
```

#### 7. **attendance** - Daily attendance

```sql
- id, user_id, date
- check_in_time, check_out_time
- status (present, absent, leave, wfh, holiday)
- hours_worked, notes
```

#### 8. **leave_requests** - Leave applications

```sql
- id, user_id, leave_type
- start_date, end_date, days_count
- reason, status, applied_at
- approved_by_id, approved_at
```

#### 9. **holidays** - Company holidays

```sql
- id, name, date, description
- is_mandatory, created_at
```

#### 10. **goals** - Employee goals

```sql
- id, user_id, title, description
- start_date, deadline, status
- priority, progress_percentage
```

#### 11. **goal_checkpoints** - Goal milestones

```sql
- id, goal_id, title, description
- is_completed, completed_at
```

#### 12. **skill_modules** - Training modules

```sql
- id, title, description, category
- duration_hours, difficulty_level
- module_link, is_active
```

#### 13. **skill_module_enrollments** - Module enrollment tracking

```sql
- id, user_id, module_id
- enrolled_at, started_at, completed_at
- progress_percentage, status
```

#### 14. **policies** - Company policies

```sql
- id, title, description, category
- document_path, version, effective_date
- created_by_id, is_active
```

#### 15. **payslips** - Salary slips

```sql
- id, user_id, month, year
- basic_salary, allowances, deductions
- net_salary, document_path
- issued_at, issued_by_id
```

#### 16. **feedback** - Performance feedback

```sql
- id, user_id, given_by_id
- subject, description, feedback_type
- rating, given_at
```

#### 17. **performance_reports** - Quarterly reviews

```sql
- id, user_id, review_period
- overall_rating, strengths, areas_for_improvement
- goals_achieved, reviewed_by_id
```

#### 18. **requests** - Employee requests

```sql
- id, user_id, request_type
- subject, description, status
- submitted_at, resolved_by_id, resolved_at
```

#### 19. **resume_screening_results** - AI screening data

```sql
- id, application_id, overall_score
- technical_skills_score, experience_score
- education_score, recommendation
- ai_summary, screened_at
```

### Database Relationships

```
users (1) ──> (N) teams (members)
users (1) ──> (N) applications
users (1) ──> (N) attendance
users (1) ──> (N) leave_requests
users (1) ──> (N) goals
users (1) ──> (N) skill_module_enrollments
users (1) ──> (N) feedback (received)
users (1) ──> (N) feedback (given)

departments (1) ──> (N) teams
departments (1) ──> (N) users

job_listings (1) ──> (N) applications
applications (1) ──> (1) resume_screening_results

goals (1) ──> (N) goal_checkpoints
```

### Enums

1. **UserRole**: EMPLOYEE, HR, MANAGER
2. **ApplicationStatus**: pending, reviewed, shortlisted, rejected, hired
3. **AttendanceStatus**: present, absent, leave, wfh, holiday
4. **LeaveType**: casual, sick, annual, maternity, paternity
5. **LeaveStatus**: pending, approved, rejected
6. **GoalStatus**: not_started, in_progress, completed

---

## Authentication System

### ✅ Implemented Features

**Authentication APIs (6 endpoints)**:

1. **POST /api/v1/auth/login**
   - Email/password login
   - Returns JWT access token & refresh token
   - Returns user profile with role

2. **POST /api/v1/auth/logout**
   - Logout (token blacklist)

3. **POST /api/v1/auth/refresh**
   - Refresh access token

4. **POST /api/v1/auth/register** (HR only)
   - Register new users

5. **POST /api/v1/auth/forgot-password**
   - Password reset request

6. **POST /api/v1/auth/reset-password**
   - Password reset with token

### JWT Token Structure

```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "role": "EMPLOYEE",
  "name": "John Doe",
  "exp": 1234567890
}
```

### Password Security

- **Hashing**: bcrypt with salt rounds
- **Validation**: Minimum 8 characters
- **Storage**: Never store plain passwords

### Frontend Integration

**Service**: `src/services/authService.ts`

```typescript
// Login
const response = await authService.login(email, password);
// Returns: { user, accessToken, refreshToken }

// Logout
await authService.logout();

// Check authentication
const isAuth = authService.isAuthenticated();
```

**Protected Routes**: Implemented in `router.tsx`
- Routes check authentication status
- Role-based route protection
- Automatic redirect to login if not authenticated

---

## Dashboard APIs

### ✅ Implemented Endpoints (6 total)

#### 1. HR Dashboard - GET /api/v1/dashboard/hr

**Returns**:
```json
{
  "overview": {
    "totalEmployees": 150,
    "totalDepartments": 8,
    "totalTeams": 25,
    "activeJobs": 12,
    "pendingApplications": 45,
    "avgAttendance": 92.5
  },
  "departmentStats": [
    {
      "departmentName": "Engineering",
      "employeeCount": 45,
      "avgAttendance": 94.2,
      "openPositions": 3
    }
  ],
  "recentApplications": [...],
  "attendanceTrend": [...],
  "leaveRequests": [...]
}
```

**Used by**: HR Dashboard page

#### 2. Manager Dashboard - GET /api/v1/dashboard/manager

**Returns**:
```json
{
  "personal": {
    "name": "Michael Chen",
    "employeeId": "EMP003",
    "position": "Engineering Manager",
    "department": "Engineering",
    "teamName": "Backend Team",
    "wfhBalance": 8,
    "leaveBalances": {...}
  },
  "team": {
    "totalMembers": 8,
    "presentToday": 7,
    "onLeaveToday": 1,
    "pendingRequests": 3,
    "teamGoalsCompleted": 12,
    "teamGoalsInProgress": 5
  },
  "attendance": [...],
  "upcomingHolidays": [...]
}
```

**Used by**: Manager Dashboard page

#### 3. Employee Dashboard - GET /api/v1/dashboard/employee

**Returns**:
```json
{
  "personal": {
    "name": "John Anderson",
    "employeeId": "EMP006",
    "position": "Software Engineer",
    "department": "Engineering",
    "manager": "Michael Chen",
    "wfhBalance": 10,
    "leaveBalances": {
      "casual": 8,
      "sick": 5,
      "annual": 12
    }
  },
  "attendance": {
    "todayCheckIn": "09:15 AM",
    "todayCheckOut": null,
    "hoursWorked": "0",
    "thisMonthPresent": 18,
    "thisMonthAbsent": 0
  },
  "goals": [...],
  "upcomingHolidays": [...],
  "recentAnnouncements": [...]
}
```

**Used by**: Employee Dashboard page

#### 4. HR Dashboard Summary - GET /api/v1/dashboard/hr/summary

Quick stats for HR widgets

#### 5. Manager Team Stats - GET /api/v1/dashboard/manager/team-stats

Detailed team analytics for managers

#### 6. Employee Quick Stats - GET /api/v1/dashboard/employee/quick-stats

Quick personal stats for employee widgets

### Frontend Integration

**Service**: `src/services/dashboardService.ts`

```typescript
// Fetch dashboard data based on role
const data = await dashboardService.getDashboardData(userRole);
// Automatically calls correct endpoint (hr, manager, or employee)

// Type-safe responses
type HRDashboardData = {...}
type ManagerDashboardData = {...}
type EmployeeDashboardData = {...}
```

---

## Role-Based Access Control

### User Hierarchy System

```
Level 1: CEO
Level 2: Department Heads / VPs
Level 3: Senior Managers
Level 4: Managers
Level 5: Senior Engineers/Staff
Level 6: Mid-level Engineers/Staff
Level 7: Junior Engineers/Staff
```

### Role Permissions Matrix

| Feature | Employee | Manager | HR |
|---------|----------|---------|-----|
| **Dashboard** | ✅ Personal | ✅ Personal + Team | ✅ Company-wide |
| **Profile** | ✅ View/Edit Own | ✅ View Team | ✅ View/Edit All |
| **Attendance** | ✅ Punch In/Out | ✅ View Team | ✅ View/Edit All |
| **Leave Requests** | ✅ Apply | ✅ Approve Team | ✅ Approve All |
| **Goals** | ✅ Own Goals | ✅ Team Goals | ✅ View All |
| **Skills** | ✅ Enroll/Complete | ✅ View Team | ✅ Manage Modules |
| **Feedback** | ✅ View Received | ✅ Give to Team | ✅ View All |
| **Job Listings** | ✅ View | ✅ View | ✅ Create/Edit |
| **Applications** | ❌ | ❌ | ✅ Full Access |
| **Employees** | ❌ | ✅ View Team | ✅ Full CRUD |
| **Announcements** | ✅ View | ✅ View | ✅ Create/Edit |
| **Policies** | ✅ View | ✅ View | ✅ Create/Edit |
| **Payslips** | ✅ View Own | ✅ View Own | ✅ Generate All |
| **Team Requests** | ❌ | ✅ Approve/Reject | ✅ View All |
| **Performance Reports** | ✅ View Own | ✅ Create for Team | ✅ View All |

### Frontend Route Protection

**Routes Structure**:

```typescript
// Public routes
/ - Home
/login - Login page

// Employee routes (/employee/*)
/employee/dashboard
/employee/profile
/employee/goals
/employee/skills
/employee/feedback
/employee/attendance
/employee/payslips
/employee/announcements
/employee/policies
/employee/job-listings

// Manager routes (/manager/*)
/manager/dashboard
/manager/team-members
/manager/team-requests
/manager/performance
/manager/job-listings
/manager/attendance
/manager/announcements
/manager/policies
/manager/payslips

// HR routes (/hr/*)
/hr/dashboard
/hr/employees
/hr/add-employee
/hr/job-listings
/hr/add-job
/hr/applications
/hr/resume-screener
/hr/announcements
/hr/policies
/hr/attendance
/hr/payslips
```

**Route Guard Logic**:
- Check authentication token exists
- Verify token not expired
- Check user role matches route requirement
- Redirect to login if not authenticated
- Redirect to appropriate dashboard if wrong role

---

## AI Features

The HRMS includes three powerful AI-powered features built with **LangChain** and **Google Gemini** models. These standalone services can be integrated with the main HRMS application.

### AI Modules Overview

```
ai/
├── JD AI/                  # Job Description Generator
│   ├── server.py          # FastAPI server (Port: 8001)
│   └── example.html       # Demo frontend
│
├── policy rag/            # Policy Q&A System
│   ├── policy_api.py      # FastAPI server (Port: 8002)
│   ├── policy_rag.py      # RAG implementation with FAISS
│   ├── frontend.html      # Demo frontend
│   └── readme.md          # Setup instructions
│
└── Resume Screener/       # AI Resume Screening
    ├── server.py          # FastAPI server (Port: 8003)
    ├── resume_screener.py # Core screening logic
    └── frontend/
        └── index.html     # Demo frontend
```

---

### 1. Job Description (JD) Generator AI

**Purpose**: Automatically generate professional, comprehensive job descriptions using AI.

**Technology Stack**:
- **Framework**: FastAPI
- **AI Model**: Google Gemini (via LangChain)
- **Port**: 8001

**Features**:
- Generate complete job descriptions from basic requirements
- Structured output with all JD components
- Company information integration
- Required vs preferred skills distinction
- Salary range suggestions
- Benefits and perks inclusion

**API Endpoints**:

```http
POST /api/generate-job-description
```

**Request Body**:
```json
{
  "company_info": {
    "name": "Tech Corp",
    "description": "Leading software company",
    "industry": "Technology",
    "values": ["Innovation", "Collaboration"]
  },
  "job_info": {
    "title": "Senior Software Engineer",
    "department": "Engineering",
    "location": "Remote",
    "employment_type": "Full-time"
  },
  "requirements": [
    {
      "requirement": "5+ years Python experience",
      "is_required": true
    },
    {
      "requirement": "React knowledge",
      "is_required": false
    }
  ],
  "additional_details": {
    "salary_range": "$120k - $160k",
    "benefits": ["Health insurance", "401k"]
  }
}
```

**Response**:
```json
{
  "job_description": {
    "title": "Senior Software Engineer",
    "company_overview": "...",
    "job_summary": "...",
    "key_responsibilities": ["...", "..."],
    "required_qualifications": ["...", "..."],
    "preferred_qualifications": ["...", "..."],
    "technical_skills": ["...", "..."],
    "benefits": ["...", "..."],
    "application_process": "..."
  }
}
```

**Quick Start**:
```bash
cd ai/JD\ AI
pip install -r requirements.txt

# Set environment variable
export GOOGLE_API_KEY=your_api_key

# Start server
python server.py

# Access at http://localhost:8001
# Demo frontend at example.html
```

**Integration with HRMS**:
- Can be called from HR Dashboard when creating job listings
- Auto-populate job posting forms
- Save time on writing detailed JDs

---

### 2. Policy RAG (Retrieval-Augmented Generation)

**Purpose**: Intelligent Q&A system for company policies using RAG technology.

**Technology Stack**:
- **Framework**: FastAPI
- **AI Model**: Google Gemini (via LangChain)
- **Vector Store**: FAISS
- **Embeddings**: Google Generative AI Embeddings
- **Port**: 8002

**Features**:
- Upload policy documents (TXT, PDF)
- Create searchable vector database
- Context-aware question answering
- Chat history support
- Multi-document retrieval
- Accurate, source-based responses

**Architecture**:
```
Policy Documents → Text Splitter → Embeddings → FAISS Vector Store
                                                        ↓
User Question → Embeddings → Similarity Search → Context Retrieval
                                                        ↓
Context + Question → Gemini → Intelligent Answer
```

**API Endpoints**:

```http
POST /api/upload-policy        # Upload policy document
POST /api/ask-question          # Ask question about policies
POST /api/clear-history         # Clear chat history
GET  /api/health                # Health check
```

**Upload Policy**:
```http
POST /api/upload-policy
Content-Type: multipart/form-data

file: <policy_document.txt>
```

**Ask Question**:
```json
{
  "question": "What is the remote work policy?",
  "session_id": "user_123"
}
```

**Response**:
```json
{
  "answer": "According to the company policy, employees can work remotely up to 3 days per week...",
  "session_id": "user_123"
}
```

**Setup Process**:

```bash
cd ai/policy\ rag

# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Set environment variable
export GOOGLE_API_KEY=your_api_key

# Step 3: Create FAISS database (first time only)
python policy_rag.py
# Upload your policy documents
# Type 'quit' when done

# Step 4: Start API server
python policy_api.py

# Access at http://localhost:8002
# Demo frontend at frontend.html
```

**Integration with HRMS**:
- Embed in Policies page
- Employees can ask questions about policies
- Reduce HR workload on policy clarifications
- Instant, accurate policy information

---

### 3. AI Resume Screener

**Purpose**: Automated resume screening and candidate evaluation using multimodal AI.

**Technology Stack**:
- **Framework**: FastAPI
- **AI Model**: Google Gemini (multimodal - text + images)
- **Document Support**: PDF, DOCX
- **Port**: 8003

**Features**:
- Multi-format resume parsing (PDF, DOCX)
- Multimodal analysis (text + visual layout)
- Skills matching with importance weighting
- Experience evaluation
- Education assessment
- Overall candidate scoring (0-100)
- Detailed recommendations
- Structured JSON output
- Batch processing support

**Core Capabilities**:
1. **Skill Matching**
   - Identify required vs preferred skills
   - Proficiency level estimation
   - Context extraction from resume

2. **Experience Analysis**
   - Years of experience calculation
   - Relevance assessment
   - Career progression evaluation

3. **Education Verification**
   - Degree matching
   - Institution recognition
   - Certification validation

4. **Scoring System**:
   - Technical Skills Score (40%)
   - Experience Score (30%)
   - Education Score (20%)
   - Additional Factors (10%)
   - Overall Score (0-100)

**API Endpoints**:

```http
POST /api/screen-resume         # Screen single resume
GET  /api/results/{job_id}      # Get screening results
GET  /api/health                # Health check
```

**Screen Resume**:
```http
POST /api/screen-resume
Content-Type: multipart/form-data

resume: <resume.pdf>
job_description: {
  "title": "Senior Python Developer",
  "required_skills": ["Python", "Django", "PostgreSQL"],
  "preferred_skills": ["AWS", "Docker"],
  "experience_required": "5+ years",
  "education_required": "Bachelor's in CS"
}
```

**Response**:
```json
{
  "status": "success",
  "candidate_name": "John Doe",
  "overall_score": 85,
  "skill_match": {
    "matched_skills": ["Python", "Django", "PostgreSQL", "AWS"],
    "missing_skills": ["Docker"],
    "skill_score": 88
  },
  "experience_match": {
    "years_experience": 6,
    "relevance_score": 90,
    "experience_score": 85
  },
  "education_match": {
    "degree": "Master's in Computer Science",
    "education_score": 95
  },
  "recommendation": "STRONG_FIT",
  "summary": "Excellent candidate with strong technical skills...",
  "detailed_analysis": {
    "strengths": ["..."],
    "concerns": ["..."],
    "suggestions": ["..."]
  }
}
```

**Quick Start**:
```bash
cd ai/Resume\ Screener

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GOOGLE_API_KEY=your_api_key

# Start server
python server.py

# Access at http://localhost:8003
# Demo frontend at frontend/index.html
```

**Integration with HRMS**:
- Integrate with Applications page
- Auto-screen incoming applications
- Sort candidates by score
- Filter by minimum score threshold
- Save screening results to database
- HR can review top candidates first

---

### AI Integration Roadmap

#### Phase 1: Standalone Services (Current)
- ✅ Three independent AI services running on separate ports
- ✅ Demo frontends for testing
- ✅ REST APIs ready for integration

#### Phase 2: HRMS Integration (Planned)
1. **Job Description Generator**
   - Add "Generate with AI" button to Add Job form
   - Pre-fill form fields with generated content
   - Save generated JDs to database

2. **Policy RAG**
   - Add policy Q&A widget to Policies page
   - Chat interface for employees
   - Policy upload through HR dashboard

3. **Resume Screener**
   - Auto-screen on application submission
   - Display scores on Applications page
   - Sort/filter by AI scores
   - Show detailed analysis to HR

#### Phase 3: Advanced Features (Future)
- Unified AI dashboard
- Batch resume screening
- Custom prompts for JD generation
- Policy version comparison
- Interview question generation
- Performance review assistance
- Learning path recommendations

---

### AI Configuration

**Environment Variables Required**:
```bash
# Add to .env file
GOOGLE_API_KEY=your_google_gemini_api_key

# Optional configurations
AI_MODEL=gemini-1.5-pro  # Default model
AI_TEMPERATURE=0.7        # Creativity level (0-1)
MAX_TOKENS=2048          # Response length
```

**Dependencies** (for each AI module):
```bash
# Common dependencies
langchain
langchain-google-genai
langchain-community
fastapi
uvicorn
python-dotenv
pydantic

# Resume Screener additional
PyPDF2
pdfplumber
pdf2image
docx2txt

# Policy RAG additional
faiss-cpu  # or faiss-gpu for better performance
```

---

### AI Best Practices

1. **API Key Security**
   - Never commit API keys to git
   - Use environment variables
   - Rotate keys regularly

2. **Cost Management**
   - Gemini API has rate limits
   - Implement caching for repeated queries
   - Use appropriate model sizes

3. **Error Handling**
   - Handle API failures gracefully
   - Provide fallback options
   - Log errors for debugging

4. **Testing**
   - Test with sample resumes/JDs
   - Validate output quality
   - Monitor AI response times

5. **User Experience**
   - Show loading indicators
   - Display progress for long operations
   - Provide clear error messages

---

## API Development Roadmap

### Current Status

**✅ Completed (85+ APIs - 80% Complete)**:
- ✅ Authentication (6 endpoints) - Login, logout, register, password reset
- ✅ Dashboards (6 endpoints) - HR, Manager, Employee dashboards with statistics
- ✅ Profile Management (12 endpoints) - Profile CRUD, document uploads, team/manager info
- ✅ Attendance Management (9 endpoints) - Punch in/out, history, summaries, team/all views
- ✅ Job Listings Management (7 endpoints) - Create, read, update, delete jobs, statistics
- ✅ Applications Management (9 endpoints) - Apply, view, status updates, resume upload/download
- ✅ Announcements (6 endpoints) - Create, view, update, delete, statistics with targeting
- ✅ Policies (9 endpoints) - CRUD, PDF upload/download, acknowledgments, statistics
- ✅ **Feedback (9 endpoints)** - Give/receive feedback, ratings, statistics
- ✅ **Payslips (11 endpoints)** - CRUD, PDF upload/download, bulk generation, statistics
- ✅ AI Services (13 endpoints) - Policy RAG, Resume Screener, JD Generator

**Total Completed**: 97 endpoints across 11 modules + AI features

**⏳ Remaining (~15 endpoints)**:
- Next priorities: Goals, Skills, Leave Management

---

### ✅ Priority 5 COMPLETED: Additional Features

#### ✅ Feedback (9 APIs) - COMPLETED

**Implemented Endpoints**:
```http
GET    /api/v1/feedback/me                    # Get my received feedback
GET    /api/v1/feedback/employee/{id}         # Get employee feedback (Manager/HR)
GET    /api/v1/feedback/given                 # Get feedback I gave
GET    /api/v1/feedback                       # Get all feedback (HR)
GET    /api/v1/feedback/{id}                  # Get feedback by ID
POST   /api/v1/feedback                       # Create feedback (Manager/HR)
PUT    /api/v1/feedback/{id}                  # Update feedback (giver only)
DELETE /api/v1/feedback/{id}                  # Delete feedback (giver/HR)
GET    /api/v1/feedback/stats/summary         # Get statistics
```

**Features**:
- ✅ Give and receive feedback with ratings (1-5)
- ✅ Feedback types: positive, constructive, goal-related, performance, general
- ✅ Time-based filtering (date range, month, quarter)
- ✅ Statistics: total count, averages, breakdown by type
- ✅ Role-based access control
- ✅ Only giver can update their feedback
- ✅ Pagination and filtering support

**Business Rules**:
- Only managers and HR can create feedback
- Employees can only view feedback they received
- Managers can view feedback for their team members
- HR has full access to all feedback
- Only the feedback giver can update it
- Giver or HR can delete feedback

**Data Tracked**:
- Subject, description, feedback type
- Optional 1-5 star rating
- Employee (recipient), giver details
- Timestamp (given_on)

**Pages Supported**: Feedback (2 pages - Employee, Manager)  
**Backend Files**: `routes/feedback.py`, `services/feedback_service.py`, `schemas/feedback_schemas.py`  
**Frontend Files**: `services/feedbackService.ts`

---

#### ✅ Payslips (11 APIs) - COMPLETED

**Implemented Endpoints**:
```http
GET    /api/v1/payslips/me                    # Get my payslips
GET    /api/v1/payslips/employee/{id}         # Get employee payslips (HR)
GET    /api/v1/payslips                       # Get all payslips (HR)
GET    /api/v1/payslips/{id}                  # Get payslip by ID
POST   /api/v1/payslips                       # Create payslip (HR)
POST   /api/v1/payslips/generate              # Generate monthly payslips (HR)
PUT    /api/v1/payslips/{id}                  # Update payslip (HR)
DELETE /api/v1/payslips/{id}                  # Delete payslip (HR)
POST   /api/v1/payslips/{id}/upload           # Upload PDF document (HR)
GET    /api/v1/payslips/{id}/download         # Download PDF document
GET    /api/v1/payslips/stats/summary         # Get statistics (HR)
```

**Features**:
- ✅ Complete salary breakdown (basic, allowances, overtime, bonus)
- ✅ Automatic calculations (gross, deductions, net salary)
- ✅ Bulk payslip generation for all employees
- ✅ PDF document upload/download (max 5MB)
- ✅ Month/year filtering
- ✅ Statistics and reporting
- ✅ Secure file storage with cleanup
- ✅ Duplicate prevention (same period)

**Salary Components**:
- Basic Salary, Allowances, Overtime Pay, Bonus
- Tax Deduction, PF Deduction, Insurance, Other Deductions
- Auto-calculated: Gross, Total Deductions, Net Salary

**Bulk Generation**:
- Generate payslips for all active employees in one API call
- Uses employee's base salary from profile
- Applies standard deductions (15% tax, 12% PF)
- Skips employees who already have payslip for the period
- Customizable pay date

**File Management**:
- PDF validation (type and size)
- Unique filename generation
- Stored in `uploads/payslips/`
- Old files replaced automatically on re-upload
- Downloaded with proper content-type headers
- File cleanup on hard delete

**Business Rules**:
- Only HR can create, update, or delete payslips
- Only HR can upload documents
- Employees can only view/download their own payslips
- HR can view/download all payslips
- Pay period end must be after start
- Pay date should be on or after period end
- No duplicate payslips for same employee & period

**Data Tracked**:
- Pay period (start/end/date), month, year
- All salary components and deductions
- PDF document path
- Issued by (HR user), issued timestamp

**Pages Supported**: Payslips (3 pages - Employee, Manager, HR)  
**Backend Files**: `routes/payslips.py`, `services/payslip_service.py`, `schemas/payslip_schemas.py`  
**Frontend Files**: `services/payslipService.ts`

---

### ✅ Priority 1 COMPLETED: User Foundation (Week 1)

#### ✅ Day 1-2: Profile Management (12 APIs) - COMPLETED

**Implemented Endpoints**:
```http
GET    /api/v1/profile/me                    # Get current user profile
GET    /api/v1/profile/{user_id}             # Get user by ID (HR/Manager)
PUT    /api/v1/profile/me                    # Update profile
POST   /api/v1/profile/upload-image          # Upload profile image
POST   /api/v1/profile/upload-document       # Upload documents (Aadhar, PAN)
GET    /api/v1/profile/documents             # Get all documents
DELETE /api/v1/profile/documents/{type}      # Delete document
GET    /api/v1/profile/manager               # Get manager info
GET    /api/v1/profile/team                  # Get team members
GET    /api/v1/profile/team/{manager_id}     # Get team by manager
GET    /api/v1/profile/stats                 # Get my statistics
GET    /api/v1/profile/stats/{user_id}       # Get user statistics
```

**Features**:
- ✅ Complete profile information with department, team, manager
- ✅ Profile image upload with validation
- ✅ Document upload (Aadhar, PAN) with automatic cleanup
- ✅ Role-based access control (HR can view all, managers view team)
- ✅ Team information and statistics
- ✅ Leave balances display

**Pages Supported**: Profile (3 pages)  
**Backend Files**: `routes/profile.py`, `services/profile_service.py`, `schemas/profile_schemas.py`  
**Frontend Files**: `services/profileService.ts`, `pages/Employee/Profile.tsx`

---

#### ✅ Day 3-5: Attendance Management (9 APIs) - COMPLETED

**Implemented Endpoints**:
```http
POST   /api/v1/attendance/punch-in           # Employee punches in
POST   /api/v1/attendance/punch-out          # Employee punches out
GET    /api/v1/attendance/today              # Get today's status
GET    /api/v1/attendance/me                 # My attendance history
GET    /api/v1/attendance/me/summary         # Monthly summary
GET    /api/v1/attendance/team               # Team attendance (Manager)
GET    /api/v1/attendance/all                # All attendance (HR)
POST   /api/v1/attendance/mark               # Mark attendance manually (HR)
DELETE /api/v1/attendance/{id}               # Delete attendance record (HR)
```

**Features**:
- ✅ Punch in/out with time validation (6 AM - 12 PM for punch-in)
- ✅ Automatic hours calculation
- ✅ Status types: present, absent, leave, wfh, holiday
- ✅ Monthly summaries with attendance %, late arrivals, early departures
- ✅ Manager view: team attendance for specific dates
- ✅ HR view: company-wide attendance with department statistics
- ✅ Manual attendance marking with audit trail
- ✅ Location tracking (office, home, client-site)

**Business Rules**:
- Cannot punch in before 6:00 AM or after 12:00 PM
- Cannot punch out before punch-in
- Automatic hours calculation on punch-out
- Late arrival tracking (after 9:30 AM)
- Early departure tracking (before 5:30 PM)
- HR can manually mark/correct attendance with audit log

**Pages Supported**: Attendance (3 pages)  
**Backend Files**: `routes/attendance.py`, `services/attendance_service.py`, `schemas/attendance_schemas.py`  
**Frontend Files**: `services/attendanceService.ts`, `pages/Common/Attendance.tsx`

---

#### ✅ Day 6-7: Job Listings Management (7 APIs) - COMPLETED

**Implemented Endpoints**:
```http
POST   /api/v1/jobs                      # Create new job listing (HR only)
GET    /api/v1/jobs                      # Get all jobs with filters
GET    /api/v1/jobs/statistics           # Get job statistics (HR only)
GET    /api/v1/jobs/{job_id}             # Get job details
PUT    /api/v1/jobs/{job_id}             # Update job listing (HR only)
DELETE /api/v1/jobs/{job_id}             # Delete/deactivate job (HR only)
GET    /api/v1/jobs/{job_id}/applications # Get job applications (HR only)
```

**Features**:
- ✅ Create and manage job postings with full details
- ✅ Search and filter jobs (department, location, employment type, keywords)
- ✅ Pagination support for large job listings
- ✅ Employment types: full-time, part-time, contract, internship
- ✅ Application deadline tracking with warnings
- ✅ View application count per job
- ✅ Soft delete for jobs with pending applications
- ✅ Job statistics for HR dashboard

**Filter Options**:
- Department ID
- Location (partial match)
- Employment type
- Active/Inactive status
- Search (position, description, skills)
- Pagination (page, page_size)

**Business Rules**:
- Only HR can create, update, or delete jobs
- Application deadline must be in the future
- Jobs with pending applications are soft-deleted (deactivated)
- Jobs without applications can be permanently deleted
- All users can view active job listings
- HR can view inactive/closed jobs

**Data Tracked**:
- Position, department, experience required
- Skills required, description
- Location, employment type, salary range
- Posted by (HR user), posted date
- Application deadline
- Active status
- Application count

**Pages Supported**: JobListings (4 pages - HR, Manager, Employee, Common)  
**Backend Files**: `routes/jobs.py`, `services/job_service.py`, `schemas/job_schemas.py`  
**Frontend Files**: `services/jobService.ts`, `components/JobListingsTable.tsx`

---

#### ✅ Day 8-10: Applications Management (9 APIs) - COMPLETED

**Implemented Endpoints**:
```http
POST   /api/v1/applications                   # Submit job application
GET    /api/v1/applications/me                # Get my applications (Employee)
GET    /api/v1/applications/statistics        # Get application statistics (HR only)
GET    /api/v1/applications                   # Get all applications (HR only)
GET    /api/v1/applications/{app_id}          # Get application details
PUT    /api/v1/applications/{app_id}/status   # Update application status (HR only)
POST   /api/v1/applications/{app_id}/resume   # Upload resume
GET    /api/v1/applications/{app_id}/resume   # Download resume
DELETE /api/v1/applications/{app_id}          # Delete application
```

**Features**:
- ✅ Job application submission for internal and external candidates
- ✅ Resume upload (PDF, DOC, DOCX, max 5MB) with validation
- ✅ Duplicate application prevention (same job + same email/user)
- ✅ Application status workflow: pending → reviewed → shortlisted → rejected/hired
- ✅ Screening notes and scores (0-100) for HR evaluation
- ✅ Filter applications by job, status, source, or search
- ✅ Application statistics for HR dashboard
- ✅ Referral tracking with referrer information
- ✅ Resume download with proper file serving

**Status Options**:
- **pending**: Initial state when application is submitted
- **reviewed**: Application has been reviewed by HR
- **shortlisted**: Candidate shortlisted for interview
- **rejected**: Application rejected
- **hired**: Candidate hired

**Application Sources**:
- **self-applied**: Candidate applied directly
- **referral**: Employee referral (includes referrer_id)
- **recruitment**: Through recruitment agency
- **internal**: Internal job posting application

**Filter Options**:
- Job ID (show applications for specific job)
- Status (pending, reviewed, shortlisted, rejected, hired)
- Source (self-applied, referral, recruitment, internal)
- Search (applicant name or email)
- Pagination (page, page_size)

**Business Rules**:
- ✅ Only HR can view all applications and update status
- ✅ Employees can only view their own applications
- ✅ Cannot apply for same job twice (checked by email or user_id)
- ✅ Application deadline validation (cannot apply after deadline)
- ✅ Resume must be PDF, DOC, or DOCX, max 5MB
- ✅ Referrer must be a valid user in the system
- ✅ Employees can only delete pending applications
- ✅ HR can delete any application
- ✅ Reviewed date automatically set when status changes from pending
- ✅ Old resume replaced when new one uploaded

**Data Tracked**:
- Job ID, applicant name, email, phone
- Resume file path, cover letter
- Application source and referrer (if applicable)
- Status, screening score, screening notes
- Applied date, reviewed date
- Applicant user ID (for internal applications)

**Statistics Provided** (HR Dashboard):
- Total applications, by status breakdown
- Applications this month
- Top 5 jobs by application count
- Applications by source distribution

**Pages Supported**: Applications (1 page - HR)  
**Backend Files**: `routes/applications.py`, `services/application_service.py`, `schemas/application_schemas.py`  
**Frontend Files**: `services/applicationService.ts`, `pages/HR/Applications.tsx`

---

### ✅ Priority 2 COMPLETED: Announcements & Policies (Week 2)

#### ✅ Announcements (6 APIs) - COMPLETED

**Implemented Endpoints**:
```http
GET    /api/v1/announcements               # List all announcements with filters
GET    /api/v1/announcements/{id}          # Get announcement details
POST   /api/v1/announcements               # Create announcement (HR/Manager)
PUT    /api/v1/announcements/{id}          # Update announcement (HR/Manager)
DELETE /api/v1/announcements/{id}          # Delete announcement (HR/Manager)
GET    /api/v1/announcements/stats/summary # Get statistics (HR/Manager)
```

**Features**:
- ✅ Create company-wide or targeted announcements
- ✅ Urgent announcements with priority display
- ✅ Expiry date support (auto-hide expired)
- ✅ Target specific departments/roles
- ✅ Soft delete support (audit trail)
- ✅ Pagination for large datasets
- ✅ Filter by expired/inactive status
- ✅ Statistics for HR dashboard

**Business Rules**:
- Only HR and Managers can create/update/delete announcements
- All users can view active, non-expired announcements
- Expired announcements hidden by default (optional include)
- Soft delete preserves data for audit
- Urgent announcements displayed prominently
- Optional link attachment for more details

**Data Tracked**:
- Title, message, optional link
- Target departments (comma-separated IDs)
- Target roles (Employee, Manager, HR)
- Urgent flag, expiry date
- Created by, created at, published date
- Active status

**Pages Supported**: Announcements (3 pages - HR, Manager, Employee)  
**Backend Files**: `routes/announcements.py`, `services/announcement_service.py`, `schemas/announcement_schemas.py`  
**Frontend Files**: `services/announcementService.ts`

---

#### ✅ Policies (9 APIs) - COMPLETED

**Implemented Endpoints**:
```http
GET    /api/v1/policies                    # List all policies (with filters)
GET    /api/v1/policies/{id}               # Get policy details
POST   /api/v1/policies                    # Create policy (HR only)
PUT    /api/v1/policies/{id}               # Update policy (HR only)
DELETE /api/v1/policies/{id}               # Delete policy (HR only)
POST   /api/v1/policies/{id}/upload        # Upload PDF document
GET    /api/v1/policies/{id}/download      # Download PDF document
POST   /api/v1/policies/{id}/acknowledge   # Acknowledge policy (all users)
GET    /api/v1/policies/{id}/acknowledgments # Get acknowledgments (HR)
GET    /api/v1/policies/stats/summary      # Get statistics (HR)
```

**Features**:
- ✅ Complete policy document management
- ✅ PDF upload/download (max 10MB)
- ✅ Policy acknowledgment tracking
- ✅ Version management
- ✅ Category organization (HR, IT, Finance, etc.)
- ✅ Effective date tracking
- ✅ Review date reminders
- ✅ Secure file storage
- ✅ Automatic file cleanup on delete
- ✅ Statistics and reporting

**File Management**:
- PDF validation (type and size)
- Unique filename generation (prevents conflicts)
- Stored in `uploads/policies/` directory
- Old files replaced automatically on re-upload
- Downloaded with proper content-type headers
- File cleanup on hard delete

**Acknowledgment System**:
- Track which users acknowledged which policies
- One acknowledgment per user per policy
- Timestamp of acknowledgment
- HR can view acknowledgment status
- Used for compliance tracking

**Business Rules**:
- Only HR can create, update, or delete policies
- All users can view active policies
- All users can download policy PDFs
- All users can acknowledge policies
- Cannot acknowledge same policy twice
- Effective date must be set
- Review date is optional (for periodic reviews)

**Data Tracked**:
- Title, description, content
- Category, version, effective date, review date
- Document file path
- Created by (HR user), created/updated timestamps
- Active status
- Acknowledgments (user, date)

**Database Models**:
- `policies` table (main policy data)
- `policy_acknowledgments` table (tracking)
- Relationship: Policy → Many Acknowledgments

**Pages Supported**: Policies (3 pages - HR, Manager, Employee)  
**Backend Files**: `routes/policies.py`, `services/policy_service.py`, `schemas/policy_schemas.py`  
**Frontend Files**: `services/policyService.ts`

---

### Priority 3: CORE FEATURES - Week 3 (5 days)

#### Job Listings (6 APIs) ⭐⭐

```http
GET    /api/v1/jobs                    # List jobs (with filters)
GET    /api/v1/jobs/{id}               # Job details
POST   /api/v1/jobs                    # Create job (HR only)
PUT    /api/v1/jobs/{id}               # Update job (HR only)
DELETE /api/v1/jobs/{id}               # Delete job (HR only)
PATCH  /api/v1/jobs/{id}/status        # Activate/Deactivate (HR only)
```

**Pages Supported**: Job Listings (4 pages)

#### Applications (7 APIs) ⭐⭐⭐

```http
GET    /api/v1/applications            # List applications (HR)
GET    /api/v1/applications/{id}       # Application details (HR)
POST   /api/v1/applications            # Submit application (public/employee)
PUT    /api/v1/applications/{id}/status # Update status (HR)
POST   /api/v1/applications/{id}/screen # AI screen resume (HR)
GET    /api/v1/applications/{id}/screening # Get screening results (HR)
DELETE /api/v1/applications/{id}       # Delete application (HR)
```

**Pages Supported**: Applications, Resume Screener (4 pages)

### Priority 4: GROWTH & DEVELOPMENT - Week 4 (5 days)

#### Goals (8 APIs) ⭐⭐⭐

```http
GET    /api/v1/goals                   # List goals
GET    /api/v1/goals/{id}              # Goal details
POST   /api/v1/goals                   # Create goal
PUT    /api/v1/goals/{id}              # Update goal
DELETE /api/v1/goals/{id}              # Delete goal
POST   /api/v1/goals/{id}/checkpoints  # Add checkpoint
PUT    /api/v1/goals/checkpoints/{id}  # Update checkpoint
DELETE /api/v1/goals/checkpoints/{id}  # Delete checkpoint
```

**Pages Supported**: Goal Tracker (2 pages)

#### Skills (8 APIs) ⭐⭐⭐

```http
GET    /api/v1/skills/modules          # List skill modules
GET    /api/v1/skills/modules/{id}     # Module details
POST   /api/v1/skills/modules          # Create module (HR)
PUT    /api/v1/skills/modules/{id}     # Update module (HR)
DELETE /api/v1/skills/modules/{id}     # Delete module (HR)
POST   /api/v1/skills/enroll/{id}      # Enroll in module
PUT    /api/v1/skills/progress/{id}    # Update progress
GET    /api/v1/skills/my-enrollments   # My enrolled modules
```

**Pages Supported**: Skill Development (2 pages)

### Priority 5: ADDITIONAL FEATURES - Later Phases

#### Feedback (5 APIs) ⭐⭐⭐

```http
GET    /api/v1/feedback                # List feedback
GET    /api/v1/feedback/{id}           # Feedback details
POST   /api/v1/feedback                # Give feedback (Manager)
PUT    /api/v1/feedback/{id}           # Update feedback (Manager)
DELETE /api/v1/feedback/{id}           # Delete feedback (Manager)
```

#### Payslips (3 APIs) ⭐⭐

```http
GET    /api/v1/payslips                # List payslips
GET    /api/v1/payslips/{id}           # Payslip details
GET    /api/v1/payslips/{id}/download  # Download PDF
```

#### Team Requests (4 APIs) ⭐⭐⭐

```http
GET    /api/v1/requests                # List requests
POST   /api/v1/requests                # Submit request
PUT    /api/v1/requests/{id}/status    # Approve/Reject (Manager)
GET    /api/v1/requests/team           # Team requests (Manager)
```

#### Leave Management (6 APIs) ⭐⭐⭐⭐

```http
GET    /api/v1/leaves                  # List leave requests
GET    /api/v1/leaves/{id}             # Leave details
POST   /api/v1/leaves                  # Apply for leave
PUT    /api/v1/leaves/{id}/status      # Approve/Reject (Manager/HR)
DELETE /api/v1/leaves/{id}             # Cancel leave
GET    /api/v1/leaves/balance          # Leave balance
```

#### Performance Reports (4 APIs) ⭐⭐⭐⭐

```http
GET    /api/v1/performance             # List reports
GET    /api/v1/performance/{id}        # Report details
POST   /api/v1/performance             # Create report (Manager/HR)
PUT    /api/v1/performance/{id}        # Update report (Manager/HR)
```

### Development Best Practices

1. **Start Simple**: Profile → Announcements → Policies
2. **Build Incrementally**: One module at a time
3. **Test Thoroughly**: Use Swagger docs for testing
4. **Update Frontend**: Add API calls to service layer
5. **Document**: Update this file with completion status

---

## Test Credentials

**Password for all users**: `pass123`

### HR Accounts (2 users)

| Email | Name | Access |
|-------|------|--------|
| sarah.johnson@company.com | Sarah Johnson | Full HR access |
| linda.martinez@company.com | Linda Martinez | Full HR access |

### Manager Accounts (3 users)

| Email | Name | Team |
|-------|------|------|
| michael.chen@company.com | Michael Chen | Backend Team |
| emily.rodriguez@company.com | Emily Rodriguez | Frontend Team |
| david.kim@company.com | David Kim | QA Team |

### Employee Accounts (10 users)

| Email | Name | Department |
|-------|------|------------|
| john.anderson@company.com | John Anderson | Engineering |
| alice.williams@company.com | Alice Williams | Engineering |
| robert.kumar@company.com | Robert Kumar | Engineering |
| maria.garcia@company.com | Maria Garcia | Marketing |
| james.wilson@company.com | James Wilson | Sales |
| priya.sharma@company.com | Priya Sharma | HR |
| daniel.brown@company.com | Daniel Brown | Finance |
| jessica.lee@company.com | Jessica Lee | Operations |
| thomas.miller@company.com | Thomas Miller | Design |
| emma.davis@company.com | Emma Davis | Product |

### Database Seed Data

All tables have been seeded with realistic data:
- 15 departments
- 15 teams
- 15 users (2 HR, 3 Managers, 10 Employees)
- 15 job listings
- 15 applications
- 150+ attendance records
- 15 leave requests
- 15 holidays
- 15 goals with 30 checkpoints
- 15 skill modules with enrollments
- 15 policies
- 15 payslips
- 15 feedback entries
- 15 announcements
- 13 resume screening results

---

## Troubleshooting

### Backend Issues

#### Port 8000 Already in Use

```bash
# Kill existing process
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

#### Database Not Found

```bash
cd backend
python database.py
```

#### Module Not Found Error

```bash
# Ensure venv is activated
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

#### CORS Errors

Add your frontend URL to `.env`:
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://your-url
```

### Frontend Issues

#### Module Export Errors

```bash
cd frontend
npm run clear-cache
npm run dev
```

#### .env File Missing

```bash
cd frontend
cp env.template .env
```

#### Vite Cache Issues

```bash
cd frontend
rm -rf node_modules/.vite
rm -rf .vite
rm -rf dist
npm install
npm run dev
```

#### API Connection Errors

1. Check backend is running: http://localhost:8000/health
2. Check `.env` has correct API URL:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```
3. Check browser console for CORS errors
4. Hard refresh browser: `Ctrl+Shift+R`

### ⚠️ 403 Forbidden Errors on Profile APIs (NEW)

**Symptoms:**
- `GET http://localhost:8000/api/v1/profile/manager 403 (Forbidden)`
- `GET http://localhost:8000/api/v1/profile/documents 403 (Forbidden)`
- Profile page shows "Failed to load profile"

**Root Cause:** Backend server not restarted after adding profile routes, or authentication token issues.

**Solution - Follow These Steps:**

**Step 1: Restart Backend Server** ⚡
```bash
# In backend terminal, press Ctrl+C to stop
# Then restart:
cd backend
python main.py

# Wait for: "INFO:     Uvicorn running on http://0.0.0.0:8000"
```

**Step 2: Clear Browser Cache & Re-login** 🔄
1. Open Browser DevTools (`F12`)
2. Go to: Application → Local Storage → http://localhost:5173
3. Right-click → "Clear"
4. Refresh page (`Ctrl+Shift+R`)
5. Login again with test credentials:
   - Email: `john.doe@company.com`
   - Password: `password123`

**Step 3: Verify Token Exists** ✅
After login, check LocalStorage (`F12` → Application):
- ✅ Should have: `access_token`, `refresh_token`, `user`
- ❌ If missing: Backend isn't sending tokens properly

**Step 4: Test Profile API** 🧪
```bash
# Get your access token from localStorage
# Then test:
curl -X GET "http://localhost:8000/api/v1/profile/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Should return: 200 OK with profile data
# If 403: Token is invalid or expired
```

**Step 5: Use Swagger UI** 📚
1. Go to: http://localhost:8000/api/docs
2. Click "Authorize" button (top right with lock icon)
3. Enter: `Bearer YOUR_ACCESS_TOKEN` (get from localStorage)
4. Click "Authorize" then "Close"
5. Try `/api/v1/profile/me` → "Try it out" → "Execute"
6. Should return 200 OK with profile data

**If Still Not Working:**
- Check backend logs for auth errors
- Ensure `uploads` folder exists: `mkdir -p backend/uploads/profiles backend/uploads/documents`
- Try different user: logout → login as manager/HR
- Check CORS: backend must allow `http://localhost:5173`

---

### Common Issues

#### Login Not Working

1. Verify backend is running
2. Check database has seeded data
3. Try test credentials (password: `password123`)
4. Check browser console for API errors
5. Check Network tab for request/response

#### Dashboard Not Loading

1. Verify login successful
2. Check access token in localStorage
3. Verify dashboard API endpoint working:
   - HR: GET /api/v1/dashboard/hr
   - Manager: GET /api/v1/dashboard/manager
   - Employee: GET /api/v1/dashboard/employee
4. Check browser console for errors

#### 401 Unauthorized Errors

1. Token expired - logout and login again
2. Token not sent - check authService includes token in header
3. Invalid token - clear localStorage and login again

#### 403 Forbidden Errors (General)

- User role doesn't match required permission
- Check user role in database
- Verify route protection matches user role
- For profile APIs specifically: See section above ⬆️

### Performance Issues

#### Slow API Response

1. Check database size (SQLite has limits)
2. Add indexes to frequently queried columns
3. Implement pagination for large datasets
4. Consider switching to PostgreSQL

#### Frontend Slow to Load

1. Clear Vite cache
2. Check bundle size
3. Implement code splitting
4. Lazy load components

### Development Tips

1. **Always activate venv** before working on backend
2. **Clear cache** after major frontend changes
3. **Use Swagger docs** (http://localhost:8000/api/docs) for API testing
4. **Check browser console** for frontend errors
5. **Check terminal logs** for backend errors
6. **Use Thunder Client/Postman** for API testing
7. **Commit often** with clear messages

---

## Next Steps

### For Backend Developers

1. **Choose Next API Module** from Priority Matrix
2. **Read API Specification** in Backend API section
3. **Create Route File** in `backend/routes/`
4. **Implement Business Logic** in `backend/services/`
5. **Test with Swagger** at http://localhost:8000/api/docs
6. **Update This Documentation**

### For Frontend Developers

1. **Wait for Backend APIs** or use mock data
2. **Create Service Functions** in `src/services/`
3. **Integrate with Pages** 
4. **Test with Real APIs**
5. **Handle Loading/Error States**

### For Full-Stack Developers

1. **Pick High-Priority Module** (Profile recommended)
2. **Build Backend APIs First**
3. **Test with Swagger/Postman**
4. **Add Frontend Integration**
5. **Test End-to-End**
6. **Move to Next Module**

---

## Additional Resources

### Documentation Links

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **React**: https://react.dev/
- **Vite**: https://vitejs.dev/
- **Tailwind CSS**: https://tailwindcss.com/
- **Radix UI**: https://www.radix-ui.com/

### API Testing Tools

- **Swagger UI**: http://localhost:8000/api/docs
- **Thunder Client**: VS Code extension
- **Postman**: Desktop application
- **curl**: Command line

### Code Quality Tools

```bash
# Backend
black .              # Format Python code
pylint **/*.py       # Lint Python code
pytest               # Run tests

# Frontend
npm run lint         # ESLint
npm run format       # Prettier
npm run type-check   # TypeScript check
```

---

## Conclusion

This documentation provides everything needed to:
- ✅ Set up development environment
- ✅ Understand system architecture
- ✅ Work with existing APIs
- ✅ Build new APIs following priority order
- ✅ Troubleshoot common issues
- ✅ Maintain code quality
- ✅ Integrate AI features

**Current Progress**: 80% complete (97 endpoints implemented)
**Core APIs**: Auth, Dashboards, Profile, Attendance, Jobs, Applications, Announcements, Policies, Feedback, Payslips ✅ Complete
**AI Features**: 3 services, 13 endpoints ✅ Complete  
**Next Milestone**: Goals, Skills, Leave Management APIs
**Timeline**: Approaching completion - 80% done

---

## 🤖 AI SERVICES COMPLETE IMPLEMENTATION

### Three AI Features Implemented

The HRMS now includes **3 powerful AI features** powered by Google Gemini:

#### 1. **Policy RAG** - AI-Powered Q&A System
- **Purpose**: Natural language questions about company policies
- **Access**: All authenticated users
- **Status**: ✅ Production Ready
- **Features**:
  - Auto-indexing when policies uploaded
  - Natural language processing
  - Context-aware conversations
  - Source citations
  - Suggested questions
  - FAISS vectorstore

**API Endpoints** (4):
- `POST /api/v1/ai/policy-rag/ask` - Ask questions
- `GET /api/v1/ai/policy-rag/suggestions` - Get suggestions
- `GET /api/v1/ai/policy-rag/status` - Check status  
- `POST /api/v1/ai/policy-rag/index/rebuild` - Rebuild index

**Example**:
```bash
POST /api/v1/ai/policy-rag/ask
{
  "question": "How many casual leaves am I allowed?",
  "chat_history": []
}

Response:
{
  "success": true,
  "answer": "Employees are entitled to 12 casual leaves per year...",
  "sources": [{"policy_title": "Leave Policy 2025", "content": "..."}]
}
```

#### 2. **Resume Screener** - AI Resume Analysis
- **Purpose**: Intelligent resume analysis against job descriptions
- **Access**: HR only
- **Status**: ✅ Production Ready
- **Features**:
  - Overall fit score (0-100)
  - Skill matching with proficiency levels
  - Experience verification
  - Education validation
  - Strengths & gaps analysis
  - Real-time streaming progress (SSE)
  - Permanent storage
  - Historical tracking

**API Endpoints** (5):
- `POST /api/v1/ai/resume-screener/screen` - Standard screening
- `POST /api/v1/ai/resume-screener/screen/stream` - With progress updates
- `GET /api/v1/ai/resume-screener/results/{id}` - Get saved results
- `GET /api/v1/ai/resume-screener/history` - View history

**Analysis Output**:
- Overall fit score: 0-100
- Skill matches: Each skill with proficiency (1-5)
- Experience: Years required vs present
- Education: Degree verification
- Strengths: Key positive points
- Gaps: Areas for improvement
- Summary: Hiring recommendation

#### 3. **Job Description Generator** - AI-Powered JD Creation
- **Purpose**: Generate professional job descriptions
- **Access**: HR only
- **Status**: ✅ Production Ready
- **Features**:
  - Two modes: Preview OR Save as Draft
  - Structured output
  - ATS-friendly formatting
  - SEO keyword extraction
  - Improve existing JDs
  - Copy/download capabilities

**API Endpoints** (4):
- `POST /api/v1/ai/job-description/generate` - Generate JD
- `POST /api/v1/ai/job-description/improve` - Improve existing
- `POST /api/v1/ai/job-description/extract-keywords` - SEO keywords
- `GET /api/v1/ai/job-description/status` - Service status

**Dual Modes**:
1. **Preview** (`save_as_draft=false`): Returns JD for review
2. **Save** (`save_as_draft=true`): Creates job listing draft

### AI Setup Instructions

#### 1. Install Dependencies (Already Done ✅)
```bash
cd backend
source .venv/bin/activate
pip install -r requirements_ai.txt
```

**Installed**: 46 AI packages including LangChain, FAISS, Google Gemini

#### 2. Configure API Key
Create `.env` file in project root:
```bash
# Get your key from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=AIza_your_actual_key_here

# AI Configuration (defaults are optimized)
GEMINI_MODEL=gemini-2.0-flash-exp
GEMINI_EMBEDDING_MODEL=models/embedding-001
GEMINI_TEMPERATURE=0.2

# Storage locations
POLICY_RAG_INDEX_DIR=ai_data/policy_index
RESUME_SCREENER_STORAGE_DIR=ai_data/resume_analysis
```

#### 3. Test Setup
```bash
cd backend
source .venv/bin/activate
python test_ai_setup.py
```

Should show: `🎉 ALL TESTS PASSED!`

#### 4. Start Backend
```bash
python3 main.py
```

Look for: `AI routes registered: Policy RAG, Resume Screener, JD Generator`

### Frontend Integration

**Services Created**:
- `frontend/src/services/aiPolicyRagService.ts` - Policy Q&A
- `frontend/src/services/aiResumeScreenerService.ts` - Resume screening
- `frontend/src/services/aiJobDescriptionService.ts` - JD generation

**Usage Example**:
```typescript
import { askPolicyQuestion } from '@/services/aiPolicyRagService';

const answer = await askPolicyQuestion({
  question: "What is the remote work policy?",
  chat_history: []
});
```

### Technical Architecture

**Backend**:
```
backend/
├── ai_services/                    # AI service classes
│   ├── policy_rag_service.py       # Policy Q&A + FAISS
│   ├── resume_screener_service.py  # Resume analysis
│   └── job_description_generator_service.py
├── routes/                         # API endpoints (13 total)
│   ├── ai_policy_rag.py
│   ├── ai_resume_screener.py
│   └── ai_job_description.py
└── schemas/ai_schemas.py           # Pydantic models
```

**Data Storage**:
```
ai_data/
├── policy_index/          # FAISS vector database
│   ├── index.faiss
│   └── index.pkl
└── resume_analysis/       # Permanent JSON storage
    └── {analysis_id}.json
```

### Performance & Cost

**Performance**:
- Policy indexing: 1-2s per policy
- Question answer: 2-3s
- Resume analysis: 5-10s per resume
- JD generation: 10-15s

**Cost** (Google Gemini Flash):
- ~$0.0001 per 1K tokens
- Typical monthly cost: < $1
- Free tier: 60 requests/minute

### Security

- **Access Control**: Role-based (HR only for screener/generator)
- **Data Privacy**: All processing via secure Gemini API
- **API Key**: Secured in environment variables
- **No External Storage**: Resumes analyzed but not stored externally

### Documentation

**Complete Guides**:
- `docs/AI_SERVICES_COMPLETE_GUIDE.md` - 1000+ lines, comprehensive guide
- `docs/AI_IMPLEMENTATION_SUMMARY.md` - Implementation overview
- `backend/AI_SERVICES_README.md` - Quick start guide
- `backend/test_ai_setup.py` - Test script

**API Docs**: http://localhost:8000/api/docs

### Key Features Implemented

✅ **Auto-Indexing**: Policies indexed automatically on upload  
✅ **Streaming Progress**: Real-time updates for resume screening  
✅ **Dual Modes**: JD Generator preview or save directly  
✅ **Permanent Storage**: All analyses saved for future reference  
✅ **Chat History**: Policy Q&A remembers conversation context  
✅ **Source Citations**: Answers include policy references  
✅ **Type Safety**: Full TypeScript support  
✅ **Cost Optimized**: Uses Gemini Flash model  
✅ **Graceful Degradation**: Backend works even if AI services fail  

### Troubleshooting

**Issue**: "AI service unavailable"
**Fix**: Check `GOOGLE_API_KEY` in `.env`

**Issue**: "No policies indexed"
**Fix**: Upload a policy - it auto-indexes immediately

**Issue**: Dependencies missing
**Fix**: `pip install -r requirements_ai.txt`

---

**Document maintained by**: Development Team  
**Last reviewed**: November 14, 2025
**Next review**: After frontend AI integration complete

