import {
  LayoutDashboard,
  FileText,
  Megaphone,
  Users,
  Briefcase,
  Scan,
  CalendarCheck,
  BookOpen,
  ScanBarcode,
  FormInputIcon,
} from "lucide-react";

const HRSidebarItems = {
  navMain: [
    {
      name: "Dashboard",
      url: "/hr",
      icon: LayoutDashboard,
    },
    {
      name: "Job Listings",
      url: "/hr/joblistings",
      icon: Briefcase,
    },
    {
      name: "Employee List",
      url: "employees-list",
      icon: Users,
    },
    {
      name: "Policies",
      url: "/hr/policies",
      icon: BookOpen,
    },
    {
      name: "Resume Screener",
      url: "/hr/resume-screener",
      icon: Scan,
    },
    {
      name: "Resume Screener History",
      url: "/hr/screening-history",
      icon: ScanBarcode,
    },
    {
      name: "Applications",
      url: "/hr/applications",
      icon: FormInputIcon,
    },
    {
      name: "Announcements",
      url: "/hr/announcements",
      icon: Megaphone,
    },
    {
      name: "Payslips",
      url: "/hr/payslips",
      icon: FileText,
    },
    {
      name: "Attendance",
      url: "/hr/attendance",
      icon: CalendarCheck,
    },
  ],
};

export default HRSidebarItems;
