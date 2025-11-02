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
  Book,
} from "lucide-react";

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { NavItems } from "./nav-projects";

const data = {
  navMain: [
    {
      name: "Dashboard",
      url: "/hr-dashboard",
      icon: PieChart,
    },
    {
      name: "Job Listings",
      url: "/joblistings",
      icon: List,
    },
    {
      name: "Employee List",
      url: "/employees-list",
      icon: Users,
    },
    {
      name: "Policies",
      url: "/hr-policies",
      icon: List,
    },
    {
      name: "Resume Screener",
      url: "/resume-screener",
      icon: Scan,
    },
    {
      name: "Announcements",
      url: "/hr-announcements",
      icon: Speaker,
    },
    {
      name: "Payslips",
      url: "/hr-payslips",
      icon: DollarSign,
    },
    {
      name: "Attendance",
      url: "/hr-attendance",
      icon: Calendar,
    }
  ],
};



export function HRSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              size="lg"
              className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
            >
              <div className="bg-sidebar-primary text-sidebar-primary-foreground flex aspect-square size-8 items-center justify-center rounded-lg">
                <Book className="size-4" />
              </div>
              PulseTrack HRMS
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <hr />
      <SidebarContent>
        <NavItems items={data.navMain} />
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenuButton size="lg" className="px-0 pl-0">
          <SidebarTrigger
            className="flex items-center justify-between px-0 pl-0 mx-0"
            withText
          />
        </SidebarMenuButton>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
