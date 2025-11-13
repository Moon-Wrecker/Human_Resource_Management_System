# GenAI HRMS - Backend API

FastAPI-based backend for the GenAI Human Resource Management System.

---

## 🎉 Step 1: Backend Setup - ✅ COMPLETED

### What's Ready:
- ✅ FastAPI application with 210+ lines
- ✅ Database with 13 models
- ✅ Configuration management
- ✅ CORS & error handling
- ✅ Project structure (7 directories)
- ✅ Complete documentation
- ✅ Automated setup scripts
- ✅ Verification tools

### Database Tables Created:
✅ users | ✅ job_listings | ✅ applications | ✅ announcements  
✅ attendance | ✅ leave_requests | ✅ payslips | ✅ goals  
✅ goal_checkpoints | ✅ skill_developments | ✅ policies  
✅ resume_screening_results | ✅ performance_reports

### Next Step: **Step 2 - Authentication APIs** 🔐

---

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and update values:

```bash
# The .env file is already created with development defaults
# For production, update SECRET_KEY, JWT_SECRET_KEY, and DATABASE_URL
```

### 4. Initialize Database

```bash
# Create database tables
python database.py
```

### 5. Run Development Server

```bash
# Run with auto-reload
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

API Documentation (Swagger UI): `http://localhost:8000/api/docs`

## 📁 Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration settings
├── database.py            # Database connection & session
├── models.py              # SQLAlchemy database models
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
│
├── routes/               # API route handlers
│   ├── __init__.py
│   ├── auth.py          # Authentication endpoints
│   ├── users.py         # User management
│   ├── dashboard.py     # Dashboard APIs
│   ├── jobs.py          # Job listings
│   ├── applications.py  # Job applications
│   ├── employees.py     # Employee management
│   ├── attendance.py    # Attendance tracking
│   ├── leaves.py        # Leave management
│   ├── goals.py         # Goals & performance
│   ├── skills.py        # Skill development
│   ├── feedback.py      # Feedback system
│   ├── teams.py         # Team management
│   └── ...
│
├── services/            # Business logic layer
│   ├── __init__.py
│   ├── auth_service.py
│   ├── user_service.py
│   ├── resume_ai_service.py
│   └── ...
│
├── utils/               # Utility functions
│   ├── __init__.py
│   ├── security.py      # Password hashing, JWT
│   ├── validators.py    # Input validation
│   ├── helpers.py       # Helper functions
│   └── dependencies.py  # FastAPI dependencies
│
├── tests/               # Test files
│   ├── __init__.py
│   ├── test_auth.py
│   └── ...
│
├── alembic/             # Database migrations
│   └── versions/
│
└── uploads/             # File uploads (not in git)
    ├── resumes/
    ├── documents/
    ├── profiles/
    ├── policies/
    ├── payslips/
    └── certificates/
```

## 🔗 API Endpoints

### Base URL
```
http://localhost:8000/api/v1
```

### Available Endpoints

- **Authentication**: `/api/v1/auth`
  - POST `/login` - User login
  - POST `/logout` - User logout
  - POST `/refresh` - Refresh token

- **Users**: `/api/v1/users`
  - GET `/me` - Get current user
  - PUT `/me` - Update profile

- **Dashboard**: `/api/v1/dashboard`
  - GET `/hr` - HR dashboard data
  - GET `/employee` - Employee dashboard data
  - GET `/manager` - Manager dashboard data

- **Jobs**: `/api/v1/jobs`
  - GET `/` - List all jobs
  - POST `/` - Create job (HR only)
  - GET `/{id}` - Get job details
  - PUT `/{id}` - Update job (HR only)

- **Applications**: `/api/v1/applications`
  - GET `/` - List applications (HR)
  - POST `/` - Submit application
  - PUT `/{id}/status` - Update status (HR)

- **Employees**: `/api/v1/employees`
  - GET `/` - List employees
  - POST `/` - Create employee (HR)
  - GET `/{id}` - Get employee details
  - PUT `/{id}` - Update employee (HR)

- **Attendance**: `/api/v1/attendance`
  - GET `/` - Get attendance records
  - POST `/punch-in` - Punch in
  - POST `/punch-out` - Punch out
  - GET `/summary` - Attendance summary

- **Leaves**: `/api/v1/leaves`
  - GET `/` - List leave requests
  - POST `/` - Submit leave request
  - PUT `/{id}/status` - Approve/reject (Manager/HR)
  - GET `/balance` - Leave balance

For complete API documentation, see: `../README_BACKEND.md`

## 🔒 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Login Flow

1. POST credentials to `/api/v1/auth/login`
2. Receive `access_token` and `refresh_token`
3. Include `access_token` in Authorization header: `Bearer <token>`
4. Refresh token when expired using `/api/v1/auth/refresh`

### Role-Based Access

- **Employee**: Basic access to own data
- **Manager**: Access to team data + approval permissions
- **HR**: Full access to all employee data + system management
- **Admin**: Full system access

## 🗄️ Database

### Development
- SQLite (default): `sqlite:///./hr_system.db`
- No additional setup required

### Production
- PostgreSQL (recommended): `postgresql://user:pass@localhost/hrms_db`
- MySQL (alternative): `mysql+pymysql://user:pass@localhost/hrms_db`

### Database Models

23 models covering:
- User & Organization (Department, Team)
- Jobs & Applications
- Attendance & Leave Management
- Goals & Performance
- Skill Development
- Feedback & Communication
- Policies & Payroll

See `models.py` for complete schema.

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_auth.py
```

## 📝 Environment Variables

Key variables in `.env`:

```env
# Security (CHANGE IN PRODUCTION!)
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database
DATABASE_URL=sqlite:///./hr_system.db

# CORS (Frontend URLs)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 🚢 Production Deployment

### Using Gunicorn

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker

```bash
# Build image
docker build -t hrms-backend .

# Run container
docker run -p 8000:8000 hrms-backend
```

## 📊 Development Workflow

1. Create feature branch
2. Implement endpoints in `routes/`
3. Add business logic in `services/`
4. Write tests in `tests/`
5. Update documentation
6. Submit PR

## 🐛 Debugging

### Check API Health

```bash
curl http://localhost:8000/health
```

### View Logs

The application logs all requests and errors. Check console output.

### Database Issues

```bash
# Recreate database
python database.py
```

## 📚 Additional Resources

- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- Pydantic Documentation: https://docs.pydantic.dev/

## 👥 Team

Backend Development Team - GenAI HRMS Project

## 📄 License

Internal project - All rights reserved

