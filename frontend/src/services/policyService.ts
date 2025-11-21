/**
 * Policy Service
 * Service layer for policies API calls with file upload/download support
 */

import api from './api';

// Types
export interface Policy {
  id: number;
  title: string;
  description?: string;
  content: string;
  category?: string;
  version: string;
  is_active: boolean;
  effective_date: string;
  review_date?: string;
  document_path?: string;
  created_by: number;
  created_at: string;
  updated_at: string;
  created_by_name?: string;
  has_document: boolean;
  document_url?: string;
  acknowledgment_count: number;
  is_acknowledged_by_user: boolean;
}

export interface PolicyListResponse {
  policies: Policy[];
  total: number;
  active: number;
}

export interface CreatePolicyData {
  title: string;
  description?: string;
  content: string;
  category?: string;
  version?: string;
  effective_date: string;
  review_date?: string;
  require_acknowledgment?: boolean;
}

export interface UpdatePolicyData {
  title?: string;
  description?: string;
  content?: string;
  category?: string;
  version?: string;
  effective_date?: string;
  review_date?: string;
  is_active?: boolean;
}

export interface PolicyAcknowledgment {
  id: number;
  policy_id: number;
  user_id: number;
  acknowledged_date: string;
  policy_title?: string;
  user_name?: string;
}

export interface PolicyAcknowledgmentListResponse {
  acknowledgments: PolicyAcknowledgment[];
  total: number;
}

export interface PolicyUploadResponse {
  policy_id: number;
  file_name: string;
  file_path: string;
  file_size: number;
  message: string;
}

export interface PolicyStats {
  total: number;
  active: number;
  inactive: number;
  with_documents: number;
  total_acknowledgments: number;
  categories: Record<string, number>;
}

/**
 * Policy Service Class
 */
class PolicyService {
  private baseUrl = '/policies';

