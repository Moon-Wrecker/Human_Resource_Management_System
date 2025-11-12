# Backend Project Structure

## 📁 Complete Directory Tree

```
backend/
│
├── 📄 main.py                      # FastAPI application entry point
├── 📄 config.py                    # Configuration management (Pydantic settings)
├── 📄 database.py                  # Database connection & session management
├── 📄 models.py                    # SQLAlchemy database models (13 tables)
├── 📄 requirements.txt             # Python dependencies (30+ packages)
│
├── 🔧 .env                         # Environment variables (not in git)
├── 🔧 .env.example                 # Environment template
├── 🔧 .gitignore                   # Git ignore rules
│
├── 📖 README.md                    # Complete backend documentation
├── 📖 QUICK_START.md              # Quick setup guide
├── 📖 PROJECT_STRUCTURE.md         # This file
│
├── 🛠️ setup.ps1                    # Automated setup script (Windows)
├── 🛠️ verify_setup.py             # Setup verification script
│
├── 💾 hr_system.db                 # SQLite database (auto-generated)
│
├── 📁 routes/                      # API route handlers
│   ├── __init__.py
│   ├── auth.py                    # [TODO] Authentication endpoints
│   ├── users.py                   # [TODO] User management
│   ├── dashboard.py               # [TODO] Dashboard APIs
│   ├── jobs.py                    # [TODO] Job listings
│   ├── applications.py            # [TODO] Applications
│   ├── employees.py               # [TODO] Employee management
│   ├── attendance.py              # [TODO] Attendance
│   ├── leaves.py                  # [TODO] Leave management
│   ├── goals.py                   # [TODO] Goals & performance
│   ├── skills.py                  # [TODO] Skill development
│   ├── feedback.py                # [TODO] Feedback
│   ├── teams.py                   # [TODO] Team management
│   ├── announcements.py           # [TODO] Announcements
│   ├── policies.py                # [TODO] Policies
│   ├── payslips.py                # [TODO] Payslips
│   └── resume.py                  # [TODO] Resume screening
│
├── 📁 services/                    # Business logic layer
│   ├── __init__.py
│   ├── auth_service.py            # [TODO] Authentication logic
│   ├── user_service.py            # [TODO] User operations
│   ├── resume_ai_service.py       # [TODO] AI resume screening
│   ├── email_service.py           # [TODO] Email notifications
│   └── file_service.py            # [TODO] File operations
│
├── 📁 utils/                       # Utility functions
│   ├── __init__.py
│   ├── security.py                # [TODO] JWT & password hashing
│   ├── dependencies.py            # [TODO] FastAPI dependencies
│   ├── validators.py              # [TODO] Input validation
│   └── helpers.py                 # [TODO] Helper functions
│
├── 📁 tests/                       # Test files
│   ├── __init__.py
│   ├── test_auth.py               # [TODO] Auth tests
│   ├── test_users.py              # [TODO] User tests
│   ├── test_dashboard.py          # [TODO] Dashboard tests
│   └── ...                        # [TODO] More tests
│
├── 📁 alembic/                     # Database migrations
│   └── versions/                  # Migration files
│
├── 📁 uploads/                     # File storage (not in git)
│   ├── .gitkeep                   # Keep directory in git
│   ├── resumes/                   # Resume uploads
│   ├── documents/                 # Document uploads (Aadhar, PAN)
│   ├── profiles/                  # Profile images
│   ├── policies/                  # Policy documents
│   ├── payslips/                  # Payslip PDFs
│   └── certificates/              # Training certificates
│
└── 📁 __pycache__/                 # Python cache (auto-generated)
```

---

## 📊 Statistics

### Files
- **Core files**: 8 (main.py, config.py, database.py, models.py, etc.)
- **Documentation**: 4 (README.md, QUICK_START.md, etc.)
- **Utility scripts**: 2 (setup.ps1, verify_setup.py)
- **Configuration**: 3 (.env, .env.example, .gitignore)
- **Total**: 18 files created

### Directories
- **Code directories**: 4 (routes, services, utils, tests)
- **Data directories**: 3 (alembic, uploads + 6 subdirectories)
- **Total**: 13 directories created

### Database
- **Tables created**: 13
- **Models defined**: 13
- **Enums defined**: 6
- **Database file**: hr_system.db (SQLite)

