# Dashboard API Documentation

## Overview

This document provides comprehensive documentation for the Dashboard APIs that serve data to HR, Manager, and Employee dashboards in the GenAI HRMS system.

## Base URL

```
http://localhost:8000/api/v1/dashboard
```

## Authentication

All dashboard endpoints require Bearer token authentication:

```
Authorization: Bearer <access_token>
```

## Endpoints

### 1. HR Dashboard

**Endpoint:** `GET /api/v1/dashboard/hr`

**Access:** HR role only

**Description:** Get comprehensive dashboard data for HR users including department statistics, attendance, and active applications.

**Response Schema:**

```json
{
  "departments": [
    {
      "department_id": 1,
      "department_name": "Engineering",
      "employee_count": 20
    }
  ],
  "department_attendance": [
    {
      "department_id": 1,
      "department_name": "Engineering",
      "present_percentage": 85.5,
      "absent_percentage": 14.5
    }
  ],
  "department_modules": [
    {
      "department_id": 1,
      "department_name": "Engineering",
      "modules_completed": 45
    }
  ],
  "active_applications": [
    {
      "application_id": 1,
      "applicant_name": "John Doe",
      "applied_role": "Software Engineer",
      "applied_date": "2025-11-10T10:00:00",
      "status": "pending",
      "source": "referral"
    }
  ],
  "total_employees": 57,
  "total_departments": 5,
  "total_active_applications": 10
}
```

**Data Points:**
- **departments:** List of departments with employee counts
- **department_attendance:** Department-wise attendance statistics (last 30 days)
- **department_modules:** Department-wise skill modules completion leaderboard
- **active_applications:** Recent active job applications (up to 10)
- **total_employees:** Total number of active employees
- **total_departments:** Total number of active departments
- **total_active_applications:** Total number of pending/reviewed applications

**Frontend Mapping:**
- Maps to `HRDashboard.tsx`
- Attendance data → Department-wise Attendance chart
- Module data → Department-wise Leaderboard chart
- Departments → Department Employee Count table
- Active applications → Active Applications table

---

### 2. Manager Dashboard

**Endpoint:** `GET /api/v1/dashboard/manager`

**Access:** Manager role only

**Description:** Get comprehensive dashboard data for Manager users including personal info and team overview.

**Response Schema:**

```json
{
  "personal_info": {
    "casual_leave": 8,
    "sick_leave": 10,
    "annual_leave": 12,
    "wfh_balance": 8
  },
  "today_attendance": {
    "date": "2025-11-13",
    "check_in_time": "2025-11-13T09:04:00",
    "check_out_time": null,
    "status": "present",
    "hours_worked": null
  },
  "upcoming_holidays": [
    {
      "id": 1,
      "name": "Diwali",
      "description": "Festival of Lights",
      "start_date": "2025-11-01",
      "end_date": "2025-11-01",
      "is_mandatory": true,
      "holiday_type": "festival"
    }
  ],
  "team_stats": {
    "team_id": 1,
    "team_name": "Backend Team",
    "total_members": 8,
    "team_training_hours": 1300.0,
    "team_performance_score": 3.9
  },
  "team_goals": {
    "total_goals": 20,
    "completed_goals": 15,
    "in_progress_goals": 3,
    "not_started_goals": 2,
    "completion_percentage": 75.0
  },
  "team_attendance": [
    {
      "employee_id": 5,
      "employee_name": "Alice Smith",
      "present_percentage": 90.0,
      "absent_percentage": 10.0
    }
  ],
  "team_modules_leaderboard": [
    {
      "employee_id": 5,
      "employee_name": "Alice Smith",
      "modules_completed": 12
    }
  ],
  "learner_rank": 3
}
```

**Data Points:**
- **personal_info:** Manager's leave balances
- **today_attendance:** Manager's attendance for today (check-in/out times)
- **upcoming_holidays:** Next 5 upcoming holidays
- **team_stats:** Team statistics (members, training hours, performance score)
- **team_goals:** Team goals progress statistics
- **team_attendance:** Team member attendance statistics (last 30 days)
- **team_modules_leaderboard:** Team member skill modules completion leaderboard
- **learner_rank:** Manager's rank in organization based on modules completed

