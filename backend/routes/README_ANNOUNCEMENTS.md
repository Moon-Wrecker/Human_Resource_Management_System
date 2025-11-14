# Announcements API - Quick Reference

**Status**: ✅ Production Ready  
**Last Updated**: November 14, 2025

---

## 🚀 Quick Start

### 1. Start Backend
```bash
cd backend
python main.py
```

API available at: `http://localhost:8000`

### 2. Test the API
```bash
cd backend/tests
python test_announcements_api.py
```

### 3. View API Docs
Open in browser: `http://localhost:8000/api/docs`

---

## 📋 Endpoints

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | `/api/v1/announcements` | All | List announcements |
| GET | `/api/v1/announcements/{id}` | All | Get by ID |
| POST | `/api/v1/announcements` | HR/Manager | Create |
| PUT | `/api/v1/announcements/{id}` | HR/Manager | Update |
| DELETE | `/api/v1/announcements/{id}` | HR/Manager | Delete |
| GET | `/api/v1/announcements/stats/summary` | HR/Manager | Statistics |

---

## 🔑 Authentication

All endpoints require JWT Bearer token:

```bash
# 1. Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "sarah.johnson@company.com", "password": "password123"}'

# 2. Use token
curl -X GET "http://localhost:8000/api/v1/announcements" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📝 Example Requests

### Create Announcement
```bash
curl -X POST "http://localhost:8000/api/v1/announcements" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Office Holiday",
    "message": "Office closed tomorrow",
    "is_urgent": false
  }'
```

### Get All Announcements
```bash
curl -X GET "http://localhost:8000/api/v1/announcements?limit=10" \
  -H "Authorization: Bearer TOKEN"
```

### Update Announcement
```bash
curl -X PUT "http://localhost:8000/api/v1/announcements/1" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"is_urgent": true}'
```

### Delete Announcement
```bash
curl -X DELETE "http://localhost:8000/api/v1/announcements/1" \
  -H "Authorization: Bearer TOKEN"
```

---

## 📚 Full Documentation

- **Complete API Reference**: `/docs/ANNOUNCEMENTS_API_DOCUMENTATION.md`
- **Frontend Integration**: `/docs/ANNOUNCEMENTS_FRONTEND_INTEGRATION.md`
- **Implementation Summary**: `/docs/ANNOUNCEMENTS_IMPLEMENTATION_SUMMARY.md`

---

## 🧪 Testing

Run the comprehensive test suite:
```bash
cd backend/tests
python test_announcements_api.py
```

---

## 📁 Files

### Backend
- `backend/routes/announcements.py` - API endpoints
- `backend/services/announcement_service.py` - Business logic
- `backend/schemas/announcement_schemas.py` - Validation schemas

### Frontend
- `frontend/src/services/announcementService.ts` - Service layer

### Tests
- `backend/tests/test_announcements_api.py` - Test suite

---

## ✅ Ready to Use!

The API is fully functional and integrated into the application. Start the backend and begin testing immediately!

