/**
 * Performance Report Service - API calls for managing employee performance reports
 */
import api from "./api";

// Types
export interface PerformanceReportCreate {
  employee_id: number;
  report_date: string; // YYYY-MM-DD
  overall_rating: number; // e.g., 1-5
  strengths: string;
  areas_for_improvement: string;
  manager_comments?: string;
}

export interface PerformanceReportUpdate {
  overall_rating?: number;
  strengths?: string;
  areas_for_improvement?: string;
  manager_comments?: string;
}

export interface MonthlyModules {
  month: string;
  modules_completed: number;
}

export interface PerformanceReportResponse {
  employee_id: number;
  employee_name: string;
  monthly_modules: MonthlyModules[];
  total_modules_completed: number;
  attendance_rate: number;
  goals_completion_rate: number;
}

export interface PerformanceReportFilters {
  page?: number;
  page_size?: number;
  employee_id?: number;
  start_date?: string; // YYYY-MM-DD
  end_date?: string; // YYYY-MM-DD
}

// Performance Report Service
const performanceReportService = {
  /**
   * Create a new performance report
   */
  async createPerformanceReport(
    data: PerformanceReportCreate,
  ): Promise<PerformanceReportResponse> {
    const response = await api.post<PerformanceReportResponse>(
      "/employee/performancereport",
      data,
    );
    return response.data;
  },

  /**
   * Get all performance reports for an employee
   */
  async getPerformanceReports(
    filters?: PerformanceReportFilters,
  ): Promise<PerformanceReportResponse> {
    const response = await api.get<PerformanceReportResponse>(
      "/dashboard/performance/me",
      { params: filters },
    );
    return response.data;
  },

  /**
   * Get a specific performance report by ID
   */
  async getPerformanceReportById(
    reportId: number,
  ): Promise<PerformanceReportResponse> {
    const response = await api.get<PerformanceReportResponse>(
      `/employee/performancereport/${reportId}`,
    );
    return response.data;
  },

  /**
   * Update a performance report
   */
  async updatePerformanceReport(
    reportId: number,
    data: PerformanceReportUpdate,
  ): Promise<PerformanceReportResponse> {
    const response = await api.put<PerformanceReportResponse>(
      `/employee/performancereport/${reportId}`,
      data,
    );
    return response.data;
  },

  /**
   * Delete a performance report
   */
  async deletePerformanceReport(
    reportId: number,
  ): Promise<{ message: string }> {
    const response = await api.delete<{ message: string }>(
      `/employee/performancereport/${reportId}`,
    );
    return response.data;
  },
};

export default performanceReportService;
