/**
 * AI Resume Screener Service
 * Frontend service for AI-powered resume screening
 */

import api, { handleApiError } from './api';
import { API_URL } from '@/config/api';

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
    const response = await api.post('/ai/resume-screener/screen', data);
    return response.data;
  } catch (error) {
    throw new Error(handleApiError(error));
  }
};

export const screenResumesWithProgress = async (
  data: ResumeScreeningRequest,
  onProgress: (progress: ScreeningProgress) => void,
  onError: (error: string) => void
): Promise<void> => {
  const token = localStorage.getItem('access_token');

  try {
    const response = await fetch(`${API_URL}/ai/resume-screener/screen/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });

    if (!response.body) {
      throw new Error('Response body is null');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }

      buffer += decoder.decode(value, { stream: true });

      const parts = buffer.split('\n\n');
      buffer = parts.pop() || '';

      for (const part of parts) {
        const lines = part.split('\n');
        let event = '';
        let data = '';

        for (const line of lines) {
          if (line.startsWith('event: ')) {
            event = line.substring(7);
          } else if (line.startsWith('data: ')) {
            data = line.substring(6);
          }
        }

        if (event && data) {
          try {
            const parsedData = JSON.parse(data);
            onProgress({ type: event as any, data: parsedData });
          } catch (e) {
            console.error('Failed to parse SSE data:', e);
          }
        }
      }
    }
  } catch (error) {
    console.error('Error in streaming resume screening:', error);
    onError('Connection error occurred');
  }
};

/**
 * Get saved screening results by analysis ID
 */
export const getScreeningResults = async (
  analysisId: string
): Promise<ResumeScreeningResult> => {
  try {
    const response = await api.get(`/ai/resume-screener/results/${analysisId}`);
    return response.data;
  } catch (error) {
    throw new Error(handleApiError(error));
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
    const response = await api.get('/ai/resume-screener/history', { params });
    return response.data;
  } catch (error) {
    throw new Error(handleApiError(error));
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

