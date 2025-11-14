# 📋 Remaining APIs Analysis for HRMS Backend

**Analysis Date**: November 14, 2025  
**Current Completion**: 84% (119 of ~154 APIs)  
**Based on**: Frontend requirements, Page-wise data requirements.txt, Milestone documents

---

## ✅ Currently Implemented (119 APIs)

### Core Modules (14 modules - 106 endpoints)
1. **Authentication** (6 APIs) ✅
2. **Dashboards** (6 APIs) ✅
3. **Profile Management** (12 APIs) ✅
4. **Attendance Management** (9 APIs) ✅
5. **Job Listings** (7 APIs) ✅
6. **Applications** (9 APIs) ✅
7. **Announcements** (6 APIs) ✅
8. **Policies** (9 APIs) ✅
9. **Feedback** (9 APIs) ✅
10. **Payslips** (11 APIs) ✅
11. **Holidays** (7 APIs) ✅ **NEW**
12. **Departments** (6 APIs) ✅ **NEW**
13. **Organization/Hierarchy** (9 APIs) ✅ **NEW**

### AI Features (13 endpoints) ✅
14. **Policy RAG** (4 APIs) ✅
15. **Resume Screener** (5 APIs) ✅
16. **Job Description Generator** (4 APIs) ✅

---

## ❌ NOT YET IMPLEMENTED (~35 APIs)

### Priority 1: Goals Management (8 APIs) ⭐⭐⭐

**Frontend Pages**: 
- `Employee/GoalTracker.tsx`
- `Employee/GoalTrackerDetail.tsx`
- Manager Dashboard (team goals)
- Employee Dashboard (learning goals pie chart)

**Required Data**:
- Goal title, description, deadline
- Checklist items (checkpoints)
- Completion status
- Progress tracking

**API Endpoints Needed**:

```http
GET    /api/v1/goals                      # List all goals (filtered by user/team)
GET    /api/v1/goals/me                   # Get my goals (employee)
GET    /api/v1/goals/team                 # Get team goals (manager)
GET    /api/v1/goals/{id}                 # Get goal details
POST   /api/v1/goals                      # Create goal (manager for employee)
PUT    /api/v1/goals/{id}                 # Update goal
DELETE /api/v1/goals/{id}                 # Delete goal
PATCH  /api/v1/goals/{id}/complete        # Mark goal as complete
```

**Checkpoint Management** (Sub-resource):
```http
GET    /api/v1/goals/{id}/checkpoints     # Get checkpoints for a goal
POST   /api/v1/goals/{id}/checkpoints     # Add checkpoint
PUT    /api/v1/goals/checkpoints/{cp_id}  # Update checkpoint
DELETE /api/v1/goals/checkpoints/{cp_id}  # Delete checkpoint
PATCH  /api/v1/goals/checkpoints/{cp_id}/complete  # Mark checkpoint complete
```

**Total**: 13 APIs (8 main + 5 checkpoints)

**Database Model**: Already exists in `models.py`
```python
class Goal(Base):
    id, user_id, title, description
    start_date, deadline, status
    priority, progress_percentage
    created_by, assigned_by
    
class GoalCheckpoint(Base):
    id, goal_id, title, description
    is_completed, completed_at
```

---

### Priority 2: Skills/Module Management (8 APIs) ⭐⭐⭐

**Frontend Pages**:
- `Employee/SkillDevelopment.tsx`
- `Employee/SkillDevelopmentDetail.tsx`
- Employee Dashboard (modules completed chart)
- HR Dashboard (department-wise modules)

**Required Data**:
- Module name, short description
- Status (completed/pending/not started)
- Module link (external course)
- Progress tracking
- Enrollment status

**API Endpoints Needed**:

```http
GET    /api/v1/skills/modules             # List all skill modules
GET    /api/v1/skills/modules/{id}        # Get module details
POST   /api/v1/skills/modules             # Create module (HR only)
PUT    /api/v1/skills/modules/{id}        # Update module (HR only)
DELETE /api/v1/skills/modules/{id}        # Delete module (HR only)

GET    /api/v1/skills/my-enrollments      # Get my enrolled modules
POST   /api/v1/skills/enroll/{id}         # Enroll in a module
PUT    /api/v1/skills/progress/{id}       # Update progress
PATCH  /api/v1/skills/{id}/complete       # Mark module as complete
GET    /api/v1/skills/stats               # Get statistics (for dashboards)
```

**Total**: 10 APIs

**Database Model**: Already exists
```python
class SkillModule(Base):
    id, name, description, category
    module_link, duration_hours
    difficulty_level, skill_areas
    is_active
    
class SkillModuleEnrollment(Base):
    id, employee_id, module_id
    status, progress_percentage
    enrolled_date, started_date, completed_at
```

---

### Priority 3: Leave Management (6-8 APIs) ⭐⭐⭐⭐

**Frontend Pages**:
- Attendance page (shows leave balances)
- Employee Dashboard (WFH left, Leaves left)
- Manager Dashboard (team leave requests)

**Required Data**:
- Leave type (casual, sick, annual, WFH)
- Leave balances per employee
- Leave requests (pending/approved/rejected)
- Date range, days count
- Approval workflow

