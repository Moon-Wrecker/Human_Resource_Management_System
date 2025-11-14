/**
 * AI Job Description Generator Service
 * Frontend service for AI-powered job description generation
 */

import api from './api';

// ==================== Types ====================

export interface CompanyInfo {
  name?: string;
  description?: string;
  industry?: string;
  values?: string[];
}

export interface JobRequirement {
  requirement: string;
  is_required: boolean;
}

export interface JobDescriptionGenerateRequest {
  job_title: string;
  job_level: string;
  department: string;
  location: string;
  employment_type?: string;
  company_info?: CompanyInfo;
  responsibilities: string[];
  requirements: JobRequirement[];
  salary_range?: string;
  benefits?: string[];
  save_as_draft?: boolean;
}

export interface JobDescriptionContent {
  title: string;
  company_overview?: string;
  job_summary: string;
  key_responsibilities: string[];
  required_qualifications: string[];
  preferred_qualifications: string[];
  benefits_section?: string;
  how_to_apply?: string;
  full_description: string;
}

export interface JobDescriptionGenerateResponse {
  success: boolean;
  data?: JobDescriptionContent;
  job_listing_id?: number;
  message?: string;
  error?: string;
}

export interface ImproveJDRequest {
  job_listing_id: number;
  improvements: string[];
}

export interface KeywordsResponse {
  success: boolean;
  keywords: string[];
  total: number;
}

export interface JDGeneratorStatus {
  available: boolean;
  model?: string;
  features?: string[];
  error?: string;
}

// ==================== Service Functions ====================

/**
 * Generate a job description using AI
 */
export const generateJobDescription = async (
  data: JobDescriptionGenerateRequest
): Promise<JobDescriptionGenerateResponse> => {
  try {
    const response = await api.post('/api/v1/ai/job-description/generate', data);
    return response.data;
  } catch (error: any) {
    console.error('Error generating job description:', error);
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to generate job description'
    };
  }
};

/**
 * Improve an existing job description
 */
export const improveJobDescription = async (
  jobListingId: number,
  improvements: string[]
): Promise<{ success: boolean; message: string; improved_description?: string }> => {
  try {
    const response = await api.post('/api/v1/ai/job-description/improve', null, {
      params: {
        job_listing_id: jobListingId,
        improvements: improvements
      }
    });
    return response.data;
  } catch (error: any) {
    console.error('Error improving job description:', error);
    throw new Error(error.response?.data?.detail || 'Failed to improve job description');
  }
};

/**
 * Extract SEO/ATS keywords from job description
 */
export const extractKeywords = async (jobDescription: string): Promise<KeywordsResponse> => {
  try {
    const response = await api.post('/api/v1/ai/job-description/extract-keywords', null, {
      params: { job_description: jobDescription }
    });
    return response.data;
  } catch (error: any) {
    console.error('Error extracting keywords:', error);
    return {
      success: false,
      keywords: [],
      total: 0
    };
  }
};

/**
 * Get JD generator status
 */
export const getJDGeneratorStatus = async (): Promise<JDGeneratorStatus> => {
  try {
    const response = await api.get('/api/v1/ai/job-description/status');
    return response.data;
  } catch (error: any) {
    console.error('Error getting JD generator status:', error);
    return {
      available: false,
      error: error.response?.data?.detail || 'Service unavailable'
    };
  }
};

// ==================== Utility Functions ====================

/**
 * Validate job description request
 */
export const validateJDRequest = (data: JobDescriptionGenerateRequest): string[] => {
  const errors: string[] = [];

  if (!data.job_title || data.job_title.trim().length === 0) {
    errors.push('Job title is required');
  }

  if (!data.job_level || data.job_level.trim().length === 0) {
    errors.push('Job level is required');
  }

  if (!data.department || data.department.trim().length === 0) {
    errors.push('Department is required');
  }

  if (!data.location || data.location.trim().length === 0) {
    errors.push('Location is required');
  }

  if (!data.responsibilities || data.responsibilities.length === 0) {
    errors.push('At least one responsibility is required');
  }

  if (!data.requirements || data.requirements.length === 0) {
    errors.push('At least one requirement is required');
  }

  return errors;
};

