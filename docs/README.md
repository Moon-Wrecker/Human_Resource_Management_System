# HRMS Documentation

Welcome to the GenAI HRMS documentation folder.

## 📚 Main Documentation Files

### 🎯 **[HRMS_COMPLETE_DOCUMENTATION.md](./HRMS_COMPLETE_DOCUMENTATION.md)** 
**Complete system documentation (2200+ lines) - START HERE**

Contains everything you need:
- ✅ Project overview & technology stack
- ✅ Quick start guides (Backend + Frontend + AI)
- ✅ Complete database schema (19 tables)
- ✅ All implemented APIs (77 endpoints)
- ✅ Detailed API implementation guides
- ✅ Role-based access control
- ✅ AI features integration
- ✅ Troubleshooting guide
- ✅ Test credentials

### 🤖 **[AI_SERVICES_COMPLETE_GUIDE.md](./AI_SERVICES_COMPLETE_GUIDE.md)**
**AI Implementation Guide (1000+ lines)**

Deep dive into AI features:
- Policy RAG (Q&A System)
- Resume Screener (Analysis)
- Job Description Generator
- Setup instructions
- API documentation
- Frontend integration
- Best practices

---

## 📊 Project Status

**Current Progress**: **80% Complete** (97 of ~112 APIs implemented)

### ✅ Completed Modules (97 endpoints)

| Module | Endpoints | Status | Description |
|--------|-----------|--------|-------------|
| Authentication | 6 | ✅ Complete | Login, logout, register, password reset |
| Dashboards | 6 | ✅ Complete | HR, Manager, Employee dashboards |
| Profile | 12 | ✅ Complete | Profile CRUD, documents, team info |
| Attendance | 9 | ✅ Complete | Punch in/out, history, summaries |
| Job Listings | 7 | ✅ Complete | Job CRUD, filters, statistics |
| Applications | 9 | ✅ Complete | Apply, view, status, resume upload |
| Announcements | 6 | ✅ Complete | Create, view, update, delete, targeting |
| Policies | 9 | ✅ Complete | CRUD, PDF upload/download, acknowledgments |
| **Feedback** | 9 | ✅ Complete | Give/receive feedback, ratings, statistics |
| **Payslips** | 11 | ✅ Complete | CRUD, PDF docs, bulk generation, stats |
| **AI Services** | 13 | ✅ Complete | Policy RAG, Resume Screener, JD Generator |

### ⏳ Remaining Modules (~15 endpoints)
- Goals (8 APIs) - Employee goal tracking with checkpoints
- Skills (8 APIs) - Skill development and module enrollment
- Leave Management (6 APIs) - Leave requests and approvals
- Performance Reports (4 APIs) - Quarterly performance reviews
- Team Requests (4 APIs) - Manager approval workflows

---

## 🚀 Quick Start

### For New Developers
1. **Read**: [HRMS_COMPLETE_DOCUMENTATION.md](./HRMS_COMPLETE_DOCUMENTATION.md) → Quick Start Guide
2. **Setup**: Follow backend and frontend setup sections
3. **Test**: Login with test credentials (password: `pass123`)
4. **Explore**: Check API documentation at http://localhost:8000/api/docs

### For Backend Developers
1. **Review**: Completed API implementations in main documentation
2. **Study**: Patterns from existing modules (Announcements, Policies)
3. **Choose**: Next API module from "Remaining Modules"
4. **Follow**: Service layer → Routes → Schemas pattern
5. **Test**: Use Swagger UI at http://localhost:8000/api/docs

### For Frontend Developers
1. **Study**: Service layer implementations in `src/services/`
2. **Check**: Component examples in `pages/` folders
3. **Review**: Completed integrations (Profile, Attendance, Jobs, Applications)
4. **Integrate**: Use existing services as templates
5. **Style**: Follow Tailwind + Radix UI patterns

