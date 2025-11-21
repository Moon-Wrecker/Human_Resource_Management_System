/**
 * Department Service - API calls for department management
 */
import api from './api';

// Types
export interface Department {
  id: number;
  name: string;
  code?: string;
  description?: string;
  head_id?: number;
  head_name?: string;
  employee_count: number;
  team_count: number;
  is_active: boolean;
  created_at: string;
}

export interface DepartmentDetail extends Department {
  teams: {
    id: number;
    name: string;
    description?: string;
    manager_id?: number;
    manager_name?: string;
    member_count: number;
  }[];
}

export interface DepartmentCreate {
  name: string;
  code?: string;
  description?: string;
  head_id?: number;
}

export interface DepartmentUpdate {
  name?: string;
  code?: string;
  description?: string;
  head_id?: number;
  is_active?: boolean;
}

export interface DepartmentListResponse {
  departments: Department[];
  total: number;
}

export interface DepartmentStats {
  total_departments: number;
  active_departments: number;
  total_employees: number;
  total_teams: number;
  departments_without_head: number;
  largest_department?: {
    id: number;
    name: string;
    employee_count: number;
  };
}

export interface DepartmentFilters {
  page?: number;
  page_size?: number;
  include_inactive?: boolean;
  search?: string;
}

// Department Service
const departmentService = {
  /**
   * Create a new department (HR only)
   */
  async createDepartment(data: DepartmentCreate): Promise<Department> {
    const response = await api.post<Department>('/departments', data);
    return response.data;
  },

  /**
   * Get all departments
   */
  async getDepartments(filters?: DepartmentFilters): Promise<DepartmentListResponse> {
    const response = await api.get<DepartmentListResponse>('/departments', { params: filters });
    return response.data;
  },

  /**
   * Get department by ID
   */
  async getDepartmentById(departmentId: number, includeTeams: boolean = false): Promise<Department | DepartmentDetail> {
    const response = await api.get<Department | DepartmentDetail>(`/departments/${departmentId}`, {
      params: { include_teams: includeTeams }
    });
    return response.data;
  },

  /**
   * Update department (HR only)
   */
  async updateDepartment(departmentId: number, data: DepartmentUpdate): Promise<Department> {
    const response = await api.put<Department>(`/departments/${departmentId}`, data);
    return response.data;
  },

  /**
   * Delete department (HR only)
   */
  async deleteDepartment(departmentId: number): Promise<{ message: string }> {
    const response = await api.delete<{ message: string }>(`/departments/${departmentId}`);
    return response.data;
  },

  /**
   * Get department statistics (HR/Manager)
   */
  async getDepartmentStats(): Promise<DepartmentStats> {
    const response = await api.get<DepartmentStats>('/departments/stats');
    return response.data;
  }
};

export default departmentService;

