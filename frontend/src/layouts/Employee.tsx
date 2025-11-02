import AppHeader from "@/components/app-header";
import { AppSidebar } from "@/components/app-sidebar";

import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { Outlet } from "react-router-dom";

const Employee = () => {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header>
          <AppHeader />
        </header>
        <hr />
        <Outlet />
        Footer
      </SidebarInset>
    </SidebarProvider>
  );
};

export default Employee;
