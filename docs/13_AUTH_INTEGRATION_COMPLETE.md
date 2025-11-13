# Authentication Integration Complete Guide
## Frontend-Backend Connection for GenAI HRMS

**Date**: November 13, 2025  
**Status**: ✅ **COMPLETE & READY TO TEST**

---

## 🎉 What's Been Completed

### ✅ Backend (Already Existing)
- **6 Authentication APIs**: Fully functional
  - POST `/api/v1/auth/login`
  - POST `/api/v1/auth/logout`
  - POST `/api/v1/auth/refresh`
  - GET `/api/v1/auth/me`
  - POST `/api/v1/auth/change-password`
  - POST `/api/v1/auth/reset-password`

- **Test Users in Database**:
  - HR: `sarah.johnson@company.com` / `password123`
  - Manager: `michael.chen@company.com` / `password123`
  - Employee: `john.doe@company.com` / `password123`

### ✅ Frontend (Just Created)
1. **API Configuration** (`src/config/api.ts`)
   - Base URL configuration
   - All endpoint definitions
   - Environment variable support

2. **Type Definitions** (`src/types/auth.ts`)
   - User interface
   - UserRole enum
   - All request/response types
   - AuthContext interface

3. **API Service** (`src/services/api.ts`)
   - Axios instance with interceptors
   - Automatic token injection
   - Automatic token refresh on 401
   - Error handling utility

4. **Auth Service** (`src/services/authService.ts`)
   - Login method
   - Logout method
   - Refresh token method
   - Get current user method
   - Change password method
   - Reset password method (HR/Manager)
   - LocalStorage management

5. **Auth Context & Provider** (`src/contexts/AuthContext.tsx`)
   - Global auth state management
   - User state
   - Token state
   - Loading state
   - Login/Logout functions
   - Auto token refresh
   - Role-based navigation

6. **Protected Route Component** (`src/components/ProtectedRoute.tsx`)
   - Route protection
   - Role-based access control
   - Automatic redirects
   - Loading states

7. **Updated Login Form** (`src/components/login-form.tsx`)
   - Connected to AuthContext
   - Form validation
   - Error handling
   - Loading states
   - Test credentials display

8. **Updated Router** (`src/router.tsx`)
   - Protected routes for HR, Manager, Employee
   - Role-based access control
   - Import statements for auth components

9. **Updated Main** (`src/main.tsx`)
   - AuthProvider wrapping
   - Router integration

10. **Environment Configuration**
    - `.env` file created
    - `env.template` for reference

---

## 📊 Response Format Matching Analysis

### Backend Response Format

#### Login Response (POST /api/v1/auth/login)
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
    "role": "HR",
    "employee_id": "EMP001",
    "department_id": 2,
    "job_role": "HR Manager",
    "hierarchy_level": 3
  }
}
```

#### Get Current User Response (GET /api/v1/auth/me)
```json
{
  "id": 1,
  "email": "sarah.johnson@company.com",
  "name": "Sarah Johnson",
  "role": "HR",
  "employee_id": "EMP001",
  "department_id": 2,
  "job_role": "HR Manager",
  "hierarchy_level": 3
}
```

#### Error Response
```json
{
  "detail": "Incorrect email or password"
}
```

### Frontend Type Definitions (✅ Matched)

```typescript
// LoginResponse interface matches backend exactly
interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

// User interface matches backend user object
interface User {
  id: number;
  email: string;
  name: string;
  role: UserRole;
  employee_id: string | null;
  department_id: number | null;
  job_role: string | null;
  hierarchy_level: number | null;
}
```

### ✅ Perfect Match
- All field names match exactly
- All types match correctly
- Error handling compatible
- No transformation needed

---

## 🚀 How to Start & Test

### Step 1: Start Backend

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if you have one)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies (if not done)
pip install -r requirements.txt

# Seed database with test users (if needed)
python3 seed_comprehensive.py

# Start backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Test Backend**:
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","environment":"development","version":"1.0.0"}
```

### Step 2: Start Frontend

```bash
# Open new terminal
cd frontend

# Install dependencies (if not done)
npm install

# Start development server
npm run dev
```

**Expected Output**:
```
VITE v7.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### Step 3: Test Login Flow

1. **Open Browser**: Navigate to `http://localhost:5173/login`

2. **Use Test Credentials**:
   - HR: `sarah.johnson@company.com` / `password123`
   - Manager: `michael.chen@company.com` / `password123`
   - Employee: `john.doe@company.com` / `password123`

3. **Expected Flow**:
   - Click "Login" button
   - Loading state shows "Logging in..."
   - On success: Auto redirect to role-specific dashboard
     - HR → `/hr` dashboard
     - Manager → `/manager` dashboard
     - Employee → `/employee` dashboard
   - On error: Red error message displays

