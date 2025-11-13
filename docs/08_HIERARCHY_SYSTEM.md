# Organizational Hierarchy System

## Overview
The User model now includes a comprehensive hierarchy system to represent organizational structure and positions within the company.

## New Fields in User Model

### 1. `job_level` (String, max 50 chars)
Human-readable job level designation:
- `"Junior"` - Entry-level employees
- `"Mid-level"` - Mid-career professionals
- `"Senior"` - Senior professionals
- `"Lead"` - Team leads
- `"Principal"` - Principal/Staff level
- `"Manager"` - People managers
- `"Director"` - Department directors
- `"VP"` - Vice Presidents
- `"C-Level"` - C-suite executives

### 2. `hierarchy_level` (Integer, default=5)
Numerical hierarchy position for programmatic ordering and filtering:

```
Level 1 = CEO / Top Management
Level 2 = VP / Director
Level 3 = Manager
Level 4 = Team Lead
Level 5 = Senior
Level 6 = Mid-level
Level 7 = Junior
```

**Lower number = Higher in hierarchy**

## Use Cases

### 1. **Organizational Charts**
```python
# Get users ordered by hierarchy
users = session.query(User).order_by(User.hierarchy_level).all()
```

### 2. **Approval Workflows**
```python
# Only managers (level <= 3) can approve
if user.hierarchy_level <= 3:
    # Allow approval
```

### 3. **Access Control**
```python
# Restrict data access based on level
if user.hierarchy_level <= 2:
    # VP+ can see all reports
```

### 4. **Salary Bands**
```python
# Define salary ranges per level
salary_bands = {
    7: (40000, 60000),   # Junior
    6: (60000, 80000),   # Mid
    5: (80000, 100000),  # Senior
    4: (95000, 115000),  # Lead
    3: (110000, 150000), # Manager
}
```

### 5. **Reporting Structure**
```python
# Get all subordinates (hierarchy_level > manager's level)
subordinates = session.query(User).filter(
    User.hierarchy_level > manager.hierarchy_level,
    User.department_id == manager.department_id
).all()
```

### 6. **Promotion Tracking**
```python
# Track promotions by comparing hierarchy_level changes
# Level 6 -> Level 5 = Promoted from Mid to Senior
```

## Current Data Example

| Level | Job Level   | Employee ID | Name               | Job Role                    |
|-------|-------------|-------------|--------------------|-----------------------------|
| 3     | Manager     | EMP001      | Sarah Johnson      | HR Manager                  |
| 3     | Manager     | EMP002      | Michael Chen       | Engineering Manager         |
| 4     | Lead        | EMP003      | Emily Rodriguez    | Frontend Lead               |
| 5     | Senior      | EMP004      | John Doe           | Senior Software Engineer    |
| 5     | Senior      | EMP007      | Maria Garcia       | UI/UX Designer              |
| 6     | Mid-level   | EMP005      | Alice Williams     | Software Engineer           |
| 6     | Mid-level   | EMP006      | Robert Kumar       | Frontend Developer          |
| 6     | Mid-level   | EMP008      | David Lee          | HR Specialist               |
| 6     | Mid-level   | EMP009      | Jessica Brown      | Financial Analyst           |
| 7     | Junior      | EMP010      | James Wilson       | Sales Executive             |

## API Endpoints Examples

### Get Users by Hierarchy Level
```http
GET /api/users?hierarchy_level=3
# Returns all managers
```

### Get Team Hierarchy
```http
GET /api/teams/{team_id}/hierarchy
# Returns team members ordered by hierarchy
```

### Check Approval Permission
```http
POST /api/requests/{request_id}/approve
# Backend checks if approver.hierarchy_level <= request.employee.hierarchy_level
```

## Frontend Integration

### Display Org Chart
```typescript
// Sort by hierarchy for org chart display
const sortedEmployees = employees.sort((a, b) => 
  a.hierarchy_level - b.hierarchy_level
);
```

### Role-Based UI
```typescript
// Show different dashboard based on level
if (user.hierarchy_level <= 3) {
  return <ManagerDashboard />;
} else if (user.hierarchy_level <= 5) {
  return <SeniorEmployeeDashboard />;
} else {
  return <EmployeeDashboard />;
}
```

## Database Query Utilities

### View Current Hierarchy
```bash
cd backend
python show_hierarchy.py
```

### Query Examples
```python
# Get all managers and above
managers = session.query(User).filter(User.hierarchy_level <= 3).all()

# Get immediate supervisor candidates (one level up)
supervisors = session.query(User).filter(
    User.hierarchy_level == employee.hierarchy_level - 1
).all()

# Get peers (same level, same department)
peers = session.query(User).filter(
    User.hierarchy_level == employee.hierarchy_level,
    User.department_id == employee.department_id,
    User.id != employee.id
).all()
```

## Benefits

1. **Clear Reporting Structure**: Easy to visualize who reports to whom
2. **Access Control**: Implement level-based permissions
3. **Workflow Automation**: Route approvals based on hierarchy
4. **Analytics**: Analyze organization by levels
5. **Career Progression**: Track promotions and level changes
6. **Salary Management**: Associate salary bands with levels
7. **Org Chart Generation**: Automatic org chart creation
8. **Search & Filter**: Find employees by level easily

## Notes

- Both fields (`job_level` and `hierarchy_level`) work together
- `job_level` is for display/human reading
- `hierarchy_level` is for programmatic logic
- Lower `hierarchy_level` number = Higher in organization
- Update both fields when promoting employees
- Consider adding audit trail for level changes

