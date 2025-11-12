# Backend API Documentation - GenAI HRMS Application

## Overview
This document outlines all the REST API endpoints required for the GenAI HRMS (Human Resource Management System) application. The system supports three user roles: **HR**, **Manager**, and **Employee**, with role-based access control.

## Technology Stack
- **Framework**: Flask/FastAPI (Python)
- **Database**: PostgreSQL/MySQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **File Storage**: Local/Cloud Storage for documents (PDFs, images)
- **GenAI Integration**: For resume screening and job description generation

## Base URL
```
http://localhost:5000/api/v1
```

---

## Table of Contents
1. [Authentication APIs](#1-authentication-apis)
2. [User Management APIs](#2-user-management-apis)
3. [Dashboard APIs](#3-dashboard-apis)
4. [Job Listing APIs](#4-job-listing-apis)
5. [Application Management APIs](#5-application-management-apis)
6. [Employee Management APIs](#6-employee-management-apis)
7. [Announcement APIs](#7-announcement-apis)
8. [Policy APIs](#8-policy-apis)
9. [Attendance APIs](#9-attendance-apis)
10. [Leave Management APIs](#10-leave-management-apis)
11. [Payslip APIs](#11-payslip-apis)
12. [Goal & Performance APIs](#12-goal--performance-apis)
13. [Skill Development APIs](#13-skill-development-apis)
14. [Feedback APIs](#14-feedback-apis)
15. [Team Management APIs](#15-team-management-apis)
16. [Resume Screening APIs](#16-resume-screening-apis)
17. [Department & Organization APIs](#17-department--organization-apis)
18. [Holiday Management APIs](#18-holiday-management-apis)

---

## API Response Format

### Success Response
```json
{
  "success": true,
  "data": {},
  "message": "Operation successful"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description"
  }
}
```

---

## 1. Authentication APIs

### 1.1 User Login
**Endpoint**: `POST /auth/login`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "name": "John Doe",
      "email": "user@example.com",
      "role": "employee",
      "employee_id": "EMP001"
    },
    "access_token": "jwt_token_here",
    "refresh_token": "refresh_token_here"
  }
}
```

### 1.2 User Logout
**Endpoint**: `POST /auth/logout`

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

### 1.3 Refresh Token
**Endpoint**: `POST /auth/refresh`

**Request Body**:
```json
{
  "refresh_token": "refresh_token_here"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "access_token": "new_jwt_token_here"
  }
}
```

### 1.4 Change Password
**Endpoint**: `POST /auth/change-password`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "old_password": "old_password",
  "new_password": "new_password"
}
```

---

## 2. User Management APIs

### 2.1 Get Current User Profile
**Endpoint**: `GET /users/me`

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "employee_id": "EMP001",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "role": "employee",
    "department": "Engineering",
    "job_role": "Software Engineer",
    "team_name": "Backend Team",
    "manager": {
      "id": 5,
      "name": "Jane Manager",
      "email": "jane@example.com"
    },
    "hire_date": "2023-01-15",
    "profile_image_path": "/uploads/profiles/user_1.jpg",
    "aadhar_document_path": "/uploads/documents/aadhar_1.pdf",
    "pan_document_path": "/uploads/documents/pan_1.pdf"
  }
}
```

### 2.2 Update User Profile
**Endpoint**: `PUT /users/me`

**Headers**: `Authorization: Bearer <token>`

**Request Body** (multipart/form-data):
```json
{
  "name": "John Doe Updated",
  "phone": "+1234567890",
  "profile_image": "<file>",
  "aadhar_document": "<file>",
  "pan_document": "<file>"
}
```

### 2.3 Get User by ID
**Endpoint**: `GET /users/{user_id}`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR, Manager (for their team)

---

## 3. Dashboard APIs

### 3.1 HR Dashboard Data
**Endpoint**: `GET /dashboard/hr`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

**Response**:
```json
{
  "success": true,
  "data": {
    "departments": [
      {
        "name": "Engineering",
        "employee_count": 50,
        "average_attendance": 85.5,
        "modules_completed": 120
      }
    ],
    "attendance_stats": [
      {
        "department": "HR",
        "present_percentage": 80,
        "absent_percentage": 20
      }
    ],
    "skill_leaderboard": [
      {
        "department": "Engineering",
        "modules_completed": 150
      }
    ],
    "active_applications": [
      {
        "applicant_name": "John Smith",
        "position": "Software Engineer",
        "applied_date": "2024-11-01"
      }
    ]
  }
}
```

### 3.2 Employee Dashboard Data
**Endpoint**: `GET /dashboard/employee`

**Headers**: `Authorization: Bearer <token>`

**Access**: Employee, Manager

**Response**:
```json
{
  "success": true,
  "data": {
    "wfh_left": 8,
    "leaves_left": 12,
    "learner_rank": 3,
    "punch_in_time": "2024-11-11T09:04:00Z",
    "punch_out_time": null,
    "learning_goals": {
      "completed": 80,
      "pending": 20
    },
    "upcoming_holidays": [
      {
        "id": 1,
        "name": "Diwali",
        "start_date": "2024-11-01",
        "end_date": "2024-11-01"
      }
    ]
  }
}
```

### 3.3 Manager Dashboard Data
**Endpoint**: `GET /dashboard/manager`

**Headers**: `Authorization: Bearer <token>`

**Access**: Manager only

**Response**:
```json
{
  "success": true,
  "data": {
    "personal": {
      "wfh_left": 8,
      "leaves_left": 12,
      "learner_rank": 2,
      "punch_in_time": "2024-11-11T09:04:00Z",
      "punch_out_time": null
    },
    "team_overview": {
      "team_goals_completed": 74,
      "team_goals_pending": 26,
      "team_attendance": [
        {
          "employee_name": "Employee 1",
          "present_percentage": 80,
          "absent_percentage": 20
        }
      ],
      "team_leaderboard": [
        {
          "employee_name": "Employee 2",
          "modules_completed": 15
        }
      ],
      "team_training_hours": 1300,
      "team_performance_score": 3.9
    },
    "upcoming_holidays": []
  }
}
```

---

## 4. Job Listing APIs

### 4.1 Get All Job Listings
**Endpoint**: `GET /jobs`

**Query Parameters**:
- `department` (optional): Filter by department
- `location` (optional): Filter by location
- `is_active` (optional): Filter by active status (default: true)
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10)

**Response**:
```json
{
  "success": true,
  "data": {
    "jobs": [
      {
        "id": 1,
        "position": "Software Engineer",
        "department": "Engineering",
        "location": "Bangalore",
        "experience_required": "2-4 years",
        "skills_required": "Python, Flask, React",
        "description": "Job description here",
        "employment_type": "full-time",
        "posted_date": "2024-11-01T10:00:00Z",
        "is_active": true
      }
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 5,
      "total_items": 50,
      "items_per_page": 10
    }
  }
}
```

### 4.2 Get Job by ID
**Endpoint**: `GET /jobs/{job_id}`

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "position": "Software Engineer",
    "department": "Engineering",
    "location": "Bangalore",
    "experience_required": "2-4 years",
    "skills_required": "Python, Flask, React",
    "description": "Detailed job description",
    "ai_generated_description": "AI enhanced description",
    "employment_type": "full-time",
    "salary_range": "10-15 LPA",
    "application_deadline": "2024-12-31",
    "posted_by": {
      "id": 2,
      "name": "HR Manager"
    },
    "posted_date": "2024-11-01T10:00:00Z",
    "is_active": true,
    "applications_count": 15
  }
}
```

### 4.3 Create Job Listing (HR Only)
**Endpoint**: `POST /jobs`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

**Request Body**:
```json
{
  "position": "Software Engineer",
  "department": "Engineering",
  "location": "Bangalore",
  "experience_required": "2-4 years",
  "skills_required": "Python, Flask, React",
  "description": "Job description",
  "employment_type": "full-time",
  "salary_range": "10-15 LPA",
  "application_deadline": "2024-12-31",
  "generate_ai_description": true
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "position": "Software Engineer",
    "ai_generated_description": "AI enhanced version of the job description",
    "created_at": "2024-11-11T10:00:00Z"
  },
  "message": "Job listing created successfully"
}
```

### 4.4 Update Job Listing (HR Only)
**Endpoint**: `PUT /jobs/{job_id}`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

**Request Body**: Same as create

### 4.5 Delete/Deactivate Job Listing (HR Only)
**Endpoint**: `DELETE /jobs/{job_id}`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

---

## 5. Application Management APIs

### 5.1 Get All Applications
**Endpoint**: `GET /applications`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

**Query Parameters**:
- `status` (optional): Filter by status (pending, reviewed, shortlisted, rejected, hired)
- `job_id` (optional): Filter by job
- `source` (optional): Filter by source (referral, self-applied)
- `page`, `limit`

**Response**:
```json
{
  "success": true,
  "data": {
    "applications": [
      {
        "id": 1,
        "applicant_name": "John Smith",
        "applicant_email": "john@example.com",
        "job": {
          "id": 1,
          "position": "Software Engineer"
        },
        "source": "self-applied",
        "status": "pending",
        "applied_date": "2024-11-01T10:00:00Z",
        "screening_score": 85.5
      }
    ],
    "pagination": {}
  }
}
```

### 5.2 Get Application by ID
**Endpoint**: `GET /applications/{application_id}`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "applicant_name": "John Smith",
    "applicant_email": "john@example.com",
    "applicant_phone": "+1234567890",
    "job": {
      "id": 1,
      "position": "Software Engineer",
      "department": "Engineering"
    },
    "resume_path": "/uploads/resumes/resume_1.pdf",
    "cover_letter": "Cover letter text",
    "source": "self-applied",
    "status": "pending",
    "screening_score": 85.5,
    "screening_notes": "Strong technical background",
    "applied_date": "2024-11-01T10:00:00Z",
    "reviewed_date": null
  }
}
```

### 5.3 Submit Job Application
**Endpoint**: `POST /applications`

**Request Body** (multipart/form-data):
```json
{
  "job_id": 1,
  "applicant_name": "John Smith",
  "applicant_email": "john@example.com",
  "applicant_phone": "+1234567890",
  "resume": "<file>",
  "cover_letter": "Cover letter text",
  "source": "self-applied"
}
```

### 5.4 Update Application Status (HR Only)
**Endpoint**: `PUT /applications/{application_id}/status`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

**Request Body**:
```json
{
  "status": "shortlisted",
  "screening_notes": "Good candidate, proceed to interview"
}
```

### 5.5 Bulk Update Applications (HR Only)
**Endpoint**: `POST /applications/bulk-update`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "application_ids": [1, 2, 3],
  "status": "reviewed"
}
```

---

## 6. Employee Management APIs

### 6.1 Get All Employees
**Endpoint**: `GET /employees`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR, Manager (limited to their team)

**Query Parameters**:
- `department` (optional)
- `team_name` (optional)
- `role` (optional)
- `search` (optional): Search by name or employee_id
- `page`, `limit`

**Response**:
```json
{
  "success": true,
  "data": {
    "employees": [
      {
        "id": 1,
        "employee_id": "EMP001",
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "department": "Engineering",
        "job_role": "Software Engineer",
        "team_name": "Backend Team",
        "manager": {
          "id": 5,
          "name": "Jane Manager"
        },
        "hire_date": "2023-01-15",
        "is_active": true
      }
    ],
    "pagination": {}
  }
}
```

### 6.2 Get Employee by ID
**Endpoint**: `GET /employees/{employee_id}`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR, Manager (their team), Self

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "employee_id": "EMP001",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "role": "employee",
    "department": "Engineering",
    "job_role": "Software Engineer",
    "team_name": "Backend Team",
    "manager": {
      "id": 5,
      "name": "Jane Manager",
      "email": "jane@example.com"
    },
    "hire_date": "2023-01-15",
    "salary": 1500000.0,
    "profile_image_path": "/uploads/profiles/user_1.jpg",
    "aadhar_document_path": "/uploads/documents/aadhar_1.pdf",
    "pan_document_path": "/uploads/documents/pan_1.pdf",
    "is_active": true
  }
}
```

### 6.3 Create Employee (HR Only)
**Endpoint**: `POST /employees`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

**Request Body** (multipart/form-data):
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "password": "temporary_password",
  "employee_id": "EMP001",
  "department": "Engineering",
  "job_role": "Software Engineer",
  "team_name": "Backend Team",
  "manager_id": 5,
  "hire_date": "2023-01-15",
  "salary": 1500000.0,
  "role": "employee",
  "aadhar_document": "<file>",
  "pan_document": "<file>",
  "profile_image": "<file>"
}
```

### 6.4 Update Employee (HR Only)
**Endpoint**: `PUT /employees/{employee_id}`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

**Request Body**: Same as create (all fields optional)

### 6.5 Delete/Deactivate Employee (HR Only)
**Endpoint**: `DELETE /employees/{employee_id}`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

### 6.6 Get Team Members (Manager)
**Endpoint**: `GET /employees/team`

**Headers**: `Authorization: Bearer <token>`

**Access**: Manager only

**Response**: List of employees reporting to the manager

---

## 7. Announcement APIs

### 7.1 Get All Announcements
**Endpoint**: `GET /announcements`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `target_department` (optional)
- `target_role` (optional)
- `is_urgent` (optional)
- `page`, `limit`

**Response**:
```json
{
  "success": true,
  "data": {
    "announcements": [
      {
        "id": 1,
        "title": "Company Holiday Announcement",
        "message": "Brief preview of the announcement",
        "is_urgent": false,
        "published_date": "2024-11-01T10:00:00Z",
        "created_by": {
          "name": "HR Manager"
        }
      }
    ],
    "pagination": {}
  }
}
```

### 7.2 Get Announcement by ID
**Endpoint**: `GET /announcements/{announcement_id}`

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Company Holiday Announcement",
    "message": "Full announcement text here",
    "link": "https://example.com/details",
    "target_departments": ["Engineering", "HR"],
    "target_roles": ["employee", "manager"],
    "is_urgent": false,
    "published_date": "2024-11-01T10:00:00Z",
    "expiry_date": "2024-12-31T23:59:59Z",
    "created_by": {
      "id": 2,
      "name": "HR Manager"
    }
  }
}
```

### 7.3 Create Announcement (HR Only)
**Endpoint**: `POST /announcements`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

**Request Body**:
```json
{
  "title": "Company Holiday Announcement",
  "message": "Full announcement text",
  "link": "https://example.com/details",
  "target_departments": ["Engineering", "HR"],
  "target_roles": ["employee", "manager"],
  "is_urgent": false,
  "expiry_date": "2024-12-31"
}
```

### 7.4 Update Announcement (HR Only)
**Endpoint**: `PUT /announcements/{announcement_id}`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

### 7.5 Delete Announcement (HR Only)
**Endpoint**: `DELETE /announcements/{announcement_id}`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

---

## 8. Policy APIs

### 8.1 Get All Policies
**Endpoint**: `GET /policies`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `category` (optional)
- `is_active` (optional)
- `page`, `limit`

**Response**:
```json
{
  "success": true,
  "data": {
    "policies": [
      {
        "id": 1,
        "title": "Work From Home Policy",
        "description": "Policy brief description",
        "category": "HR",
        "version": "2.0",
        "effective_date": "2024-01-01",
        "is_active": true
      }
    ],
    "pagination": {}
  }
}
```

### 8.2 Get Policy by ID
**Endpoint**: `GET /policies/{policy_id}`

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Work From Home Policy",
    "description": "Policy description",
    "content": "Full policy content",
    "category": "HR",
    "version": "2.0",
    "effective_date": "2024-01-01",
    "review_date": "2025-01-01",
    "document_path": "/uploads/policies/wfh_policy.pdf",
    "is_active": true,
    "created_by": {
      "name": "HR Manager"
    },
    "created_at": "2023-12-01T10:00:00Z"
  }
}
```

### 8.3 Create Policy (HR Only)
**Endpoint**: `POST /policies`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

**Request Body** (multipart/form-data):
```json
{
  "title": "Work From Home Policy",
  "description": "Policy description",
  "content": "Full policy content",
  "category": "HR",
  "version": "2.0",
  "effective_date": "2024-01-01",
  "review_date": "2025-01-01",
  "document": "<file>"
}
```

### 8.4 Update Policy (HR Only)
**Endpoint**: `PUT /policies/{policy_id}`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

### 8.5 Download Policy Document
**Endpoint**: `GET /policies/{policy_id}/download`

**Headers**: `Authorization: Bearer <token>`

**Response**: File download

---

## 9. Attendance APIs

### 9.1 Get Attendance Records
**Endpoint**: `GET /attendance`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `employee_id` (optional): For HR/Manager to view specific employee
- `start_date` (optional): Filter by date range
- `end_date` (optional)
- `status` (optional): Filter by status
- `page`, `limit`

**Access**: Employee (own), Manager (team), HR (all)

**Response**:
```json
{
  "success": true,
  "data": {
    "attendance_records": [
      {
        "id": 1,
        "employee": {
          "id": 1,
          "name": "John Doe",
          "employee_id": "EMP001"
        },
        "date": "2024-11-11",
        "status": "present",
        "check_in_time": "2024-11-11T09:04:00Z",
        "check_out_time": "2024-11-11T18:30:00Z",
        "hours_worked": 9.43,
        "location": "office"
      }
    ],
    "summary": {
      "total_days": 20,
      "present_days": 18,
      "absent_days": 1,
      "wfh_days": 1,
      "leave_days": 0,
      "attendance_percentage": 95.0
    },
    "pagination": {}
  }
}
```

### 9.2 Get Attendance Summary
**Endpoint**: `GET /attendance/summary`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `employee_id` (optional)
- `month` (optional): Format YYYY-MM
- `year` (optional)

**Response**:
```json
{
  "success": true,
  "data": {
    "employee_id": "EMP001",
    "month": "2024-11",
    "total_working_days": 22,
    "present_days": 18,
    "absent_days": 1,
    "wfh_days": 2,
    "leave_days": 1,
    "holiday_days": 0,
    "attendance_percentage": 95.45,
    "average_hours_worked": 8.5,
    "wfh_left": 8,
    "leaves_left": 12
  }
}
```

### 9.3 Punch In
**Endpoint**: `POST /attendance/punch-in`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "location": "office"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "check_in_time": "2024-11-11T09:04:00Z",
    "status": "present"
  },
  "message": "Punched in successfully"
}
```

### 9.4 Punch Out
**Endpoint**: `POST /attendance/punch-out`

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "check_in_time": "2024-11-11T09:04:00Z",
    "check_out_time": "2024-11-11T18:30:00Z",
    "hours_worked": 9.43,
    "status": "present"
  },
  "message": "Punched out successfully"
}
```

### 9.5 Get Department-wise Attendance (HR/Manager)
**Endpoint**: `GET /attendance/department-stats`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR, Manager

**Query Parameters**:
- `department` (optional)
- `date` (optional): Default today

**Response**:
```json
{
  "success": true,
  "data": {
    "departments": [
      {
        "department": "Engineering",
        "total_employees": 50,
        "present_count": 42,
        "absent_count": 3,
        "wfh_count": 5,
        "leave_count": 0,
        "present_percentage": 84.0
      }
    ],
    "overall": {
      "total_employees": 100,
      "present_percentage": 85.0
    }
  }
}
```

---

## 10. Leave Management APIs

### 10.1 Get Leave Requests
**Endpoint**: `GET /leaves`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `employee_id` (optional): For managers/HR
- `status` (optional): pending, approved, rejected
- `leave_type` (optional)
- `start_date`, `end_date` (optional)
- `page`, `limit`

**Access**: Employee (own), Manager (team), HR (all)

**Response**:
```json
{
  "success": true,
  "data": {
    "leave_requests": [
      {
        "id": 1,
        "employee": {
          "id": 1,
          "name": "John Doe",
          "employee_id": "EMP001"
        },
        "leave_type": "casual",
        "start_date": "2024-11-15",
        "end_date": "2024-11-17",
        "days_requested": 3,
        "subject": "Personal work",
        "reason": "Need to attend family function",
        "status": "pending",
        "requested_date": "2024-11-10T10:00:00Z"
      }
    ],
    "pagination": {}
  }
}
```

### 10.2 Get Leave Balance
**Endpoint**: `GET /leaves/balance`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `employee_id` (optional): For managers/HR

**Response**:
```json
{
  "success": true,
  "data": {
    "employee_id": "EMP001",
    "leave_balances": {
      "casual": {
        "total": 12,
        "used": 4,
        "remaining": 8
      },
      "sick": {
        "total": 12,
        "used": 2,
        "remaining": 10
      },
      "annual": {
        "total": 15,
        "used": 10,
        "remaining": 5
      }
    },
    "wfh_balance": {
      "total": 24,
      "used": 16,
      "remaining": 8
    }
  }
}
```

### 10.3 Submit Leave Request
**Endpoint**: `POST /leaves`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "leave_type": "casual",
  "start_date": "2024-11-15",
  "end_date": "2024-11-17",
  "subject": "Personal work",
  "reason": "Need to attend family function"
}
```

### 10.4 Approve/Reject Leave Request (Manager/HR)
**Endpoint**: `PUT /leaves/{leave_id}/status`

**Headers**: `Authorization: Bearer <token>`

**Access**: Manager (team members), HR (all)

**Request Body**:
```json
{
  "status": "approved",
  "rejection_reason": "Optional if rejected"
}
```

### 10.5 Cancel Leave Request
**Endpoint**: `DELETE /leaves/{leave_id}`

**Headers**: `Authorization: Bearer <token>`

**Access**: Employee (own pending requests), Manager (team), HR (all)

---

## 11. Payslip APIs

### 11.1 Get Payslips
**Endpoint**: `GET /payslips`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `employee_id` (optional): For HR
- `year` (optional)
- `month` (optional)
- `page`, `limit`

**Access**: Employee (own), HR (all)

**Response**:
```json
{
  "success": true,
  "data": {
    "payslips": [
      {
        "id": 1,
        "employee": {
          "id": 1,
          "name": "John Doe",
          "employee_id": "EMP001"
        },
        "pay_period_start": "2024-11-01",
        "pay_period_end": "2024-11-30",
        "pay_date": "2024-12-01",
        "gross_salary": 150000.0,
        "total_deductions": 30000.0,
        "net_salary": 120000.0,
        "payslip_file_path": "/uploads/payslips/payslip_1_nov_2024.pdf",
        "generated_date": "2024-11-30T10:00:00Z"
      }
    ],
    "pagination": {}
  }
}
```

### 11.2 Get Payslip by ID
**Endpoint**: `GET /payslips/{payslip_id}`

**Headers**: `Authorization: Bearer <token>`

**Access**: Employee (own), HR (all)

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "employee": {
      "id": 1,
      "name": "John Doe",
      "employee_id": "EMP001"
    },
    "pay_period_start": "2024-11-01",
    "pay_period_end": "2024-11-30",
    "pay_date": "2024-12-01",
    "basic_salary": 100000.0,
    "allowances": 30000.0,
    "overtime_pay": 5000.0,
    "bonus": 15000.0,
    "gross_salary": 150000.0,
    "tax_deduction": 20000.0,
    "pf_deduction": 8000.0,
    "insurance_deduction": 2000.0,
    "other_deductions": 0.0,
    "total_deductions": 30000.0,
    "net_salary": 120000.0,
    "payslip_file_path": "/uploads/payslips/payslip_1_nov_2024.pdf",
    "generated_date": "2024-11-30T10:00:00Z"
  }
}
```

### 11.3 Generate Payslip (HR Only)
**Endpoint**: `POST /payslips`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

**Request Body**:
```json
{
  "employee_id": 1,
  "pay_period_start": "2024-11-01",
  "pay_period_end": "2024-11-30",
  "pay_date": "2024-12-01",
  "basic_salary": 100000.0,
  "allowances": 30000.0,
  "overtime_pay": 5000.0,
  "bonus": 15000.0,
  "tax_deduction": 20000.0,
  "pf_deduction": 8000.0,
  "insurance_deduction": 2000.0,
  "other_deductions": 0.0
}
```

### 11.4 Download Payslip
**Endpoint**: `GET /payslips/{payslip_id}/download`

**Headers**: `Authorization: Bearer <token>`

**Response**: PDF file download

### 11.5 Bulk Generate Payslips (HR Only)
**Endpoint**: `POST /payslips/bulk-generate`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

**Request Body**:
```json
{
  "pay_period_start": "2024-11-01",
  "pay_period_end": "2024-11-30",
  "pay_date": "2024-12-01",
  "employee_ids": [1, 2, 3, 4]
}
```

---

## 12. Goal & Performance APIs

### 12.1 Get Goals
**Endpoint**: `GET /goals`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `employee_id` (optional): For managers/HR
- `status` (optional): not_started, in_progress, completed
- `category` (optional)
- `page`, `limit`

**Access**: Employee (own), Manager (team), HR (all)

**Response**:
```json
{
  "success": true,
  "data": {
    "goals": [
      {
        "id": 1,
        "employee": {
          "id": 1,
          "name": "John Doe"
        },
        "title": "Complete React Course",
        "description": "Learn React fundamentals",
        "category": "learning",
        "start_date": "2024-11-01",
        "target_date": "2024-12-31",
        "status": "in_progress",
        "progress_percentage": 60.0,
        "assigned_by": {
          "name": "Manager Name"
        }
      }
    ],
    "pagination": {}
  }
}
```

### 12.2 Get Goal by ID
**Endpoint**: `GET /goals/{goal_id}`

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "employee": {
      "id": 1,
      "name": "John Doe"
    },
    "title": "Complete React Course",
    "description": "Learn React fundamentals and build projects",
    "category": "learning",
    "start_date": "2024-11-01",
    "target_date": "2024-12-31",
    "completion_date": null,
    "status": "in_progress",
    "progress_percentage": 60.0,
    "assigned_by": {
      "id": 5,
      "name": "Manager Name"
    },
    "checkpoints": [
      {
        "id": 1,
        "title": "Complete basic tutorials",
        "description": "Finish first 5 chapters",
        "sequence_number": 1,
        "is_completed": true,
        "completed_date": "2024-11-15T10:00:00Z"
      },
      {
        "id": 2,
        "title": "Build a todo app",
        "description": "Create a simple todo application",
        "sequence_number": 2,
        "is_completed": false,
        "completed_date": null
      }
    ]
  }
}
```

### 12.3 Create Goal
**Endpoint**: `POST /goals`

**Headers**: `Authorization: Bearer <token>`

**Access**: Employee (self), Manager (for team), HR (all)

**Request Body**:
```json
{
  "employee_id": 1,
  "title": "Complete React Course",
  "description": "Learn React fundamentals",
  "category": "learning",
  "start_date": "2024-11-01",
  "target_date": "2024-12-31",
  "checkpoints": [
    {
      "title": "Complete basic tutorials",
      "description": "Finish first 5 chapters",
      "sequence_number": 1
    }
  ]
}
```

### 12.4 Update Goal
**Endpoint**: `PUT /goals/{goal_id}`

**Headers**: `Authorization: Bearer <token>`

### 12.5 Update Goal Progress
**Endpoint**: `PUT /goals/{goal_id}/progress`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "progress_percentage": 75.0,
  "status": "in_progress"
}
```

### 12.6 Update Checkpoint Status
**Endpoint**: `PUT /goals/checkpoints/{checkpoint_id}`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "is_completed": true
}
```

### 12.7 Get Performance Reports
**Endpoint**: `GET /performance/reports`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `employee_id` (optional)
- `report_type` (optional): quarterly, annual
- `start_date`, `end_date` (optional)
- `page`, `limit`

**Response**:
```json
{
  "success": true,
  "data": {
    "reports": [
      {
        "id": 1,
        "employee": {
          "id": 1,
          "name": "John Doe"
        },
        "report_period_start": "2024-01-01",
        "report_period_end": "2024-03-31",
        "report_type": "quarterly",
        "overall_rating": 4.5,
        "goals_completion_rate": 85.0,
        "attendance_rate": 95.0,
        "training_completion_rate": 80.0,
        "created_by": {
          "name": "Manager Name"
        }
      }
    ],
    "pagination": {}
  }
}
```

### 12.8 Get Performance Analytics
**Endpoint**: `GET /performance/analytics`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `employee_id` (optional)
- `start_date`, `end_date` (optional)

**Response**:
```json
{
  "success": true,
  "data": {
    "employee_id": "EMP001",
    "period": {
      "start": "2024-01-01",
      "end": "2024-11-11"
    },
    "modules_completed": {
      "total": 25,
      "monthly_breakdown": [
        { "month": "2024-01", "count": 3 },
        { "month": "2024-02", "count": 5 }
      ]
    },
    "goals": {
      "total": 10,
      "completed": 7,
      "in_progress": 2,
      "not_started": 1
    },
    "attendance_rate": 95.5,
    "average_rating": 4.3
  }
}
```

---

## 13. Skill Development APIs

### 13.1 Get Skill Development Modules
**Endpoint**: `GET /skills/modules`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `employee_id` (optional)
- `category` (optional)
- `status` (optional): Filter by completion status
- `page`, `limit`

**Response**:
```json
{
  "success": true,
  "data": {
    "modules": [
      {
        "id": 1,
        "module_name": "Python Programming Advanced",
        "description": "Advanced Python concepts and best practices",
        "category": "Programming",
        "skill_areas": ["Python", "OOP", "Design Patterns"],
        "total_modules": 10,
        "completed_modules": 6,
        "progress_percentage": 60.0,
        "enrolled_date": "2024-09-01",
        "target_completion_date": "2024-12-31",
        "is_certified": false
      }
    ],
    "pagination": {}
  }
}
```

### 13.2 Get Module by ID
**Endpoint**: `GET /skills/modules/{module_id}`

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "employee": {
      "id": 1,
      "name": "John Doe"
    },
    "module_name": "Python Programming Advanced",
    "description": "Advanced Python concepts including OOP, design patterns, and best practices",
    "category": "Programming",
    "skill_areas": ["Python", "OOP", "Design Patterns"],
    "total_modules": 10,
    "completed_modules": 6,
    "progress_percentage": 60.0,
    "enrolled_date": "2024-09-01",
    "target_completion_date": "2024-12-31",
    "completion_date": null,
    "certificate_path": null,
    "is_certified": false
  }
}
```