4. **Verify Authentication**:
   - Check browser localStorage:
     - `access_token` should be present
     - `refresh_token` should be present
     - `user` should contain user data
   - Check browser DevTools Network tab:
     - POST to `/api/v1/auth/login` should return 200
     - Subsequent requests should have `Authorization: Bearer ...` header

5. **Test Protected Routes**:
   - Try accessing `/hr` as employee → Should redirect to `/employee`
   - Try accessing `/manager` as HR → Should redirect to `/hr`
   - Try accessing any protected route without login → Should redirect to `/login`

6. **Test Logout**:
   - Find logout button in your layout
   - Click logout
   - Should clear localStorage
   - Should redirect to `/login`
   - Trying to access protected routes should redirect to login

---

## 🔍 Testing Checklist

### ✅ Basic Authentication
- [ ] Login with HR credentials → redirects to `/hr`
- [ ] Login with Manager credentials → redirects to `/manager`
- [ ] Login with Employee credentials → redirects to `/employee`
- [ ] Login with invalid credentials → shows error message
- [ ] Login with empty fields → shows validation error

### ✅ Token Management
- [ ] Access token is stored in localStorage
- [ ] Refresh token is stored in localStorage
- [ ] User data is stored in localStorage
- [ ] Authorization header is added to API requests
- [ ] Token refresh happens automatically on 401

