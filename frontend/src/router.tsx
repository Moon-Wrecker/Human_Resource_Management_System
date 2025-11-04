import { lazy } from "react";
import { createBrowserRouter } from "react-router-dom";
import App from "@/App";

const Employee = lazy(() => import("@/layouts/Employee"));
const HR = lazy(() => import("@/layouts/HR"));
const Manager = lazy(() => import("@/layouts/Manager"))
const Home = lazy(() => import("@/pages/Home"));
const Login = lazy(() => import("@/pages/Login"));
const EmployeeDashboard = lazy(() => import("@/pages/Employee/EmployeeDashboard"));
const HRDashboard = lazy(() => import("@/pages/HR/HRDashboard"));
const HRJobListings = lazy(() => import("@/pages/HR/JobListings"));
const AddJobForm = lazy(() => import ("@/pages/HR/AddJobForm"));
const EmployeesList = lazy(() => import ("@/pages/HR/EmployeesList"));
const AddEmployeeForm = lazy(() => import ("@/pages/HR/AddEmployeeForm"));
const HRPolicies = lazy(() => import ("@/pages/HR/Policies"));
const ResumeScreener = lazy(() => import ("@/pages/HR/ResumeScreener"));
const ResumeScreenerResults = lazy(() => import ("@/pages/HR/ResumeScreenerResults"));
const Announcements = lazy(() => import ("@/pages/HR/Announcements"));
const Payslips = lazy(() => import ("@/pages/Common/Payslips"));
const Applications = lazy(() => import ("@/pages/HR/Applications"));
const Attendance = lazy(() => import ("@/pages/Common/Attendance"));
const PerformanceReport = lazy(() => import ("@/pages/Common/PerformanceReport"));
const ManagerDashboard = lazy(() => import ("@/pages/Manager/ManagerDashboard"));
const TeamRequests = lazy(() => import ("@/pages/Manager/TeamRequests"));
const TeamMembers = lazy(()=>  import ("@/pages/Manager/TeamMembers"));
const JobListings = lazy(() => import ("@/pages/Common/JobListings"));

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        index: true,
        element: <Home />,
      },
    ],
  },
  { path: "/login", element: <Login /> },
  {
    path: "/employee-dashboard",
    element: <Employee />,
    children: [
      {
        index: true,
        element: <EmployeeDashboard />,
      },
    ],
  },
  {
    path: "/employee-payslips",
    element: <Employee />,
    children: [
      {
        index: true,
        element: <Payslips/>,
      },
    ],
  },
  {
    path: "/hr-dashboard",
    element: <HR/>,
    children: [
      {
        index: true,
        element: <HRDashboard />,
      },
    ],
  },
  {
    path: "/hrjoblistings",
    element: <HR />,
    children: [
      {
        index: true,
        element: <HRJobListings />,
      },
    ],
  },
  {
    path: "/hrjoblistings/add-new-job",
    element: <HR />,
    children: [
      {
        index: true,
        element: < AddJobForm/>,
      },
    ],
  },
  {
    path: "/employees-list",
    element: <HR />,
    children: [
      {
        index: true,
        element: < EmployeesList/>,
      },
    ],
  },
  {
    path: "/employees-list/add-new-employee",
    element: <HR />,
    children: [
      {
        index: true,
        element: < AddEmployeeForm/>,
      },
    ],
  },
  {
    path: "/hr-policies",
    element: <HR />,
    children: [
      {
        index: true,
        element: < HRPolicies/>,
      },
    ],
  },
  {
    path: "/resume-screener",
    element: <HR />,
    children: [
      {
        index: true,
        element: < ResumeScreener/>,
      },
    ],
  },
  {
    path: "/resume-screener/results",
    element: <HR />,
    children: [
      {
        index: true,
        element: < ResumeScreenerResults/>,
      },
    ],
  },
  {
    path: "/hr-announcements",
    element: <HR />,
    children: [
      {
        index: true,
        element: <Announcements/>,
      },
    ],
  },
  {
    path: "/hr-payslips",
    element: <HR />,
    children: [
      {
        index: true,
        element: <Payslips/>,
      },
    ],
  },
  {
    path: "/manager-payslips",
    element: <HR />,
    children: [
      {
        index: true,
        element: <Payslips/>,
      },
    ],
  },
  {
    path: "/applications",
    element: <HR />,
    children: [
      {
        index: true,
        element: <Applications/>,
      },
    ],
  },
  {
    path: "/hr-attendance",
    element: <HR />,
    children: [
      {
        index: true,
        element: <Attendance/>,
      },
    ],
  },
  {
    path: "/hr-performance-report",
    element: <HR />,
    children: [
      {
        index: true,
        element: <PerformanceReport/>,
      },
    ],
  },
  {
    path: "/manager-dashboard",
    element: <Manager />,
    children: [
      {
        index: true,
        element: <ManagerDashboard/>,
      },
    ],
  },
  {
    path: "/team-requests",
    element: <Manager />,
    children: [
      {
        index: true,
        element: <TeamRequests/>,
      },
    ],
  },
  {
    path: "/team-members",
    element: <Manager />,
    children: [
      {
        index: true,
        element: <TeamMembers/>,
      },
    ],
  },
  {
    path: "/manager-joblistings",
    element: <Manager />,
    children: [
      {
        index: true,
        element: <JobListings/>,
      },
    ],
  },
  {
    path: "/employee-joblistings",
    element: <Employee />,
    children: [
      {
        index: true,
        element: <JobListings/>,
      },
    ],
  },
]);

export default router;