### Dependencies
- **Total packages**: 30+
- **Core frameworks**: FastAPI, SQLAlchemy, Uvicorn
- **Authentication**: python-jose, passlib
- **Data validation**: Pydantic
- **File handling**: Pillow, PyPDF2
- **Testing**: pytest

---

## 🔍 File Descriptions

### Core Application Files

#### `main.py` (210 lines)
- FastAPI application initialization
- CORS middleware configuration
- Global exception handlers
- Startup/shutdown events
- Health check endpoint
- API documentation configuration

#### `config.py` (95 lines)
- Pydantic-based settings management
- Environment variable loading
- Configuration validation
- Upload directory creation
- Type-safe configuration access

#### `database.py` (57 lines)
- SQLAlchemy engine setup
- Session management
- Database dependency for FastAPI
- Table creation/deletion functions
- Connection pooling

#### `models.py` (476 lines)
- 13 SQLAlchemy models:
  1. User (employees, HR, managers)
  2. JobListing
  3. Application
  4. Announcement
  5. Attendance
  6. LeaveRequest
  7. Payslip
  8. Goal
  9. GoalCheckpoint
  10. SkillDevelopment
  11. Policy
  12. ResumeScreeningResult
  13. PerformanceReport
- 6 Enum types
- Relationships defined
- Indexes for performance

### Configuration Files

#### `.env`
```env
APP_NAME=GenAI HRMS API
DATABASE_URL=sqlite:///./hr_system.db
SECRET_KEY=...
JWT_SECRET_KEY=...
CORS_ORIGINS=http://localhost:3000,...
```

#### `requirements.txt` (30+ packages)
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pydantic==2.5.3
...
```

#### `.gitignore`
- Python cache files
- Virtual environment
- Database files
- Environment variables
- Upload directories
- IDE files
- Logs

### Documentation Files

#### `README.md` (400+ lines)
- Project overview
- Quick start guide
- API endpoints overview
- Database configuration
- Testing instructions
- Deployment guide

#### `QUICK_START.md`
- 5-minute setup guide
- Common commands
- Troubleshooting
- Environment variables

#### `PROJECT_STRUCTURE.md` (this file)
- Complete directory tree
- File descriptions
- Statistics

### Utility Scripts

#### `setup.ps1` (PowerShell)
- Automated setup for Windows
- Virtual environment creation
- Dependency installation
- Database initialization
- Colored output

#### `verify_setup.py`
- Verify all files exist
- Check directories
- Verify packages installed
- Check database creation
- Detailed status report

---

## 🗄️ Database Schema

### Tables & Relationships

```
users (1) ────────> (N) team_members
  │                       │
  │ manages               │ belongs_to
  │                       │
  └─────────────> (1) manager

users (1) ────────> (N) job_listings (posted_by)
users (1) ────────> (N) applications (applicant)
users (1) ────────> (N) attendance (employee)
users (1) ────────> (N) leave_requests (employee)
users (1) ────────> (N) payslips (employee)
users (1) ────────> (N) goals (employee)
users (1) ────────> (N) skill_developments (employee)

