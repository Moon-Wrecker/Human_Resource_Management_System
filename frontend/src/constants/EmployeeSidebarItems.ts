import {
  LayoutDashboard,
  BarChart,
  FileText,
  Megaphone,
  Briefcase,
  CalendarCheck,
  BookOpen,
  Target,
  Lightbulb,
} from "lucide-react";

const EmployeeSidebarItems = [
  {
    name: "Dashboard",
    url: "/employee/dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "Performance Report",
    url: "/employee/performance-report",
    icon: BarChart,
  },
  {
    name: "Payslips",
    url: "/employee/payslips",
    icon: FileText,
  },
  {
    name: "Announcements",
    url: "/employee/announcements",
    icon: Megaphone,
  },
  {
    name: "Job Listings",
    url: "/employee/job-listings",
    icon: Briefcase,
  },
  {
    name: "Attendance",
    url: "/employee/attendance",
    icon: CalendarCheck,
  },
  {
    name: "Policies",
    url: "/employee/policies",
    icon: BookOpen,
  },
  {
    name: "Goal Tracker",
    url: "/employee/goal-tracker",
    icon: Target,
  },
  {
    name: "Skill Development",
    url: "/employee/skill-development",
    icon: Lightbulb,
  },
];

export default EmployeeSidebarItems;
