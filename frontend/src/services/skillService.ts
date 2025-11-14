/**
 * Skills/Modules Service - API calls for skill development and module management
 */
import api from './api';

// Types
export interface SkillModuleCreate {
  name: string;
  description?: string;
  category?: string;
  module_link?: string;
  duration_hours?: number;
  difficulty_level?: 'beginner' | 'intermediate' | 'advanced';
  skill_areas?: string;
  is_active?: boolean;
}

export interface SkillModuleUpdate {
  name?: string;
  description?: string;
  category?: string;
  module_link?: string;
  duration_hours?: number;
  difficulty_level?: 'beginner' | 'intermediate' | 'advanced';
  skill_areas?: string;
  is_active?: boolean;
}

export interface SkillModule {
  id: number;
  name: string;
  description?: string;
  category?: string;
  module_link?: string;
  duration_hours?: number;
  difficulty_level?: string;
  skill_areas?: string;
  is_active: boolean;
  created_at: string;
  
  // Enrollment stats
  total_enrollments?: number;
  completed_count?: number;
}

export interface SkillModuleListResponse {
  modules: SkillModule[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface EnrollmentCreate {
  module_id: number;
  target_completion_date?: string;  // Format: YYYY-MM-DD
}

export interface EnrollmentProgressUpdate {
  progress_percentage: number;  // 0-100
  status?: 'not_started' | 'pending' | 'completed';
}

export interface EnrollmentComplete {
  score?: number;  // 0-100
  certificate_path?: string;
}

export interface Enrollment {
  id: number;
  employee_id: number;
  employee_name?: string;
  module_id: number;
  module_name?: string;
  
  // Progress tracking
  status: string;
  progress_percentage: number;
  enrolled_date: string;
  started_date?: string;
  completed_date?: string;
  target_completion_date?: string;
  
  // Results
  certificate_path?: string;
  score?: number;
  
  created_at: string;
}

export interface MyEnrollment {
  id: number;
  module_id: number;
  module_name: string;
  module_description?: string;
  module_link?: string;
  category?: string;
  duration_hours?: number;
  difficulty_level?: string;
  
  // My progress
  status: string;
  progress_percentage: number;
  enrolled_date: string;
  started_date?: string;
  completed_date?: string;
  target_completion_date?: string;
  score?: number;
  certificate_path?: string;
}

export interface EnrollmentListResponse {
  enrollments: Enrollment[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface SkillStats {
  total_modules: number;
  active_modules: number;
  total_enrollments: number;
  completed_enrollments: number;
  in_progress_enrollments: number;
  by_category: Record<string, number>;
  by_difficulty: Record<string, number>;
  by_status: Record<string, number>;
  average_completion_rate: number;
}

export interface ModuleFilters {
  page?: number;
  page_size?: number;
  search?: string;
  category?: string;
  difficulty?: string;
  include_inactive?: boolean;
}

export interface EnrollmentFilters {
  page?: number;
  page_size?: number;
  employee_id?: number;
  module_id?: number;
  status?: string;
}

// Skill Service
const skillService = {
  // ========== Module Management (HR Only) ==========
  
  /**
   * Create new skill module (HR only)
   */
  async createModule(data: SkillModuleCreate): Promise<SkillModule> {
    const response = await api.post<SkillModule>('/skills/modules', data);
    return response.data;
  },

  /**
   * Get all skill modules with filters
   */
  async getModules(filters?: ModuleFilters): Promise<SkillModuleListResponse> {
    const response = await api.get<SkillModuleListResponse>('/skills/modules', { params: filters });
    return response.data;
  },

  /**
   * Get module by ID
   */
  async getModuleById(moduleId: number): Promise<SkillModule> {
    const response = await api.get<SkillModule>(`/skills/modules/${moduleId}`);
    return response.data;
  },

  /**
   * Update skill module (HR only)
   */
  async updateModule(moduleId: number, data: SkillModuleUpdate): Promise<SkillModule> {
    const response = await api.put<SkillModule>(`/skills/modules/${moduleId}`, data);
    return response.data;
  },

  /**
   * Delete skill module (HR only)
   */
  async deleteModule(moduleId: number): Promise<{ message: string }> {
    const response = await api.delete<{ message: string }>(`/skills/modules/${moduleId}`);
    return response.data;
  },

  // ========== Enrollment Management (Employee) ==========
  
  /**
   * Enroll in a skill module (employee)
   */
  async enrollInModule(data: EnrollmentCreate): Promise<Enrollment> {
    const response = await api.post<Enrollment>('/skills/enroll', data);
    return response.data;
  },

  /**
   * Get my enrollments (employee)
   */
  async getMyEnrollments(filters?: { page?: number; page_size?: number; status?: string }): Promise<MyEnrollment[]> {
    const response = await api.get<MyEnrollment[]>('/skills/my-enrollments', { params: filters });
    return response.data;
  },

  /**
   * Get all enrollments (HR)
   */
  async getAllEnrollments(filters?: EnrollmentFilters): Promise<EnrollmentListResponse> {
    const response = await api.get<EnrollmentListResponse>('/skills/enrollments', { params: filters });
    return response.data;
  },

  /**
   * Update enrollment progress (employee)
   */
  async updateEnrollmentProgress(enrollmentId: number, data: EnrollmentProgressUpdate): Promise<Enrollment> {
    const response = await api.put<Enrollment>(`/skills/enrollments/${enrollmentId}/progress`, data);
    return response.data;
  },

  /**
   * Mark enrollment as complete (employee)
   */
  async markEnrollmentComplete(enrollmentId: number, data: EnrollmentComplete): Promise<Enrollment> {
    const response = await api.patch<Enrollment>(`/skills/enrollments/${enrollmentId}/complete`, data);
    return response.data;
  },

  /**
   * Get skills statistics (HR)
   */
  async getSkillStats(): Promise<SkillStats> {
    const response = await api.get<SkillStats>('/skills/stats');
    return response.data;
  }
};

export default skillService;

