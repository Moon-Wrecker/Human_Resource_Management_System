# Dashboard APIs - Quick Reference Guide

**Last Updated**: November 13, 2025  
**Status**: ✅ All APIs Production-Ready

---

## 🎯 **Quick Overview**

| Dashboard | API Endpoint | Role Required | Coverage | Status |
|-----------|-------------|---------------|----------|--------|
| **Employee** | `GET /api/v1/dashboard/employee` | Employee, Manager | 100% | ✅ Ready |
| **Manager** | `GET /api/v1/dashboard/manager` | Manager | 100% | ✅ Ready |
| **HR** | `GET /api/v1/dashboard/hr` | HR, Admin | 287% | ✅✅ Ready |

---

## 📋 **1. Employee Dashboard**

### **API Call**

```typescript
// Frontend Request
const response = await api.get('/api/v1/dashboard/employee');
```

### **Response Structure**

```typescript
{
  employee_name: "John Doe",
  
  leave_balance: {
    casual_leave: 8,      // 👉 Casual leaves left
    sick_leave: 10,       // 👉 Sick leaves left
    annual_leave: 12,     // 👉 Annual leaves left
    wfh_balance: 16       // 👉 WFH days left
  },
  
  today_attendance: {
    date: "2025-11-13",
    check_in_time: "09:04:00",   // 👉 Punch in time
    check_out_time: null,         // 👉 Punch out time (null if not checked out)
    status: "present",            // 👉 present | absent | wfh | leave
    hours_worked: null            // 👉 Calculated after checkout
  },
  
  upcoming_holidays: [
    {
      id: 1,
      name: "Christmas",
      description: "Christmas Day",
      start_date: "2025-12-25",
      end_date: "2025-12-25",
      is_mandatory: true,
      holiday_type: "festival"
    }
  ],
  
  learning_goals: {
    total_goals: 5,           // 👉 Total goals
    completed_goals: 4,       // 👉 Completed (for pie chart)
    pending_goals: 1,         // 👉 Pending (for pie chart)
    completion_percentage: 80.0
  },
  
  learner_rank: 3   // 👉 Employee's rank among all employees
}
```

### **Frontend Display** ✅ **IMPLEMENTED**

```typescript
// ✅ Display each leave type in separate cards (no calculation needed)
<Card title="Casual Leave">{data.leave_balance.casual_leave}</Card>
<Card title="Sick Leave">{data.leave_balance.sick_leave}</Card>
<Card title="Annual Leave">{data.leave_balance.annual_leave}</Card>
<Card title="WFH Left">{data.leave_balance.wfh_balance}</Card>

// 2. Punch In/Out Display
const punchIn = data.today_attendance?.check_in_time || 'N/A';
const punchOut = data.today_attendance?.check_out_time || 'Not checked out';

// 3. Pie Chart Data
const pieData = {
  labels: ['Completed', 'Pending'],
  data: [data.learning_goals.completed_goals, data.learning_goals.pending_goals]
};
```

---

## 📋 **2. Manager Dashboard**

### **API Call**

```typescript
// Frontend Request
const response = await api.get('/api/v1/dashboard/manager');
```

### **Response Structure**

```typescript
{
  personal_info: {
    casual_leave: 8,
    sick_leave: 10,
    annual_leave: 12,
    wfh_balance: 16
  },
  
  today_attendance: {
    date: "2025-11-13",
    check_in_time: "09:00:00",
    check_out_time: null,
    status: "present",
    hours_worked: null
  },
  
  upcoming_holidays: [ /* Same as Employee */ ],
  
  team_stats: {
    total_members: 8,                    // 👉 Team size
    avg_attendance_percentage: 87.5,     // 👉 Team avg attendance
    avg_modules_completed: 12.3          // 👉 Team avg modules
  },
  
  team_goals: {
    total_goals: 40,                     // 👉 All team goals
    completed_goals: 30,                 // 👉 Team completed
    pending_goals: 10,                   // 👉 Team pending
    completion_percentage: 75.0
  },
  
  team_attendance: [
    {
      employee_id: 5,
      employee_name: "Alice Smith",
      present_percentage: 90.0,          // 👉 Member's attendance %
      absent_percentage: 10.0
    },
    // ... more team members
  ],
  
  team_modules_leaderboard: [
    {
      employee_id: 8,
      employee_name: "Bob Johnson",
      modules_completed: 25              // 👉 Modules for leaderboard
    },
    // ... more team members (sorted by modules)
  ],
  
  learner_rank: 2   // 👉 Manager's personal rank
}
```

### **Frontend Display** ✅ **IMPLEMENTED**

