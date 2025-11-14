/**
 * Team Requests Service
 * API service for managing team requests and approvals
 */

import api from './api';

// Types
export type RequestType = 'wfh' | 'leave' | 'equipment' | 'travel' | 'other';
export type RequestStatus = 'pending' | 'approved' | 'rejected';

export interface RequestCreate {
  request_type: RequestType;
  subject: string;
  description: string;
  request_date?: string; // ISO date format (YYYY-MM-DD)
}

export interface RequestUpdate {
  subject?: string;
  description?: string;
  request_date?: string;
}

export interface RequestStatusUpdate {
  status: RequestStatus;
  rejection_reason?: string; // Required when rejecting
}

export interface TeamRequest {
  id: number;
  employee_id: number;
  employee_name: string | null;
  
  // Request details
  request_type: string;
  subject: string;
  description: string;
  request_date: string | null;
  
  // Approval workflow
  status: string;
  approved_by: number | null;
  approved_by_name: string | null;
  approved_date: string | null;
  rejection_reason: string | null;
  
  // Timestamps
  submitted_date: string;
}

export interface RequestListResponse {
  requests: TeamRequest[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface RequestStatsResponse {
  total_requests: number;
  pending_requests: number;
  approved_requests: number;
  rejected_requests: number;
  by_request_type: Record<string, number>;
  by_status: Record<string, number>;
  by_month: Record<string, number>;
}

export interface RequestFilters {
  request_type?: string;
  status?: string;
  employee_id?: number;
  search?: string;
  page?: number;
  page_size?: number;
}

class RequestService {
  /**
   * Submit a new request
   */
  async submitRequest(data: RequestCreate): Promise<TeamRequest> {
    const response = await api.post('/requests', data);
    return response.data;
  }

  /**
   * Get my requests (current user's requests)
   */
  async getMyRequests(filters?: RequestFilters): Promise<RequestListResponse> {
    const response = await api.get('/requests/me', { params: filters });
    return response.data;
  }

  /**
   * Get team requests (Manager)
   */
  async getTeamRequests(filters?: RequestFilters): Promise<RequestListResponse> {
    const response = await api.get('/requests/team', { params: filters });
    return response.data;
  }

  /**
   * Get all requests (HR)
   */
  async getAllRequests(filters?: RequestFilters): Promise<RequestListResponse> {
    const response = await api.get('/requests/all', { params: filters });
    return response.data;
  }

  /**
   * Get request by ID
   */
  async getRequestById(requestId: number): Promise<TeamRequest> {
    const response = await api.get(`/requests/${requestId}`);
    return response.data;
  }

  /**
   * Update request (Employee, only pending requests)
   */
  async updateRequest(
    requestId: number,
    data: RequestUpdate
  ): Promise<TeamRequest> {
    const response = await api.put(`/requests/${requestId}`, data);
    return response.data;
  }

  /**
   * Approve or reject request (Manager/HR)
   */
  async updateRequestStatus(
    requestId: number,
    data: RequestStatusUpdate
  ): Promise<TeamRequest> {
    const response = await api.put(`/requests/${requestId}/status`, data);
    return response.data;
  }

  /**
   * Delete request (Employee, only pending requests)
   */
  async deleteRequest(requestId: number): Promise<{ message: string }> {
    const response = await api.delete(`/requests/${requestId}`);
    return response.data;
  }

  /**
   * Get request statistics
   */
  async getRequestStatistics(): Promise<RequestStatsResponse> {
    const response = await api.get('/requests/stats');
    return response.data;
  }

  // Helper methods

  /**
   * Get request type display name
   */
  getRequestTypeLabel(type: string): string {
    const labels: Record<string, string> = {
      wfh: 'Work From Home',
      leave: 'Leave Request',
      equipment: 'Equipment Request',
      travel: 'Travel Request',
      other: 'Other Request'
    };
    return labels[type] || type;
  }

  /**
   * Get status color for UI
   */
  getStatusColor(status: string): string {
    const colors: Record<string, string> = {
      pending: 'yellow',
      approved: 'blue',
      rejected: 'red'
    };
    return colors[status] || 'gray';
  }

  /**
   * Format date for display
   */
  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }

  /**
   * Format datetime for display
   */
  formatDateTime(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  /**
   * Check if request can be edited
   */
  canEditRequest(request: TeamRequest, userId: number): boolean {
    return (
      request.employee_id === userId &&
      request.status === 'pending'
    );
  }

  /**
   * Check if request can be deleted
   */
  canDeleteRequest(request: TeamRequest, userId: number): boolean {
    return (
      request.employee_id === userId &&
      request.status === 'pending'
    );
  }

  /**
   * Check if request can be approved/rejected
   */
  canApproveRejectRequest(request: TeamRequest, userRole: string): boolean {
    return (
      request.status === 'pending' &&
      (userRole === 'manager' || userRole === 'hr')
    );
  }

  /**
   * Approve a request (convenience method)
   */
  async approveRequest(requestId: number): Promise<TeamRequest> {
    return this.updateRequestStatus(requestId, { status: 'approved' });
  }

  /**
   * Reject a request (convenience method)
   */
  async rejectRequest(
    requestId: number,
    rejectionReason: string
  ): Promise<TeamRequest> {
    return this.updateRequestStatus(requestId, {
      status: 'rejected',
      rejection_reason: rejectionReason
    });
  }
}

export default new RequestService();

