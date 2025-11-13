# Dashboard APIs - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

This guide will help you quickly test the new dashboard APIs and see them in action!

---

## Prerequisites

- Python 3.10+ installed
- Node.js 16+ installed
- Git clone of the project

---

## Step 1: Start Backend (2 minutes)

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if not already activated)
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies (if not already done)
pip install -r requirements.txt

# Run database seeding (IMPORTANT - creates test data)
python seed_comprehensive.py

# Start backend server
uvicorn main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
```

**Verify Backend:**
Open browser: http://localhost:8000/api/docs
You should see the Swagger API documentation with dashboard endpoints.

---

## Step 2: Start Frontend (1 minute)

Open a **new terminal** (keep backend running):

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already done)
npm install

# Start frontend development server
npm run dev
```

**Expected Output:**
```
VITE v7.1.12  ready in 462 ms

➜  Local:   http://localhost:5174/
➜  Network: use --host to expose
```

**Verify Frontend:**
Open browser: http://localhost:5174
You should see the login page.

---

## Step 3: Test Dashboards (2 minutes)

### Test HR Dashboard

1. **Login as HR:**
   - Email: `sarah.johnson@company.com`
   - Password: `password123`

2. **View Dashboard:**
   - You should be redirected to HR Dashboard
   - Verify you see:
     - ✅ Department-wise Attendance chart
     - ✅ Department-wise Leaderboard chart
     - ✅ Department Employee Count table
     - ✅ Active Applications list

3. **Expected Data:**
   - Multiple departments with employee counts
   - Attendance percentages (present/absent)
   - Module completion counts
   - Recent job applications

---

### Test Manager Dashboard

1. **Logout** and **Login as Manager:**
   - Email: `robert.chen@company.com`
   - Password: `password123`

2. **View Dashboard:**
   - You should be redirected to Manager Dashboard
   - Verify you see:
     - ✅ WFH Left, Leaves Left, Learner Rank cards
     - ✅ Punch In/Out times
     - ✅ Upcoming Holidays list
     - ✅ Team Goals pie chart
     - ✅ Learner Leaderboard chart
     - ✅ Team Training Hours and Performance Score

3. **Expected Data:**
   - Personal leave balances
   - Today's attendance (if seeded)
   - Upcoming holidays
   - Team statistics and goals

---

### Test Employee Dashboard

1. **Logout** and **Login as Employee:**
   - Email: `john.doe@company.com`
   - Password: `password123`

2. **View Dashboard:**
   - You should be redirected to Employee Dashboard
   - Verify you see:
     - ✅ Welcome message with employee name
     - ✅ Learner Rank, WFH Left, Leaves Left cards
     - ✅ Learning Goals doughnut chart
     - ✅ Punch In/Out times
     - ✅ Upcoming Holidays list

3. **Expected Data:**
   - Employee name: "John Doe"
   - Leave balances from database
   - Learning goals completion percentage
   - Upcoming holidays

---

## 🧪 API Testing with cURL

### Test HR Dashboard API

```bash
# Step 1: Login and get token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "sarah.johnson@company.com",
    "password": "password123"
  }'

# Copy the access_token from response

# Step 2: Get HR Dashboard
curl -X GET http://localhost:8000/api/v1/dashboard/hr \
  -H "Authorization: Bearer <paste_access_token_here>"
```

### Test Manager Dashboard API

```bash
# Step 1: Login as Manager
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "robert.chen@company.com",
    "password": "password123"
  }'

# Step 2: Get Manager Dashboard
curl -X GET http://localhost:8000/api/v1/dashboard/manager \
  -H "Authorization: Bearer <paste_access_token_here>"
```

### Test Employee Dashboard API

```bash
# Step 1: Login as Employee
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@company.com",
    "password": "password123"
  }'

# Step 2: Get Employee Dashboard
curl -X GET http://localhost:8000/api/v1/dashboard/employee \
  -H "Authorization: Bearer <paste_access_token_here>"
```

---

## 🔍 Verify API Endpoints in Swagger

1. Open: http://localhost:8000/api/docs
2. Click on **"Dashboard"** section
3. You should see these endpoints:
   - `GET /api/v1/dashboard/hr`
   - `GET /api/v1/dashboard/manager`
   - `GET /api/v1/dashboard/employee`
   - `GET /api/v1/dashboard/me`
   - `GET /api/v1/dashboard/performance/{employee_id}`
   - `GET /api/v1/dashboard/performance/me`

