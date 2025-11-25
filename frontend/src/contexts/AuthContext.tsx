/**
 * Authentication Context
 * Provides authentication state and methods throughout the app
 */

import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import authService from '@/services/authService';
import type { User, AuthContextType } from '@/types/auth';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  // Initialize auth state from localStorage
  useEffect(() => {
    const initAuth = () => {
      const storedUser = authService.getStoredUser();
      const storedToken = authService.getStoredAccessToken();

      if (storedUser && storedToken) {
        setUser(storedUser);
        setAccessToken(storedToken);
        
        // Verify token is still valid by fetching current user
        authService
          .getCurrentUser()
          .then((currentUser) => {
            setUser(currentUser);
            // Update stored user if data changed
            localStorage.setItem('user', JSON.stringify(currentUser));
          })
          .catch(() => {
            // Token invalid, clear auth data
            handleLogout();
          });
      }
      
      setIsLoading(false);
    };

    initAuth();
  }, []);

  /**
   * Login user
   */
  const login = async (email: string, password: string): Promise<void> => {
    try {
      setIsLoading(true);
      const response = await authService.login(email, password);
      
      // Store auth data
      authService.storeAuthData(response);
      
      // Update state
      setUser(response.user);
      setAccessToken(response.access_token);
      
      // Navigate based on role
      navigateByRole(response.user.role);
    } catch (error) {
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Logout user
   */
  const logout = async () => {
    try {
      await authService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      handleLogout();
    }
  };

  /**
   * Handle logout cleanup
   */
  const handleLogout = () => {
    authService.clearAuthData();
    setUser(null);
    setAccessToken(null);
    navigate('/login');
  };

  /**
   * Refresh access token
   */
  const refreshToken = async (): Promise<void> => {
    try {
      const storedRefreshToken = authService.getStoredRefreshToken();
      
      if (!storedRefreshToken) {
        throw new Error('No refresh token available');
      }
      
      const response = await authService.refreshToken(storedRefreshToken);
      
      // Update tokens
      localStorage.setItem('access_token', response.access_token);
      if (response.refresh_token) {
        localStorage.setItem('refresh_token', response.refresh_token);
      }
      
      setAccessToken(response.access_token);
    } catch (error) {
      handleLogout();
      throw error;
    }
  };

  /**
   * Change password
   */
  const changePassword = async (
    currentPassword: string,
    newPassword: string
  ): Promise<void> => {
    try {
      await authService.changePassword(currentPassword, newPassword);
    } catch (error) {
      throw error;
    }
  };

  /**
   * Navigate user based on their role
   */
  const navigateByRole = (role: string) => {
    const roleRoutes: Record<string, string> = {
      hr: '/hr',
      manager: '/manager',
      employee: '/employee',
      admin: '/hr', // Default admins to HR dashboard
    };
    
    const route = roleRoutes[role.toLowerCase()] || '/employee';
    navigate(route);
  };

  const value: AuthContextType = {
    user,
    accessToken,
    isAuthenticated: !!user && !!accessToken,
    isLoading,
    login,
    logout,
    refreshToken,
    changePassword,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

/**
 * Hook to use auth context
 */
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};

