# SE Project - PulseTrack HRMS (GenAI-Powered Human Resource Management System)

Software Engineering Project - September 2025, Team 11

## Problem Statement

**Problem Statement: GenAI-Powered HRMS for Modern Workforce Management**

Design and build a comprehensive Human Resource Management System that leverages GenAI to revolutionize workforce management. HR teams and employees struggle with outdated, manual systems that are inefficient and impersonal. The solution addresses genuine user concerns by integrating AI-powered features for job description generation, resume screening, and policy assistance, making HR processes smarter, faster, and more human-centric. The system caters to multiple user roles including HR managers, employees, team leads, executives, and IT administrators.

## Project Structure

```
├── backend/                    # FastAPI backend application
│   ├── main.py                # Main FastAPI application
│   ├── models.py              # SQLAlchemy database models
│   ├── database.py            # Database configuration
│   ├── config.py              # Configuration settings
│   ├── requirements.txt       # Python dependencies
│   ├── requirements_ai.txt    # AI-specific dependencies
│   ├── hr_system.db           # SQLite database
│   ├── openapi.yaml           # Auto-generated API specification
│   ├── routes/                # API route handlers (24+ modules)
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── employees.py      # Employee management
│   │   ├── dashboard.py      # Role-specific dashboards
│   │   ├── ai_job_description.py    # GenAI JD generator
│   │   ├── ai_resume_screener.py    # GenAI resume analysis
│   │   ├── ai_policy_rag.py         # GenAI policy chatbot
│   │   ├── leaves.py         # Leave management
│   │   ├── attendance.py     # Attendance tracking
│   │   ├── payslips.py       # Payroll management
│   │   ├── feedback.py       # Performance reviews
│   │   ├── goals.py          # Goal setting
│   │   └── ... (18+ more modules)
│   ├── services/              # Business logic services
│   ├── schemas/               # Pydantic request/response schemas
│   ├── ai_services/           # GenAI service integrations
│   │   ├── job_description_generator_service.py
│   │   ├── resume_screener_service.py
│   │   └── policy_rag_service.py
│   ├── ai_data/               # AI data storage
│   │   ├── policy_index/     # Vector database for policies
│   │   ├── resume_analysis/  # Analyzed resumes
│   │   └── temp/             # Temporary AI processing files
│   ├── uploads/               # User-uploaded files
│   │   ├── resumes/
│   │   ├── policies/
│   │   ├── documents/
│   │   └── profiles/
│   └── utils/                 # Utility functions (JWT, password hashing)
├── frontend/                   # React + TypeScript frontend
│   ├── src/                   # Source code
│   │   ├── App.tsx           # Main application component
│   │   ├── router.tsx        # React Router configuration
│   │   ├── pages/            # Page components (32 pages)
│   │   ├── components/       # Reusable UI components (43 components)
│   │   ├── layouts/          # Layout components
│   │   ├── services/         # API service functions (21 services)
│   │   ├── contexts/         # React contexts
│   │   └── hooks/            # Custom React hooks
│   ├── public/                # Public assets
│   ├── package.json           # Node.js dependencies
│   └── vite.config.ts         # Vite build configuration
├── docs/                       # Documentation
│   └── HRMS_COMPLETE_DOCUMENTATION.md
├── README.md                   # Basic project README
└── ultra_readme.md             # This comprehensive README
```

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements_ai.txt
   ```

3. Set up environment variables (create `.env` file in backend/):
   ```env
   SECRET_KEY=your-secret-key-here
   GEMINI_API_KEY=your-google-gemini-api-key
   DATABASE_URL=sqlite:///./hr_system.db
   ```

4. Initialize the database with seed data:
   ```bash
   python seed_comprehensive.py
   ```

5. Run the backend server:
   ```bash
   python main.py
   ```
   Server will start at `http://localhost:8000`

6. View interactive API documentation:
   - Swagger UI: `http://localhost:8000/api/docs`
   - ReDoc: `http://localhost:8000/api/redoc`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Create environment file (`.env` in frontend/):
   ```env
   VITE_API_URL=http://localhost:8000
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```
   Frontend will start at `http://localhost:5173`

### Demo Credentials

For demo purposes, you can use the following credentials:

- **HR Manager**: Username: `hr_admin`, Password: `password123`
- **Employee**: Username: `emp_user`, Password: `password123`  
- **Team Lead**: Username: `manager_user`, Password: `password123`
- **Executive**: Username: `exec_user`, Password: `password123`

## Features