### 13.3 Enroll in Module
**Endpoint**: `POST /skills/modules`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "module_name": "Python Programming Advanced",
  "description": "Advanced Python concepts",
  "category": "Programming",
  "skill_areas": ["Python", "OOP"],
  "total_modules": 10,
  "target_completion_date": "2024-12-31"
}
```

### 13.4 Update Module Progress
**Endpoint**: `PUT /skills/modules/{module_id}/progress`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "completed_modules": 7,
  "progress_percentage": 70.0
}
```

### 13.5 Mark Module as Completed
**Endpoint**: `PUT /skills/modules/{module_id}/complete`

**Headers**: `Authorization: Bearer <token>`

**Request Body** (multipart/form-data):
```json
{
  "certificate": "<file>"
}
```

### 13.6 Get Skill Statistics
**Endpoint**: `GET /skills/statistics`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `employee_id` (optional)

**Response**:
```json
{
  "success": true,
  "data": {
    "total_modules": 15,
    "completed_modules": 8,
    "in_progress_modules": 5,
    "not_started_modules": 2,
    "certifications_earned": 6,
    "completion_rate": 53.33,
    "categories": [
      {
        "name": "Programming",
        "total": 8,
        "completed": 5
      }
    ]
  }
}
```

---

## 14. Feedback APIs

