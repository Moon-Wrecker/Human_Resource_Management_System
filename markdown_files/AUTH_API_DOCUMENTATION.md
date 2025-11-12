# Authentication API Documentation & Testing

## 📋 Overview

Complete JWT-based authentication system for the GenAI HRMS application.

**Base URL**: `http://localhost:8000/api/v1`  
**Swagger Docs**: `http://localhost:8000/api/docs`  
**ReDoc**: `http://localhost:8000/api/redoc`

---

## 🔐 Authentication Flow

### No Public Signup
- HR/Manager adds employees to the system
- Employees receive credentials from HR
- Direct login with email and password

### JWT Tokens
- **Access Token**: Short-lived (60 minutes) - used for API requests
- **Refresh Token**: Long-lived (30 days) - used to get new access tokens

---

## 📡 API Endpoints

### 1. POST `/auth/login` - User Login

Authenticate user and receive JWT tokens.

**Request Body:**
```json
{
  "email": "sarah.johnson@company.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "email": "sarah.johnson@company.com",
    "name": "Sarah Johnson",
    "role": "hr",
    "employee_id": "EMP001",
    "department_id": 2,
    "job_role": "HR Manager",
    "hierarchy_level": 3
  }
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Incorrect email or password"
}
```

**Test Credentials:**
- **HR**: `sarah.johnson@company.com` / `password123`
- **Manager**: `michael.chen@company.com` / `password123`
- **Employee**: `john.doe@company.com` / `password123`

---

### 2. POST `/auth/refresh` - Refresh Access Token

Get new access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Invalid or expired refresh token"
}
```

---

### 3. GET `/auth/me` - Get Current User

Get current authenticated user information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "sarah.johnson@company.com",
  "name": "Sarah Johnson",
  "role": "hr",
  "employee_id": "EMP001",
  "department_id": 2,
  "job_role": "HR Manager",
  "hierarchy_level": 3
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Invalid authentication credentials"
}
```

---

### 4. POST `/auth/change-password` - Change Password

Change current user's password.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "current_password": "password123",
  "new_password": "newpassword456"
}
```

**Response (200 OK):**
```json
{
  "message": "Password changed successfully"
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Current password is incorrect"
}
```

---

### 5. POST `/auth/reset-password` - Reset Employee Password

Reset employee password. **HR or Manager only**.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "employee_id": 5,
  "new_password": "TempPass123!",
  "require_change_on_login": true
}
```

**Response (200 OK):**
```json
{
  "message": "Password reset successfully for employee ID 5"
}
```

**Response (403 Forbidden):**
```json
{
  "detail": "Only HR or Manager can perform this action"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Employee not found or inactive"
}
```

---

### 6. POST `/auth/logout` - Logout

Logout user (client-side token invalidation).

**Response (200 OK):**
```json
{
  "message": "Logged out successfully"
}
```

**Note**: Client should remove tokens from storage.

---

## 🧪 Test Results

### Test Summary

**Date**: 2025-11-12  
**Total Tests**: 10  
**Passed**: ✅ 10/10 (100%)  
**Failed**: ❌ 0/10 (0%)

### Individual Test Results

| # | Test Name | Status | Details |
|---|-----------|--------|---------|
| 1 | Login as HR | ✅ PASS | Login successful! User: Sarah Johnson (hr) |
| 2 | Login as Manager | ✅ PASS | Login successful! User: Michael Chen (manager) |
| 3 | Login as Employee | ✅ PASS | Login successful! User: John Doe (employee) |
| 4 | Invalid Credentials | ✅ PASS | Correctly rejected with 401 |
| 5 | Get Current User | ✅ PASS | Retrieved user: Sarah Johnson |
| 6 | Get User Without Token | ✅ PASS | Correctly rejected with 403 |
| 7 | Refresh Token | ✅ PASS | Successfully refreshed access token |
| 8 | Change Password | ✅ PASS | Password changed successfully (and reverted) |
| 9 | Reset Password (HR) | ✅ PASS | HR successfully reset employee password |
| 10 | Employee Reset Password | ✅ PASS | Correctly denied with 403 |

---

## 🔒 Security Features

### Password Security
- **Hashing**: BCrypt with automatic salt generation
- **Validation**: Minimum 6 characters (can be adjusted)
- **Reset**: Only HR/Manager can reset passwords
- **Change**: Users can change their own password

### JWT Security
- **Algorithm**: HS256
- **Secret Key**: Configurable via environment variable
- **Token Types**: Separate access and refresh tokens
- **Expiration**: Access token expires in 60 minutes
- **Refresh**: Refresh token expires in 30 days

### Authorization Levels
1. **Public**: Login endpoint
2. **Authenticated**: All endpoints require valid access token
3. **Role-Based**:
   - **HR**: Full access (can reset passwords)
   - **Manager**: Can reset passwords for their team
   - **Employee**: Limited access (can only change own password)

---

## 🚀 Using the API

### Step 1: Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "sarah.johnson@company.com",
    "password": "password123"
  }'
```

### Step 2: Use Access Token

```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <your_access_token>"
```

### Step 3: Refresh Token (when expired)

```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "<your_refresh_token>"
  }'
```

---

## 📂 File Structure

```
backend/
├── routes/
│   └── auth.py                 # Auth endpoints with Swagger docs
├── services/
│   └── auth_service.py         # Auth business logic
├── utils/
│   ├── password_utils.py       # Password hashing/verification
│   ├── jwt_utils.py            # JWT token generation/validation
│   └── dependencies.py         # Reusable FastAPI dependencies
├── schemas/
│   └── auth_schemas.py         # Pydantic request/response models
├── config.py                   # Configuration (JWT settings)
├── main.py                     # FastAPI app with auth routes
└── test_auth.py                # Automated test suite
```

---

## ⚙️ Configuration

Environment variables (`.env` file):

```env
# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30

# Database
DATABASE_URL=sqlite:///./hr_system.db

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 🛡️ Error Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Success |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Invalid/expired token or wrong credentials |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

---

## 📝 Next Steps

### Completed ✅
- [x] JWT authentication implementation
- [x] Login endpoint
- [x] Token refresh
- [x] Password change/reset
- [x] Role-based access control
- [x] Comprehensive testing
- [x] Swagger documentation

### To Be Implemented 🚧
- [ ] Password strength validation
- [ ] Account lockout after failed attempts
- [ ] Email-based password reset
- [ ] Two-factor authentication (2FA)
- [ ] Session management
- [ ] Audit logging for auth events
- [ ] Token blacklist/revocation

---

## 🔗 Related Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

---

**Last Updated**: November 12, 2025  
**API Version**: 1.0.0  
**Test Status**: All tests passing ✅

