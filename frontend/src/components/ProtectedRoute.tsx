/**
 * Protected Route Component
 * Wraps routes that require authentication
 */

import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import type { UserRole } from '@/types/auth';

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles?: UserRole[] | string[];
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  allowedRoles 
}) => {
  const { user, isAuthenticated, isLoading } = useAuth();

  // Show loading state while checking authentication
  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"></div>
          <p className="mt-4 text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated || !user) {
    return <Navigate to="/login" replace />;
  }

  // Check role-based access if roles are specified
  if (allowedRoles && allowedRoles.length > 0) {
    const userRole = user.role.toLowerCase();
    const hasAccess = allowedRoles.some(
      (role) => role.toLowerCase() === userRole
    );

    if (!hasAccess) {
      // Redirect to user's appropriate dashboard
      const defaultRoutes: Record<string, string> = {
        hr: '/hr',
        manager: '/manager',
        employee: '/employee',
        admin: '/hr',
      };
      
      const redirectRoute = defaultRoutes[userRole] || '/';
      return <Navigate to={redirectRoute} replace />;
    }
  }

  return <>{children}</>;
};

export default ProtectedRoute;