**API Endpoints Needed**:

```http
GET    /api/v1/leaves/balance             # Get my leave balances
GET    /api/v1/leaves/balance/{user_id}   # Get user leave balance (HR/Manager)
GET    /api/v1/leaves                     # List leave requests
GET    /api/v1/leaves/me                  # My leave requests
GET    /api/v1/leaves/team                # Team leave requests (Manager)
GET    /api/v1/leaves/{id}                # Get leave details
POST   /api/v1/leaves                     # Apply for leave
PUT    /api/v1/leaves/{id}/status         # Approve/Reject (Manager/HR)
DELETE /api/v1/leaves/{id}                # Cancel leave request
```

**Total**: 9 APIs

**Database Model**: Already exists
```python
class LeaveRequest(Base):
    id, user_id, leave_type
    start_date, end_date, days_count
    reason, status
    applied_at, approved_by, approved_at
    rejection_reason
```

**Note**: Leave balances currently stored in User model. May need dedicated balance tracking.

---

### Priority 4: Team Requests/Approvals (4-5 APIs) ⭐⭐⭐

**Frontend Pages**:
- `Manager/TeamRequests.tsx`

**Required Data**:
- Employee name
- Request type (leave, career development, etc.)
- Status (pending approval/rejected/approved)
- Date, subject, description
- Approval/rejection actions

**API Endpoints Needed**:

```http
GET    /api/v1/requests                   # List requests (filtered)
GET    /api/v1/requests/team              # Team requests (Manager)
GET    /api/v1/requests/me                # My requests (Employee)
GET    /api/v1/requests/{id}              # Get request details
POST   /api/v1/requests                   # Submit request (Employee)
PUT    /api/v1/requests/{id}/status       # Approve/Reject (Manager)
DELETE /api/v1/requests/{id}              # Delete request
```

**Total**: 7 APIs

**Database Model**: Already exists
```python
class Request(Base):
    id, employee_id, request_type
    subject, description, request_date
    status, approved_by, approved_date
    rejection_reason, submitted_date
```

---

### Priority 5: Performance Reports (3-4 APIs) ⭐⭐

**Frontend Pages**:
- `Employee/PerformanceReport.tsx`
- `Common/PerformanceReport.tsx`
- HR/Manager dashboards

**Required Data**:
- Modules completed month-wise (graph)
- Total modules completed
- Performance metrics over time
- Goal achievement rates
- Attendance patterns

**API Endpoints Needed**:

```http
GET    /api/v1/performance/me             # My performance report
GET    /api/v1/performance/{user_id}      # User performance (HR/Manager)
GET    /api/v1/performance/team           # Team performance (Manager)
GET    /api/v1/performance/department     # Department performance (HR)
```

**Total**: 4 APIs

**Database Model**: Already exists
```python
class PerformanceReport(Base):
    id, user_id, review_period
    overall_rating, strengths
    areas_for_improvement, goals_achieved
    reviewed_by, reviewed_at
```

---

### Priority 6: Employees Management (5-6 APIs) ⭐⭐

**Frontend Pages**:
- `HR/EmployeesList.tsx`
- `HR/AddEmployeeForm.tsx`

**Required Data**:
- Employee list with department filter
- Employee details (name, email, phone, department, team, manager)
- Documents (Aadhar, PAN)
- Add/Edit/View employee
- Deactivate employee

**API Endpoints Needed**:

```http
GET    /api/v1/employees                  # List all employees (HR)
GET    /api/v1/employees/{id}             # Get employee details (HR)
POST   /api/v1/employees                  # Add new employee (HR) - May already exist as auth/register
PUT    /api/v1/employees/{id}             # Update employee (HR)
DELETE /api/v1/employees/{id}             # Deactivate employee (HR)
GET    /api/v1/employees/stats            # Employee statistics (HR)
```

**Total**: 6 APIs

**Note**: Some overlap with Profile APIs. May only need HR-specific views and bulk operations.

---


## 📊 Summary of Remaining Work

### By Module

| Module | APIs Needed | Priority | Complexity | Estimated Time |
|--------|-------------|----------|------------|----------------|
| **Goals** | 13 | ⭐⭐⭐ High | Medium | 2-3 days |
| **Skills** | 10 | ⭐⭐⭐ High | Medium | 2-3 days |
| **Leave Management** | 9 | ⭐⭐⭐⭐ Very High | Medium | 2-3 days |
| **Team Requests** | 7 | ⭐⭐⭐ High | Low-Medium | 1-2 days |
| **Performance Reports** | 4 | ⭐⭐ Medium | Medium | 1-2 days |
| **Employees Management** | 6 | ⭐⭐ Medium | Low | 1 day |
| ~~**Org Hierarchy**~~ | ~~3~~ | ✅ Complete | - | - |
| ~~**Holidays**~~ | ~~5~~ | ✅ Complete | - | - |
| ~~**Departments**~~ | ~~6~~ | ✅ Complete | - | - |

**Total Remaining**: ~35 endpoints  
**Recently Completed**: Holidays (7), Departments (6), Organization/Hierarchy (9) = 22 APIs