### ✅ Protected Routes
- [ ] Cannot access `/hr` without authentication
- [ ] Cannot access `/manager` without authentication
- [ ] Cannot access `/employee` without authentication
- [ ] Role-based access control works (HR can't access `/manager`, etc.)

### ✅ Logout
- [ ] Logout button clears localStorage
- [ ] Logout redirects to `/login`
- [ ] After logout, cannot access protected routes

### ✅ Session Persistence
- [ ] Refresh page while logged in → stays logged in
- [ ] Close browser and reopen → stays logged in (if tokens valid)
- [ ] Expired token triggers refresh automatically

---

## 🐛 Troubleshooting

### Issue: "Network Error" or "Failed to fetch"

**Cause**: Backend not running or CORS issue

**Solution**:
```bash
# 1. Verify backend is running
curl http://localhost:8000/health

# 2. Check backend logs for CORS errors
# Backend should allow http://localhost:5173 in CORS origins

# 3. Verify .env file in frontend
cat frontend/.env
# Should show: VITE_API_BASE_URL=http://localhost:8000
```

### Issue: "401 Unauthorized" on login

**Cause**: Database not seeded or wrong credentials

**Solution**:
```bash
# Seed database
cd backend
python3 seed_comprehensive.py

# Or use these exact credentials:
# sarah.johnson@company.com / password123
```

### Issue: "Module not found" errors in frontend

**Cause**: Dependencies not installed

**Solution**:
```bash
cd frontend
npm install
```

### Issue: Token refresh keeps failing

**Cause**: Refresh token expired or invalid

**Solution**:
1. Clear localStorage in browser DevTools
2. Log in again

### Issue: Can't import from '@/...'

**Cause**: TypeScript path alias not configured

**Solution**: Check `tsconfig.json` has:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### Issue: CORS errors in browser console

**Backend Issue**: Check `backend/config.py`:
```python
CORS_ORIGINS: List[str] = os.getenv(
    "CORS_ORIGINS", 
    "http://localhost:3000,http://localhost:5173,http://localhost:5174"
).split(",")
```

Should include `http://localhost:5173`

---

## 📁 File Structure Created

```
frontend/
├── .env                                    # ✅ Created
├── env.template                            # ✅ Created
├── src/
│   ├── config/
│   │   └── api.ts                         # ✅ Created - API configuration
│   ├── types/
│   │   └── auth.ts                        # ✅ Created - Type definitions
│   ├── services/
│   │   ├── api.ts                         # ✅ Created - Axios instance
│   │   └── authService.ts                 # ✅ Created - Auth methods
│   ├── contexts/
│   │   └── AuthContext.tsx                # ✅ Created - Global auth state
│   ├── components/
│   │   ├── ProtectedRoute.tsx             # ✅ Created - Route protection
│   │   └── login-form.tsx                 # ✅ Updated - Connected to auth
│   ├── router.tsx                         # ✅ Updated - Protected routes
│   └── main.tsx                           # ✅ Updated - AuthProvider added
```

---

## 🔐 Security Features Implemented

1. **Token Storage**: LocalStorage (consider httpOnly cookies for production)
2. **Automatic Token Refresh**: Axios interceptor handles 401 responses
3. **CSRF Protection**: JWT tokens (stateless)
4. **Role-Based Access Control**: Route-level protection
5. **Password Validation**: Minimum 6 characters (frontend + backend)
6. **Secure Headers**: Authorization header for API calls
7. **Error Handling**: Graceful error messages, no sensitive data exposed

---

## 🎯 Next Steps After Auth is Working

Once authentication is verified working:

1. **Update Header/Sidebar Components**:
   ```typescript
   import { useAuth } from '@/contexts/AuthContext';
   
   const Header = () => {
     const { user, logout } = useAuth();
     
     return (
       <header>
         <p>Welcome, {user?.name}</p>
         <button onClick={logout}>Logout</button>
       </header>
     );
   };
   ```

2. **Add Logout Functionality to Layouts**:
   - Update `Employee.tsx`, `HR.tsx`, `Manager.tsx` layouts
   - Add logout button to sidebar or header

3. **Create Profile Page**:
   - Use `authService.getCurrentUser()` to fetch latest user data
   - Use `authService.changePassword()` for password change

4. **Implement Dashboard APIs** (Next Priority):
   - GET `/api/v1/dashboard/hr`
   - GET `/api/v1/dashboard/employee`
   - GET `/api/v1/dashboard/manager`

5. **Add User Context to Other Pages**:
   ```typescript
   const { user } = useAuth();
   // Use user.role, user.name, etc. in components
   ```

---

## 📝 Backend Auth API Summary

All endpoints are **READY and TESTED**:

| Endpoint | Method | Auth Required | Status |
|----------|--------|---------------|--------|
| `/api/v1/auth/login` | POST | ❌ No | ✅ Ready |
| `/api/v1/auth/logout` | POST | ✅ Yes | ✅ Ready |
| `/api/v1/auth/refresh` | POST | ❌ No | ✅ Ready |
| `/api/v1/auth/me` | GET | ✅ Yes | ✅ Ready |
| `/api/v1/auth/change-password` | POST | ✅ Yes | ✅ Ready |
| `/api/v1/auth/reset-password` | POST | ✅ Yes (HR/Manager) | ✅ Ready |

---

## 🧪 Manual Testing Script

```bash
# 1. Test Backend Health
curl http://localhost:8000/health

# 2. Test Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"sarah.johnson@company.com","password":"password123"}'

# Save the access_token from response

# 3. Test Get Current User
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"

# 4. Test Logout
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

---

## ✅ Completion Checklist

### Backend
- [x] Auth APIs implemented
- [x] JWT token generation working
- [x] Token verification working
- [x] Role-based access control
- [x] Test users in database
- [x] CORS configured

### Frontend
- [x] API configuration created
- [x] Type definitions created
- [x] Axios instance with interceptors
- [x] Auth service with all methods
- [x] Auth context & provider
- [x] Protected route component
- [x] Login form updated
- [x] Router protected
- [x] Main.tsx wrapped with AuthProvider
- [x] Environment variables configured

### Integration
- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Login flow tested and working
- [ ] Token refresh working
- [ ] Protected routes working
- [ ] Logout working
- [ ] Role-based navigation working

---

## 🎓 How It All Works Together

### Login Flow
1. User enters credentials in login form
2. Form calls `login()` from AuthContext
3. AuthContext calls `authService.login()`
4. authService makes POST to `/api/v1/auth/login` via axios
5. Backend validates credentials, returns tokens + user data
6. authService stores tokens in localStorage
7. AuthContext updates state with user & token
8. AuthContext navigates to role-specific dashboard
9. All subsequent API calls include Authorization header (via interceptor)

### Token Refresh Flow
1. User makes API request
2. Backend returns 401 (token expired)
3. Axios interceptor catches 401
4. Interceptor calls `/api/v1/auth/refresh` with refresh_token
5. Backend returns new access_token
6. Interceptor updates localStorage
7. Interceptor retries original request with new token
8. If refresh fails, user is logged out and redirected to login

### Protected Route Flow
1. User tries to access `/hr`
2. ProtectedRoute component checks `isAuthenticated`
3. If not authenticated → redirect to `/login`
4. If authenticated, check user role vs allowedRoles
5. If role allowed → render children (HR layout)
6. If role not allowed → redirect to user's default dashboard

---

## 🚀 You're Ready!

**Everything is connected and ready to test!**

1. Start backend: `uvicorn main:app --reload` (in backend folder)
2. Start frontend: `npm run dev` (in frontend folder)
3. Open browser: `http://localhost:5173/login`
4. Login with test credentials
5. Enjoy your fully integrated authentication system! 🎉

---

**Questions or Issues?**
- Check the Troubleshooting section above
- Verify both backend and frontend are running
- Check browser console for errors
- Check backend logs for API errors
- Verify .env file has correct API_BASE_URL

---

*Document Version: 1.0*  
*Last Updated: November 13, 2025*  
*Status: Complete & Ready for Testing*

