# 📁 Frontend Documentation - HRMS Application

## Overview

This is a **React + TypeScript** Human Resources Management System (HRMS) with **role-based access control** for three user types: **Employee**, **HR**, and **Manager**.

---

## 🏗️ Technology Stack

- **Framework**: React 19.2.0 with TypeScript
- **Build Tool**: Vite 7.1.7
- **Routing**: React Router DOM v7
- **Styling**: Tailwind CSS v4
- **UI Components**: Radix UI (accessible component library)
- **Charts**: Recharts 2.15.4
- **Icons**: Lucide React
- **Date Handling**: date-fns & react-day-picker
- **Package Manager**: pnpm

---

## 🔄 Application Flow

### Entry Point Flow
```
index.html → main.tsx → router.tsx → App.tsx/Layouts → Pages
```

1. **`main.tsx`**: Initializes React app and provides the router
2. **`router.tsx`**: Defines all routes and lazy loads components
3. **`App.tsx`**: Simple wrapper with `<Outlet />` for child routes
4. **Layouts**: Role-specific layouts (Employee/HR/Manager) with sidebar navigation
5. **Pages**: Individual feature pages

---

## 📂 Folder Structure

```
frontend/
├── public/                      # Static assets
├── src/
│   ├── assets/                  # Images, logos, etc.
│   ├── components/              # Reusable UI components
│   │   ├── ui/                  # 20+ Radix-based primitives
│   │   ├── *-sidebar.tsx        # Role-specific sidebars
│   │   ├── *-header.tsx         # Header components
│   │   ├── AreaChart.tsx        # Chart components
│   │   ├── FeedbackTable.tsx    # Data tables
│   │   └── ...
│   ├── constants/               # Navigation & config
│   │   ├── EmployeeSidebarItems.ts
│   │   ├── HRSidebaritems.ts
│   │   └── ManagerSidebarItems.ts
│   ├── hooks/                   # Custom React hooks
│   │   └── use-mobile.ts
│   ├── layouts/                 # Role-based layouts
│   │   ├── Employee.tsx
│   │   ├── HR.tsx
│   │   └── Manager.tsx
│   ├── lib/                     # Utilities
│   │   └── utils.ts
│   ├── pages/                   # Application pages
│   │   ├── Common/              # Shared pages
│   │   ├── Employee/            # Employee-specific
│   │   ├── HR/                  # HR-specific
│   │   ├── Manager/             # Manager-specific
│   │   ├── Home.tsx
│   │   └── Login.tsx
│   ├── App.tsx                  # Root component
│   ├── main.tsx                 # Application entry
│   ├── router.tsx               # Route configuration
│   └── index.css                # Global styles
├── package.json
├── vite.config.ts               # Vite configuration
├── tsconfig.json                # TypeScript config
└── tailwind.config.js           # Tailwind config
```

---

## 🎯 Component Breakdown

### `/src/components/`
**Layout Components**:
- `app-header.tsx`, `EmployeeHeader.tsx` - Application headers
- `Employee-sidebar.tsx`, `HR-sidebar.tsx`, `Manager-sidebar.tsx` - Role-specific navigation
- `nav-main.tsx`, `nav-projects.tsx`, `nav-user.tsx` - Navigation elements

**Data Visualization**:
- `AreaChart.tsx` - Area/line charts
- `dougnut-chart.tsx` - Pie/doughnut charts
- `horizontal-bar-chart.tsx` - Horizontal bar charts
- `multi-bar-chart.tsx` - Multi-series bar charts

**Feature Components**:
- `FeedbackTable.tsx` - Feedback data display
- `JobListingsTable.tsx` - Job postings for employees
- `JobListingsTableManager.tsx` - Job postings for managers
- `FullCalendar.tsx` - Calendar view
- `EmployeeDashboardCard.tsx` - Dashboard widgets
- `login-form.tsx` - Authentication form

**UI Components (`/ui/`)**: 20+ accessible components
- Forms: `input`, `label`, `checkbox`, `select`, `field`
- Navigation: `breadcrumb`, `dropdown-menu`, `sidebar`
- Feedback: `dialog`, `tooltip`, `skeleton`
- Data: `table`, `calendar`, `chart`
- Layout: `card`, `separator`, `scroll-area`, `sheet`, `collapsible`
- Actions: `button`, `avatar`

