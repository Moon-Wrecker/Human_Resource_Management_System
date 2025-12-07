"use client";

import * as React from "react";
import AppLogo from "../assets/app-logo.svg";

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

import ManagerSidebarItems from "@/constants/ManagerSidebarItems";

export function ManagerSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
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
                <img src={AppLogo} alt="App Logo" className="h-8 w-auto" />
              </div>
              PulseTrack HRMS
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <hr />
      <SidebarContent>
        <NavItems items={ManagerSidebarItems} />
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
