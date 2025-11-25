# Comprehensive API Testing Results - ALL 171+ Endpoints

**Generated**: 2025-11-26 00:52:11  
**Duration**: 304.50s  
**Backend**: http://localhost:8000

## 📊 Executive Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| **Total Tests** | 146 | 100% |
| ✅ **Passed** | 89 | 61.0% |
| ❌ **Failed** | 57 | 39.0% |
| ⚠️ **Errors** | 0 | 0.0% |
| **Success Rate** | - | **61.0%** |

## 📈 Coverage Analysis

- **Target Coverage**: 171+ API endpoints
- **Endpoints Tested**: 146
- **Coverage Achieved**: ~85.4%

## 📋 Detailed Results by Module

### Test 1: HR Login

- **Status**: ✅ PASSED
- **Endpoint**: `POST /auth/login`
- **Role**: None
- **Time**: 2324ms
- **Response**: HTTP 200 (expected 200)

### Test 2: MANAGER Login

- **Status**: ✅ PASSED
- **Endpoint**: `POST /auth/login`
- **Role**: None
- **Time**: 2255ms
- **Response**: HTTP 200 (expected 200)

### Test 3: EMPLOYEE Login

- **Status**: ✅ PASSED
- **Endpoint**: `POST /auth/login`
- **Role**: None
- **Time**: 2265ms
- **Response**: HTTP 200 (expected 200)

### Test 4: Get Current User

- **Status**: ✅ PASSED
- **Endpoint**: `GET /auth/me`
- **Role**: employee
- **Time**: 2038ms
- **Response**: HTTP 200 (expected 200)

### Test 5: Refresh Token

- **Status**: ❌ FAILED
- **Endpoint**: `POST /auth/refresh-token`
- **Role**: employee
- **Time**: 2072ms
- **Response**: HTTP 404 (expected 401)
- **Error**: Expected 401, got 404

### Test 6: Change Password

- **Status**: ✅ PASSED
- **Endpoint**: `POST /auth/change-password`
- **Role**: employee
- **Time**: 2441ms
- **Response**: HTTP 200 (expected 200)

### Test 7: Reset Password Request

- **Status**: ❌ FAILED
- **Endpoint**: `POST /auth/reset-password`
- **Role**: None
- **Time**: 2044ms
- **Response**: HTTP 403 (expected 200)
- **Error**: Expected 200, got 403

### Test 8: Logout

- **Status**: ✅ PASSED
- **Endpoint**: `POST /auth/logout`
- **Role**: employee
- **Time**: 2046ms
- **Response**: HTTP 200 (expected 200)

### Test 9: HR Login

- **Status**: ✅ PASSED
- **Endpoint**: `POST /auth/login`
- **Role**: None
- **Time**: 2247ms
- **Response**: HTTP 200 (expected 200)

### Test 10: MANAGER Login

- **Status**: ✅ PASSED
- **Endpoint**: `POST /auth/login`
- **Role**: None
- **Time**: 2262ms
- **Response**: HTTP 200 (expected 200)

### Test 11: EMPLOYEE Login

- **Status**: ❌ FAILED
- **Endpoint**: `POST /auth/login`
- **Role**: None
- **Time**: 2267ms
- **Response**: HTTP 401 (expected 200)
- **Error**: Expected 200, got 401

### Test 12: Employee Dashboard

- **Status**: ✅ PASSED
- **Endpoint**: `GET /dashboard/employee`
- **Role**: employee
- **Time**: 2090ms
- **Response**: HTTP 200 (expected 200)

### Test 13: Manager Dashboard

- **Status**: ✅ PASSED
- **Endpoint**: `GET /dashboard/manager`
- **Role**: manager
- **Time**: 2098ms
- **Response**: HTTP 200 (expected 200)

### Test 14: HR Dashboard

- **Status**: ✅ PASSED
- **Endpoint**: `GET /dashboard/hr`
- **Role**: hr
- **Time**: 2088ms
- **Response**: HTTP 200 (expected 200)

### Test 15: My Dashboard (Auto-detect)

- **Status**: ✅ PASSED
- **Endpoint**: `GET /dashboard/me`
- **Role**: employee
- **Time**: 2091ms
- **Response**: HTTP 200 (expected 200)

### Test 16: Employee Performance

- **Status**: ✅ PASSED
- **Endpoint**: `GET /dashboard/performance/3`
- **Role**: manager
- **Time**: 2052ms
- **Response**: HTTP 200 (expected 200)

### Test 17: My Performance

