import {
  LayoutDashboard,
  FileText,
  Megaphone,
  Users,
  Briefcase,
  Scan,
  CalendarCheck,
  BookOpen,
} from "lucide-react";

const HRSidebarItems = {
  navMain: [
    {
      name: "Dashboard",
      url: "/hr-dashboard",
      icon: LayoutDashboard,
    },
    {
      name: "Job Listings",
      url: "/hrjoblistings",
      icon: Briefcase,
    },
    {
      name: "Employee List",
      url: "/employees-list",
      icon: Users,
    },
    {
      name: "Policies",
      url: "/hr-policies",
      icon: BookOpen,
    },
    {
      name: "Resume Screener",
      url: "/resume-screener",
      icon: Scan,
    },
    {
      name: "Announcements",
      url: "/hr-announcements",
      icon: Megaphone,
    },
    {
      name: "Payslips",
      url: "/hr-payslips",
      icon: FileText,
    },
    {
      name: "Attendance",
      url: "/hr-attendance",
      icon: CalendarCheck,
    }
  ],
};


export default HRSidebarItems;