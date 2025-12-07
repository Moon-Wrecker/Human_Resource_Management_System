# PulseTrack HRMS - GenAI-Powered Human Resource Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.2-blue.svg)](https://reactjs.org/)

> **Team 11** | Software Engineering Project | IIT Madras | September 2025

PulseTrack HRMS is a **next-generation, AI-powered Human Resource Management System** designed to revolutionize workforce management by making HR processes smarter, faster, and more human-centric. Built with cutting-edge GenAI technologies, PulseTrack brings intelligence and automation to every aspect of HR operations.

---

## 🚀 What Makes PulseTrack HRMS Different?

Unlike traditional HRMS applications, PulseTrack HRMS stands out with:

### 🤖 **AI-First Architecture**

- **Smart Policy Assistant**: 24/7 AI-powered chatbot using Retrieval-Augmented Generation (RAG) for instant policy queries
- **Intelligent Resume Screening**: AI analyzes and ranks candidates automatically based on job requirements
- **Auto Job Description Generator**: Creates professional, comprehensive JDs using Google Gemini AI
- **AI Performance Insights**: Automated performance report generation with actionable recommendations

### 🎯 **Modern Technology Stack**

- **FastAPI Backend**: High-performance, async Python framework with auto-generated API documentation
- **React 19 Frontend**: Modern, responsive UI with TypeScript and Tailwind CSS
- **Vector Database**: ChromaDB for semantic search capabilities
- **LangChain Integration**: Advanced RAG pipeline for intelligent document processing

### 💡 **User-Centric Design**

- **Role-Based Dashboards**: Personalized dashboards for HR, Managers, Employees, and Executives
- **Real-Time Analytics**: Live workforce insights and performance metrics
- **Self-Service Portal**: Empowers employees with instant access to payslips, policies, and more
- **Mobile-Responsive**: Works seamlessly across all devices

### ⚡ **Comprehensive Feature Set**

- **165+ API Endpoints**: Fully documented with OpenAPI/Swagger
- **16 User Stories**: Complete implementation covering all HR workflows
- **Multi-Role Access Control**: Granular permissions for different user types
- **Enterprise-Grade Security**: JWT authentication, password hashing, role-based access

### 🔄 **Automation & Efficiency**

- Automated leave approvals workflow
- Intelligent goal tracking with milestone management
- Automated payslip generation
- Bulk employee data management

---

## 📋 Features Overview

### For HR Managers

- 📊 **Comprehensive Dashboard** with real-time workforce analytics
- 🤖 **AI Resume Screener** for automated candidate evaluation
- 📝 **AI Job Description Generator** for creating professional JDs
- 👥 **Employee Database Management** with advanced filtering
- 📋 **Policy Management** with AI-powered search
- 📢 **Announcements** and company-wide communications

### For Managers/Team Leads

- 🎯 **Team Performance Dashboard** with detailed metrics
- ✅ **Goal Setting & Tracking** for team members
- 💬 **Feedback Management** for continuous employee reviews
- 📚 **Skill Development** module management
- 👥 **Team Request Management** (leave approvals, access requests)
- 📊 **Team Analytics** and performance insights

### For Employees

- 🏠 **Personal Dashboard** with performance overview
- 💰 **Payslip Access** with download functionality
- 📅 **Leave Management** with real-time status updates
- 🎓 **Skill Development** tracking and course enrollment
- 💬 **Feedback Review** from managers and peers
- 🤖 **AI Policy Chatbot** for instant HR policy answers
- 📢 **Company Announcements** and updates

### AI-Powered Features

- 🧠 **Policy RAG Chatbot**: Ask any policy question in natural language
- 🔍 **Resume Screener**: Upload resumes and get AI-powered candidate rankings
- ✍️ **JD Generator**: Generate professional job descriptions from simple requirements
- 📈 **Performance Reports**: AI-generated insights and recommendations

---

## 🛠️ Technology Stack

### Backend

- **Framework**: FastAPI (Python 3.8+)
- **Database**: SQLite with SQLAlchemy ORM
- **AI/ML**:
  - Google Gemini API (Natural Language Processing)
  - ChromaDB (Vector Database)
  - LangChain (RAG Framework)
  - PyPDF2 (Document Processing)
- **Authentication**: JWT tokens with bcrypt password hashing
- **API Documentation**: Auto-generated OpenAPI 3.0 (Swagger/ReDoc)

### Frontend

- **Framework**: React 19.2 with TypeScript
- **Styling**: Tailwind CSS 4.1
- **UI Components**: Radix UI primitives
- **Charts**: Recharts for data visualization
- **Routing**: React Router v7
- **HTTP Client**: Axios
- **Build Tool**: Vite 7

### DevOps & Tools