---

## 📄 Pages Architecture

### **Public Pages (2)**
- **`Home.tsx`** - Landing page with "Get Started" CTA
- **`Login.tsx`** - Authentication page with login form

### **Common Pages (6)** - Shared across roles
Located in `/pages/Common/`:
- **`Announcements.tsx`** - View company announcements
- **`Attendance.tsx`** - Track attendance records
- **`JobListings.tsx`** - Browse internal job postings
- **`Payslips.tsx`** - View salary slips
- **`PerformanceReport.tsx`** - Performance metrics overview
- **`Policies.tsx`** - Company policies documentation

### **Employee Pages (9)** - `/pages/Employee/`
1. **`EmployeeDashboard.tsx`** - Personal overview dashboard
2. **`Profile.tsx`** - Personal profile management
3. **`FeedbackPage.tsx`** - Submit feedback
4. **`FeedbackReport.tsx`** - View received feedback
5. **`GoalTracker.tsx`** - List of assigned goals
6. **`GoalTrackerDetail.tsx`** - Individual goal details (dynamic route)
7. **`SkillDevelopment.tsx`** - Available training programs
8. **`SkillDevelopmentDetail.tsx`** - Course details (dynamic route)
9. **`PerformanceReport.tsx`** - Employee-specific performance view

Plus access to common pages (Payslips, Attendance, Announcements, Job Listings, Policies)

### **HR Pages (9)** - `/pages/HR/`
1. **`HRDashboard.tsx`** - HR analytics and overview
2. **`EmployeesList.tsx`** - Employee directory management
3. **`AddEmployeeForm.tsx`** - Onboard new employees
4. **`JobListings.tsx`** - Manage job postings
5. **`AddJobForm.tsx`** - Create new job posting
6. **`Applications.tsx`** - Review job applications
7. **`ResumeScreener.tsx`** - AI-powered resume screening upload
8. **`ResumeScreenerResults.tsx`** - View screening results
9. **`Announcements.tsx`** - Create and manage announcements

Plus access to Policies (create/edit), and common pages (Payslips, Attendance, Performance Report)

### **Manager Pages (4)** - `/pages/Manager/`
1. **`ManagerDashboard.tsx`** - Team overview and analytics
2. **`TeamMembers.tsx`** - Team roster management
3. **`TeamRequests.tsx`** - Approve/deny team requests
4. **`JobListings.tsx`** - Manager-specific job listings view

Plus access to common pages (Performance Report, Payslips, Announcements, Job Listings, Attendance, Policies, Profile)

**Total Pages**: ~31 distinct pages with role-based access control

---

## 🛣️ Routing Structure

### **Public Routes**
```
/              → Home (landing page)
/login         → Login page
```

### **Employee Routes** (`/employee/*`)
```
/employee                              → Dashboard
/employee/performance-report           → Performance metrics
/employee/performance-report/feedbacks → Feedback details
/employee/payslips                     → View payslips
/employee/attendance                   → Attendance records
/employee/announcements                → Company updates
/employee/job-listings                 → Internal opportunities
/employee/policies                     → Company policies
/employee/goal-tracker                 → Goals list
/employee/goal-tracker/:id             → Specific goal details
/employee/skill-development            → Training programs
/employee/skills/:slug                 → Course details
/employee/profile                      → User profile
```

### **HR Routes** (`/hr/*`)
```
/hr                                    → HR Dashboard
/hr/joblistings                        → Job postings management
/hr/joblistings/add-new-job            → Create job posting (nested)
/hr/employees-list                     → Employee directory
/hr/employees-list/add-new-employee    → Onboard employee (nested)
/hr/policies                           → Policy management
/hr/resume-screener                    → Upload resumes for AI screening
/hr/resume-screener/results            → View screening results
/hr/announcements                      → Create announcements
/hr/payslips                           → Manage payslips
/hr/applications                       → Job applications
/hr/attendance                         → Attendance management
/hr/performance-report                 → Performance analytics
```

