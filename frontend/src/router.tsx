import { lazy } from "react";
import { createBrowserRouter } from "react-router-dom";
import App from "@/App";
import RootLayout from "@/layouts/RootLayout";
import ProtectedRoute from "@/components/ProtectedRoute";

const Home = lazy(() => import("@/pages/Home"));
const Login = lazy(() => import("@/pages/Login"));
const Employee = lazy(() => import("@/layouts/Employee"));
const HR = lazy(() => import("@/layouts/HR"));
const Manager = lazy(() => import("@/layouts/Manager"));
const EmployeeDashboard = lazy(
  () => import("@/pages/Employee/EmployeeDashboard"),
);
const HRDashboard = lazy(() => import("@/pages/HR/HRDashboard"));
const JobListingsEmployee = lazy(() => import("@/pages/Employee/JobListings"));
const AddJobForm = lazy(() => import("@/pages/HR/AddJobForm"));
const EmployeesList = lazy(() => import("@/pages/HR/EmployeesList"));
const AddEmployeeForm = lazy(() => import("@/pages/HR/AddEmployeeForm"));
const Policies = lazy(() => import("@/pages/HR/Policies"));
const ResumeScreener = lazy(() => import("@/pages/HR/ResumeScreener"));
const HRJobListings = lazy(() => import("@/pages/HR/JobListings"));
const TeamRequests = lazy(() => import("@/pages/Manager/TeamRequests"));
const ResumeScreenerResults = lazy(
  () => import("@/pages/HR/ResumeScreenerResults"),
);
const Announcements = lazy(() => import("@/pages/HR/Announcements"));
const AnnouncementsEmployee = lazy(
  () => import("@/pages/Common/Announcements"),
);
const AnnouncementsDetailsEmployee = lazy(
  () => import("@/pages/Common/AnnouncementDetails"),
);
const Payslips = lazy(() => import("@/pages/Common/Payslips"));
const PayslipsDetails = lazy(() => import("@/pages/Common/PayslipsDetail"));
const Applications = lazy(() => import("@/pages/HR/Applications"));
const Attendance = lazy(() => import("@/pages/Common/Attendance"));
const PerformanceReport = lazy(
  () => import("@/pages/Common/PerformanceReport"),
);
const EmployeePerformanceReport = lazy(
  () => import("@/pages/Employee/PerformanceReport"),
);
const PoliciesEmployee = lazy(() => import("@/pages/Common/Policies"));
const GoalTrackerEmployee = lazy(() => import("@/pages/Employee/GoalTracker"));
const VisitPage = lazy(() => import("@/pages/Employee/GoalTrackerDetail"));
const SkillDevelopment = lazy(
  () => import("@/pages/Employee/SkillDevelopment"),
);
const ManagerDashboard = lazy(() => import("@/pages/Manager/ManagerDashboard"));
const TeamMembers = lazy(() => import("@/pages/Manager/TeamMembers"));
const ViewEmployee = lazy(() => import("@/pages/Manager/ViewEmployee"));
const EmployeeProfile = lazy(() => import("@/pages/Employee/Profile"));
const SkillVisit = lazy(
  () => import("@/pages/Employee/SkillDevelopmentDetail"),
);
const FeedbackReport = lazy(() => import("@/pages/Employee/FeedbackReport"));

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
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
        path: "/employee",
        element: (
          <ProtectedRoute allowedRoles={["employee", "manager"]}>
            <Employee />
          </ProtectedRoute>
        ),
        children: [
          {
            index: true,
            element: <EmployeeDashboard />,
          },
          {
            path: "performance-report",
            element: <EmployeePerformanceReport />,
          },
          {
            path: "performance-report/feedbacks",
            element: <FeedbackReport />,
          },
          {
            path: "payslips",
            element: <Payslips />,
          },
          {
            path: "payslips/:id",
            element: <PayslipsDetails />,
          },
          {
            path: "attendance",
            element: <Attendance />,
          },
          {
            path: "announcements",
            element: <AnnouncementsEmployee />,
          },
          {
            path: "announcements/:id",
            element: <AnnouncementsDetailsEmployee />,
          },

          {
            path: "job-listings",
            element: <JobListingsEmployee />,
          },
          {
            path: "policies",
            element: <PoliciesEmployee />,
          },
          {
            path: "goal-tracker",
            element: <GoalTrackerEmployee />,
          },
          {
            path: "goal-tracker/:goal/:id",
            element: <VisitPage />,
          },
          {
            path: "skill-development",
            element: <SkillDevelopment />,
          },
          {
            path: "skills/:slug",
            element: <SkillVisit />,
          },
          {
            path: "profile",
            element: <EmployeeProfile />,
          },
        ],
      },
      {
        path: "/hr",
        element: (
          <ProtectedRoute allowedRoles={["hr", "admin"]}>
            <HR />
          </ProtectedRoute>
        ),
        children: [
          {
            index: true,
            element: <HRDashboard />,
          },
          {
            path: "joblistings",
            element: <HRJobListings />,
          },
          {
            path: "add-new-job",
            element: <AddJobForm />,
          },
          {
            path: "employees-list",
            element: <EmployeesList />,
          },
          {
            path: "add-new-employee",
            element: <AddEmployeeForm />,
          },
          {
            path: "policies",
            element: <Policies />,
          },
          {
            path: "resume-screener",
            element: <ResumeScreener />,
          },
          {
            path: "resume-screener/results",
            element: <ResumeScreenerResults />,
          },
          {
            path: "announcements",
            element: <Announcements />,
          },
          {
            path: "payslips",
            element: <Payslips />,
          },
          {
            path: "applications",
            element: <Applications />,
          },
          {
            path: "attendance",
            element: <Attendance />,
          },
          {
            path: "performance-report",
            element: <PerformanceReport />,
          },
          {
            path: "profile",
            element: <EmployeeProfile />,
          },
        ],
      },
      {
        path: "/manager",
        element: (
          <ProtectedRoute allowedRoles={["manager"]}>
            <Manager />
          </ProtectedRoute>
        ),
        children: [
          {
            index: true,
            element: <ManagerDashboard />,
          },
          {
            path: "performance-report",
            element: <PerformanceReport />,
          },
          {
            path: "team-members",
            element: <TeamMembers />,
          },
          {
            path: "team-members/view/:employeeId",
            element: <ViewEmployee />,
          },
          {
            path: "team-requests",
            element: <TeamRequests />,
          },
          {
            path: "payslips",
            element: <Payslips />,
          },
          {
            path: "attendance",
            element: <Attendance />,
          },
          {
            path: "announcements",
            element: <AnnouncementsEmployee />,
          },
          {
            path: "announcements/:id",
            element: <AnnouncementsDetailsEmployee />,
          },

          {
            path: "job-listings",
            element: <JobListingsEmployee />,
          },
          {
            path: "policies",
            element: <PoliciesEmployee />,
          },
          {
            path: "profile",
            element: <EmployeeProfile />,
          },
        ],
      },
    ],
  },
]);

export default router;
