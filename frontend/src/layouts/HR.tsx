import AppHeader from "@/components/app-header";
import { HRSidebar } from "@/components/HR-sidebar";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { Outlet } from "react-router-dom";

const HR = () => {
  return (
    <SidebarProvider>
      <HRSidebar />
      <SidebarInset>
        <AppHeader />
        <hr />
        <Outlet />
      </SidebarInset>
    </SidebarProvider>
  );
};

export default HR;
