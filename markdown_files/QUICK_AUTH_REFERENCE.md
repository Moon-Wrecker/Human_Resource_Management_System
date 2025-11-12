# Authentication - Quick Reference

## 🚀 Quick Start

### Start Server
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

### Access Swagger
```
http://localhost:8000/api/docs
```

---

## 🔑 Test Credentials

| Role | Email | Password |
|------|-------|----------|
| HR | `sarah.johnson@company.com` | `password123` |
| Manager | `michael.chen@company.com` | `password123` |
| Employee | `john.doe@company.com` | `password123` |

---

## 📡 Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/v1/auth/login` | POST | ❌ | Login |
| `/api/v1/auth/refresh` | POST | ❌ | Refresh token |
| `/api/v1/auth/me` | GET | ✅ | Get user info |
| `/api/v1/auth/change-password` | POST | ✅ | Change password |
| `/api/v1/auth/reset-password` | POST | ✅ HR/Mgr | Reset password |
| `/api/v1/auth/logout` | POST | ❌ | Logout |

---

## 💻 Quick Examples

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"sarah.johnson@company.com","password":"password123"}'
```

### Get Current User
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Change Password
```bash
curl -X POST http://localhost:8000/api/v1/auth/change-password \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"current_password":"password123","new_password":"newpass123"}'
```

---

## 🔐 Token Details

- **Access Token**: 60 minutes
- **Refresh Token**: 30 days
- **Format**: `Authorization: Bearer <token>`

---

## ✅ Test Status

**All 10 tests passing!**

1. ✅ Login as HR
2. ✅ Login as Manager
3. ✅ Login as Employee
4. ✅ Invalid credentials (401)
5. ✅ Get current user
6. ✅ No token rejected (403)
7. ✅ Refresh token
8. ✅ Change password
9. ✅ Reset password (HR)
10. ✅ Employee forbidden (403)

---

**Full Documentation**: See `AUTH_API_DOCUMENTATION.md`