### **Manager Routes** (`/manager/*`)
```
/manager                               → Manager Dashboard
/manager/performance-report            → Team performance
/manager/team-members                  → Team roster
/manager/team-requests                 → Approve/deny requests
/manager/payslips                      → View team payslips
/manager/attendance                    → Team attendance
/manager/announcements                 → View announcements
/manager/job-listings                  → Internal opportunities
/manager/policies                      → Company policies
/manager/profile                       → User profile
```

---

## 🏗️ Layout System

Each role has a dedicated layout with consistent structure:

### **Layout Components**
```tsx
// Employee.tsx, HR.tsx, Manager.tsx
<SidebarProvider>
  <RoleSpecificSidebar />
  <SidebarInset>
    <Header />
    <hr />
    <Outlet />  {/* Child pages render here */}
  </SidebarInset>
</SidebarProvider>
```

**Features**:
- Collapsible sidebar with responsive behavior
- Role-specific navigation menus
- Breadcrumb navigation in header
- Consistent layout across all pages

---

## 🎨 UI/UX Pattern

```
┌─────────────────────────────────────────────┐
│  Header (Breadcrumbs, User Menu, Search)    │
├──────────┬──────────────────────────────────┤
│          │                                  │
│ Sidebar  │    Page Content                  │
│ (Nav     │    (<Outlet />)                  │
│  Menu)   │                                  │
│          │    - Charts                      │
│          │    - Tables                      │
│          │    - Forms                       │
│          │                                  │
└──────────┴──────────────────────────────────┘
```

---

## 🔑 Key Features

### **1. Role-Based Access Control (RBAC)**
Three distinct user experiences with specific permissions and pages:
- **Employee**: Self-service portal for personal HR needs
- **HR**: Administrative control over employees, policies, recruitment
- **Manager**: Team management and oversight

### **2. Lazy Loading**
All pages are lazy-loaded using React's `lazy()` for optimal performance:
```tsx
const Home = lazy(() => import("@/pages/Home"));
```

### **3. Nested Routing**
Forms and detail pages use nested routes:
- Add Job Form opens within Job Listings page
- Goal details are subroutes of Goal Tracker
- Skill course details under Skill Development

### **4. Responsive Design**
- Tailwind CSS utility-first styling
- Custom `use-mobile` hook for device detection
- Collapsible sidebars for mobile devices
- Mobile-optimized components

### **5. Data Visualization**
Multiple chart types using Recharts:
- **Area Chart**: Trend analysis
- **Doughnut Chart**: Distribution metrics
- **Horizontal Bar Chart**: Comparative data
- **Multi Bar Chart**: Multi-series comparisons

### **6. Accessibility**
- Radix UI components ensure WCAG compliance
- Keyboard navigation support
- Screen reader friendly
- Focus management

### **7. Type Safety**
- Full TypeScript implementation
- Type-safe routing
- Component prop validation
- API response typing

---

## 🚀 Getting Started

### **Prerequisites**
- Node.js 18+ 
- pnpm (preferred) or npm

### **Installation**
```bash
cd frontend
pnpm install
# or
npm install
```

### **Development**
```bash
pnpm dev
# or
npm run dev
```
Runs on `http://localhost:5173` (default Vite port)

### **Build for Production**
```bash
pnpm build
# or
npm run build
```
Output: `dist/` folder

### **Preview Production Build**
```bash
pnpm preview
# or
npm run preview
```

### **Linting**
```bash
pnpm lint
# or
npm run lint
```

---

## 📦 Key Dependencies

### **Core**
- `react` & `react-dom` (19.2.0) - UI library
- `react-router-dom` (7.9.4) - Routing
- `typescript` (5.9.3) - Type safety

### **Styling**
- `tailwindcss` (4.1.14) - Utility-first CSS
- `@tailwindcss/vite` (4.1.14) - Vite integration
- `class-variance-authority` - Component variants
- `tailwind-merge` - Class merging utility
- `clsx` - Conditional classes

### **UI Components**
- `@radix-ui/react-*` - Accessible primitives
  - dialog, dropdown-menu, select, tooltip
  - avatar, checkbox, collapsible, label
  - scroll-area, separator, slot

### **Visualization**
- `recharts` (2.15.4) - Charting library

### **Utilities**
- `lucide-react` (0.546.0) - Icon library
- `date-fns` (4.1.0) - Date manipulation
- `react-day-picker` (9.11.1) - Date picker
- `react-hotkeys-hook` (5.2.1) - Keyboard shortcuts

