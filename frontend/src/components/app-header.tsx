import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuShortcut,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu";
import { Bell, User } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { useNavigate } from "react-router-dom";

export default function AppHeader() {
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout failed:', error);
      // Force navigation even if logout API fails
      navigate('/login');
    }
  };

  const getProfilePath = () => {
    const role = user?.role?.toLowerCase();
    if (role === 'hr' || role === 'admin') return '/hr/profile';
    if (role === 'manager') return '/manager/profile';
    return '/employee/profile';
  };

  const handleProfileClick = () => {
    navigate(getProfilePath());
  };

  const getOrganizationalChartPath = () => {
    const role = user?.role?.toLowerCase();
    if (role === 'hr' || role === 'admin') return '/hr/organizational-chart';
    if (role === 'manager') return '/manager/organizational-chart';
    return '/employee/organizational-chart'; // Default for employee and others
  };

  return (
    <div className="flex h-16 shrink-0 items-center justify-end px-4  gap-2 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12">


      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="outline" className="cursor-pointer" size="icon">
            <User />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="w-56" align="start">
          <DropdownMenuLabel>My Account</DropdownMenuLabel>
          <DropdownMenuGroup>
            <DropdownMenuItem onClick={handleProfileClick} className="cursor-pointer">
              Profile
              <DropdownMenuShortcut>⇧⌘P</DropdownMenuShortcut>
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => navigate(getOrganizationalChartPath())} className="cursor-pointer">
              Organizational Chart
            </DropdownMenuItem>
          </DropdownMenuGroup>
          <DropdownMenuSeparator />
          <DropdownMenuItem onClick={handleLogout} className="cursor-pointer">
            Log out
            <DropdownMenuShortcut>⇧⌘Q</DropdownMenuShortcut>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}
