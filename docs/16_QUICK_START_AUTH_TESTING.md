# Quick Start: Testing Authentication Integration

**Goal**: Get the full auth system running in under 5 minutes!

---

## ⚡ Prerequisites

- ✅ Node.js installed (v18+ recommended)
- ✅ Python 3.8+ installed
- ✅ pip installed

---

## 🚀 5-Minute Setup

### Terminal 1: Backend

```bash
# 1. Navigate to project root
cd /home/manasrastogi/Documents/Personal_Project/soft-engg-project-sep-2025-se-SEP-11

# 2. Activate virtual environment (use the existing venv in project root)
source venv/bin/activate

# 3. Navigate to backend
cd backend

# 4. Install/upgrade dependencies (if needed)
pip install pydantic-settings

# 5. Verify database exists and has data
python3 -c "from database import engine, SessionLocal; from models import User; session = SessionLocal(); print(f'Users in database: {session.query(User).count()}'); session.close()"

# If shows 0 users, seed the database:
python3 seed_comprehensive.py

# 6. Start backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Leave this terminal running!**

---

### Terminal 2: Frontend

```bash
# 1. Open new terminal, navigate to frontend
cd /home/manasrastogi/Documents/Personal_Project/soft-engg-project-sep-2025-se-SEP-11/frontend

# 2. Verify dependencies installed
npm list axios

# If axios not found:
npm install

# 3. Verify .env file exists
cat .env

# If file doesn't exist or empty:
echo "VITE_API_BASE_URL=http://localhost:8000" > .env
echo "VITE_ENV=development" >> .env

# 4. Start frontend dev server
npm run dev
```

**Expected Output**:
```
VITE v7.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

**Leave this terminal running!**

---

## 🧪 Test Authentication

### Step 1: Open Browser

Navigate to: `http://localhost:5173/login`

### Step 2: Test Login

Use any of these test accounts:

| Role | Email | Password |
|------|-------|----------|
| HR | sarah.johnson@company.com | password123 |
| Manager | michael.chen@company.com | password123 |
| Employee | john.doe@company.com | password123 |

### Step 3: Verify Success

✅ **On Successful Login:**
- No error message appears
- Page redirects automatically:
  - HR → `/hr` (HR Dashboard)
  - Manager → `/manager` (Manager Dashboard)
  - Employee → `/employee` (Employee Dashboard)

✅ **Check LocalStorage:**
Open browser DevTools → Application → LocalStorage → `http://localhost:5173`

Should see:
- `access_token` - JWT token
- `refresh_token` - Refresh token
- `user` - JSON with user data

### Step 4: Verify Protected Routes

Try these URLs manually:

| URL | Expected Behavior |
|-----|-------------------|
| `/login` | Shows login page (if not logged in) |
| `/hr` | Redirects to login (if not logged in) |
| `/manager` | Redirects to login (if not logged in) |
| `/employee` | Redirects to login (if not logged in) |

**After Logging In:**

| URL | Role | Expected Behavior |
|-----|------|-------------------|
| `/hr` | HR | ✅ Shows HR Dashboard |
| `/hr` | Employee | ❌ Redirects to `/employee` |
| `/manager` | Manager | ✅ Shows Manager Dashboard |
| `/manager` | Employee | ❌ Redirects to `/employee` |
| `/employee` | Any | ✅ Shows Employee Dashboard |

---

## 🔍 Debugging Checklist

### Backend Not Starting?

```bash
# Check if port 8000 is already in use
lsof -i :8000

# If something is using it, kill it:
kill -9 <PID>

# Or use different port:
uvicorn main:app --reload --host 0.0.0.0 --port 8001
# Then update frontend .env: VITE_API_BASE_URL=http://localhost:8001
```

### Frontend Not Starting?

```bash
# Check if port 5173 is in use
lsof -i :5173

# Clear npm cache if issues
rm -rf node_modules
npm install

# Try starting again
npm run dev
```

### "Network Error" in Browser?

**Check Backend is Running:**
```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "environment": "development",
    "version": "1.0.0"
  }
}
```

**Check CORS:**
Backend logs should NOT show CORS errors. If they do:
```bash
cd backend
# Edit config.py, ensure CORS_ORIGINS includes:
# "http://localhost:5173"
```

### "401 Unauthorized" on Login?

**Check Database Has Users:**
```bash
cd backend
python3 -c "from database import SessionLocal; from models import User; s = SessionLocal(); print([u.email for u in s.query(User).all()])"
```

Should show email addresses. If empty:
```bash
python3 seed_comprehensive.py
```

### Login Button Does Nothing?