### Core HR Management
- **Employee Management**: Complete employee database with personal, job, and contact details
- **Attendance Tracking**: Real-time attendance monitoring and reporting
- **Leave Management**: Leave application, approval workflow, and balance tracking
- **Payroll System**: Automated payslip generation and salary management
- **Performance Management**: Goal setting, feedback, and performance reviews
- **Department Management**: Organizational structure and department hierarchy
- **Holiday Calendar**: Company-wide holiday management
- **Announcements**: Internal communication and company updates

### GenAI-Powered Features

#### 1. AI Job Description Generator
- **Technology**: Google Gemini 1.5 Flash
- **Capability**: Generate professional job descriptions from simple inputs
- **Features**: 
  - Role-based JD generation
  - Industry-specific customization
  - Skill requirement suggestions
  - Qualification recommendations

#### 2. Smart Resume Screener
- **Technology**: Google Gemini + PyPDF2
- **Capability**: Automated resume analysis and candidate scoring
- **Features**:
  - PDF resume parsing
  - Skill matching against job requirements
  - Candidate ranking
  - Qualification verification
  - Experience analysis

#### 3. 24/7 Policy Chatbot (RAG-based)
- **Technology**: Langchain + ChromaDB + Google Gemini
- **Capability**: Instant answers to company policy questions
- **Features**:
  - Semantic search through policy documents
  - Context-aware responses
  - Source citation
  - Multi-document retrieval
  - Conversational interface

### User Role-Specific Features

#### HR Manager Dashboard
- Real-time workforce analytics
- Department-wise attendance monitoring
- Employee headcount tracking
- Job posting management portal
- Resume screening interface
- Policy management system

#### Employee Portal
- Personal dashboard with performance metrics
- Payslip access and download
- Leave application and tracking
- Policy query chatbot
- Skill development modules
- Goal tracking

#### Team Lead Dashboard
- Team performance monitoring
- Employee review interface
- Goal setting for team members
- Skill assignment and tracking
- Team attendance overview
- Feedback management

#### Executive Dashboard
- Strategic HR analytics
- Workforce insights and trends
- High-level performance metrics
- Budget and headcount planning
- Customizable KPI dashboards

#### IT Administrator Panel
- User role management
- Permission configuration
- System integration settings
- Security and access control
- Audit logs and monitoring

## Technical Architecture

### Backend Stack
- **Framework**: FastAPI (Python 3.x)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Authorization**: Role-Based Access Control (RBAC)
- **API Documentation**: OpenAPI 3.0 / Swagger
- **File Storage**: Local filesystem with organized uploads
- **Validation**: Pydantic schemas

### Frontend Stack
- **Framework**: React 19.2 with TypeScript
- **Routing**: React Router DOM v7
- **UI Library**: Radix UI components
- **Styling**: Tailwind CSS v4
- **Build Tool**: Vite v7
- **State Management**: React Context API
- **HTTP Client**: Axios
- **Charts**: Recharts
- **Icons**: Lucide React

### GenAI Integrations
1. **Google Gemini API** - Natural language processing and content generation
2. **ChromaDB** - Vector database for semantic search
3. **Langchain** - RAG pipeline orchestration and LLM application framework
4. **PyPDF2** - PDF parsing for resume and policy documents

## API Overview

### Statistics
- **Total Endpoints**: 137 API endpoints
- **API Categories**: 24 functional groups
- **User Stories Covered**: 16/16 (100%)
- **GenAI Services**: 4 integrated services
- **Authentication**: JWT-based with role permissions

### Major API Categories
- **Authentication & Authorization** (6 endpoints)
- **Dashboard & Analytics** (6 endpoints)
- **Employee Management** (6 endpoints)
- **AI - Job Description Generator** (4 endpoints)
- **AI - Resume Screener** (4 endpoints)
- **AI - Policy RAG Chatbot** (4 endpoints)
- **Goals & Task Management** (20 endpoints)
- **Leave Management** (11 endpoints)
- **Attendance Tracking** (9 endpoints)
- **Payroll & Payslips** (11 endpoints)
- **Performance Feedback** (9 endpoints)
- **Skills Development** (11 endpoints)
- **Policies & Compliance** (10 endpoints)
- **Job Listings** (7 endpoints)
- Plus 10+ more categories...

### Key API Endpoints

#### GenAI Endpoints
```
POST   /api/v1/ai/job-description/generate    # Generate job description
POST   /api/v1/ai/resume-screener/screen      # Screen resume against JD
POST   /api/v1/ai/policy-rag/ask              # Ask policy question
GET    /api/v1/ai/policy-rag/history          # Get chat history
```

