/**
 * Leave Management Service - API calls for leave requests and balance
 */
import api from './api';

// Types
export interface LeaveRequestCreate {
  leave_type: 'casual' | 'sick' | 'annual' | 'maternity' | 'paternity';
  start_date: string;  // Format: YYYY-MM-DD
  end_date: string;    // Format: YYYY-MM-DD
  subject?: string;
  reason?: string;
  description?: string;
}

export interface LeaveRequestUpdate {
  start_date?: string;
  end_date?: string;
  subject?: string;
  reason?: string;
  description?: string;
}

export interface LeaveStatusUpdate {
  status: 'approved' | 'rejected';
  rejection_reason?: string;
}

export interface LeaveRequest {
  id: number;
  employee_id: number;
  employee_name?: string;
  
  // Leave details
  leave_type: string;
  start_date: string;
  end_date: string;
  days_requested: number;
  
  // Request details
  subject?: string;
  reason?: string;
  description?: string;
  
  // Approval workflow
  status: string;
  approved_by?: number;
  approved_by_name?: string;
  approved_date?: string;
  rejection_reason?: string;
  
  // Timestamps
  requested_date: string;
}

export interface LeaveBalance {
  employee_id: number;
  employee_name: string;
  casual_leave_balance: number;
  sick_leave_balance: number;
  annual_leave_balance: number;
  wfh_balance: number;
}

export interface LeaveListResponse {
  leaves: LeaveRequest[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface LeaveStats {
  total_requests: number;
  pending_requests: number;
  approved_requests: number;
  rejected_requests: number;
  by_leave_type: Record<string, number>;
  by_status: Record<string, number>;
  by_month: Record<string, number>;
}

export interface LeaveFilters {
  page?: number;
  page_size?: number;
  status?: string;
  leave_type?: string;
  employee_id?: number;
}

// Leave Service
const leaveService = {
  /**
   * Apply for leave (employee)
   */
  async applyForLeave(data: LeaveRequestCreate): Promise<LeaveRequest> {
    const response = await api.post<LeaveRequest>('/leaves', data);
    return response.data;
  },

  /**
   * Get my leave requests (employee)
   */
  async getMyLeaveRequests(filters?: LeaveFilters): Promise<LeaveListResponse> {
    const response = await api.get<LeaveListResponse>('/leaves/me', { params: filters });
    return response.data;
  },

  /**
   * Get team leave requests (manager)
   */
  async getTeamLeaveRequests(filters?: LeaveFilters): Promise<LeaveListResponse> {
    const response = await api.get<LeaveListResponse>('/leaves/team', { params: filters });
    return response.data;
  },

  /**
   * Get all leave requests (HR)
   */
  async getAllLeaveRequests(filters?: LeaveFilters): Promise<LeaveListResponse> {
    const response = await api.get<LeaveListResponse>('/leaves/all', { params: filters });
    return response.data;
  },

  /**
   * Get my leave balance (employee)
   */
  async getMyLeaveBalance(): Promise<LeaveBalance> {
    const response = await api.get<LeaveBalance>('/leaves/balance/me');
    return response.data;
  },

  /**
   * Get employee leave balance (HR/Manager)
   */
  async getEmployeeLeaveBalance(employeeId: number): Promise<LeaveBalance> {
    const response = await api.get<LeaveBalance>(`/leaves/balance/${employeeId}`);
    return response.data;
  },

  /**
   * Get leave request by ID
   */
  async getLeaveRequestById(leaveId: number): Promise<LeaveRequest> {
    const response = await api.get<LeaveRequest>(`/leaves/${leaveId}`);
    return response.data;
  },

  /**
   * Update leave request (employee, only if pending)
   */
  async updateLeaveRequest(leaveId: number, data: LeaveRequestUpdate): Promise<LeaveRequest> {
    const response = await api.put<LeaveRequest>(`/leaves/${leaveId}`, data);
    return response.data;
  },

  /**
   * Approve or reject leave (manager/HR)
   */
  async updateLeaveStatus(leaveId: number, data: LeaveStatusUpdate): Promise<LeaveRequest> {
    const response = await api.patch<LeaveRequest>(`/leaves/${leaveId}/status`, data);
    return response.data;
  },

  /**
   * Cancel leave request (employee, only if pending)
   */
  async cancelLeaveRequest(leaveId: number): Promise<{ message: string }> {
    const response = await api.delete<{ message: string }>(`/leaves/${leaveId}`);
    return response.data;
  },

  /**
   * Get leave statistics (HR/Manager)
   */
  async getLeaveStats(): Promise<LeaveStats> {
    const response = await api.get<LeaveStats>('/leaves/stats/summary');
    return response.data;
  }
};

export default leaveService;

