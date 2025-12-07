"use client";
import AppLogo from "../assets/app-logo.svg";
import * as React from "react";
import HRSidebarItems from "@/constants/HRSidebaritems";

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
              <img src={AppLogo} alt="App Logo" className="h-8 w-auto" />
              PulseTrack HRMS
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <hr />
      <SidebarContent>
        <NavItems items={HRSidebarItems.navMain} />
      </SidebarContent>
      <SidebarFooter>
        <SidebarTrigger
          className="flex items-center justify-between px-2"
                  />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