### For AI/ML Developers
1. **Read**: [AI_SERVICES_COMPLETE_GUIDE.md](./AI_SERVICES_COMPLETE_GUIDE.md)
2. **Setup**: Install dependencies: `pip install -r requirements_ai.txt`
3. **Configure**: Add `GOOGLE_API_KEY` to `.env` file
4. **Test**: Run `python test_ai_setup.py`
5. **Integrate**: Use services in `backend/ai_services/`

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens
- **API Docs**: Swagger/OpenAPI
- **Port**: 8000

### Frontend
- **Framework**: React 19.2.0
- **Language**: TypeScript
- **Build Tool**: Vite 7.1.7
- **Routing**: React Router DOM v7
- **Styling**: Tailwind CSS v4
- **UI Components**: Radix UI
- **Charts**: Recharts 2.15.4
- **Port**: 5173

### AI Services
- **Framework**: LangChain
- **AI Model**: Google Gemini (Flash)
- **Vector Store**: FAISS
- **Dependencies**: 46 AI packages
- **Total Endpoints**: 13 AI APIs

---

## 📞 Support & Troubleshooting

### Common Issues

**Backend won't start?**
- Check port 8000 is free
- Verify `venv` is activated
- Run `pip install -r requirements.txt`

**Frontend errors?**
- Run `npm run clear-cache`
- Check `.env` has `VITE_API_BASE_URL=http://localhost:8000`
- Hard refresh: `Ctrl+Shift+R`

**API 403/401 errors?**
- Clear localStorage and re-login
- Check token exists in localStorage
- Verify backend is running

**AI services not working?**
- Check `GOOGLE_API_KEY` in `.env`
- Run `pip install -r requirements_ai.txt`
- Verify with `python test_ai_setup.py`

### Test Credentials

All passwords: `pass123`

**HR Accounts**:
- `sarah.johnson@company.com`
- `linda.martinez@company.com`

**Manager Accounts**:
- `michael.chen@company.com`
- `emily.rodriguez@company.com`
- `david.kim@company.com`

**Employee Accounts**:
- `john.anderson@company.com`
- `alice.williams@company.com`
- `robert.kumar@company.com`

### API Documentation
- **Swagger UI**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health
- **API Root**: http://localhost:8000/api/v1

---

## 📝 Documentation Updates

### November 14, 2025
- ✅ Consolidated all documentation into main file
- ✅ Updated progress to 70% complete (77 endpoints)
- ✅ Added Announcements API (6 endpoints)
- ✅ Added Policies API (9 endpoints)
- ✅ Documented AI Services (13 endpoints)
- ✅ Removed redundant documentation files

### Files Consolidated
- ✅ ANNOUNCEMENTS_API_DOCUMENTATION.md → Main doc
- ✅ ANNOUNCEMENTS_FRONTEND_INTEGRATION.md → Main doc
- ✅ ANNOUNCEMENTS_IMPLEMENTATION_SUMMARY.md → Main doc
- ✅ POLICIES_IMPLEMENTATION_SUMMARY.md → Main doc
- ✅ JOB_LISTINGS_API_IMPLEMENTATION.md → Main doc
- ✅ ATTENDANCE_ERRORS_FIX.md → Main doc
- ✅ AI_TEST_RESULTS.md → Main doc
- ✅ AI_SETUP_COMPLETE.md → Main doc
- ✅ AI_IMPLEMENTATION_SUMMARY.md → Main doc

**Result**: From 12 files → 2 comprehensive files

---

## 🎯 Next Steps

### Immediate Priorities
1. **Goals API** (8 endpoints) - Employee goal tracking with checkpoints
2. **Skills API** (8 endpoints) - Skill development and module enrollment
3. **Feedback API** (5 endpoints) - Manager feedback system

### Documentation Tasks
- Update main doc as new APIs are completed
- Add troubleshooting entries as issues arise
- Keep progress percentage updated

---

**Last Updated**: November 14, 2025  
**Version**: 1.0  
**Status**: Production Ready (70% Complete)  
**Maintained by**: Development Team