**Frontend Mapping:**
- Maps to `ManagerDashboard.tsx`
- personal_info → WFH Left, Leaves Left cards
- today_attendance → Punch In/Out card
- upcoming_holidays → Upcoming Holidays card
- team_goals → Team Goals pie chart
- team_modules_leaderboard → Learner Leaderboard chart
- team_stats → Team training hours and performance score cards

---

### 3. Employee Dashboard

**Endpoint:** `GET /api/v1/dashboard/employee`

**Access:** Employee role only

**Description:** Get comprehensive dashboard data for Employee users including personal info and learning goals.

**Response Schema:**

```json
{
  "employee_name": "John Doe",
  "leave_balance": {
    "casual_leave": 8,
    "sick_leave": 10,
    "annual_leave": 12,
    "wfh_balance": 8
  },
  "today_attendance": {
    "date": "2025-11-13",
    "check_in_time": "2025-11-13T09:04:00",
    "check_out_time": null,
    "status": "present",
    "hours_worked": null
  },
  "upcoming_holidays": [
    {
      "id": 1,
      "name": "Diwali",
      "description": "Festival of Lights",
      "start_date": "2025-11-01",
      "end_date": "2025-11-01",
      "is_mandatory": true,
      "holiday_type": "festival"
    }
  ],
  "learning_goals": {
    "total_goals": 5,
    "completed_goals": 4,
    "pending_goals": 1,
    "completion_percentage": 80.0
  },
  "learner_rank": 3
}
```

**Data Points:**
- **employee_name:** Employee's full name
- **leave_balance:** Employee's leave balances (casual, sick, annual, WFH)
- **today_attendance:** Today's attendance (check-in/out times)
- **upcoming_holidays:** Next 5 upcoming holidays
- **learning_goals:** Goals statistics (completed vs pending)
- **learner_rank:** Employee's rank in organization based on modules completed

**Frontend Mapping:**
- Maps to `EmployeeDashboard.tsx`
- employee_name → Welcome message
- leave_balance → WFH Left, Leaves Left cards
- today_attendance → Punch In/Out card
- upcoming_holidays → Upcoming Holidays card
- learning_goals → Learning Goals doughnut chart
- learner_rank → Learner Rank card

---

### 4. My Dashboard (Auto-route)

**Endpoint:** `GET /api/v1/dashboard/me`

**Access:** All authenticated users

**Description:** Automatically routes to appropriate dashboard based on user role.

**Response Schema:**

```json
{
  "role": "hr" | "manager" | "employee",
  "dashboard_data": {
    // Role-specific dashboard data
  }
}
```

---

### 5. Employee Performance Metrics

**Endpoint:** `GET /api/v1/dashboard/performance/{employee_id}`

**Query Parameters:**
- `months` (optional): Number of months of data (1-24, default: 12)

**Access:**
- HR: Can view any employee's performance
- Manager: Can view their team members' performance
- Employee: Can only view their own performance

**Description:** Get detailed performance metrics for an employee including monthly module completion trend.

**Response Schema:**

```json
{
  "employee_id": 5,
  "employee_name": "John Doe",
  "monthly_modules": [
    {
      "month": "2025-01",
      "modules_completed": 3
    },
    {
      "month": "2025-02",
      "modules_completed": 5
    }
  ],
  "total_modules_completed": 25,
  "attendance_rate": 95.5,
  "goals_completion_rate": 80.0
}
```

**Data Points:**
- **monthly_modules:** Array of monthly module completion data (for graphs)
- **total_modules_completed:** Total number of modules completed
- **attendance_rate:** Attendance percentage (last 90 days)
- **goals_completion_rate:** Goals completion percentage

**Frontend Mapping:**
- Maps to `PerformanceReport.tsx`
- monthly_modules → Modules completed month-wise graph

---

### 6. My Performance Metrics

**Endpoint:** `GET /api/v1/dashboard/performance/me`

**Query Parameters:**
- `months` (optional): Number of months of data (1-24, default: 12)

**Access:** All authenticated users

**Description:** Get performance metrics for the current user.

---

## Error Responses

### 401 Unauthorized

```json
{
  "detail": "Invalid authentication credentials"
}
```

### 403 Forbidden

```json
{
  "detail": "Only HR can perform this action"
}
```

### 404 Not Found

