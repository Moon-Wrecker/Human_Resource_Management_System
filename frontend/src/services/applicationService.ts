/**
 * Service for job applications management
 */
import api from './api';

// Type definitions (using 'type' for better ES module compatibility)
export type ApplicationStatus = 'pending' | 'reviewed' | 'shortlisted' | 'rejected' | 'hired';
export type ApplicationSource = 'self-applied' | 'referral' | 'recruitment' | 'internal';

export type CreateApplicationRequest = {
  job_id: number;
  applicant_name: string;
  applicant_email: string;
  applicant_phone?: string;
  cover_letter?: string;
  source?: ApplicationSource;
  referred_by?: number;
};

export type UpdateApplicationStatusRequest = {
  status: ApplicationStatus;
  screening_notes?: string;
  screening_score?: number;
};

export type ApplicationResponse = {
  id: number;
  job_id: number;
  job_position?: string;
  job_department?: string;
  applicant_id?: number;
  applicant_name: string;
  applicant_email: string;
  applicant_phone?: string;
  resume_path?: string;
  cover_letter?: string;
  source: string;
  referred_by?: number;
  referrer_name?: string;
  status: string;
  screening_score?: number;
  screening_notes?: string;
  applied_date: string;
  reviewed_date?: string;
};

export type ApplicationsListResponse = {
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  applications: ApplicationResponse[];
};

export type ApplicationFilters = {
  job_id?: number;
  status?: string;
  source?: string;
  search?: string;
};

export type ApplicationStatisticsResponse = {
  total_applications: number;
  pending_applications: number;
  reviewed_applications: number;
  shortlisted_applications: number;
  rejected_applications: number;
  hired_applications: number;
  applications_this_month: number;
  top_jobs: Array<{ position: string; application_count: number }>;
  applications_by_source: Record<string, number>;
};

export type MessageResponse = {
  message: string;
};

export type ResumeUploadResponse = {
  message: string;
  resume_path: string;
  file_size: number;
};

// API methods
const applicationService = {
  /**
   * Create a new job application
   */
  async createApplication(data: CreateApplicationRequest): Promise<ApplicationResponse> {
    const response = await api.post('/applications/', data);
    return response.data;
  },

  /**
   * Get my applications (for current user)
   */
  async getMyApplications(page: number = 1, page_size: number = 20): Promise<ApplicationsListResponse> {
    const response = await api.get('/applications/me', {
      params: { page, page_size }
    });
    return response.data;
  },

  /**
   * Get application statistics (HR only)
   */
  async getApplicationStatistics(): Promise<ApplicationStatisticsResponse> {
    const response = await api.get('/applications/statistics');
    return response.data;
  },

  /**
   * Get all applications with filters (HR only)
   */
  async getAllApplications(
    page: number = 1,
    page_size: number = 20,
    filters?: ApplicationFilters
  ): Promise<ApplicationsListResponse> {
    const params: any = { page, page_size };
    if (filters) {
      if (filters.job_id !== undefined) params.job_id = filters.job_id;
      if (filters.status) params.status = filters.status;
      if (filters.source) params.source = filters.source;
      if (filters.search) params.search = filters.search;
    }
    const response = await api.get('/applications/', { params });
    return response.data;
  },

  /**
   * Get application by ID
   */
  async getApplicationById(applicationId: number): Promise<ApplicationResponse> {
    const response = await api.get(`/applications/${applicationId}`);
    return response.data;
  },

  /**
   * Update application status (HR only)
   */
  async updateApplicationStatus(
    applicationId: number,
    data: UpdateApplicationStatusRequest
  ): Promise<ApplicationResponse> {
    const response = await api.put(`/applications/${applicationId}/status`, data);
    return response.data;
  },

  /**
   * Upload resume for an application
   */
  async uploadResume(applicationId: number, file: File): Promise<ResumeUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post(`/applications/${applicationId}/resume`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  },

  /**
   * Download resume for an application
   */
  async downloadResume(applicationId: number): Promise<Blob> {
    const response = await api.get(`/applications/${applicationId}/resume`, {
      responseType: 'blob'
    });
    return response.data;
  },

  /**
   * Delete an application
   */
  async deleteApplication(applicationId: number): Promise<MessageResponse> {
    const response = await api.delete(`/applications/${applicationId}`);
    return response.data;
  }
};

// Helper functions
export const formatApplicationStatus = (status: string): string => {
  const statusMap: Record<string, string> = {
    'pending': 'Pending Review',
    'reviewed': 'Reviewed',
    'shortlisted': 'Shortlisted',
    'rejected': 'Rejected',
    'hired': 'Hired'
  };
  return statusMap[status] || status;
};

export const getApplicationStatusColor = (status: string): string => {
  const colorMap: Record<string, string> = {
    'pending': 'yellow',
    'reviewed': 'blue',
    'shortlisted': 'green',
    'rejected': 'red',
    'hired': 'purple'
  };
  return colorMap[status] || 'gray';
};

export const formatApplicationSource = (source: string): string => {
  const sourceMap: Record<string, string> = {
    'self-applied': 'Self Applied',
    'referral': 'Referral',
    'recruitment': 'Recruitment Agency',
    'internal': 'Internal'
  };
  return sourceMap[source] || source;
};

export const getApplicationSourceIcon = (source: string): string => {
  const iconMap: Record<string, string> = {
    'self-applied': '👤',
    'referral': '🤝',
    'recruitment': '🏢',
    'internal': '🏠'
  };
  return iconMap[source] || '📄';
};

export const validateResume = (file: File): { valid: boolean; error?: string } => {
  const MAX_SIZE = 5 * 1024 * 1024; // 5MB
  const ALLOWED_TYPES = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
  
  if (!ALLOWED_TYPES.includes(file.type)) {
    return {
      valid: false,
      error: 'Only PDF, DOC, and DOCX files are allowed'
    };
  }
  
  if (file.size > MAX_SIZE) {
    return {
      valid: false,
      error: 'File size must be less than 5MB'
    };
  }
  
  return { valid: true };
};

export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

export const formatDateTime = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

export default applicationService;