### 14.1 Get Feedback
**Endpoint**: `GET /feedback`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `employee_id` (optional): For managers/HR
- `given_by` (optional): Filter by who gave feedback
- `start_date`, `end_date` (optional)
- `page`, `limit`

**Access**: Employee (received feedback), Manager (team), HR (all)

**Response**:
```json
{
  "success": true,
  "data": {
    "feedbacks": [
      {
        "id": 1,
        "employee": {
          "id": 1,
          "name": "John Doe"
        },
        "subject": "Great work on Q3 project",
        "description": "Excellent performance and team collaboration",
        "given_by": {
          "id": 5,
          "name": "Jane Manager"
        },
        "given_on": "2024-10-15T10:00:00Z"
      }
    ],
    "pagination": {}
  }
}
```

### 14.2 Get Feedback by ID
**Endpoint**: `GET /feedback/{feedback_id}`

**Headers**: `Authorization: Bearer <token>`

### 14.3 Create Feedback (Manager/HR)
**Endpoint**: `POST /feedback`

**Headers**: `Authorization: Bearer <token>`

**Access**: Manager (for team), HR (all)

**Request Body**:
```json
{
  "employee_id": 1,
  "subject": "Great work on Q3 project",
  "description": "Excellent performance and team collaboration. Key achievements include..."
}
```

