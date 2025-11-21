/**
 * Authentication Types
 * Type definitions for authentication and user data
 */

export interface User {
  id: number;
  email: string;
  name: string;
  role: UserRole;
  employee_id: string | null;
  department_id: number | null;
  job_role: string | null;
  hierarchy_level: number | null;
}

export enum UserRole {
  EMPLOYEE = 'employee',
  HR = 'hr',
  MANAGER = 'manager',
  ADMIN = 'admin',
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface ChangePasswordRequest {
  current_password: string;
  new_password: string;
}

export interface ResetPasswordRequest {
  employee_id: number;
  new_password: string;
  require_change_on_login?: boolean;
}

export interface MessageResponse {
  message: string;
}

export interface AuthContextType {
  user: User | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
  changePassword: (currentPassword: string, newPassword: string) => Promise<void>;
}


