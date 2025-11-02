"use client";

import * as React from "react";
import {
  List,
  PieChart,
  Users,
  BookOpen,
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
      url: "#",
      icon: PieChart,
      isActive: true,
    },
    {
      title: "Job Listings",
      url:"#",
      icon: List,
      isActive: false,
    },
    {
      title: "Employee List",
      url: "#",
      icon: Users,
      isActive: true,
    },
    {
      title: "Policies",
      url:"#",
      icon: BookOpen,
      isActive: false,
    },
    {
      title: "Resume Screener",
      url: "#",
      icon: PieChart,
      isActive: true,
    },
    {
      title: "Announcements",
      url:"#",
      icon: List,
      isActive: false,
    },
    {
      title: "Payslips",
      url: "employee-payslips",
      icon: PieChart,
      isActive: true,
    },
    {
      title: "Attendance",
      url:"#",
      icon: List,
      isActive: false,
    }
  ],
};

export function EmployeeSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
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