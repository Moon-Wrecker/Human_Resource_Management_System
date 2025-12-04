/**
 * AI Job Description Service
 * API calls for AI-powered job description generation
 */
import api from './api';

// ===== TYPE DEFINITIONS =====

export type AIRequirement = {
  requirement: string;
  is_required: boolean;
};

export type AICompanyInfo = {
  name: string;
  description: string;
  industry: string;
  values: string[];
};

export type GenerateJDRequest = {
  job_title: string;
  job_level: string;
  department?: string;
  location?: string;
  employment_type?: string;
  responsibilities?: string[];
  requirements: AIRequirement[];
  company_info?: AICompanyInfo;
  salary_range?: string;
  benefits?: string[];
  save_as_draft?: boolean;
};

export type JDContent = {
  title: string;
  summary: string;
  key_responsibilities: string[];
  required_qualifications: string[];
  preferred_qualifications: string[];
  benefits: string[];
  full_description: string;
};

export type GenerateJDResponse = {
  success: boolean;
  data: JDContent;
  job_listing_id?: number;
  message: string;
};

// ===== SERVICE CLASS =====

class AIJobDescriptionService {
  /**
   * Generate a job description using AI
   * @param data - The data needed to generate the job description
   * @returns The generated job description content
   */
  async generateJobDescription(data: GenerateJDRequest): Promise<GenerateJDResponse> {
    const response = await api.post('/ai/job-description/generate', data);
    return response.data;
  }
}

// Export singleton instance
const aiJobDescriptionService = new AIJobDescriptionService();
export default aiJobDescriptionService;