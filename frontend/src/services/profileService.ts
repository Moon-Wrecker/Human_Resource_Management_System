/**
 * Profile Service
 * API calls for profile management
 */

import api, { handleApiError } from './api';

export interface ProfileData {
  id: number;
  name: string;
  email: string;
  phone?: string;
  employee_id?: string;
  role: string;
  job_role?: string;
  job_level?: string;
  hierarchy_level?: number;
  hire_date?: string;
  salary?: number;
  department_id?: number;
  department_name?: string;
  team_id?: number;
  team_name?: string;
  manager_id?: number;
  manager_name?: string;
  manager_email?: string;
  casual_leave_balance: number;
  sick_leave_balance: number;
  annual_leave_balance: number;
  wfh_balance: number;
  profile_image_path?: string;
  profile_image_url?: string;
  aadhar_document_path?: string;
  aadhar_document_url?: string;
  pan_document_path?: string;
  pan_document_url?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface UpdateProfileData {
  name?: string;
  phone?: string;
}

export interface DocumentUploadResponse {
  message: string;
  document_type: string;
  file_path: string;
  file_url: string;
  uploaded_at: string;
}

export interface UserDocuments {
  profile_image?: {
    path: string;
    url: string;
    uploaded_at: string;
  };
  aadhar_card?: {
    path: string;
    url: string;
    uploaded_at: string;
  };
  pan_card?: {
    path: string;
    url: string;
    uploaded_at: string;
  };
}

export interface ManagerInfo {
  id: number;
  name: string;
  email: string;
  phone?: string;
  employee_id?: string;
  job_role?: string;
  department_name?: string;
  profile_image_url?: string;
}

export interface TeamMember {
  id: number;
  name: string;
  email: string;
  employee_id?: string;
  job_role?: string;
  job_level?: string;
  phone?: string;
  profile_image_url?: string;
  is_active: boolean;
}

export interface TeamData {
  team_id?: number;
  team_name?: string;
  department_name?: string;
  total_members: number;
  members: TeamMember[];
}

export interface ProfileStats {
  total_goals: number;
  completed_goals: number;
  in_progress_goals: number;
  total_skill_modules: number;
  completed_skill_modules: number;
  total_training_hours: number;
  attendance_percentage: number;
  leaves_taken_this_year: number;
}

class ProfileService {
  /**
   * Get current user's profile
   */
  async getMyProfile(): Promise<ProfileData> {
    try {
      const response = await api.get('/profile/me');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get user profile by ID (HR/Manager only)
   */
  async getUserProfile(userId: number): Promise<ProfileData> {
    try {
      const response = await api.get(`/profile/${userId}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Update current user's profile
   */
  async updateMyProfile(data: UpdateProfileData): Promise<ProfileData> {
    try {
      const response = await api.put('/profile/me', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Upload profile image
   */
  async uploadProfileImage(file: File): Promise<DocumentUploadResponse> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await api.post('/profile/upload-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Upload document (Aadhar or PAN)
   */
  async uploadDocument(documentType: 'aadhar' | 'pan', file: File): Promise<DocumentUploadResponse> {
    try {
      const formData = new FormData();
      formData.append('document_type', documentType);
      formData.append('file', file);

      const response = await api.post('/profile/upload-document', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get user's uploaded documents
   */
  async getMyDocuments(): Promise<UserDocuments> {
    try {
      const response = await api.get('/profile/documents');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Delete a document
   */
  async deleteDocument(documentType: 'profile_image' | 'aadhar' | 'pan'): Promise<{ message: string }> {
    try {
      const response = await api.delete(`/profile/documents/${documentType}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get manager information
   */
  async getMyManager(): Promise<ManagerInfo> {
    try {
      const response = await api.get('/profile/manager');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get team members
   */
  async getMyTeam(): Promise<TeamData> {
    try {
      const response = await api.get('/profile/team');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get team by manager ID (HR only)
   */
  async getTeamByManager(managerId: number): Promise<TeamData> {
    try {
      const response = await api.get(`/profile/team/${managerId}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get profile statistics
   */
  async getMyStats(): Promise<ProfileStats> {
    try {
      const response = await api.get('/profile/stats');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get user statistics by ID (HR/Manager only)
   */
  async getUserStats(userId: number): Promise<ProfileStats> {
    try {
      const response = await api.get(`/profile/stats/${userId}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }
}

export default new ProfileService();

// Explicit type exports for better TypeScript support
export type {
  ProfileData,
  UpdateProfileData,
  DocumentUploadResponse,
  UserDocuments,
  ManagerInfo,
  TeamMember,
  TeamData,
  ProfileStats
};