```typescript
// 1. Leave Balance Cards - Display Separately
<Card title="Casual Leave">{data.personal_info.casual_leave}</Card>
<Card title="Sick Leave">{data.personal_info.sick_leave}</Card>
<Card title="Annual Leave">{data.personal_info.annual_leave}</Card>
<Card title="WFH Left">{data.personal_info.wfh_balance}</Card>

// 2. Team Stats Cards
<Card title="Team Size">{data.team_stats.total_members}</Card>
<Card title="Avg Attendance">{data.team_stats.avg_attendance_percentage}%</Card>

// 3. Team Attendance Table
data.team_attendance.map(member => (
  <TableRow>
    <td>{member.employee_name}</td>
    <td>{member.present_percentage}%</td>
  </TableRow>
))

// 4. Modules Leaderboard
data.team_modules_leaderboard.map((member, index) => (
  <LeaderboardRow rank={index + 1}>
    {member.employee_name} - {member.modules_completed} modules
  </LeaderboardRow>
))
```

---

## 📋 **3. HR Dashboard**

### **API Call**

```typescript
// Frontend Request
const response = await api.get('/api/v1/dashboard/hr');
```

### **Response Structure**

```typescript
{
  departments: [
    {
      department_id: 1,
      department_name: "Engineering",
      employee_count: 20               // 👉 Employees in dept
    },
    // ... more departments
  ],
  
  department_attendance: [
    {
      department_id: 1,
      department_name: "Engineering",
      present_percentage: 85.5,        // 👉 Dept attendance %
      absent_percentage: 14.5
    },
    // ... more departments
  ],
  
  department_modules: [
    {
      department_id: 1,
      department_name: "Engineering",
      modules_completed: 45            // 👉 Total modules by dept
    },
    // ... more departments
  ],
  
  active_applications: [
    {
      application_id: 1,
      applicant_name: "John Doe",      // 👉 Applicant name
      applied_role: "Software Engineer", // 👉 Applied role
      applied_date: "2025-11-10T10:00:00",
      status: "pending",               // 👉 pending | reviewed | shortlisted
      source: "referral"               // 👉 referral | self-applied
    },
    // ... more applications
  ],
  
  total_employees: 57,                 // 👉 Total company employees
  total_departments: 5,                // 👉 Total departments
  total_active_applications: 10        // 👉 Total active applications
}
```

### **Frontend Charts**

```typescript
// 1. Department Employee Count Chart
const deptChart = {
  labels: data.departments.map(d => d.department_name),
  data: data.departments.map(d => d.employee_count)
};

// 2. Department Attendance Chart
const attendanceChart = {
  labels: data.department_attendance.map(d => d.department_name),
  datasets: [
    {
      label: 'Present %',
      data: data.department_attendance.map(d => d.present_percentage)
    },
    {
      label: 'Absent %',
      data: data.department_attendance.map(d => d.absent_percentage)
    }
  ]
};

// 3. Department Modules Chart
const modulesChart = {
  labels: data.department_modules.map(d => d.department_name),
  data: data.department_modules.map(d => d.modules_completed)
};

// 4. Applications Table
{data.active_applications.map(app => (
  <TableRow key={app.application_id}>
    <td>{app.applicant_name}</td>
    <td>{app.applied_role}</td>
    <td>{formatDate(app.applied_date)}</td>
    <td><Badge color={getStatusColor(app.status)}>{app.status}</Badge></td>
  </TableRow>
))}
```

---

## 🔐 **Authentication**

All dashboard APIs require JWT authentication:

```typescript
// Add token to request headers (auto-handled by axios interceptor)
headers: {
  'Authorization': `Bearer ${accessToken}`
}
```

---

## ⚠️ **Error Handling**

### **Common HTTP Status Codes**

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Display data |
| 401 | Unauthorized | Redirect to login |
| 403 | Forbidden | Show "Access Denied" |
| 404 | Not Found | Show error message |
| 500 | Server Error | Show error message |

### **Example Error Handler**

```typescript
try {
  const response = await api.get('/api/v1/dashboard/employee');
  setData(response.data);
} catch (error) {
  if (error.response?.status === 401) {
    // Redirect to login
    navigate('/login');
  } else if (error.response?.status === 403) {
    // Show access denied
    setError('You do not have permission to view this page');
  } else {
    // Show generic error
    setError('Failed to load dashboard data');
  }
}
```

---

## 🎨 **UI Component Suggestions**

### **Employee Dashboard**

```
┌─────────────────────────────────────────┐
│          Employee Dashboard              │
├─────────────────────────────────────────┤
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐│
│  │ WFH  │  │Leaves│  │Punch │  │Punch ││
│  │ Left │  │ Left │  │  In  │  │ Out  ││
│  └──────┘  └──────┘  └──────┘  └──────┘│
├─────────────────────────────────────────┤
│  Upcoming Holidays                       │
│  • Christmas - Dec 25                    │
│  • New Year - Jan 1                      │
├─────────────────────────────────────────┤
│  Learning Goals         ┌──────────┐    │
│                        │  PIE     │    │
│  Completed: 4          │  CHART   │    │
│  Pending: 1            │          │    │
│  80% Complete          └──────────┘    │
└─────────────────────────────────────────┘
```

### **Manager Dashboard**