### 14.4 Update Feedback
**Endpoint**: `PUT /feedback/{feedback_id}`

**Headers**: `Authorization: Bearer <token>`

### 14.5 Delete Feedback
**Endpoint**: `DELETE /feedback/{feedback_id}`

**Headers**: `Authorization: Bearer <token>`

---

## 15. Team Management APIs

### 15.1 Get Team Requests (Manager)
**Endpoint**: `GET /team/requests`

**Headers**: `Authorization: Bearer <token>`

**Access**: Manager only

**Query Parameters**:
- `status` (optional): pending, approved, rejected
- `request_type` (optional): wfh, leave, other
- `page`, `limit`

**Response**:
```json
{
  "success": true,
  "data": {
    "requests": [
      {
        "id": 1,
        "employee": {
          "id": 1,
          "name": "John Doe",
          "employee_id": "EMP001"
        },
        "request_type": "wfh",
        "subject": "WFH Request",
        "description": "Need to work from home due to personal reasons",
        "date": "2024-11-15",
        "status": "pending",
        "submitted_date": "2024-11-10T10:00:00Z"
      }
    ],
    "pagination": {}
  }
}
```

### 15.2 Get Team Members
**Endpoint**: `GET /team/members`

**Headers**: `Authorization: Bearer <token>`