- **Version Control**: Git
- **Package Management**: pip/uv (Python), pnpm (Node.js)
- **Development**: Hot reload, auto-restart
- **Testing**: Comprehensive test suite for APIs

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** and npm ([Download](https://nodejs.org/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Google Gemini API Key** ([Get one free](https://makersuite.google.com/app/apikey))

### Installation & Setup

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-org/soft-engg-project-sep-2025-se-SEP-11.git
cd soft-engg-project-sep-2025-se-SEP-11
```

#### 2️⃣ Backend Setup

**For Windows:**

```bash
pip3 install uv

# Create .venv
uv venv
uv sync

.venv/scripts/activate

# Create .env file (copy from .env.example if available)
# Add your configuration:
# - GOOGLE_API_KEY=your-gemini-api-key
# - GOOGLE_API_KEY_1=your-gemini-api-key

# Initialize database and seed data
uv run backend/database.py
uv run backend/seed_data.py

# Start the backend server
uv run backend/main.py
```

**For Linux/Mac:**

```bash
pip3 install uv

# Create .venv
uv venv
uv sync

source .venv/scripts/activate

# Create .env file (copy from .env.example if available)
# Add your configuration:
# - GOOGLE_API_KEY=your-gemini-api-key
# - GOOGLE_API_KEY_1=your-gemini-api-key

# Initialize database and seed data
uv run backend/database.py
uv run backend/seed_data.py

# Start the backend server
uv run backend/main.py

```

The backend will start at: `http://localhost:8000`

- API Documentation: `http://localhost:8000/api/docs`
- Alternative Docs: `http://localhost:8000/api/redoc`
- Health Check: `http://localhost:8000/health`

#### 3️⃣ Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file from template
cp env.template .env

# Update .env with backend URL (default: http://localhost:8000)
# VITE_API_BASE_URL=http://localhost:8000

# Start development server
npm run dev
```

The frontend will start at: `http://localhost:5173`

---

## 🧪 Test Credentials

After running `seed_data.py`, you can login with these credentials:

### HR Manager

- **Email**: `sarah.johnson@company.com`
- **Password**: `pass123`

### Team Manager

- **Email**: `michael.chen@company.com`
- **Password**: `pass123`

### Employee

- **Email**: `john.anderson@company.com`
- **Password**: `pass123`

---

## 📊 Project Statistics

- **Total API Endpoints**: 165+
- **User Stories Implemented**: 16/16 (100%)
- **Lines of Code**: 15,000+
- **API Categories**: 24 distinct modules
- **AI Integrations**: 4 (Gemini, ChromaDB, LangChain, PyPDF2)
- **Database Tables**: 20+ comprehensive entities
- **Role Types**: 5 (HR, Manager, Employee, Executive, IT Admin)

---

## 📁 Project Structure

```
soft-engg-project-sep-2025-se-SEP-11/
├── backend/                    # FastAPI backend
│   ├── routes/                # API route handlers (24 modules)
│   ├── services/              # Business logic layer
│   ├── schemas/               # Pydantic models for validation
│   ├── ai_services/           # AI integration services
│   ├── models.py              # SQLAlchemy database models
│   ├── main.py                # FastAPI application entry point
│   ├── database.py            # Database configuration
│   ├── config.py              # Application settings
│   ├── seed_data.py           # Database seeding script
│   └── requirements.txt       # Python dependencies
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/             # Page components (HR, Manager, Employee)
│   │   ├── services/          # API client services
│   │   ├── contexts/          # React contexts (Auth)
│   │   ├── layouts/           # Layout components
│   │   └── router.tsx         # Application routing
│   └── package.json           # Node.js dependencies
├── docs/                       # Documentation
│   └── HRMS_COMPLETE_DOCUMENTATION.md
└── README.md                   # This file
```

---

## 🎯 Key Differentiators vs Traditional HRMS

| Feature               | Traditional HRMS                  | PulseTrack HRMS                                |
| --------------------- | --------------------------------- | ---------------------------------------------- |
| **Policy Queries**    | Search through documents manually | AI-powered 24/7 chatbot with instant answers   |
| **Resume Screening**  | Manual review by HR team          | Automated AI screening with candidate ranking  |
| **Job Descriptions**  | Written manually                  | AI-generated professional JDs in seconds       |
| **API Documentation** | Often outdated or missing         | Auto-generated, always up-to-date Swagger docs |
| **Tech Stack**        | Legacy frameworks                 | Modern FastAPI + React 19                      |
| **Performance**       | Synchronous, slower               | Async, high-performance architecture           |
| **User Experience**   | Complex, cluttered UI             | Clean, role-specific, intuitive interface      |
| **Mobile Support**    | Limited or none                   | Fully responsive design                        |
| **Development**       | Slow iteration cycles             | Hot reload, fast development                   |
| **Scalability**       | Monolithic architecture           | Microservices-ready, modular design            |

---

## 📖 Documentation

- **Complete Documentation**: [`docs/HRMS_COMPLETE_DOCUMENTATION.md`](docs/HRMS_COMPLETE_DOCUMENTATION.md)
- **API Documentation**: Available at `http://localhost:8000/api/docs` when server is running
- **OpenAPI Specification**: [`backend/openapi.yaml`](backend/openapi.yaml)
- **Frontend Setup Guide**: [`frontend/SetupGuide.md`](frontend/SetupGuide.md)
- **Troubleshooting**: [`frontend/TROUBLESHOOTING.md`](frontend/TROUBLESHOOTING.md)

---

## 🤝 Contributing

This is an academic project for IIT Madras Software Engineering course (Team 11, September 2025).

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Team

**Team 11** - IIT Madras, Software Engineering Project, September 2025

---

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- FastAPI framework for excellent developer experience
- React and Tailwind CSS communities for modern frontend tools
- LangChain for RAG implementation
- All open-source contributors

---

## 📞 Support

For issues, questions, or contributions:

- **Documentation**: See `docs/` folder
- **API Issues**: Check `http://localhost:8000/api/docs`

---

**Built with ❤️ by Team 11**