  /**
   * Get all policies
   * @param params Query parameters for filtering and pagination
   * @returns List of policies with metadata
   */
  async getPolicies(params?: {
    include_inactive?: boolean;
    category?: string;
    skip?: number;
    limit?: number;
  }): Promise<PolicyListResponse> {
    try {
      const response = await api.get<PolicyListResponse>(this.baseUrl, {
        params: params || {},
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching policies:', error);
      throw error;
    }
  }

  /**
   * Get policy by ID
   * @param id Policy ID
   * @returns Policy object
   */
  async getPolicyById(id: number): Promise<Policy> {
    try {
      const response = await api.get<Policy>(`${this.baseUrl}/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching policy ${id}:`, error);
      throw error;
    }
  }

  /**
   * Create a new policy (HR only)
   * @param data Policy data
   * @returns Created policy
   */
  async createPolicy(data: CreatePolicyData): Promise<Policy> {
    try {
      const response = await api.post<Policy>(this.baseUrl, data);
      return response.data;
    } catch (error) {
      console.error('Error creating policy:', error);
      throw error;
    }
  }

  /**
   * Update a policy (HR only)
   * @param id Policy ID
   * @param data Update data
   * @returns Updated policy
   */
  async updatePolicy(
    id: number,
    data: UpdatePolicyData
  ): Promise<Policy> {
    try {
      const response = await api.put<Policy>(`${this.baseUrl}/${id}`, data);
      return response.data;
    } catch (error) {
      console.error(`Error updating policy ${id}:`, error);
      throw error;
    }
  }

  /**
   * Delete a policy (HR only)
   * @param id Policy ID
   * @param hardDelete Whether to permanently delete (default: false)
   * @returns Success message
   */
  async deletePolicy(
    id: number,
    hardDelete: boolean = false
  ): Promise<{ message: string }> {
    try {
      const response = await api.delete<{ message: string }>(
        `${this.baseUrl}/${id}`,
        {
          params: { hard_delete: hardDelete },
        }
      );
      return response.data;
    } catch (error) {
      console.error(`Error deleting policy ${id}:`, error);
      throw error;
    }
  }

  /**
   * Upload policy document (PDF) (HR only)
   * @param policyId Policy ID
   * @param file PDF file to upload
   * @returns Upload response with file details
   */
  async uploadPolicyDocument(
    policyId: number,
    file: File
  ): Promise<PolicyUploadResponse> {
    try {
      // Create form data
      const formData = new FormData();
      formData.append('file', file);

      // Upload with multipart/form-data
      const response = await api.post<PolicyUploadResponse>(
        `${this.baseUrl}/${policyId}/upload`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error(`Error uploading policy document for ${policyId}:`, error);
      throw error;
    }
  }

  /**
   * Download policy document (PDF)
   * @param policyId Policy ID
   * @returns Blob of the PDF file
   */
  async downloadPolicyDocument(policyId: number): Promise<Blob> {
    try {
      const response = await api.get<Blob>(
        `${this.baseUrl}/${policyId}/download`,
        {
          responseType: 'blob',
        }
      );
      return response.data;
    } catch (error) {
      console.error(`Error downloading policy document ${policyId}:`, error);
      throw error;
    }
  }

  /**
   * Download policy document and trigger browser download
   * @param policyId Policy ID
   * @param filename Custom filename (optional)
   */
  async downloadAndSavePolicyDocument(
    policyId: number,
    filename?: string
  ): Promise<void> {
    try {
      const blob = await this.downloadPolicyDocument(policyId);

      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename || `policy-${policyId}.pdf`;
      document.body.appendChild(link);
      link.click();

      // Cleanup
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error triggering policy download:', error);
      throw error;
    }
  }

  /**
   * Acknowledge a policy
   * @param policyId Policy ID
   * @returns Acknowledgment record
   */
  async acknowledgePolicy(policyId: number): Promise<PolicyAcknowledgment> {
    try {
      const response = await api.post<PolicyAcknowledgment>(
        `${this.baseUrl}/${policyId}/acknowledge`
      );
      return response.data;
    } catch (error) {
      console.error(`Error acknowledging policy ${policyId}:`, error);
      throw error;
    }
  }

  /**
   * Get policy acknowledgments (HR only)
   * @param policyId Policy ID
   * @param params Pagination parameters
   * @returns List of acknowledgments
   */
  async getPolicyAcknowledgments(
    policyId: number,
    params?: {
      skip?: number;
      limit?: number;
    }
  ): Promise<PolicyAcknowledgmentListResponse> {
    try {
      const response = await api.get<PolicyAcknowledgmentListResponse>(
        `${this.baseUrl}/${policyId}/acknowledgments`,
        {
          params: params || {},
        }
      );
      return response.data;
    } catch (error) {
      console.error(`Error fetching policy acknowledgments for ${policyId}:`, error);
      throw error;
    }
  }

  /**
   * Get policy statistics (HR only)
   * @returns Statistics object
   */
  async getStatistics(): Promise<PolicyStats> {
    try {
      const response = await api.get<PolicyStats>(
        `${this.baseUrl}/stats/summary`
      );
      return response.data;
    } catch (error) {
      console.error('Error fetching policy statistics:', error);
      throw error;
    }
  }

  /**
   * Get active policies (helper method)
   * @param limit Number of policies to fetch (default: 10)
   * @returns Active policies
   */
  async getActivePolicies(limit: number = 10): Promise<Policy[]> {
    try {
      const response = await this.getPolicies({ limit, include_inactive: false });
      return response.policies;
    } catch (error) {
      console.error('Error fetching active policies:', error);
      throw error;
    }
  }

  /**
   * Get policies by category
   * @param category Category name
   * @param limit Maximum results
   * @returns Policies in category
   */
  async getPoliciesByCategory(category: string, limit: number = 100): Promise<Policy[]> {
    try {
      const response = await this.getPolicies({ category, limit });
      return response.policies;
    } catch (error) {
      console.error(`Error fetching policies for category ${category}:`, error);
      throw error;
    }
  }

  /**
   * Check if policy requires acknowledgment
   * @param policy Policy object
   * @returns True if user hasn't acknowledged yet
   */
  requiresAcknowledgment(policy: Policy): boolean {
    return !policy.is_acknowledged_by_user;
  }

  /**
   * Format policy date for display
   * @param dateString ISO date string
   * @returns Formatted date string
   */
  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    });
  }

  /**
   * Format policy datetime for display
   * @param dateString ISO datetime string
   * @returns Formatted datetime string
   */
  formatDateTime(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  }

  /**
   * Get file size in human-readable format
   * @param bytes File size in bytes
   * @returns Formatted file size
   */
  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
  }

  /**
   * Validate PDF file before upload
   * @param file File to validate
   * @param maxSizeMB Maximum file size in MB
   * @returns Error message if invalid, null if valid
   */
  validatePolicyFile(file: File, maxSizeMB: number = 10): string | null {
    // Check file type
    if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
      return 'Only PDF files are allowed';
    }

    // Check file size
    const maxSizeBytes = maxSizeMB * 1024 * 1024;
    if (file.size > maxSizeBytes) {
      return `File size exceeds maximum allowed (${maxSizeMB}MB)`;
    }

    // Check filename
    if (file.name.length > 255) {
      return 'Filename is too long';
    }

    return null;
  }
}

// Export singleton instance
const policyService = new PolicyService();
export default policyService;

