/**
 * Feedback Service
 * 
 * API service layer for feedback management
 */

import api from './api';

// ==================== Types ====================

export interface FeedbackResponse {
  id: number;
  employee_id: number;
  employee_name: string;
  given_by: number;
  given_by_name: string;
  subject: string;
  description: string;
  feedback_type?: string;
  rating?: number;
  given_on: string;
}

export interface FeedbackListResponse {
  feedback: FeedbackResponse[];
  total: number;
  page: number;
  page_size: number;
}

export interface FeedbackCreateRequest {
  employee_id: number;
  subject: string;
  description: string;
  feedback_type?: string;
  rating?: number;
}

export interface FeedbackUpdateRequest {
  subject?: string;
  description?: string;
  feedback_type?: string;
  rating?: number;
}

export interface FeedbackStatsResponse {
  total_feedback: number;
  this_month: number;
  this_quarter: number;
  average_rating?: number;
  by_type: Record<string, number>;
  recent_feedback: FeedbackResponse[];
}

export interface FeedbackFilters {
  skip?: number;
  limit?: number;
  start_date?: string;
  end_date?: string;
  feedback_type?: string;
  employee_id?: number;
  given_by?: number;
}

// ==================== Service Functions ====================

/**
 * Get feedback for current user
 */
export const getMyFeedback = async (filters?: FeedbackFilters): Promise<FeedbackListResponse> => {
  const params = new URLSearchParams();
  if (filters?.skip) params.append('skip', filters.skip.toString());
  if (filters?.limit) params.append('limit', filters.limit.toString());
  if (filters?.start_date) params.append('start_date', filters.start_date);
  if (filters?.end_date) params.append('end_date', filters.end_date);
  if (filters?.feedback_type) params.append('feedback_type', filters.feedback_type);

  const response = await api.get(`/feedback/me?${params.toString()}`);
  return response.data;
};

/**
 * Get feedback for a specific employee
 */
export const getEmployeeFeedback = async (
  employeeId: number,
  filters?: FeedbackFilters
): Promise<FeedbackListResponse> => {
  const params = new URLSearchParams();
  if (filters?.skip) params.append('skip', filters.skip.toString());
  if (filters?.limit) params.append('limit', filters.limit.toString());
  if (filters?.start_date) params.append('start_date', filters.start_date);
  if (filters?.end_date) params.append('end_date', filters.end_date);
  if (filters?.feedback_type) params.append('feedback_type', filters.feedback_type);

  const response = await api.get(`/feedback/employee/${employeeId}?${params.toString()}`);
  return response.data;
};

/**
 * Get feedback given by current user
 */
export const getFeedbackGiven = async (filters?: FeedbackFilters): Promise<FeedbackListResponse> => {
  const params = new URLSearchParams();
  if (filters?.skip) params.append('skip', filters.skip.toString());
  if (filters?.limit) params.append('limit', filters.limit.toString());

  const response = await api.get(`/feedback/given?${params.toString()}`);
  return response.data;
};

/**
 * Get all feedback (HR only)
 */
export const getAllFeedback = async (filters?: FeedbackFilters): Promise<FeedbackListResponse> => {
  const params = new URLSearchParams();
  if (filters?.skip) params.append('skip', filters.skip.toString());
  if (filters?.limit) params.append('limit', filters.limit.toString());
  if (filters?.employee_id) params.append('employee_id', filters.employee_id.toString());
  if (filters?.given_by) params.append('given_by', filters.given_by.toString());
  if (filters?.feedback_type) params.append('feedback_type', filters.feedback_type);

  const response = await api.get(`/feedback?${params.toString()}`);
  return response.data;
};

/**
 * Get feedback by ID
 */
export const getFeedbackById = async (feedbackId: number): Promise<FeedbackResponse> => {
  const response = await api.get(`/feedback/${feedbackId}`);
  return response.data;
};

/**
 * Create new feedback
 */
export const createFeedback = async (data: FeedbackCreateRequest): Promise<FeedbackResponse> => {
  const response = await api.post('/feedback', data);
  return response.data;
};

/**
 * Update feedback
 */
export const updateFeedback = async (
  feedbackId: number,
  data: FeedbackUpdateRequest
): Promise<FeedbackResponse> => {
  const response = await api.put(`/feedback/${feedbackId}`, data);
  return response.data;
};

/**
 * Delete feedback
 */
export const deleteFeedback = async (feedbackId: number): Promise<{ message: string }> => {
  const response = await api.delete(`/feedback/${feedbackId}`);
  return response.data;
};

/**
 * Get feedback statistics
 */
export const getFeedbackStats = async (employeeId?: number): Promise<FeedbackStatsResponse> => {
  const params = new URLSearchParams();
  if (employeeId) params.append('employee_id', employeeId.toString());

  const response = await api.get(`/feedback/stats/summary?${params.toString()}`);
  return response.data;
};

// ==================== Helper Functions ====================

/**
 * Format feedback date for display
 */
export const formatFeedbackDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  });
};

/**
 * Get feedback type color
 */
export const getFeedbackTypeColor = (type?: string): string => {
  const colors: Record<string, string> = {
    positive: 'text-green-600 bg-green-100',
    constructive: 'text-yellow-600 bg-yellow-100',
    'goal-related': 'text-blue-600 bg-blue-100',
    performance: 'text-purple-600 bg-purple-100',
    general: 'text-gray-600 bg-gray-100'
  };
  return colors[type || 'general'] || colors.general;
};

/**
 * Get feedback type badge
 */
export const getFeedbackTypeBadge = (type?: string): string => {
  const badges: Record<string, string> = {
    positive: 'Positive',
    constructive: 'Constructive',
    'goal-related': 'Goal Related',
    performance: 'Performance',
    general: 'General'
  };
  return badges[type || 'general'] || badges.general;
};

/**
 * Filter feedback by time period
 */
export const getFeedbackByTimePeriod = (
  feedbackList: FeedbackResponse[],
  period: 'all' | 'this-month' | 'this-quarter' | 'this-year'
): FeedbackResponse[] => {
  if (period === 'all') return feedbackList;

  const now = new Date();
  const filtered = feedbackList.filter(feedback => {
    const feedbackDate = new Date(feedback.given_on);
    
    switch (period) {
      case 'this-month':
        return (
          feedbackDate.getMonth() === now.getMonth() &&
          feedbackDate.getFullYear() === now.getFullYear()
        );
      
      case 'this-quarter':
        const currentQuarter = Math.floor(now.getMonth() / 3);
        const feedbackQuarter = Math.floor(feedbackDate.getMonth() / 3);
        return (
          feedbackQuarter === currentQuarter &&
          feedbackDate.getFullYear() === now.getFullYear()
        );
      
      case 'this-year':
        return feedbackDate.getFullYear() === now.getFullYear();
      
      default:
        return true;
    }
  });

  return filtered;
};

export default {
  getMyFeedback,
  getEmployeeFeedback,
  getFeedbackGiven,
  getAllFeedback,
  getFeedbackById,
  createFeedback,
  updateFeedback,
  deleteFeedback,
  getFeedbackStats,
  formatFeedbackDate,
  getFeedbackTypeColor,
  getFeedbackTypeBadge,
  getFeedbackByTimePeriod
};