### **Dev Tools**
- `vite` (7.1.7) - Build tool
- `@vitejs/plugin-react` - React plugin
- `eslint` - Code linting
- `typescript-eslint` - TS linting rules

---

## 🗂️ Navigation Configuration

### **Employee Sidebar** (9 items)
```typescript
EmployeeSidebarItems = [
  Dashboard, Performance Report, Payslips, 
  Announcements, Job Listings, Attendance, 
  Policies, Goal Tracker, Skill Development
]
```

### **HR Sidebar** (8 items)
```typescript
HRSidebarItems = [
  Dashboard, Job Listings, Employee List, 
  Policies, Resume Screener, Announcements,
  Payslips, Attendance
]
```

### **Manager Sidebar** (8 items)
```typescript
ManagerSidebarItems = [
  Dashboard, Team Members, Team Requests,
  Payslips, Announcements, Job Listings,
  Attendance, Policies
]
```

---

## 🔧 Configuration Files

- **`vite.config.ts`** - Vite build configuration
- **`tsconfig.json`** - TypeScript compiler options
- **`tsconfig.app.json`** - App-specific TS config
- **`tsconfig.node.json`** - Node-specific TS config
- **`eslint.config.js`** - ESLint rules
- **`components.json`** - UI component configuration (shadcn/ui style)
- **`package.json`** - Dependencies and scripts

---

## 🎯 Development Patterns

### **Component Structure**
```tsx
// Typical page component
import { Component } from "@/components/ui/component";
import { useNavigate } from "react-router-dom";

const PageName = () => {
  const navigate = useNavigate();
  
  return (
    <div className="p-6">
      {/* Page content */}
    </div>
  );
};

export default PageName;
```

### **Path Aliases**
Using `@/` for clean imports:
```tsx
import { Button } from "@/components/ui/button";
import { EmployeeSidebar } from "@/components/Employee-sidebar";
```

### **Lazy Loading Pattern**
```tsx
const PageName = lazy(() => import("@/pages/PageName"));
```

---

## 📊 Page Count Summary

| Role     | Exclusive Pages | Shared Pages | Total |
|----------|----------------|--------------|-------|
| Employee | 9              | 6            | 15    |
| HR       | 9              | 5            | 14    |
| Manager  | 4              | 9            | 13    |
| Public   | 2              | 0            | 2     |
| **Total**| **24**         | **6**        | **~31**|

---

## 🔐 Authentication Flow

1. User lands on `/` (Home page)
2. Clicks "Get Started - Login"
3. Redirected to `/login`
4. Submits credentials via `LoginForm`
5. On success, redirected to role-specific dashboard:
   - Employee → `/employee`
   - HR → `/hr`
   - Manager → `/manager`

---

## 📈 Performance Optimizations

1. **Code Splitting**: Lazy loading all routes
2. **Tree Shaking**: ES modules with Vite
3. **Optimized Dependencies**: Using specific Radix UI packages
4. **CSS Optimization**: Tailwind JIT compilation
5. **Asset Optimization**: Vite's built-in optimizations

---

## 🐛 Troubleshooting

### Build Errors
```bash
# Clear cache and reinstall
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### TypeScript Errors
```bash
# Check TypeScript config
npx tsc --noEmit
```

### Linting Issues
```bash
# Auto-fix linting issues
pnpm lint --fix
```

---

## 📝 Notes

- **Modern React**: Using React 19 features
- **Type-Safe Routing**: Full TypeScript support in routes
- **Accessible by Default**: Radix UI ensures WCAG compliance
- **Production-Ready**: Optimized build with Vite
- **Scalable Architecture**: Clear separation of concerns

---

## 🎓 Learning Resources

- [React Router v7 Docs](https://reactrouter.com/)
- [Tailwind CSS Docs](https://tailwindcss.com/)
- [Radix UI Docs](https://www.radix-ui.com/)
- [Recharts Docs](https://recharts.org/)
- [Vite Docs](https://vitejs.dev/)

---

**Last Updated**: November 11, 2025  
**Version**: 0.0.0  
**Maintained By**: SEP-11 Team