---

## 🎯 Recommended Implementation Order

### Week 1: Core Employee Features
1. **Goals APIs** (8 main APIs + checkpoints)
   - Most requested by employees
   - Ties into dashboard visualizations
   - Medium complexity

2. **Skills APIs** (10 APIs)
   - Employee learning and development
   - HR management of modules
   - Enrollment tracking

### Week 2: Operational Features
3. **Leave Management APIs** (9 APIs)
   - Critical for attendance system completion
   - Approval workflows
   - Balance tracking

4. **Team Requests APIs** (7 APIs)
   - Manager approval workflows
   - General request management

### Week 3: Analytics & Admin
5. **Performance Reports APIs** (4 APIs)
   - Aggregated data from goals/skills/attendance
   - Analytics for dashboards

6. **Employees Management APIs** (6 APIs)
   - HR administrative functions
   - May leverage existing profile APIs

### ✅ Completed (No longer needed)
- ~~Holidays APIs (7 APIs)~~ ✅ Done
- ~~Departments APIs (6 APIs)~~ ✅ Done
- ~~Organization Hierarchy APIs (9 APIs)~~ ✅ Done

---

## 📝 Implementation Notes

### Database Models
✅ **All database models already exist** in `models.py`:
- Goal, GoalCheckpoint
- SkillModule, SkillModuleEnrollment
- LeaveRequest
- Request
- PerformanceReport
- ~~Holiday~~ ✅ Implemented
- ~~Department~~ ✅ Implemented
- ~~User (with hierarchy relationships)~~ ✅ Implemented

### Patterns to Follow
All remaining APIs should follow the established pattern:
1. **Schemas**: Create in `backend/schemas/{module}_schemas.py`
2. **Services**: Business logic in `backend/services/{module}_service.py`
3. **Routes**: API endpoints in `backend/routes/{module}.py`
4. **Frontend**: Service layer in `frontend/src/services/{module}Service.ts`

### Access Control
- **Goals**: Manager can create for employees, employees view own
- **Skills**: HR creates modules, employees enroll
- **Leaves**: Employees apply, managers/HR approve
- **Requests**: Employees submit, managers approve
- **Performance**: HR/Managers create, employees view own
- **Employees**: HR only (full CRUD)
- ~~**Holidays**: HR manages, all view~~ ✅ Implemented
- ~~**Departments**: HR manages, all view~~ ✅ Implemented
- ~~**Organization**: All users view hierarchy~~ ✅ Implemented

---

## 🚀 Quick Start for Next Developer

### To Implement Goals API:

1. **Create Schema** (`backend/schemas/goal_schemas.py`):
   - GoalCreate, GoalUpdate, GoalResponse
   - CheckpointCreate, CheckpointUpdate, CheckpointResponse

2. **Create Service** (`backend/services/goal_service.py`):
   - `create_goal()`, `get_goals()`, `update_goal()`
   - `add_checkpoint()`, `complete_checkpoint()`

3. **Create Routes** (`backend/routes/goals.py`):
   - 8 main endpoints + 5 checkpoint endpoints
   - Role-based access control

4. **Register in main.py**:
   ```python
   from routes.goals import router as goals_router
   app.include_router(goals_router, prefix="/api/v1")
   ```

5. **Create Frontend Service** (`frontend/src/services/goalService.ts`):
   - TypeScript types and API calls

6. **Update Frontend Pages**:
   - Replace hardcoded data with API calls
   - Add loading states and error handling

---

## ✅ Checklist for Each New API Module

- [ ] Database model exists (verify in `models.py`)
- [ ] Create Pydantic schemas (request/response)
- [ ] Implement service layer (business logic)
- [ ] Create API routes with documentation
- [ ] Add role-based access control
- [ ] Register routes in `main.py`
- [ ] Test with Swagger UI
- [ ] Create TypeScript service
- [ ] Update frontend pages
- [ ] Test end-to-end
- [ ] Update documentation

---

## 🎉 Recent Updates (November 14, 2025)

### ✅ Newly Implemented (22 APIs)

**Holidays API** (7 endpoints):
- Complete CRUD operations
- Upcoming holidays for dashboards
- Statistics and filtering
- Files: `holiday_schemas.py`, `holiday_service.py`, `holidays.py`, `holidayService.ts`

**Departments API** (6 endpoints):
- Department management (HR)
- Employee and team counts
- Department hierarchy
- Files: `department_schemas.py`, `department_service.py`, `departments.py`, `departmentService.ts`

**Organization/Hierarchy API** (9 endpoints):
- Full org hierarchy
- Manager chain (employee → CEO)
- Reporting structure
- Org chart as tree
- Files: `organization_schemas.py`, `organization_service.py`, `organization.py`, `organizationService.ts`

**Documentation**: See `HIERARCHY_DEPARTMENTS_HOLIDAYS_IMPLEMENTATION_COMPLETE.md` for full details.

---

**Last Updated**: November 14, 2025 (Updated after Holidays/Departments/Org implementation)  
**Current Status**: 84% Complete (119/154 APIs)  
**Next Priority**: Goals APIs (13 endpoints) - High Priority

