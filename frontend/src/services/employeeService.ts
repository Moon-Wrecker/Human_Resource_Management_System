/**
 * Employee Management Service - API calls for employee management (HR only)
 */
import api from './api';

// Types
export interface EmployeeCreate {
  // Basic Info
  name: string;
  email: string;
  password: string;
  phone?: string;
  
  // Work Info
  employee_id?: string;
  position?: string;
  department_id?: number;
  team_id?: number;
  manager_id?: number;
  
  // Role & Hierarchy
  role?: 'employee' | 'manager' | 'hr' | 'admin';
  hierarchy_level?: number;
  
  // Dates
  date_of_birth?: string;  // Format: YYYY-MM-DD
  join_date?: string;       // Format: YYYY-MM-DD
  
  // Compensation
  salary?: number;
  
  // Emergency Contact
  emergency_contact?: string;
  
  // Leave Balances
  casual_leave_balance?: number;
  sick_leave_balance?: number;
  annual_leave_balance?: number;
  wfh_balance?: number;
}

export interface EmployeeUpdate {
  // Basic Info
  name?: string;
  email?: string;
  phone?: string;
  
  // Work Info
  employee_id?: string;
  position?: string;
  department_id?: number;
  team_id?: number;
  manager_id?: number;
  
  // Role & Hierarchy
  role?: string;
  hierarchy_level?: number;
  
  // Dates
  date_of_birth?: string;
  join_date?: string;
  
  // Compensation
  salary?: number;
  
  // Status
  is_active?: boolean;
  
  // Emergency Contact
  emergency_contact?: string;
  
  // Leave Balances
  casual_leave_balance?: number;
  sick_leave_balance?: number;
  annual_leave_balance?: number;
  wfh_balance?: number;
}

export interface EmployeeResponse {
  id: number;
  employee_id?: string;
  name: string;
  email: string;
  phone?: string;
  
  // Work Info
  position?: string;
  department?: string;
  department_id?: number;
  team?: string;
  team_id?: number;
  manager?: string;
  manager_id?: number;
  
  // Role & Status
  role: string;
  hierarchy_level?: number;
  is_active: boolean;
  
  // Dates
  date_of_birth?: string;
  join_date?: string;
  created_at: string;
  
  // Compensation
  salary?: number;
  
  // Documents
  aadhar_document_path?: string;
  pan_document_path?: string;
  profile_image_path?: string;
  
  // Leave Balances
  casual_leave_balance: number;
  sick_leave_balance: number;
  annual_leave_balance: number;
  wfh_balance: number;
}

export interface EmployeeListItem {
  id: number;
  employee_id?: string;
  name: string;
  email: string;
  phone?: string;
  position?: string;
  department?: string;
  team?: string;
  manager?: string;
  role: string;
  is_active: boolean;
  join_date?: string;
}

export interface EmployeeListResponse {
  employees: EmployeeListItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface EmployeeStats {
  total_employees: number;
  active_employees: number;
  inactive_employees: number;
  by_department: Record<string, number>;
  by_role: Record<string, number>;
  by_team: Record<string, number>;
  recent_hires: number;
  average_tenure_days: number;
}

export interface EmployeeFilters {
  page?: number;
  page_size?: number;
  search?: string;
  department_id?: number;
  team_id?: number;
  role?: string;
  is_active?: boolean;
}

// Employee Service
const employeeService = {
  /**
   * Create a new employee (HR only)
   */
  async createEmployee(data: EmployeeCreate): Promise<EmployeeResponse> {
    const response = await api.post<EmployeeResponse>('/employees', data);
    return response.data;
  },

  /**
   * Get all employees with filters (HR only)
   */
  async getEmployees(filters?: EmployeeFilters): Promise<EmployeeListResponse> {
    const response = await api.get<EmployeeListResponse>('/employees', { params: filters });
    return response.data;
  },

  /**
   * Get employee by ID (HR only)
   */
  async getEmployeeById(employeeId: number): Promise<EmployeeResponse> {
    const response = await api.get<EmployeeResponse>(`/employees/${employeeId}`);
    return response.data;
  },

  /**
   * Update employee (HR only)
   */
  async updateEmployee(employeeId: number, data: EmployeeUpdate): Promise<EmployeeResponse> {
    const response = await api.put<EmployeeResponse>(`/employees/${employeeId}`, data);
    return response.data;
  },

  /**
   * Deactivate employee (HR only)
   */
  async deactivateEmployee(employeeId: number): Promise<{ message: string }> {
    const response = await api.delete<{ message: string }>(`/employees/${employeeId}`);
    return response.data;
  },

  /**
   * Get employee statistics (HR only)
   */
  async getEmployeeStats(): Promise<EmployeeStats> {
    const response = await api.get<EmployeeStats>('/employees/stats');
    return response.data;
  }
};

export default employeeService;