- **Status**: ❌ FAILED
- **Endpoint**: `GET /dashboard/performance/me`
- **Role**: employee
- **Time**: 2068ms
- **Response**: HTTP 422 (expected 200)
- **Error**: Expected 200, got 422 - 

### Test 18: Create Employee

- **Status**: ❌ FAILED
- **Endpoint**: `POST /employees`
- **Role**: hr
- **Time**: 2274ms
- **Response**: HTTP 500 (expected 201)
- **Error**: Expected 201, got 500 - Failed to create employee: 1 validation error for EmployeeResponse
emergency_contact
  Field required [type=missing, input_value={'id': 6, 'employee_id': ...: 15, 'wfh_balance': 24}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.11/v/missing

### Test 19: Get All Employees

- **Status**: ✅ PASSED
- **Endpoint**: `GET /employees`
- **Role**: hr
- **Time**: 2096ms
- **Response**: HTTP 200 (expected 200)

### Test 20: Get Employee Stats

- **Status**: ✅ PASSED
- **Endpoint**: `GET /employees/stats`
- **Role**: hr
- **Time**: 2078ms
- **Response**: HTTP 200 (expected 200)

### Test 21: Create Department

- **Status**: ✅ PASSED
- **Endpoint**: `POST /departments`
- **Role**: hr
- **Time**: 2096ms
- **Response**: HTTP 201 (expected 201)

### Test 22: Get All Departments

- **Status**: ✅ PASSED
- **Endpoint**: `GET /departments`
- **Role**: employee
- **Time**: 2086ms
- **Response**: HTTP 200 (expected 200)

### Test 23: Get Department Stats

- **Status**: ✅ PASSED
- **Endpoint**: `GET /departments/stats`
- **Role**: hr
- **Time**: 2067ms
- **Response**: HTTP 200 (expected 200)

### Test 24: Get Department Details

- **Status**: ✅ PASSED
- **Endpoint**: `GET /departments/3`
- **Role**: employee
- **Time**: 2063ms
- **Response**: HTTP 200 (expected 200)

### Test 25: Update Department

- **Status**: ✅ PASSED
- **Endpoint**: `PUT /departments/3`
- **Role**: hr
- **Time**: 2053ms
- **Response**: HTTP 200 (expected 200)

### Test 26: Delete Department

- **Status**: ✅ PASSED
- **Endpoint**: `DELETE /departments/3`
- **Role**: hr
- **Time**: 2086ms
- **Response**: HTTP 200 (expected 200)

### Test 27: Create Team

- **Status**: ❌ FAILED
- **Endpoint**: `POST /teams`
- **Role**: hr
- **Time**: 2063ms
- **Response**: HTTP 404 (expected 201)
- **Error**: Expected 201, got 404

### Test 28: Get All Teams

- **Status**: ❌ FAILED
- **Endpoint**: `GET /teams`
- **Role**: employee
- **Time**: 2046ms
- **Response**: HTTP 404 (expected 200)
- **Error**: Expected 200, got 404

### Test 29: Get Team Stats

- **Status**: ❌ FAILED
- **Endpoint**: `GET /teams/stats`
- **Role**: hr
- **Time**: 2069ms
- **Response**: HTTP 404 (expected 200)
- **Error**: Expected 200, got 404

### Test 30: Punch In

- **Status**: ✅ PASSED
- **Endpoint**: `POST /attendance/punch-in`
- **Role**: employee
- **Time**: 2074ms
- **Response**: HTTP 200 (expected 200)

### Test 31: Get Today's Attendance

- **Status**: ✅ PASSED
- **Endpoint**: `GET /attendance/today`
- **Role**: employee
- **Time**: 2086ms
- **Response**: HTTP 200 (expected 200)

### Test 32: Punch Out

- **Status**: ❌ FAILED
- **Endpoint**: `POST /attendance/punch-out`
- **Role**: employee
- **Time**: 2075ms
- **Response**: HTTP 400 (expected 200)
- **Error**: Expected 200, got 400 - Already punched out for today

### Test 33: Get My Attendance

- **Status**: ✅ PASSED
- **Endpoint**: `GET /attendance/me`
- **Role**: employee
- **Time**: 2052ms
- **Response**: HTTP 200 (expected 200)

### Test 34: Get My Summary

- **Status**: ✅ PASSED
- **Endpoint**: `GET /attendance/me/summary`
- **Role**: employee
- **Time**: 2063ms
- **Response**: HTTP 200 (expected 200)

### Test 35: Get Team Attendance

- **Status**: ❌ FAILED
- **Endpoint**: `GET /attendance/team`
- **Role**: manager
- **Time**: 2085ms
- **Response**: HTTP 500 (expected 200)
- **Error**: Expected 200, got 500 - 

### Test 36: Get All Attendance

- **Status**: ✅ PASSED
- **Endpoint**: `GET /attendance/all`
- **Role**: hr
- **Time**: 2096ms
- **Response**: HTTP 200 (expected 200)

### Test 37: Mark Attendance (HR)

- **Status**: ❌ FAILED
- **Endpoint**: `POST /attendance/mark`
- **Role**: hr
- **Time**: 2043ms
- **Response**: HTTP 422 (expected 200)
- **Error**: Expected 200, got 422 - 

### Test 38: Create Job

- **Status**: ✅ PASSED
- **Endpoint**: `POST /jobs`
- **Role**: hr
- **Time**: 2090ms
- **Response**: HTTP 201 (expected 201)

### Test 39: Get All Jobs

- **Status**: ✅ PASSED
- **Endpoint**: `GET /jobs`
- **Role**: employee
- **Time**: 2075ms
- **Response**: HTTP 200 (expected 200)

### Test 40: Get Job Statistics

- **Status**: ✅ PASSED
- **Endpoint**: `GET /jobs/statistics`
- **Role**: hr
- **Time**: 2108ms
- **Response**: HTTP 200 (expected 200)

### Test 41: Get Job Details

- **Status**: ✅ PASSED
- **Endpoint**: `GET /jobs/1`
- **Role**: employee
- **Time**: 2378ms
- **Response**: HTTP 200 (expected 200)

### Test 42: Update Job

- **Status**: ✅ PASSED
- **Endpoint**: `PUT /jobs/1`
- **Role**: hr
- **Time**: 2081ms
- **Response**: HTTP 200 (expected 200)

### Test 43: Get Job Applications

- **Status**: ✅ PASSED
- **Endpoint**: `GET /jobs/1/applications`
- **Role**: hr
- **Time**: 2067ms
- **Response**: HTTP 200 (expected 200)

### Test 44: Delete Job

- **Status**: ✅ PASSED
- **Endpoint**: `DELETE /jobs/1`
- **Role**: hr
- **Time**: 2076ms
- **Response**: HTTP 200 (expected 200)

### Test 45: Submit Application

- **Status**: ❌ FAILED
- **Endpoint**: `POST /applications/apply`
- **Role**: None
- **Time**: 2053ms
- **Response**: HTTP 405 (expected 201)
- **Error**: Expected 201, got 405

### Test 46: Get All Applications

- **Status**: ✅ PASSED
- **Endpoint**: `GET /applications`
- **Role**: hr
- **Time**: 2076ms
- **Response**: HTTP 200 (expected 200)

### Test 47: Get Application Stats

- **Status**: ❌ FAILED
- **Endpoint**: `GET /applications/stats`
- **Role**: hr
- **Time**: 2067ms
- **Response**: HTTP 422 (expected 200)
- **Error**: Expected 200, got 422 - 

### Test 48: Get Recent Applications

- **Status**: ❌ FAILED
- **Endpoint**: `GET /applications/recent`
- **Role**: hr
- **Time**: 2061ms
- **Response**: HTTP 422 (expected 200)
- **Error**: Expected 200, got 422 - 

### Test 49: Create Leave Request

- **Status**: ✅ PASSED
- **Endpoint**: `POST /leaves`
- **Role**: employee
- **Time**: 2093ms
- **Response**: HTTP 201 (expected 201)

### Test 50: Get My Leaves

- **Status**: ✅ PASSED
- **Endpoint**: `GET /leaves/me`
- **Role**: employee
- **Time**: 2095ms
- **Response**: HTTP 200 (expected 200)

### Test 51: Get Leave Balance

- **Status**: ✅ PASSED
- **Endpoint**: `GET /leaves/balance/me`
- **Role**: employee
- **Time**: 2070ms
- **Response**: HTTP 200 (expected 200)

### Test 52: Get Team Leaves

- **Status**: ✅ PASSED
- **Endpoint**: `GET /leaves/team`
- **Role**: manager
- **Time**: 2071ms
- **Response**: HTTP 200 (expected 200)

### Test 53: Get All Leaves (HR)

- **Status**: ✅ PASSED
- **Endpoint**: `GET /leaves/all`
- **Role**: hr
- **Time**: 2059ms
- **Response**: HTTP 200 (expected 200)

### Test 54: Get Leave Stats

- **Status**: ❌ FAILED
- **Endpoint**: `GET /leaves/stats`
- **Role**: hr
- **Time**: 2056ms
- **Response**: HTTP 422 (expected 200)
- **Error**: Expected 200, got 422 - 

### Test 55: Get Leave Details

- **Status**: ✅ PASSED
- **Endpoint**: `GET /leaves/2`
- **Role**: employee
- **Time**: 2065ms
- **Response**: HTTP 200 (expected 200)

### Test 56: Update Leave Status

- **Status**: ❌ FAILED
- **Endpoint**: `PUT /leaves/2/status`
- **Role**: manager
- **Time**: 2041ms
- **Response**: HTTP 405 (expected 200)
- **Error**: Expected 200, got 405

### Test 57: Cancel Leave

- **Status**: ✅ PASSED
- **Endpoint**: `DELETE /leaves/2`
- **Role**: employee
- **Time**: 2088ms
- **Response**: HTTP 200 (expected 200)

### Test 58: Create Holiday

- **Status**: ✅ PASSED
- **Endpoint**: `POST /holidays`
- **Role**: hr
- **Time**: 2087ms
- **Response**: HTTP 201 (expected 201)

### Test 59: Get All Holidays

- **Status**: ✅ PASSED
- **Endpoint**: `GET /holidays`
- **Role**: employee
- **Time**: 2084ms
- **Response**: HTTP 200 (expected 200)

### Test 60: Get Upcoming Holidays

- **Status**: ✅ PASSED
- **Endpoint**: `GET /holidays/upcoming`
- **Role**: employee
- **Time**: 2076ms
- **Response**: HTTP 200 (expected 200)

### Test 61: Get Holiday Stats

- **Status**: ✅ PASSED
- **Endpoint**: `GET /holidays/stats`
- **Role**: hr
- **Time**: 2080ms
- **Response**: HTTP 200 (expected 200)

### Test 62: Get Holiday Details

- **Status**: ✅ PASSED
- **Endpoint**: `GET /holidays/1`
- **Role**: employee
- **Time**: 2054ms
- **Response**: HTTP 200 (expected 200)

### Test 63: Update Holiday

- **Status**: ✅ PASSED
- **Endpoint**: `PUT /holidays/1`
- **Role**: hr
- **Time**: 2084ms
- **Response**: HTTP 200 (expected 200)

### Test 64: Delete Holiday

- **Status**: ✅ PASSED
- **Endpoint**: `DELETE /holidays/1`
- **Role**: hr
- **Time**: 2071ms
- **Response**: HTTP 200 (expected 200)

### Test 65: Create Announcement

- **Status**: ✅ PASSED
- **Endpoint**: `POST /announcements`
- **Role**: hr
- **Time**: 2096ms
- **Response**: HTTP 201 (expected 201)

### Test 66: Get All Announcements

- **Status**: ✅ PASSED
- **Endpoint**: `GET /announcements`
- **Role**: employee
- **Time**: 2086ms
- **Response**: HTTP 200 (expected 200)

### Test 67: Get Announcement Stats

- **Status**: ✅ PASSED
- **Endpoint**: `GET /announcements/stats/summary`
- **Role**: hr
- **Time**: 2093ms
- **Response**: HTTP 200 (expected 200)

### Test 68: Get Announcement Details

- **Status**: ✅ PASSED
- **Endpoint**: `GET /announcements/1`
- **Role**: employee
- **Time**: 2051ms
- **Response**: HTTP 200 (expected 200)

### Test 69: Update Announcement

- **Status**: ✅ PASSED
- **Endpoint**: `PUT /announcements/1`
- **Role**: hr
- **Time**: 2076ms
- **Response**: HTTP 200 (expected 200)

### Test 70: Delete Announcement

- **Status**: ✅ PASSED
- **Endpoint**: `DELETE /announcements/1`
- **Role**: hr
- **Time**: 2087ms
- **Response**: HTTP 200 (expected 200)

### Test 71: Create Policy

- **Status**: ✅ PASSED
- **Endpoint**: `POST /policies`
- **Role**: hr
- **Time**: 2079ms
- **Response**: HTTP 201 (expected 201)

### Test 72: Get All Policies

- **Status**: ✅ PASSED
- **Endpoint**: `GET /policies`
- **Role**: employee
- **Time**: 2097ms
- **Response**: HTTP 200 (expected 200)

### Test 73: Get Policy Stats

- **Status**: ❌ FAILED
- **Endpoint**: `GET /policies/stats`
- **Role**: hr
- **Time**: 2049ms
- **Response**: HTTP 422 (expected 200)
- **Error**: Expected 200, got 422 - 

### Test 74: Search Policies

- **Status**: ❌ FAILED
- **Endpoint**: `POST /policies/search`
- **Role**: employee
- **Time**: 2062ms
- **Response**: HTTP 405 (expected 200)
- **Error**: Expected 200, got 405

### Test 75: Get Policy Details

- **Status**: ✅ PASSED
- **Endpoint**: `GET /policies/1`
- **Role**: employee
- **Time**: 2076ms
- **Response**: HTTP 200 (expected 200)

### Test 76: Update Policy

- **Status**: ✅ PASSED
- **Endpoint**: `PUT /policies/1`
- **Role**: hr
- **Time**: 2070ms
- **Response**: HTTP 200 (expected 200)

### Test 77: Get Policy History

- **Status**: ❌ FAILED
- **Endpoint**: `GET /policies/1/history`
- **Role**: employee
- **Time**: 2054ms
- **Response**: HTTP 404 (expected 200)
- **Error**: Expected 200, got 404

### Test 78: Acknowledge Policy

- **Status**: ❌ FAILED
- **Endpoint**: `POST /policies/1/acknowledge`
- **Role**: employee
- **Time**: 2080ms
- **Response**: HTTP 201 (expected 200)
- **Error**: Expected 200, got 201

### Test 79: Get My Acknowledgements

- **Status**: ❌ FAILED
- **Endpoint**: `GET /policies/my-acknowledgements`
- **Role**: employee
- **Time**: 2052ms
- **Response**: HTTP 422 (expected 200)
- **Error**: Expected 200, got 422 - 

### Test 80: Delete Policy

- **Status**: ✅ PASSED
- **Endpoint**: `DELETE /policies/1`
- **Role**: hr
- **Time**: 2083ms
- **Response**: HTTP 200 (expected 200)

### Test 81: Generate Payslip

- **Status**: ✅ PASSED
- **Endpoint**: `POST /payslips`
- **Role**: hr
- **Time**: 2088ms
- **Response**: HTTP 201 (expected 201)

### Test 82: Get My Payslips

- **Status**: ✅ PASSED
- **Endpoint**: `GET /payslips/me`
- **Role**: employee
- **Time**: 2087ms
- **Response**: HTTP 200 (expected 200)

### Test 83: Get My Latest Payslip

- **Status**: ❌ FAILED
- **Endpoint**: `GET /payslips/me/latest`
- **Role**: employee
- **Time**: 2054ms
- **Response**: HTTP 404 (expected 200)
- **Error**: Expected 200, got 404

### Test 84: Get All Payslips (HR)

- **Status**: ✅ PASSED
- **Endpoint**: `GET /payslips`
- **Role**: hr
- **Time**: 2089ms
- **Response**: HTTP 200 (expected 200)

### Test 85: Get Payslip Stats

- **Status**: ❌ FAILED
- **Endpoint**: `GET /payslips/stats`
- **Role**: hr
- **Time**: 2064ms
- **Response**: HTTP 422 (expected 200)
- **Error**: Expected 200, got 422 - 

### Test 86: Get Payslip Details

- **Status**: ✅ PASSED
- **Endpoint**: `GET /payslips/1`
- **Role**: employee
- **Time**: 2072ms
- **Response**: HTTP 200 (expected 200)

### Test 87: Update Payslip

- **Status**: ✅ PASSED
- **Endpoint**: `PUT /payslips/1`
- **Role**: hr
- **Time**: 2071ms
- **Response**: HTTP 200 (expected 200)

### Test 88: Get Employee Payslips

- **Status**: ✅ PASSED
- **Endpoint**: `GET /payslips/employee/3`
- **Role**: hr
- **Time**: 2075ms
- **Response**: HTTP 200 (expected 200)

### Test 89: Download Payslip PDF

- **Status**: ❌ FAILED
- **Endpoint**: `GET /payslips/1/download`
- **Role**: employee
- **Time**: 2044ms
- **Response**: HTTP 404 (expected 200)
- **Error**: Expected 200, got 404

### Test 90: Email Payslip

- **Status**: ❌ FAILED
- **Endpoint**: `POST /payslips/1/email`
- **Role**: hr
- **Time**: 2044ms
- **Response**: HTTP 404 (expected 200)
- **Error**: Expected 200, got 404

### Test 91: Delete Payslip

- **Status**: ✅ PASSED
- **Endpoint**: `DELETE /payslips/1`
- **Role**: hr
- **Time**: 2046ms
- **Response**: HTTP 200 (expected 200)

### Test 92: Give Feedback

- **Status**: ✅ PASSED
- **Endpoint**: `POST /feedback`
- **Role**: manager
- **Time**: 2067ms
- **Response**: HTTP 201 (expected 201)

### Test 93: Get My Feedback

- **Status**: ✅ PASSED
- **Endpoint**: `GET /feedback/me`
- **Role**: employee
- **Time**: 2052ms
- **Response**: HTTP 200 (expected 200)

### Test 94: Get Team Feedback

- **Status**: ❌ FAILED
- **Endpoint**: `GET /feedback/team`
- **Role**: manager
- **Time**: 2067ms
- **Response**: HTTP 422 (expected 200)
- **Error**: Expected 200, got 422 - 

### Test 95: Get All Feedback (HR)

- **Status**: ❌ FAILED
- **Endpoint**: `GET /feedback`
- **Role**: hr
- **Time**: 2052ms
- **Response**: HTTP 403 (expected 200)
- **Error**: Expected 200, got 403

### Test 96: Get Feedback Stats

- **Status**: ❌ FAILED
- **Endpoint**: `GET /feedback/stats`
- **Role**: hr
- **Time**: 2071ms
- **Response**: HTTP 422 (expected 200)
- **Error**: Expected 200, got 422 - 

### Test 97: Get Feedback Details

- **Status**: ✅ PASSED
- **Endpoint**: `GET /feedback/1`
- **Role**: employee
- **Time**: 2052ms
- **Response**: HTTP 200 (expected 200)

### Test 98: Update Feedback

- **Status**: ✅ PASSED
- **Endpoint**: `PUT /feedback/1`
- **Role**: manager
- **Time**: 2070ms
- **Response**: HTTP 200 (expected 200)

### Test 99: Get Employee Feedback

- **Status**: ✅ PASSED
- **Endpoint**: `GET /feedback/employee/3`
- **Role**: manager
- **Time**: 2067ms
- **Response**: HTTP 200 (expected 200)

### Test 100: Delete Feedback

- **Status**: ❌ FAILED
- **Endpoint**: `DELETE /feedback/1`
- **Role**: hr
- **Time**: 2082ms
- **Response**: HTTP 403 (expected 200)
- **Error**: Expected 200, got 403

### Test 101: Create Skill Module

- **Status**: ✅ PASSED
- **Endpoint**: `POST /skills/modules`
- **Role**: hr
- **Time**: 2106ms
- **Response**: HTTP 201 (expected 201)

### Test 102: Get All Modules

- **Status**: ✅ PASSED
- **Endpoint**: `GET /skills/modules`
- **Role**: employee
- **Time**: 2051ms
- **Response**: HTTP 200 (expected 200)

### Test 103: Get My Enrollments

- **Status**: ✅ PASSED
- **Endpoint**: `GET /skills/my-enrollments`
- **Role**: employee
- **Time**: 2051ms
- **Response**: HTTP 200 (expected 200)

### Test 104: Get Skill Stats

- **Status**: ✅ PASSED
- **Endpoint**: `GET /skills/stats`
- **Role**: hr
- **Time**: 2073ms
- **Response**: HTTP 200 (expected 200)

### Test 105: Get Module Details

- **Status**: ✅ PASSED
- **Endpoint**: `GET /skills/modules/1`
- **Role**: employee
- **Time**: 2066ms
- **Response**: HTTP 200 (expected 200)

### Test 106: Enroll in Module

- **Status**: ❌ FAILED
- **Endpoint**: `POST /skills/modules/1/enroll`
- **Role**: employee
- **Time**: 2045ms
- **Response**: HTTP 404 (expected 201)
- **Error**: Expected 201, got 404

### Test 107: Update Progress

- **Status**: ❌ FAILED
- **Endpoint**: `PUT /skills/my-enrollments/progress`
- **Role**: employee
- **Time**: 2067ms
- **Response**: HTTP 404 (expected 200)
- **Error**: Expected 200, got 404

### Test 108: Get Module Enrollments (HR)

- **Status**: ✅ PASSED
- **Endpoint**: `GET /skills/enrollments`
- **Role**: hr
- **Time**: 2052ms
- **Response**: HTTP 200 (expected 200)

### Test 109: Update Module

- **Status**: ✅ PASSED
- **Endpoint**: `PUT /skills/modules/1`
- **Role**: hr
- **Time**: 2077ms
- **Response**: HTTP 200 (expected 200)

### Test 110: Delete Module

- **Status**: ✅ PASSED
- **Endpoint**: `DELETE /skills/modules/1`
- **Role**: hr
- **Time**: 2074ms
- **Response**: HTTP 200 (expected 200)

### Test 111: Create Goal

- **Status**: ✅ PASSED
- **Endpoint**: `POST /goals`
- **Role**: manager
- **Time**: 2105ms
- **Response**: HTTP 201 (expected 201)

### Test 112: Get My Goals

- **Status**: ✅ PASSED
- **Endpoint**: `GET /goals/me`
- **Role**: employee
- **Time**: 2071ms
- **Response**: HTTP 200 (expected 200)

### Test 113: Get Team Goals

- **Status**: ✅ PASSED
- **Endpoint**: `GET /goals/team`
- **Role**: manager
- **Time**: 2069ms
- **Response**: HTTP 200 (expected 200)

### Test 114: Get All Goals (HR)

- **Status**: ❌ FAILED
- **Endpoint**: `GET /goals`
- **Role**: hr
- **Time**: 2052ms
- **Response**: HTTP 405 (expected 200)
- **Error**: Expected 200, got 405

### Test 115: Get Goal Stats

- **Status**: ❌ FAILED
- **Endpoint**: `GET /goals/stats`
- **Role**: hr
- **Time**: 2050ms
- **Response**: HTTP 422 (expected 200)
- **Error**: Expected 200, got 422 - 

### Test 116: Get Goal Details

- **Status**: ✅ PASSED
- **Endpoint**: `GET /goals/1`
- **Role**: employee
- **Time**: 2055ms
- **Response**: HTTP 200 (expected 200)

### Test 117: Update Goal

- **Status**: ✅ PASSED
- **Endpoint**: `PUT /goals/1`
- **Role**: manager
- **Time**: 2096ms
- **Response**: HTTP 200 (expected 200)

### Test 118: Update Goal Status

- **Status**: ❌ FAILED
- **Endpoint**: `PUT /goals/1/status`
- **Role**: manager
- **Time**: 2038ms
- **Response**: HTTP 405 (expected 200)
- **Error**: Expected 200, got 405

### Test 119: Add Checkpoint

- **Status**: ✅ PASSED
- **Endpoint**: `POST /goals/1/checkpoints`
- **Role**: manager
- **Time**: 2084ms
- **Response**: HTTP 201 (expected 201)

### Test 120: Get Goal Checkpoints

- **Status**: ❌ FAILED
- **Endpoint**: `GET /goals/1/checkpoints`
- **Role**: employee
- **Time**: 2066ms
- **Response**: HTTP 405 (expected 200)
- **Error**: Expected 200, got 405

### Test 121: Get Employee Goals

- **Status**: ❌ FAILED
- **Endpoint**: `GET /goals/employee/3`
- **Role**: manager
- **Time**: 2052ms
- **Response**: HTTP 404 (expected 200)
- **Error**: Expected 200, got 404

### Test 122: Delete Goal

- **Status**: ✅ PASSED
- **Endpoint**: `DELETE /goals/1`
- **Role**: manager
- **Time**: 2083ms
- **Response**: HTTP 200 (expected 200)

### Test 123: Create Request

- **Status**: ❌ FAILED
- **Endpoint**: `POST /requests`
- **Role**: employee
- **Time**: 2065ms
- **Response**: HTTP 500 (expected 201)
- **Error**: Expected 201, got 500 - 

### Test 124: Get My Requests

- **Status**: ❌ FAILED
- **Endpoint**: `GET /requests/me`
- **Role**: employee
- **Time**: 2073ms
- **Response**: HTTP 500 (expected 200)
- **Error**: Expected 200, got 500 - 

### Test 125: Get Team Requests

- **Status**: ❌ FAILED
- **Endpoint**: `GET /requests/team`
- **Role**: manager
- **Time**: 2058ms
- **Response**: HTTP 500 (expected 200)
- **Error**: Expected 200, got 500 - 

### Test 126: Get All Requests (HR)

- **Status**: ❌ FAILED
- **Endpoint**: `GET /requests`
- **Role**: hr
- **Time**: 2065ms
- **Response**: HTTP 405 (expected 200)
- **Error**: Expected 200, got 405

### Test 127: Get Request Stats

- **Status**: ❌ FAILED
- **Endpoint**: `GET /requests/stats`
- **Role**: hr
- **Time**: 2069ms
- **Response**: HTTP 500 (expected 200)
- **Error**: Expected 200, got 500 - 

### Test 128: Get Full Org Hierarchy

- **Status**: ❌ FAILED
- **Endpoint**: `GET /organization/hierarchy`
- **Role**: employee
- **Time**: 2091ms
- **Response**: HTTP 500 (expected 200)
- **Error**: Expected 200, got 500 - 

### Test 129: Get Dept Hierarchy

- **Status**: ❌ FAILED
- **Endpoint**: `GET /organization/hierarchy/department/1`
- **Role**: employee
- **Time**: 2103ms
- **Response**: HTTP 500 (expected 200)
- **Error**: Expected 200, got 500 - 

### Test 130: Get Team Hierarchy

- **Status**: ❌ FAILED
- **Endpoint**: `GET /organization/hierarchy/team/1`
- **Role**: employee
- **Time**: 2081ms
- **Response**: HTTP 500 (expected 200)
- **Error**: Expected 200, got 500 - 

### Test 131: Get My Manager Chain

- **Status**: ❌ FAILED
- **Endpoint**: `GET /organization/manager-chain/me`
- **Role**: employee
- **Time**: 2077ms
- **Response**: HTTP 500 (expected 200)
- **Error**: Expected 200, got 500 - 

### Test 132: Get User Manager Chain

- **Status**: ❌ FAILED
- **Endpoint**: `GET /organization/manager-chain/3`
- **Role**: hr
- **Time**: 2069ms
- **Response**: HTTP 500 (expected 200)
- **Error**: Expected 200, got 500 - 

### Test 133: Get My Reporting Structure

- **Status**: ❌ FAILED
- **Endpoint**: `GET /organization/reporting-structure/me`
- **Role**: employee
- **Time**: 2093ms
- **Response**: HTTP 500 (expected 200)
- **Error**: Expected 200, got 500 - 

### Test 134: Get User Reporting Structure

- **Status**: ❌ FAILED
- **Endpoint**: `GET /organization/reporting-structure/3`
- **Role**: hr
- **Time**: 2085ms
- **Response**: HTTP 500 (expected 200)
- **Error**: Expected 200, got 500 - 

### Test 135: Get Org Chart

- **Status**: ❌ FAILED
- **Endpoint**: `GET /organization/org-chart`
- **Role**: employee
- **Time**: 2072ms
- **Response**: HTTP 500 (expected 200)
- **Error**: Expected 200, got 500 - 

### Test 136: Get My Profile

- **Status**: ✅ PASSED
- **Endpoint**: `GET /profile/me`
- **Role**: employee
- **Time**: 2079ms
- **Response**: HTTP 200 (expected 200)

### Test 137: Update My Profile

- **Status**: ✅ PASSED
- **Endpoint**: `PUT /profile/me`
- **Role**: employee
- **Time**: 2085ms
- **Response**: HTTP 200 (expected 200)

### Test 138: Get User Profile

- **Status**: ✅ PASSED
- **Endpoint**: `GET /profile/3`
- **Role**: hr
- **Time**: 2071ms
- **Response**: HTTP 200 (expected 200)

### Test 139: Get My Team Members

- **Status**: ❌ FAILED
- **Endpoint**: `GET /profile/team`
- **Role**: manager
- **Time**: 2037ms
- **Response**: HTTP 422 (expected 200)
- **Error**: Expected 200, got 422 - 

### Test 140: Get My Skills

- **Status**: ❌ FAILED
- **Endpoint**: `GET /profile/skills/me`
- **Role**: employee
- **Time**: 2045ms
- **Response**: HTTP 404 (expected 200)
- **Error**: Expected 200, got 404

### Test 141: Update My Skills

- **Status**: ❌ FAILED
- **Endpoint**: `PUT /profile/skills`
- **Role**: employee
- **Time**: 2082ms
- **Response**: HTTP 405 (expected 200)
- **Error**: Expected 200, got 405

### Test 142: Get Profile Stats

- **Status**: ❌ FAILED
- **Endpoint**: `GET /profile/stats`
- **Role**: hr
- **Time**: 2079ms
- **Response**: HTTP 422 (expected 200)
- **Error**: Expected 200, got 422 - 

### Test 143: Get My Notifications

- **Status**: ❌ FAILED
- **Endpoint**: `GET /notifications/me`
- **Role**: employee
- **Time**: 2055ms
- **Response**: HTTP 404 (expected 200)
- **Error**: Expected 200, got 404

### Test 144: Get Unread Count

- **Status**: ❌ FAILED
- **Endpoint**: `GET /notifications/unread/count`
- **Role**: employee
- **Time**: 2051ms
- **Response**: HTTP 404 (expected 200)
- **Error**: Expected 200, got 404

### Test 145: Get Unread Notifications

- **Status**: ❌ FAILED
- **Endpoint**: `GET /notifications/unread`
- **Role**: employee
- **Time**: 2071ms
- **Response**: HTTP 404 (expected 200)
- **Error**: Expected 200, got 404

### Test 146: Create Notification

- **Status**: ❌ FAILED
- **Endpoint**: `POST /notifications`
- **Role**: hr
- **Time**: 2074ms
- **Response**: HTTP 404 (expected 201)
- **Error**: Expected 201, got 404


---

**Report Generated**: 2025-11-26 00:52:11
