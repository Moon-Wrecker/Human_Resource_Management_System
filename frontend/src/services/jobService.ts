/**
 * Job Service - API calls for job listings management
 */
import api from './api';

// ===== TYPE DEFINITIONS (using 'export type' for better ES module compatibility) =====

export type EmploymentType = 'full-time' | 'part-time' | 'contract' | 'internship';

export type JobListing = {
  id: number;
  position: string;
  department_id: number;
  department_name?: string;
  experience_required?: string;
  skills_required?: string;
  description?: string;
  ai_generated_description?: string;
  location?: string;
  employment_type: string;
  salary_range?: string;
  is_active: boolean;
  posted_by: number;
  posted_by_name?: string;
  posted_date: string;
  application_deadline?: string;
  application_count?: number;
  created_at: string;
  updated_at: string;
}

export type CreateJobRequest = {
  position: string;
  department_id: number;
  experience_required?: string;
  skills_required?: string;
  description?: string;
  location?: string;
  employment_type?: EmploymentType;
  salary_range?: string;
  application_deadline?: string;
}

export type UpdateJobRequest = {
  position?: string;
  department_id?: number;
  experience_required?: string;
  skills_required?: string;
  description?: string;
  location?: string;
  employment_type?: EmploymentType;
  salary_range?: string;
  application_deadline?: string;
  is_active?: boolean;
}

export type JobFilters = {
  department_id?: number;
  location?: string;
  employment_type?: string;
  is_active?: boolean;
  search?: string;
  page?: number;
  page_size?: number;
}

export type JobListingsResponse = {
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  jobs: JobListing[];
}

export type JobStatistics = {
  total_jobs: number;
  active_jobs: number;
  closed_jobs: number;
  total_applications: number;
  applications_this_month: number;
  top_departments: Array<{
    department: string;
    job_count: number;
  }>;
}

export type JobApplication = {
  id: number;
  applicant_name: string;
  applicant_email: string;
  applied_date: string;
  status: string;
  resume_path?: string;
}

// ===== SERVICE CLASS =====

class JobService {
  /**
   * Create a new job listing (HR only)
   */
  async createJob(data: CreateJobRequest): Promise<JobListing> {
    const response = await api.post('/jobs', data);
    return response.data;
  }

  /**
   * Get all job listings with filters and pagination
   */
  async getAllJobs(filters?: JobFilters): Promise<JobListingsResponse> {
    const params = new URLSearchParams();
    
    if (filters) {
      if (filters.department_id !== undefined) params.append('department_id', String(filters.department_id));
      if (filters.location) params.append('location', filters.location);
      if (filters.employment_type) params.append('employment_type', filters.employment_type);
      if (filters.is_active !== undefined) params.append('is_active', String(filters.is_active));
      if (filters.search) params.append('search', filters.search);
      if (filters.page) params.append('page', String(filters.page));
      if (filters.page_size) params.append('page_size', String(filters.page_size));
    }
    
    const response = await api.get(`/jobs?${params.toString()}`);
    return response.data;
  }

  /**
   * Get job by ID
   */
  async getJobById(jobId: number): Promise<JobListing> {
    const response = await api.get(`/jobs/${jobId}`);
    return response.data;
  }

  /**
   * Update a job listing (HR only)
   */
  async updateJob(jobId: number, data: UpdateJobRequest): Promise<JobListing> {
    const response = await api.put(`/jobs/${jobId}`, data);
    return response.data;
  }

  /**
   * Delete a job listing (HR only)
   */
  async deleteJob(jobId: number): Promise<{ message: string }> {
    const response = await api.delete(`/jobs/${jobId}`);
    return response.data;
  }

  /**
   * Get all applications for a specific job (HR only)
   */
  async getJobApplications(jobId: number): Promise<JobApplication[]> {
    const response = await api.get(`/jobs/${jobId}/applications`);
    return response.data;
  }

  /**
   * Get job statistics (HR only)
   */
  async getJobStatistics(): Promise<JobStatistics> {
    const response = await api.get('/jobs/statistics');
    return response.data;
  }

  /**
   * Helper: Format date for display
   */
  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  }

  /**
   * Helper: Check if deadline is approaching (within 7 days)
   */
  isDeadlineApproaching(deadline?: string): boolean {
    if (!deadline) return false;
    const deadlineDate = new Date(deadline);
    const today = new Date();
    const daysUntilDeadline = Math.floor((deadlineDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
    return daysUntilDeadline >= 0 && daysUntilDeadline <= 7;
  }

  /**
   * Helper: Check if deadline has passed
   */
  isDeadlinePassed(deadline?: string): boolean {
    if (!deadline) return false;
    const deadlineDate = new Date(deadline);
    const today = new Date();
    return deadlineDate < today;
  }

  /**
   * Helper: Get employment type badge color
   */
  getEmploymentTypeBadge(type: string): { label: string; color: string } {
    const types: Record<string, { label: string; color: string }> = {
      'full-time': { label: 'Full-time', color: 'success' },
      'part-time': { label: 'Part-time', color: 'info' },
      'contract': { label: 'Contract', color: 'warning' },
      'internship': { label: 'Internship', color: 'secondary' }
    };
    return types[type] || { label: type, color: 'default' };
  }
}

// Export singleton instance
const jobService = new JobService();
export default jobService;