**Access**: Manager only

**Response**:
```json
{
  "success": true,
  "data": {
    "team_name": "Backend Team",
    "manager": {
      "id": 5,
      "name": "Jane Manager"
    },
    "members": [
      {
        "id": 1,
        "employee_id": "EMP001",
        "name": "John Doe",
        "email": "john@example.com",
        "job_role": "Software Engineer",
        "department": "Engineering",
        "hire_date": "2023-01-15",
        "profile_image_path": "/uploads/profiles/user_1.jpg"
      }
    ],
    "total_members": 10
  }
}
```

### 15.3 Get Team Statistics (Manager)
**Endpoint**: `GET /team/statistics`

**Headers**: `Authorization: Bearer <token>`

**Access**: Manager only

**Response**:
```json
{
  "success": true,
  "data": {
    "team_name": "Backend Team",
    "total_members": 10,
    "attendance": {
      "today_present": 8,
      "today_wfh": 1,
      "today_leave": 1,
      "average_attendance_rate": 92.5
    },
    "performance": {
      "average_rating": 4.2,
      "goals_completion_rate": 78.0,
      "training_hours": 1300,
      "performance_score": 3.9
    },
    "leaves": {
      "pending_requests": 3,
      "approved_this_month": 8
    }
  }
}
```

### 15.4 Approve/Reject Team Request (Manager)
**Endpoint**: `PUT /team/requests/{request_id}/status`

