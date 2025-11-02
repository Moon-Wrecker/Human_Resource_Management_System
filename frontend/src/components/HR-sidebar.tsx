"use client";

import * as React from "react";
import {
  List,
  PieChart,
  Users,
  Calendar,
  DollarSign,
  Speaker,
  Scan,
} from "lucide-react";

import { NavMain } from "@/components/nav-main";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenuButton,
  SidebarRail,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { TeamSwitcher } from "./team-switcher";

const data = {
  navMain: [
    {
      title: "Dashboard",
      url: "/hr-dashboard",
      icon: PieChart,
    },
    {
      title: "Job Listings",
      url:"/joblistings",
      icon: List,
    },
    {
      title: "Employee List",
      url: "/employees-list",
      icon: Users,
    },
    {
      title: "Policies",
      url:"/hr-policies",
      icon: List,
    },
    {
      title: "Resume Screener",
      url: "/resume-screener",
      icon: Scan,
    },
    {
      title: "Announcements",
      url:"/hr-announcements",
      icon: Speaker,
    },
    {
      title: "Payslips",
      url: "/hr-payslips",
      icon: DollarSign,
    },
    {
      title: "Attendance",
      url:"/hr-attendance",
      icon: Calendar,
    }
  ],
};

export function HRSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <TeamSwitcher />
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={data.navMain} />
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenuButton size="lg">
          <div className=" flex aspect-square size-8 items-center justify-center rounded-lg">
            <SidebarTrigger />
          </div>
          Collapse Sidebar
        </SidebarMenuButton>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
