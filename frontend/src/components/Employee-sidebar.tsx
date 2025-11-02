"use client";

import * as React from "react";
import { Book } from "lucide-react";

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
import EmployeeSidebarItems from "@/constants/EmployeeSidebarItems";

export function EmployeeSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
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
        <NavItems items={EmployeeSidebarItems} />
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
