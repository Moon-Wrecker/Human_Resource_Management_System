import {
  LayoutDashboard,
  FileText,
  Megaphone,
  Briefcase,
  CalendarCheck,
  BookOpen,
  Users,
} from "lucide-react";

const ManagerSidebarItems = [
  {
    name: "Dashboard",
    url: "/manager",
    icon: LayoutDashboard,
  },
  {
    name: "Team Members",
    url: "/manager/team-members",
    icon: Users,
  },
  {
    name: "Team Requests",
    url: "/manager/team-requests",
    icon: Users,
  },
  {
    name: "Payslips",
    url: "/manager/payslips",
    icon: FileText,
  },
  {
    name: "Announcements",
    url: "/manager/announcements",
    icon: Megaphone,
  },
  {
    name: "Job Listings",
    url: "/manager/job-listings",
    icon: Briefcase,
  },
  {
    name: "Attendance",
    url: "/manager/attendance",
    icon: CalendarCheck,
  },
  {
    name: "Policies",
    url: "/manager/policies",
    icon: BookOpen,
  },
];

export default ManagerSidebarItems;
