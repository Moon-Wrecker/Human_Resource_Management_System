/**
 * Authentication Service
 * Handles all authentication-related API calls
 */

import api, { handleApiError } from './api';
import { API_ENDPOINTS } from '@/config/api';
import type {
  LoginRequest,
  LoginResponse,
  TokenResponse,
  RefreshTokenRequest,
  ChangePasswordRequest,
  ResetPasswordRequest,
  MessageResponse,
  User,
} from '@/types/auth';

class AuthService {
  /**
   * Login user with email and password
   */
  async login(email: string, password: string): Promise<LoginResponse> {
    try {
      const response = await api.post<LoginResponse>(
        API_ENDPOINTS.AUTH.LOGIN,
        { email, password } as LoginRequest
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Logout user (client-side)
   */
  async logout(): Promise<MessageResponse> {
    try {
      const response = await api.post<MessageResponse>(API_ENDPOINTS.AUTH.LOGOUT);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Refresh access token using refresh token
   */
  async refreshToken(refreshToken: string): Promise<TokenResponse> {
    try {
      const response = await api.post<TokenResponse>(
        API_ENDPOINTS.AUTH.REFRESH,
        { refresh_token: refreshToken } as RefreshTokenRequest
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get current authenticated user
   */
  async getCurrentUser(): Promise<User> {
    try {
      const response = await api.get<User>(API_ENDPOINTS.AUTH.ME);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Change current user's password
   */
  async changePassword(
    currentPassword: string,
    newPassword: string
  ): Promise<MessageResponse> {
    try {
      const response = await api.post<MessageResponse>(
        API_ENDPOINTS.AUTH.CHANGE_PASSWORD,
        {
          current_password: currentPassword,
          new_password: newPassword,
        } as ChangePasswordRequest
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Reset employee password (HR/Manager only)
   */
  async resetPassword(
    employeeId: number,
    newPassword: string,
    requireChangeOnLogin: boolean = true
  ): Promise<MessageResponse> {
    try {
      const response = await api.post<MessageResponse>(
        API_ENDPOINTS.AUTH.RESET_PASSWORD,
        {
          employee_id: employeeId,
          new_password: newPassword,
          require_change_on_login: requireChangeOnLogin,
        } as ResetPasswordRequest
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Store authentication data in localStorage
   */
  storeAuthData(data: LoginResponse): void {
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    localStorage.setItem('user', JSON.stringify(data.user));
  }

  /**
   * Clear authentication data from localStorage
   */
  clearAuthData(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  }

  /**
   * Get stored user from localStorage
   */
  getStoredUser(): User | null {
    const userStr = localStorage.getItem('user');
    if (!userStr) return null;
    
    try {
      return JSON.parse(userStr) as User;
    } catch {
      return null;
    }
  }

  /**
   * Get stored access token
   */
  getStoredAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  /**
   * Get stored refresh token
   */
  getStoredRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    const token = this.getStoredAccessToken();
    const user = this.getStoredUser();
    return !!(token && user);
  }
}

export default new AuthService();