**Headers**: `Authorization: Bearer <token>`

**Access**: Manager only

**Request Body**:
```json
{
  "status": "approved",
  "rejection_reason": "Optional if rejected"
}
```

---

## 16. Resume Screening APIs

### 16.1 Screen Resume (HR Only)
**Endpoint**: `POST /resume/screen`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

**Request Body** (multipart/form-data):
```json
{
  "application_id": 1,
  "resume": "<file>",
  "job_description": "Job description text or path"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "screening_result_id": 1,
    "overall_score": 85.5,
    "technical_skills_score": 90.0,
    "experience_score": 82.0,
    "education_score": 85.0,
    "matched_keywords": ["Python", "Flask", "React", "PostgreSQL"],
    "missing_keywords": ["Docker", "Kubernetes"],
    "strengths": "Strong technical background with relevant experience",
    "weaknesses": "Limited DevOps experience",
    "recommendation": "recommend",
    "screened_date": "2024-11-11T10:00:00Z"
  },
  "message": "Resume screened successfully"
}
```

### 16.2 Get Screening Result
**Endpoint**: `GET /resume/screen/{screening_id}`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "application": {
      "id": 1,
      "applicant_name": "John Smith",
      "position": "Software Engineer"
    },
    "overall_score": 85.5,
    "technical_skills_score": 90.0,
    "experience_score": 82.0,
    "education_score": 85.0,
    "matched_keywords": ["Python", "Flask", "React", "PostgreSQL"],
    "missing_keywords": ["Docker", "Kubernetes"],
    "strengths": "Strong technical background with 3+ years experience",
    "weaknesses": "Limited cloud and DevOps experience",
    "recommendation": "recommend",
    "screening_model_version": "1.0",
    "screened_date": "2024-11-11T10:00:00Z"
  }
}
```

### 16.3 Bulk Screen Resumes (HR Only)
**Endpoint**: `POST /resume/screen/bulk`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

**Request Body**:
```json
{
  "job_id": 1,
  "application_ids": [1, 2, 3, 4, 5]
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "total_screened": 5,
    "results": [
      {
        "application_id": 1,
        "screening_result_id": 1,
        "overall_score": 85.5,
        "recommendation": "recommend"
      }
    ]
  },
  "message": "Bulk screening completed"
}
```

---

## 17. Department & Organization APIs

### 17.1 Get All Departments
**Endpoint**: `GET /departments`

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "success": true,
  "data": {
    "departments": [
      {
        "id": 1,
        "name": "Engineering",
        "description": "Software development and engineering",
        "head": {
          "id": 10,
          "name": "Department Head"
        },
        "employee_count": 50,
        "teams_count": 5
      }
    ]
  }
}
```