4. Click **"Authorize"** button at top
5. Enter access token from login
6. Try out the endpoints directly from Swagger UI!

---

## 📊 Data Verification Checklist

### HR Dashboard Data Points
- [ ] Department names displayed correctly
- [ ] Employee counts per department are non-zero
- [ ] Attendance percentages add up (present + absent)
- [ ] Leaderboard shows module completion counts
- [ ] Active applications list shows applicant names and roles

### Manager Dashboard Data Points
- [ ] Leave balances are reasonable numbers (0-24)
- [ ] Punch in/out times display or show "N/A"
- [ ] Holidays are future dates
- [ ] Team goals show completed vs pending
- [ ] Leaderboard shows team member names
- [ ] Training hours and performance score are displayed

### Employee Dashboard Data Points
- [ ] Employee name matches logged-in user
- [ ] Leave balances display correctly
- [ ] Learning goals percentage calculates correctly
- [ ] Learner rank shows a number or "N/A"
- [ ] Holidays list is populated

---

## 🐛 Troubleshooting

### Backend Won't Start
**Error:** `ModuleNotFoundError`
**Fix:** 
```bash
pip install -r requirements.txt
```

**Error:** `Database is locked`
**Fix:** 
```bash
# Stop backend, delete database, reseed
rm hr_system.db
python seed_comprehensive.py
uvicorn main:app --reload --port 8000
```

---

### Frontend Shows Error

**Error:** "Failed to load dashboard data"
**Cause:** Backend not running or wrong URL
**Fix:** 
1. Check backend is running on port 8000
2. Verify `.env` file in frontend has correct API URL:
   ```
   VITE_API_URL=http://localhost:8000/api/v1
   ```

---

**Error:** "403 Forbidden"
**Cause:** Wrong user role accessing wrong dashboard
**Fix:** 
- HR users → `/hr` routes
- Manager users → `/manager` routes  
- Employee users → `/employee` routes

---

### Empty Data on Dashboard

**Cause:** Database not seeded
**Fix:**
```bash
cd backend
python seed_comprehensive.py
```

This creates:
- 3 Departments
- 1 Team
- 10+ Users (HR, Managers, Employees)
- Attendance records
- Goals
- Skill modules
- Job applications
- Holidays

---

## 📝 Test Accounts Summary

| Role | Email | Password | Dashboard URL |
|------|-------|----------|---------------|
| HR | `sarah.johnson@company.com` | `password123` | `/hr` |
| Manager | `robert.chen@company.com` | `password123` | `/manager` |
| Employee | `john.doe@company.com` | `password123` | `/employee` |

---

## ✅ Success Criteria

You've successfully set up the dashboard APIs if:

1. ✅ Backend starts without errors
2. ✅ Frontend loads login page
3. ✅ Can login with test accounts
4. ✅ Each role sees their respective dashboard
5. ✅ Dashboard displays real data (not hardcoded)
6. ✅ Charts and tables render correctly
7. ✅ No console errors in browser
8. ✅ API calls visible in Network tab

---

## 🎉 Next Steps

Once everything is working:

1. **Explore Other Pages:**
   - Attendance page
   - Profile page
   - Job Listings
   - Applications (HR)
   - Team Management (Manager)

2. **Add More Test Data:**
   - Modify `seed_comprehensive.py`
   - Add more departments, users, goals
   - Create attendance records for different dates

3. **Customize:**
   - Adjust date ranges for statistics
   - Modify chart colors and styles
   - Add new dashboard widgets

4. **Production Deployment:**
   - Update `.env` with production API URL
   - Build frontend: `npm run build`
   - Deploy backend with proper database
   - Configure HTTPS and CORS

---

## 📚 More Information

- **Complete API Docs:** `docs/20_DASHBOARD_API_DOCUMENTATION.md`
- **Implementation Details:** `docs/21_DASHBOARD_IMPLEMENTATION_SUMMARY.md`
- **Backend Setup:** `docs/04_BACKEND_README.md`
- **Frontend Setup:** `docs/07_FRONTEND_README.md`

---

**Questions or Issues?**
Check the troubleshooting section or refer to the comprehensive documentation!

**Happy Testing! 🚀**

---

*Last Updated: November 13, 2025*


