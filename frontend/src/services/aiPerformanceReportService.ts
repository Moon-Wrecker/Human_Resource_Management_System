import api from "./api";

// Type definitions for AI Performance Report
export type AIPerformanceReportResponse = {
  // TODO: Define the full structure based on backend AIReportResponse schema
  report_id: string;
  employee_id: number;
  time_period: string;
  report_template: string;
  executive_summary: string;
  strengths: string[];
  areas_for_development: string[];
  actionable_recommendations: string[];
  performance_snapshot: Record<string, any>; // Adjust as needed
  generated_at: string;
  // Add other fields as needed from the backend schema
};

export enum AITimePeriodEnum {
  LAST_30_DAYS = "last_30_days",
  LAST_90_DAYS = "last_90_days",
  LAST_180_DAYS = "last_180_days",
  LAST_365_DAYS = "last_365_days",
  CURRENT_QUARTER = "current_quarter",
  PREVIOUS_QUARTER = "previous_quarter",
  CURRENT_YEAR = "current_year",
  CUSTOM = "custom",
}

export enum AIReportTemplateEnum {
  QUICK_SUMMARY = "quick_summary",
  STANDARD_REVIEW = "standard_review",
  COMPREHENSIVE_REVIEW = "comprehensive_review",
  LEADERSHIP_FOCUS = "leadership_focus",
  TECHNICAL_FOCUS = "technical_focus",
  CUSTOM = "custom",
}

export type GetPersonalReportParams = {
  time_period?: AITimePeriodEnum;
  start_date?: string; // YYYY-MM-DD
  end_date?: string; // YYYY-MM-DD
  template?: AIReportTemplateEnum;
  include_team_comparison?: boolean;
  include_period_comparison?: boolean;
};

export type ReportTemplate = {
  name: string;
  description: string;
  metrics_count: number | string;
  recommended_for: string;
  available_to: string[];
};

export type GetReportTemplatesResponse = {
  templates: Record<string, ReportTemplate>;
  user_role: string;
  note: string;
};

const aiPerformanceReportService = {
  async getPersonalPerformanceReport(
    params: GetPersonalReportParams,
  ): Promise<AIPerformanceReportResponse> {
    const response = await api.get("/ai/performance-report/individual/me", {
      params,
    });
    return response.data;
  },

  async getReportTemplates(): Promise<GetReportTemplatesResponse> {
    const response = await api.get("/ai/performance-report/templates");
    return response.data;
  },
};

export default aiPerformanceReportService;