```
┌─────────────────────────────────────────┐
│          Manager Dashboard               │
├─────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │Team Size │  │Avg Att % │  │Goals % ││
│  │    8     │  │  87.5%   │  │  75%   ││
│  └──────────┘  └──────────┘  └────────┘│
├─────────────────────────────────────────┤
│  Team Attendance                         │
│  ┌────────────────────────────────────┐ │
│  │Name          │ Present % │ Absent %││ │
│  │Alice Smith   │   90.0%   │  10.0% ││ │
│  │Bob Johnson   │   85.0%   │  15.0% ││ │
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Modules Leaderboard                     │
│  🥇 Bob Johnson - 25 modules            │
│  🥈 Alice Smith - 22 modules            │
│  🥉 Carol White - 18 modules            │
└─────────────────────────────────────────┘
```

### **HR Dashboard**

```
┌─────────────────────────────────────────┐
│             HR Dashboard                 │
├─────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │  Total   │  │  Total   │  │ Active ││
│  │Employees │  │  Depts   │  │  Apps  ││
│  │   57     │  │    5     │  │   10   ││
│  └──────────┘  └──────────┘  └────────┘│
├─────────────────────────────────────────┤
│  Department Employee Count               │
│  [====================] Engineering (20) │
│  [============]         Sales (15)       │
│  [=======]              HR (5)           │
├─────────────────────────────────────────┤
│  Department Attendance                   │
│  HR         [████████] 92%               │
│  Sales      [███████ ] 88%               │
│  Engineering[██████  ] 85%               │
├─────────────────────────────────────────┤
│  Active Applications                     │
│  John Doe - Software Engineer - Pending  │
│  Jane Smith - Product Manager - Reviewed │
└─────────────────────────────────────────┘
```

---

## 📊 **Chart Libraries Recommendation**

| Library | Best For | Dashboards |
|---------|----------|------------|
| **Chart.js** | Pie, Bar, Line charts | Employee, Manager, HR |
| **Recharts** | React-native charts | All |
| **ApexCharts** | Advanced charts | HR (multi-bar) |
| **Victory** | Customizable charts | All |

### **Example with Chart.js**

```typescript
import { Pie, Bar } from 'react-chartjs-2';

// Employee - Learning Goals Pie Chart
<Pie data={{
  labels: ['Completed', 'Pending'],
  datasets: [{
    data: [data.learning_goals.completed_goals, data.learning_goals.pending_goals],
    backgroundColor: ['#10B981', '#EF4444']
  }]
}} />

// HR - Department Employees Bar Chart
<Bar data={{
  labels: data.departments.map(d => d.department_name),
  datasets: [{
    label: 'Employees',
    data: data.departments.map(d => d.employee_count),
    backgroundColor: '#3B82F6'
  }]
}} />
```

---

## ✅ **Testing Checklist**

### **For Each Dashboard**

- [ ] API returns 200 OK
- [ ] All required fields are present
- [ ] Data types match TypeScript interfaces
- [ ] Null values are handled properly
- [ ] Arrays are populated correctly
- [ ] Numbers are within expected ranges
- [ ] Dates are in ISO format
- [ ] Charts render without errors
- [ ] Loading states work
- [ ] Error states work

---

## 🚀 **Quick Start**

1. **Install Dependencies**
```bash
npm install axios chart.js react-chartjs-2
```

2. **Create API Service**
```typescript
// src/services/dashboardService.ts
export const getEmployeeDashboard = () => api.get('/api/v1/dashboard/employee');
export const getManagerDashboard = () => api.get('/api/v1/dashboard/manager');
export const getHRDashboard = () => api.get('/api/v1/dashboard/hr');
```

3. **Use in Component**
```typescript
const [data, setData] = useState(null);
const [loading, setLoading] = useState(true);

useEffect(() => {
  const fetchData = async () => {
    try {
      const response = await getEmployeeDashboard();
      setData(response.data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };
  fetchData();
}, []);
```

---

## 📚 **Full Documentation**

For detailed analysis, see:
- `EMPLOYEE_DASHBOARD_ANALYSIS.md` - Employee Dashboard details
- `MANAGER_DASHBOARD_ANALYSIS.md` - Manager Dashboard details
- `HR_DASHBOARD_ANALYSIS.md` - HR Dashboard details
- `COMPLETE_DASHBOARD_ANALYSIS.md` - Overall comparison

---

## 💡 **Pro Tips**

1. **Cache Dashboard Data**: Dashboard data doesn't change frequently, consider caching for 5-10 minutes
2. **Use Loading Skeletons**: Show skeleton loaders while data is fetching
3. **Handle Null Values**: Some fields can be null (e.g., `today_attendance`, `learner_rank`)
4. **Format Numbers**: Use `toFixed(1)` for percentages, `toLocaleString()` for large numbers
5. **Color Code Status**: Use different colors for different attendance statuses
6. **Add Refresh Button**: Let users manually refresh dashboard data
7. **Show Last Updated**: Display when data was last fetched

---

**Generated**: November 13, 2025  
**Status**: ✅ Ready for Implementation  
**Support**: Check individual dashboard analysis documents for detailed information

---

*Quick, easy, and ready to use!* 🚀

