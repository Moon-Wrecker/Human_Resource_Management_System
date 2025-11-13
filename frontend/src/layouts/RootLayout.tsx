/**
 * Root Layout
 * Wraps the entire app with AuthProvider
 */

import { Outlet } from "react-router-dom";
import { AuthProvider } from "@/contexts/AuthContext";

export default function RootLayout() {
  return (
    <AuthProvider>
      <Outlet />
    </AuthProvider>
  );
}


