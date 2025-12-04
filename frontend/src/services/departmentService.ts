/**
 * Department Service
 * API calls for department management
 */
import api from './api';

// ===== TYPE DEFINITIONS =====

export type Department = {
  id: number;
  name: string;
  code?: string;
  head_of_department_id?: number;
  head_of_department_name?: string;
  employee_count?: number;
  team_count?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
};

export type DepartmentListResponse = {
  departments: Department[];
  total: number;
};

// ===== SERVICE CLASS =====

class DepartmentService {
  /**
   * Get all departments
   */
  async getAllDepartments(): Promise<DepartmentListResponse> {
    const response = await api.get('/departments');
    return response.data;
  }
}

// Export singleton instance
const departmentService = new DepartmentService();
export default departmentService;