#### Core HRMS Endpoints
```
GET    /api/v1/dashboard/hr                   # HR manager dashboard
GET    /api/v1/dashboard/manager              # Team lead dashboard
GET    /api/v1/employees                      # List employees
POST   /api/v1/leaves                         # Apply for leave
GET    /api/v1/payslips/me                    # Get my payslips
POST   /api/v1/feedback                       # Submit performance feedback
POST   /api/v1/goals                          # Create goal
```

## User Stories Implementation

All 16 user stories from project requirements are fully implemented:

### HR Manager Stories (6/6) ✅
1. ✅ **Dashboard Monitoring** - Real-time workforce analytics and attendance
2. ✅ **Job Description Management** - AI-powered JD generation and management
3. ✅ **Job Posting Management** - Centralized job posting portal
4. ✅ **Employee Database** - Complete employee information management
5. ✅ **Resume Screening** - AI-automated resume analysis and ranking
6. ✅ **Policy Access** - 24/7 policy portal with AI chatbot

### Employee Stories (4/4) ✅
7. ✅ **Performance Tracking** - Personal performance metrics and feedback
8. ✅ **Payslip Access** - Monthly payslip viewing and downloading
9. ✅ **Leave Notifications** - Real-time leave status notifications
10. ✅ **Policy Queries** - Instant policy answers via AI chatbot

### Team Lead Stories (4/4) ✅
11. ✅ **Skill Development** - Team skill tracking and module assignment
12. ✅ **Goal Setting** - Clear goal setting and tracking for team members
13. ✅ **Team Performance Dashboard** - Comprehensive team analytics
14. ✅ **Employee Reviews** - Structured review and feedback system

### Executive & Admin Stories (2/2) ✅
15. ✅ **Strategic Analytics** - High-level HR insights and workforce planning
16. ✅ **System Administration** - User roles, permissions, and security

## Project Milestones

### ✅ Milestone 1: Problem Definition & User Research
- User interviews and surveys conducted
- Problem statement defined
- 16 user stories created across 5 user roles
- Initial requirements gathered

### ✅ Milestone 2: Design & Prototyping
- System architecture designed
- Database schema created
- UI/UX mockups developed
- Technical stack selected

### ✅ Milestone 3: Core Implementation
- Backend API development
- Frontend UI implementation
- Database integration
- Authentication system

### ✅ Milestone 4: API Documentation & GenAI Integration
- 137 API endpoints documented
- OpenAPI/Swagger specification generated
- 4 GenAI services integrated
- Comprehensive error handling
- Complete code documentation

## Testing & Quality Assurance

### Backend Testing
- API endpoint testing
- Authentication and authorization testing
- Database transaction testing
- Error handling validation
- GenAI service integration testing

### Frontend Testing
- Component rendering tests
- User flow testing
- API integration testing
- Cross-browser compatibility
- Responsive design validation

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Granular permission system
- **Password Hashing**: Secure password storage with bcrypt
- **Input Validation**: Comprehensive request validation with Pydantic
- **SQL Injection Prevention**: ORM-based database queries
- **File Upload Security**: Type validation and secure storage
- **API Rate Limiting**: Protection against abuse
- **CORS Configuration**: Controlled cross-origin requests

## Performance Optimization

- **Database Indexing**: Optimized query performance
- **Lazy Loading**: Efficient data loading in frontend
- **Caching**: Strategic caching of frequently accessed data
- **Code Splitting**: Optimized bundle sizes
- **Async Operations**: Non-blocking I/O operations
- **Connection Pooling**: Efficient database connections

## Future Enhancements

- Mobile application (iOS/Android)
- Advanced analytics and reporting
- Integration with third-party HR tools
- Biometric attendance system
- Video interview scheduling
- Learning Management System (LMS)
- Employee self-service mobile app
- Advanced AI features (sentiment analysis, predictive analytics)

## Documentation

- **API Documentation**: `backend/API_DOCUMENTATION_MILESTONE4.md`
- **OpenAPI Specification**: `backend/openapi.yaml`
- **Complete Project Documentation**: `docs/HRMS_COMPLETE_DOCUMENTATION.md`
- **Setup Guides**: `frontend/SetupGuide.md`
- **Troubleshooting**: `frontend/TROUBLESHOOTING.md`
- **User Stories**: `useful_folder/user_stories.md`

## Contributing Team

**Team 11 - IIT Madras**  
Software Engineering Project - September 2025

## License

This project is developed as part of the Software Engineering course at IIT Madras.

## Support & Contact

For issues, questions, or contributions, please refer to the project documentation or contact the development team.

---

**Status**: ✅ All milestones complete | 16/16 user stories implemented | 137 APIs documented | 4 GenAI services integrated

**Last Updated**: November 14, 2025

