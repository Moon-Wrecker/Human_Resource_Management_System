"use client";

import * as React from "react";

import { NavItems } from "@/components/nav-projects";
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
import AppLogo from "../assets/app-logo.svg";

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              size="lg"
              className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
            >
              <img src={AppLogo} alt="App Logo" className="h-8 w-auto" />
              PulseTrack HRMS
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <hr />
      <SidebarContent>
        <NavItems items={EmployeeSidebarItems} />
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenuButton size="lg" className="px-0 pl-0">
          <SidebarTrigger
            className="flex items-center justify-between px-0 pl-0 mx-0"
          />
        </SidebarMenuButton>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
