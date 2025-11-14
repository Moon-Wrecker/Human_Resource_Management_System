/**
 * AI Resume Screener Service
 * Frontend service for AI-powered resume screening
 */

import api from './api';

// ==================== Types ====================

export interface ResumeScreeningRequest {
  job_id: number;
  job_description?: string;
  resume_ids?: number[];
}

export interface SkillMatch {
  skill_name: string;
  present_in_resume: boolean;
  importance_level: number;
  proficiency_level?: number;
  context?: string;
}

export interface ExperienceMatch {
  area: string;
  years_required: number;
  years_present: number;
  relevance_score: number;
  context?: string;
}

export interface EducationMatch {
  requirement: string;
  has_match: boolean;
  details: string;
}

export interface ResumeAnalysis {
  candidate_name: string;
  application_id?: number;
  overall_fit_score: number;
  skill_matches: SkillMatch[];
  experience_matches: ExperienceMatch[];
  education_match: EducationMatch;
  strengths: string[];
  gaps: string[];
  summary: string;
  analysis_date: string;
  error?: string;
}

export interface ResumeScreeningResult {
  success: boolean;
  job_id: number;
  job_title?: string;
  results: ResumeAnalysis[];
  total_analyzed: number;
  average_score: number;
  top_candidate?: string;
  analysis_id?: string;
  error?: string;
}

export interface ScreeningHistoryItem {
  analysis_id: string;
  job_id: number;
  job_title: string;
  timestamp: string;
  total_analyzed: number;
  average_score: number;
  top_candidate?: string;
}

export interface ScreeningHistory {
  success: boolean;
  total: number;
  history: ScreeningHistoryItem[];
}

export interface ScreeningProgress {
  type: 'start' | 'result' | 'complete' | 'error';
  data: any;
}

// ==================== Service Functions ====================

/**
 * Screen resumes against a job description
 */
export const screenResumes = async (
  data: ResumeScreeningRequest
): Promise<ResumeScreeningResult> => {
  try {
    const response = await api.post('/api/v1/ai/resume-screener/screen', data);
    return response.data;
  } catch (error: any) {
    console.error('Error screening resumes:', error);
    return {
      success: false,
      job_id: data.job_id,
      results: [],
      total_analyzed: 0,
      average_score: 0,
      error: error.response?.data?.detail || 'Failed to screen resumes'
    };
  }
};

/**
 * Screen resumes with streaming progress (Server-Sent Events)
 */
export const screenResumesWithProgress = (
  data: ResumeScreeningRequest,
  onProgress: (progress: ScreeningProgress) => void,
  onError: (error: string) => void
): EventSource => {
  const token = localStorage.getItem('token');
  const queryParams = new URLSearchParams({
    job_id: data.job_id.toString(),
    ...(data.job_description && { job_description: data.job_description }),
    ...(data.resume_ids && { resume_ids: JSON.stringify(data.resume_ids) })
  });

  const eventSource = new EventSource(
    `${import.meta.env.VITE_API_BASE_URL}/api/v1/ai/resume-screener/screen/stream?${queryParams}&token=${token}`
  );

  eventSource.addEventListener('start', (event) => {
    const data = JSON.parse(event.data);
    onProgress({ type: 'start', data });
  });

  eventSource.addEventListener('result', (event) => {
    const data = JSON.parse(event.data);
    onProgress({ type: 'result', data });
  });

  eventSource.addEventListener('complete', (event) => {
    const data = JSON.parse(event.data);
    onProgress({ type: 'complete', data });
    eventSource.close();
  });

  eventSource.addEventListener('error', (event: any) => {
    const data = JSON.parse(event.data || '{}');
    onError(data.error || 'Streaming error occurred');
    eventSource.close();
  });

  eventSource.onerror = () => {
    onError('Connection error occurred');
    eventSource.close();
  };

  return eventSource;
};

/**
 * Get saved screening results by analysis ID
 */
export const getScreeningResults = async (
  analysisId: string
): Promise<ResumeScreeningResult> => {
  try {
    const response = await api.get(`/api/v1/ai/resume-screener/results/${analysisId}`);
    return response.data;
  } catch (error: any) {
    console.error('Error getting screening results:', error);
    throw new Error(error.response?.data?.detail || 'Failed to get results');
  }
};

/**
 * Get screening history
 */
export const getScreeningHistory = async (
  jobId?: number
): Promise<ScreeningHistory> => {
  try {
    const params = jobId ? { job_id: jobId } : {};
    const response = await api.get('/api/v1/ai/resume-screener/history', { params });
    return response.data;
  } catch (error: any) {
    console.error('Error getting screening history:', error);
    return {
      success: false,
      total: 0,
      history: []
    };
  }
};

// ==================== Utility Functions ====================

/**
 * Calculate score color based on fit score
 */
export const getScoreColor = (score: number): string => {
  if (score >= 80) return 'text-green-600';
  if (score >= 60) return 'text-yellow-600';
  if (score >= 40) return 'text-orange-600';
  return 'text-red-600';
};

/**
 * Get score label
 */
export const getScoreLabel = (score: number): string => {
  if (score >= 80) return 'Excellent Fit';
  if (score >= 60) return 'Good Fit';
  if (score >= 40) return 'Fair Fit';
  return 'Poor Fit';
};

/**
 * Format analysis date
 */
export const formatAnalysisDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
};

/**
 * Export screening results to CSV
 */
export const exportResultsToCSV = (result: ResumeScreeningResult): string => {
  const headers = [
    'Candidate Name',
    'Overall Fit Score',
    'Strengths',
    'Gaps',
    'Summary'
  ];

  const rows = result.results.map(r => [
    r.candidate_name,
    r.overall_fit_score.toString(),
    r.strengths.join('; '),
    r.gaps.join('; '),
    r.summary
  ]);

  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
  ].join('\n');

  return csvContent;
};

/**
 * Download CSV file
 */
export const downloadCSV = (content: string, filename: string): void => {
  const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', filename);
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

