"use client";

import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { Book } from "lucide-react";

export function TeamSwitcher() {
  return (
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
  );
}
