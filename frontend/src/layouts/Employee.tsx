import AppHeader from "@/components/app-header";
import { EmployeeSidebar } from "@/components/Employee-sidebar";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { Outlet } from "react-router-dom";

const Employee = () => {
  return (
    <SidebarProvider>
      <EmployeeSidebar />
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

export default Employee;