```json
{
  "detail": "Employee not found"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Failed to fetch dashboard data: <error message>"
}
```

---

## Frontend-Backend Data Alignment

### HR Dashboard
| Frontend Component | Backend Data Source | Data Model |
|-------------------|---------------------|------------|
| Department-wise Attendance Chart | `department_attendance` | Attendance → aggregated by Department |
| Department-wise Leaderboard | `department_modules` | SkillModuleEnrollment → aggregated by Department |
| Department Employee Count Table | `departments` | User → grouped by Department |
| Active Applications Table | `active_applications` | Application (status: pending/reviewed) |

### Manager Dashboard
| Frontend Component | Backend Data Source | Data Model |
|-------------------|---------------------|------------|
| WFH Left / Leaves Left | `personal_info` | User (manager) leave balances |
| Punch In/Out | `today_attendance` | Attendance (today) |
| Upcoming Holidays | `upcoming_holidays` | Holiday |
| Team Goals Chart | `team_goals` | Goal → filtered by team members |
| Learner Leaderboard | `team_modules_leaderboard` | SkillModuleEnrollment → by team |
| Team Stats | `team_stats` | Team, SkillModule, PerformanceReport |

### Employee Dashboard
| Frontend Component | Backend Data Source | Data Model |
|-------------------|---------------------|------------|
| Welcome Message | `employee_name` | User.name |
| WFH Left / Leaves Left | `leave_balance` | User leave balances |
| Punch In/Out | `today_attendance` | Attendance (today) |
| Upcoming Holidays | `upcoming_holidays` | Holiday |
| Learning Goals Chart | `learning_goals` | Goal (employee) |
| Learner Rank | `learner_rank` | Calculated from SkillModuleEnrollment |

---

## Business Logic

### Attendance Calculation
- Attendance percentage calculated over last 30 days (configurable)
- Present status includes: PRESENT, WFH
- Absent status includes: ABSENT, LEAVE

### Learner Rank Calculation
- Based on total completed skill modules
- Rank = number of employees with more completed modules + 1
- Employees with no completed modules return null rank

### Team Performance Score
- Average of overall_rating from PerformanceReport
- Calculated from reports in last 90 days
- Returns 0.0 if no performance reports exist

### Team Training Hours
- Sum of duration_hours from completed SkillModules
- Only counts modules with status = COMPLETED

---

## Usage Examples

### cURL Examples

#### 1. Get HR Dashboard

```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/hr" \
  -H "Authorization: Bearer <access_token>"
```

#### 2. Get Manager Dashboard

```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/manager" \
  -H "Authorization: Bearer <access_token>"
```

#### 3. Get Employee Dashboard

```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/employee" \
  -H "Authorization: Bearer <access_token>"
```

#### 4. Get My Dashboard (Auto-route)

```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/me" \
  -H "Authorization: Bearer <access_token>"
```

#### 5. Get Employee Performance

```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/performance/5?months=6" \
  -H "Authorization: Bearer <access_token>"
```

---

## Frontend Integration Guide

### React/TypeScript Example

```typescript
import { api } from '@/config/api';

// Get HR Dashboard
const getHRDashboard = async () => {
  const response = await api.get('/dashboard/hr');
  return response.data;
};

// Get Manager Dashboard
const getManagerDashboard = async () => {
  const response = await api.get('/dashboard/manager');
  return response.data;
};

// Get Employee Dashboard
const getEmployeeDashboard = async () => {
  const response = await api.get('/dashboard/employee');
  return response.data;
};

// Get My Dashboard (auto-route)
const getMyDashboard = async () => {
  const response = await api.get('/dashboard/me');
  return response.data;
};

// Get Performance Metrics
const getPerformanceMetrics = async (employeeId: number, months: number = 12) => {
  const response = await api.get(`/dashboard/performance/${employeeId}`, {
    params: { months }
  });
  return response.data;
};
```

---

## Notes

1. All timestamps are in UTC
2. Percentage values are rounded to 2 decimal places
3. Attendance statistics default to last 30 days but can be configured
4. Performance report uses last 90 days of data
5. Holiday list returns next 5 upcoming holidays (configurable)
6. Active applications list returns up to 10 most recent applications

---

Last Updated: November 13, 2025