/**
 * Format job description for display
 */
export const formatJobDescription = (content: JobDescriptionContent): string => {
  let formatted = `# ${content.title}\n\n`;

  if (content.company_overview) {
    formatted += `## About Us\n${content.company_overview}\n\n`;
  }

  formatted += `## Job Summary\n${content.job_summary}\n\n`;

  formatted += `## Key Responsibilities\n`;
  content.key_responsibilities.forEach((resp, idx) => {
    formatted += `${idx + 1}. ${resp}\n`;
  });
  formatted += '\n';

  formatted += `## Required Qualifications\n`;
  content.required_qualifications.forEach((qual, idx) => {
    formatted += `${idx + 1}. ${qual}\n`;
  });
  formatted += '\n';

  if (content.preferred_qualifications && content.preferred_qualifications.length > 0) {
    formatted += `## Preferred Qualifications\n`;
    content.preferred_qualifications.forEach((qual, idx) => {
      formatted += `${idx + 1}. ${qual}\n`;
    });
    formatted += '\n';
  }

  if (content.benefits_section) {
    formatted += `## Benefits\n${content.benefits_section}\n\n`;
  }

  if (content.how_to_apply) {
    formatted += `## How to Apply\n${content.how_to_apply}\n\n`;
  }

  return formatted;
};

/**
 * Convert job description to HTML
 */
export const convertToHTML = (content: JobDescriptionContent): string => {
  let html = `<h1>${content.title}</h1>`;

  if (content.company_overview) {
    html += `<h2>About Us</h2><p>${content.company_overview}</p>`;
  }

  html += `<h2>Job Summary</h2><p>${content.job_summary}</p>`;

  html += `<h2>Key Responsibilities</h2><ul>`;
  content.key_responsibilities.forEach(resp => {
    html += `<li>${resp}</li>`;
  });
  html += `</ul>`;

  html += `<h2>Required Qualifications</h2><ul>`;
  content.required_qualifications.forEach(qual => {
    html += `<li>${qual}</li>`;
  });
  html += `</ul>`;

  if (content.preferred_qualifications && content.preferred_qualifications.length > 0) {
    html += `<h2>Preferred Qualifications</h2><ul>`;
    content.preferred_qualifications.forEach(qual => {
      html += `<li>${qual}</li>`;
    });
    html += `</ul>`;
  }

  if (content.benefits_section) {
    html += `<h2>Benefits</h2><p>${content.benefits_section}</p>`;
  }

  if (content.how_to_apply) {
    html += `<h2>How to Apply</h2><p>${content.how_to_apply}</p>`;
  }

  return html;
};

/**
 * Copy job description to clipboard
 */
export const copyToClipboard = async (text: string): Promise<boolean> => {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (error) {
    console.error('Failed to copy to clipboard:', error);
    return false;
  }
};

/**
 * Download job description as text file
 */
export const downloadAsTextFile = (content: string, filename: string): void => {
  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);

  link.setAttribute('href', url);
  link.setAttribute('download', filename);
  link.style.visibility = 'hidden';

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

/**
 * Create a draft request from form data
 */
export const createDraftRequest = (formData: any): JobDescriptionGenerateRequest => {
  return {
    job_title: formData.title,
    job_level: formData.experience_required || 'mid',
    department: formData.department,
    location: formData.location,
    employment_type: formData.job_type || 'full-time',
    responsibilities: formData.responsibilities
      ? formData.responsibilities.split('\n').filter((r: string) => r.trim())
      : [],
    requirements: formData.qualifications
      ? formData.qualifications.split('\n').filter((q: string) => q.trim()).map((req: string) => ({
          requirement: req,
          is_required: true
        }))
      : [],
    salary_range: formData.salary_range,
    save_as_draft: true
  };
};

/**
 * Check if JD Generator is available
 */
export const isJDGeneratorAvailable = async (): Promise<boolean> => {
  try {
    const status = await getJDGeneratorStatus();
    return status.available;
  } catch {
    return false;
  }
};

