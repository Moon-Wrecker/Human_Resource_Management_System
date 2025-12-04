import AppHeader from "@/components/app-header";
import { ManagerSidebar } from "@/components/Manager-sidebar";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { Outlet } from "react-router-dom";

const Manager = () => {
  return (
    <SidebarProvider>
      <ManagerSidebar />
      <SidebarInset>
        <header>
          <AppHeader />
        </header>
        <hr />
        <Outlet />
      </SidebarInset>
    </SidebarProvider>
  );
};

export default Manager;

