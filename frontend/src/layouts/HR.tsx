import { HRSidebar } from "@/components/HR-sidebar";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { Outlet } from "react-router-dom";

const HR = () => {
  return (
    <SidebarProvider>
      <HRSidebar />
      <SidebarInset>
        <Outlet /> Footer
      </SidebarInset>
    </SidebarProvider>
  );
};

export default HR;