**Check Browser Console:**
- Open DevTools → Console
- Look for error messages
- Common issues:
  - "useAuth must be used within an AuthProvider" → Routing issue
  - "Network Error" → Backend not running
  - CORS errors → Backend CORS misconfigured

### TypeScript Errors?

```bash
cd frontend
# Check for import errors
npm run build

# If errors, check:
ls src/types/auth.ts
ls src/services/authService.ts
ls src/contexts/AuthContext.tsx
ls src/components/ProtectedRoute.tsx
ls src/config/api.ts

# All should exist
```

---

## 📊 Verify Everything Works

### Test Matrix

| Test | Steps | Expected Result | Status |
|------|-------|-----------------|--------|
| **Login - HR** | 1. Go to /login<br>2. Enter HR credentials<br>3. Click Login | Redirects to /hr | [ ] |
| **Login - Manager** | 1. Go to /login<br>2. Enter Manager credentials<br>3. Click Login | Redirects to /manager | [ ] |
| **Login - Employee** | 1. Go to /login<br>2. Enter Employee credentials<br>3. Click Login | Redirects to /employee | [ ] |
| **Wrong Password** | 1. Go to /login<br>2. Enter wrong password<br>3. Click Login | Shows error message | [ ] |
| **Empty Fields** | 1. Go to /login<br>2. Leave fields empty<br>3. Click Login | Shows validation error | [ ] |
| **Protected Route** | 1. Logout<br>2. Try to access /hr directly | Redirects to /login | [ ] |
| **Role-Based Access** | 1. Login as Employee<br>2. Try to access /hr | Redirects to /employee | [ ] |
| **Logout** | 1. Login<br>2. Find logout button<br>3. Click logout | Redirects to /login,<br>localStorage cleared | [ ] |
| **Token Refresh** | 1. Login<br>2. Wait 1 hour<br>3. Make API call | Token refreshes<br>automatically | [ ] |
| **Session Persistence** | 1. Login<br>2. Refresh page | Stays logged in | [ ] |

---

## 🎯 What to Do After Auth Works

### 1. Add Logout Button to Layouts

**Update `frontend/src/layouts/HR.tsx` (and others):**

```typescript
import { useAuth } from '@/contexts/AuthContext';

export default function HRLayout() {
  const { user, logout } = useAuth();
  
  return (
    <div>
      <header>
        <p>Welcome, {user?.name}</p>
        <button onClick={logout}>Logout</button>
      </header>
      {/* Rest of layout */}
    </div>
  );
}
```

### 2. Test API Calls with Auth

**Example - Fetch Dashboard Data:**

```typescript
import api from '@/services/api';

const fetchDashboard = async () => {
  try {
    const response = await api.get('/dashboard/hr');
    console.log(response.data);
  } catch (error) {
    console.error('Error:', error);
  }
};
```

The `api` instance automatically includes the auth token!

### 3. Next APIs to Implement

Priority order:
1. ✅ Auth APIs (COMPLETE!)
2. ⏭️ Dashboard APIs (HR, Manager, Employee)
3. ⏭️ User Profile API
4. ⏭️ Employee Management APIs

---

## 📞 Need Help?

### Check These Files

1. **Backend Running?** → Check Terminal 1 for errors
2. **Frontend Running?** → Check Terminal 2 for errors
3. **CORS Issues?** → Check `backend/config.py` line 35
4. **Database Empty?** → Run `python3 seed_comprehensive.py`
5. **Frontend Errors?** → Check browser console
6. **API Errors?** → Check Network tab in DevTools

### Common Error Solutions

| Error | Solution |
|-------|----------|
| "Module not found" | `cd frontend && npm install` |
| "Database not found" | `cd backend && python3 seed_comprehensive.py` |
| "Port already in use" | Kill process: `lsof -i :8000` then `kill -9 <PID>` |
| "CORS error" | Check backend CORS_ORIGINS includes frontend URL |
| "401 Unauthorized" | Check credentials, check database has users |
| "useAuth must be used within AuthProvider" | Check router.tsx has RootLayout wrapper |

---

## ✅ Success Criteria

You'll know everything works when:

- ✅ Backend starts without errors
- ✅ Frontend starts without errors
- ✅ Can login with any test account
- ✅ Redirects to correct dashboard based on role
- ✅ Protected routes redirect to login when not authenticated
- ✅ Role-based access control works
- ✅ LocalStorage contains tokens after login
- ✅ Logout clears localStorage and redirects to login
- ✅ Page refresh doesn't log you out

---

## 🎉 Congratulations!

If all tests pass, your authentication system is **fully integrated and working!**

**Next Steps:**
1. Implement Dashboard APIs
2. Add logout buttons to layouts
3. Implement user profile page
4. Continue with other API integrations

---

**Happy Coding!** 🚀

*Generated: November 13, 2025*