### 17.2 Get Department Statistics
**Endpoint**: `GET /departments/{department_id}/statistics`

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "success": true,
  "data": {
    "department": "Engineering",
    "total_employees": 50,
    "attendance_rate": 92.5,
    "average_performance_rating": 4.1,
    "modules_completed": 250,
    "training_hours": 5000,
    "teams": [
      {
        "name": "Backend Team",
        "employee_count": 10,
        "manager": "Jane Manager"
      }
    ]
  }
}
```

### 17.3 Get Organization Hierarchy
**Endpoint**: `GET /organization/hierarchy`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `employee_id` (optional): Get hierarchy for specific employee

**Response**:
```json
{
  "success": true,
  "data": {
    "employee": {
      "id": 1,
      "name": "John Doe",
      "job_role": "Software Engineer"
    },
    "manager": {
      "id": 5,
      "name": "Jane Manager",
      "job_role": "Engineering Manager"
    },
    "manager_chain": [
      {
        "id": 5,
        "name": "Jane Manager",
        "job_role": "Engineering Manager",
        "level": 1
      },
      {
        "id": 10,
        "name": "Department Head",
        "job_role": "VP Engineering",
        "level": 2
      }
    ],
    "direct_reports": []
  }
}
```

### 17.4 Get Organization Chart
**Endpoint**: `GET /organization/chart`

**Headers**: `Authorization: Bearer <token>`

**Response**: Tree structure of entire organization

---

## 18. Holiday Management APIs

### 18.1 Get Holidays
**Endpoint**: `GET /holidays`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `year` (optional): Default current year
- `month` (optional)
- `upcoming` (optional): Boolean to get only upcoming holidays

**Response**:
```json
{
  "success": true,
  "data": {
    "holidays": [
      {
        "id": 1,
        "name": "Diwali",
        "description": "Festival of Lights",
        "start_date": "2024-11-01",
        "end_date": "2024-11-01",
        "is_mandatory": true,
        "applies_to_departments": ["all"]
      },
      {
        "id": 2,
        "name": "Christmas",
        "start_date": "2024-12-25",
        "end_date": "2024-12-25",
        "is_mandatory": true
      }
    ]
  }
}
```

### 18.2 Create Holiday (HR Only)
**Endpoint**: `POST /holidays`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

**Request Body**:
```json
{
  "name": "Diwali",
  "description": "Festival of Lights",
  "start_date": "2024-11-01",
  "end_date": "2024-11-01",
  "is_mandatory": true,
  "applies_to_departments": ["all"]
}
```

### 18.3 Update Holiday (HR Only)
**Endpoint**: `PUT /holidays/{holiday_id}`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

### 18.4 Delete Holiday (HR Only)
**Endpoint**: `DELETE /holidays/{holiday_id}`

**Headers**: `Authorization: Bearer <token>`

**Access**: HR only

---

## Additional Endpoints

### File Upload
**Endpoint**: `POST /files/upload`

**Headers**: `Authorization: Bearer <token>`

**Request Body** (multipart/form-data):
```json
{
  "file": "<file>",
  "category": "resume|document|policy|payslip|certificate|profile"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "file_path": "/uploads/resumes/file_name.pdf",
    "file_name": "file_name.pdf",
    "file_size": 102400,
    "mime_type": "application/pdf"
  }
}
```

### File Download
**Endpoint**: `GET /files/download`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `path`: File path to download

**Response**: File stream

---

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Invalid or missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Resource already exists |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error |

---

## Authentication & Authorization

### JWT Token Structure
```json
{
  "user_id": 1,
  "employee_id": "EMP001",
  "role": "employee",
  "exp": 1699999999
}
```

### Role-based Access Control

| Role | Permissions |
|------|-------------|
| **Employee** | View own data, submit applications/requests, manage own goals/skills |
| **Manager** | All employee permissions + manage team members, approve/reject team requests, view team analytics |
| **HR** | All permissions + manage all employees, job listings, applications, policies, payslips, announcements |
| **Admin** | Full system access |

---

## Pagination

All list endpoints support pagination with these query parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)

Pagination response format:
```json
{
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 100,
    "items_per_page": 10,
    "has_next": true,
    "has_previous": false
  }
}
```

---

## Filtering & Sorting

Most GET endpoints support:
- **Filtering**: Use query parameters matching field names
- **Sorting**: `sort_by=field_name&sort_order=asc|desc`
- **Search**: `search=keyword` (searches across relevant fields)

---

## Rate Limiting

- **General APIs**: 100 requests per minute per user
- **File Upload**: 10 requests per minute per user
- **Resume Screening**: 20 requests per minute per HR user

---

## WebSocket Events (Optional for Real-time Features)

### Connection
```
ws://localhost:5000/ws?token=<jwt_token>
```

### Events
- `attendance:punch` - Real-time punch in/out notifications
- `announcement:new` - New announcement published
- `request:status` - Request status updated
- `notification:new` - General notifications

---

## Development Guidelines

1. **API Versioning**: All endpoints are prefixed with `/api/v1`
2. **Date Format**: ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
3. **File Size Limits**: 
   - Resumes: 5MB
   - Documents: 10MB
   - Profile images: 2MB
4. **Supported File Types**:
   - Documents: PDF
   - Images: JPEG, PNG
5. **Database**: Use transactions for multi-step operations
6. **Logging**: Log all API requests and errors
7. **Security**: 
   - Use HTTPS in production
   - Implement CORS properly
   - Sanitize all inputs
   - Use prepared statements for SQL

---

## Next Steps for Backend Development

1. **Setup Project Structure**
   - Initialize Flask/FastAPI project
   - Setup virtual environment
   - Install dependencies
   - Configure database connection

2. **Implement Core Features**
   - Authentication & JWT
   - User management
   - Role-based access control
   - File upload/download

3. **Build API Endpoints** (Priority Order)
   - Authentication APIs
   - Dashboard APIs (all three roles)
   - Employee Management
   - Job Listings & Applications
   - Attendance & Leave Management
   - Remaining endpoints

4. **Integrate GenAI Features**
   - Resume screening model
   - Job description generation
   - Performance insights

5. **Testing & Documentation**
   - Unit tests
   - Integration tests
   - API documentation (Swagger/OpenAPI)
   - Postman collection

---

## Technology Recommendations

```python
# requirements.txt
flask==3.0.0
flask-sqlalchemy==3.1.1
flask-jwt-extended==4.6.0
flask-cors==4.0.0
flask-migrate==4.0.5
python-dotenv==1.0.0
werkzeug==3.0.1
psycopg2-binary==2.9.9  # PostgreSQL
pymysql==1.1.0  # MySQL alternative
pandas==2.1.3
numpy==1.26.2
python-multipart==0.0.6
Pillow==10.1.0
PyPDF2==3.0.1
boto3==1.29.7  # AWS S3 for file storage
redis==5.0.1  # Caching
celery==5.3.4  # Background tasks
gunicorn==21.2.0  # Production server
pytest==7.4.3
```

---

**Document Version**: 1.0  
**Last Updated**: November 11, 2024  
**Prepared By**: Backend Development Team