job_listings (1) ─> (N) applications
applications (1) ─> (1) resume_screening_results
goals (1) ────────> (N) goal_checkpoints
```

### Enums

1. **UserRole**: employee, hr, manager, admin
2. **ApplicationStatus**: pending, reviewed, shortlisted, rejected, hired
3. **AttendanceStatus**: present, absent, leave, wfh, holiday
4. **LeaveType**: casual, sick, annual, maternity, paternity
5. **LeaveStatus**: pending, approved, rejected
6. **GoalStatus**: not_started, in_progress, completed

---

## 🚦 API Endpoints (Planned)

### Authentication (`/api/v1/auth`)
- POST `/login` - User login
- POST `/logout` - User logout
- POST `/refresh` - Refresh token

### Users (`/api/v1/users`)
- GET `/me` - Get current user
- PUT `/me` - Update profile

### Dashboard (`/api/v1/dashboard`)
- GET `/hr` - HR dashboard
- GET `/employee` - Employee dashboard
- GET `/manager` - Manager dashboard

### Jobs (`/api/v1/jobs`)
- GET `/` - List jobs
- POST `/` - Create job (HR)
- GET `/{id}` - Job details
- PUT `/{id}` - Update job (HR)

### Applications (`/api/v1/applications`)
- GET `/` - List applications (HR)
- POST `/` - Submit application
- PUT `/{id}/status` - Update status (HR)

### Employees (`/api/v1/employees`)
- GET `/` - List employees
- POST `/` - Create employee (HR)
- GET `/{id}` - Employee details
- PUT `/{id}` - Update employee (HR)

### Attendance (`/api/v1/attendance`)
- GET `/` - Attendance records
- POST `/punch-in` - Punch in
- POST `/punch-out` - Punch out
- GET `/summary` - Summary

### Leaves (`/api/v1/leaves`)
- GET `/` - Leave requests
- POST `/` - Submit request
- PUT `/{id}/status` - Approve/reject
- GET `/balance` - Leave balance

### Goals (`/api/v1/goals`)
- GET `/` - List goals
- POST `/` - Create goal
- GET `/{id}` - Goal details
- PUT `/{id}` - Update goal

### Skills (`/api/v1/skills`)
- GET `/modules` - List modules
- POST `/modules` - Enroll in module
- PUT `/modules/{id}/progress` - Update progress

### Feedback (`/api/v1/feedback`)
- GET `/` - List feedback
- POST `/` - Create feedback
- GET `/{id}` - Feedback details

### Teams (`/api/v1/teams`)
- GET `/members` - Team members (Manager)
- GET `/requests` - Team requests (Manager)
- GET `/statistics` - Team stats (Manager)

### Resume Screening (`/api/v1/resume`)
- POST `/screen` - Screen resume (HR + AI)
- GET `/screen/{id}` - Screening results

---

## 🔐 Security Features

### Implemented
- ✅ CORS configuration
- ✅ Environment variable protection
- ✅ .gitignore for sensitive files
- ✅ SQLAlchemy SQL injection protection
- ✅ Global exception handling

### To Implement (Step 2+)
- ⏳ JWT authentication
- ⏳ Password hashing (bcrypt)
- ⏳ Role-based access control
- ⏳ Rate limiting
- ⏳ Input validation (Pydantic)
- ⏳ File upload validation
- ⏳ HTTPS (production)

---

## 📈 Development Roadmap

### ✅ Step 1: Backend Setup (COMPLETED)
- Project structure
- Database models
- Configuration
- Documentation

### ⏳ Step 2: Authentication (NEXT)
- User registration
- Login/logout
- JWT tokens
- Password hashing

### ⏳ Step 3: Dashboard APIs
- HR dashboard
- Employee dashboard
- Manager dashboard

### ⏳ Step 4: Core Features
- Employee management
- Job listings
- Applications
- Attendance

### ⏳ Step 5: Advanced Features
- Goals & performance
- Skill development
- Feedback system
- File uploads

### ⏳ Step 6: GenAI Features
- Resume screening
- Job description generation
- Performance insights

### ⏳ Step 7: Testing & Deployment
- Unit tests
- Integration tests
- Production deployment
- CI/CD pipeline

---

## 🎯 Next Steps

1. **Add missing models** (30 min)
   - Department, Team, Holiday, Request, Feedback, Notification

2. **Implement authentication** (4-6 hours)
   - Auth routes (`routes/auth.py`)
   - Auth service (`services/auth_service.py`)
   - Security utils (`utils/security.py`)

3. **Create dashboard APIs** (4-6 hours)
   - Dashboard routes (`routes/dashboard.py`)
   - Data aggregation logic

4. **Build remaining APIs** (20-30 hours)
   - Follow priority order in README_BACKEND.md

---

## 📞 Team Coordination

### Share with Frontend Team:
- ✅ Base URL: `http://localhost:8000/api/v1`
- ✅ API Docs: `http://localhost:8000/api/docs`
- ✅ Health Check: `http://localhost:8000/health`
- ⏳ Auth endpoints: Coming in Step 2
- ⏳ Sample JWT token: Coming in Step 2

### Share with Backend Team:
- ✅ This structure document
- ✅ `README.md` for full documentation
- ✅ `QUICK_START.md` for setup
- ✅ `step_1.md` for detailed setup info

---

## 🎉 Congratulations!

You've successfully set up a **production-ready FastAPI backend skeleton** with:

- ✅ Clean project structure
- ✅ Comprehensive database schema
- ✅ Configuration management
- ✅ Error handling & logging
- ✅ CORS for frontend integration
- ✅ Complete documentation
- ✅ Automated setup scripts
- ✅ Verification tools

**Backend Infrastructure: 100% Complete** 🎊

**Ready for API development!** 🚀

---

**Last Updated**: November 11, 2024  
**Version**: 1.0.0  
**Maintainer**: Backend Development Team

