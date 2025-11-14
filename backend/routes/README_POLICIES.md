# Policies API - Quick Reference

**Status**: ✅ Production Ready with File Upload/Download  
**Last Updated**: November 14, 2025

---

## 🚀 Quick Start

### 1. Start Backend
```bash
cd backend
python main.py
```

API available at: `http://localhost:8000`

### 2. View API Docs
Open in browser: `http://localhost:8000/api/docs`

---

## 📋 Endpoints

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | `/api/v1/policies` | All | List policies |
| GET | `/api/v1/policies/{id}` | All | Get by ID |
| POST | `/api/v1/policies` | HR/Manager | Create |
| PUT | `/api/v1/policies/{id}` | HR/Manager | Update |
| DELETE | `/api/v1/policies/{id}` | HR/Manager | Delete |
| **POST** | `/api/v1/policies/{id}/upload` | **HR/Manager** | **Upload PDF** |
| **GET** | `/api/v1/policies/{id}/download` | **All** | **Download PDF** |
| POST | `/api/v1/policies/{id}/acknowledge` | All | Acknowledge |
| GET | `/api/v1/policies/{id}/acknowledgments` | HR/Manager | Get acknowledgments |
| GET | `/api/v1/policies/stats/summary` | HR/Manager | Statistics |

---

## 🔑 Authentication

All endpoints require JWT Bearer token:

```bash
# 1. Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "sarah.johnson@company.com", "password": "password123"}'

# 2. Use token
curl -X GET "http://localhost:8000/api/v1/policies" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📝 Example Requests

### Create Policy
```bash
curl -X POST "http://localhost:8000/api/v1/policies" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Remote Work Policy",
    "content": "Policy content here...",
    "category": "HR",
    "effective_date": "2025-01-01"
  }'
```

### Upload PDF Document
```bash
curl -X POST "http://localhost:8000/api/v1/policies/1/upload" \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@policy-document.pdf"
```

### Download PDF Document
```bash
curl -X GET "http://localhost:8000/api/v1/policies/1/download" \
  -H "Authorization: Bearer TOKEN" \
  --output policy.pdf
```

### Acknowledge Policy
```bash
curl -X POST "http://localhost:8000/api/v1/policies/1/acknowledge" \
  -H "Authorization: Bearer TOKEN"
```

### Get All Policies
```bash
curl -X GET "http://localhost:8000/api/v1/policies?limit=10" \
  -H "Authorization: Bearer TOKEN"
```

---

## 📁 Files

### Backend
- `backend/routes/policies.py` - API endpoints
- `backend/services/policy_service.py` - Business logic + file handling
- `backend/schemas/policy_schemas.py` - Validation schemas
- `backend/models.py` - Database models (Policy, PolicyAcknowledgment)

### Frontend
- `frontend/src/services/policyService.ts` - Service layer with file upload/download

### Storage
- `backend/uploads/policies/` - PDF document storage

---

## 🎯 Key Features

✅ **CRUD Operations** - Create, Read, Update, Delete  
✅ **File Upload** - PDF documents with validation  
✅ **File Download** - Secure file serving  
✅ **Acknowledgment Tracking** - Who acknowledged and when  
✅ **Role-Based Access** - HR/Manager can manage, All can view  
✅ **Statistics** - Category breakdown, acknowledgment counts  
✅ **Soft Delete** - Audit trail maintained  

---

## 🔐 File Upload Limits

- **Allowed Types**: PDF only
- **Max File Size**: 10MB
- **Storage**: `uploads/policies/`
- **Validation**: Type, size, filename checks

---

## 📚 Full Documentation

- **Implementation Summary**: `/docs/POLICIES_IMPLEMENTATION_SUMMARY.md`
- **Swagger UI**: `http://localhost:8000/api/docs`

---

## ✅ Ready to Use!

The API is fully functional with complete file upload/download support. Start the backend and begin testing immediately!

**Note**: Unlike simple CRUD APIs, this includes real file handling with validation, security, and proper cleanup!

