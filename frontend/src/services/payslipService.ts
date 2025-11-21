/**
 * Payslip Service
 * 
 * API service layer for payslip management
 */

import api from './api';

// ==================== Types ====================

export interface PayslipResponse {
  id: number;
  employee_id: number;
  employee_name: string;
  employee_id_number: string;
  pay_period_start: string;
  pay_period_end: string;
  pay_date: string;
  month: number;
  year: number;
  basic_salary: number;
  allowances: number;
  overtime_pay: number;
  bonus: number;
  gross_salary: number;
  tax_deduction: number;
  pf_deduction: number;
  insurance_deduction: number;
  other_deductions: number;
  total_deductions: number;
  net_salary: number;
  payslip_file_path?: string;
  has_document: boolean;
  issued_at: string;
  issued_by?: number;
  issued_by_name?: string;
}

export interface PayslipListResponse {
  payslips: PayslipResponse[];
  total: number;
  page: number;
  page_size: number;
}

export interface PayslipCreateRequest {
  employee_id: number;
  pay_period_start: string;
  pay_period_end: string;
  pay_date: string;
  basic_salary: number;
  allowances?: number;
  overtime_pay?: number;
  bonus?: number;
  tax_deduction?: number;
  pf_deduction?: number;
  insurance_deduction?: number;
  other_deductions?: number;
}

export interface PayslipUpdateRequest {
  pay_period_start?: string;
  pay_period_end?: string;
  pay_date?: string;
  basic_salary?: number;
  allowances?: number;
  overtime_pay?: number;
  bonus?: number;
  tax_deduction?: number;
  pf_deduction?: number;
  insurance_deduction?: number;
  other_deductions?: number;
}

export interface PayslipGenerateRequest {
  month: number;
  year: number;
  pay_date?: string;
}

export interface PayslipStatsResponse {
  total_payslips: number;
  this_month: number;
  total_payout_this_month: number;
  average_salary: number;
  employees_paid: number;
  pending_payslips: number;
}

export interface PayslipFilters {
  skip?: number;
  limit?: number;
  employee_id?: number;
  month?: number;
  year?: number;
}

// ==================== Service Functions ====================

/**
 * Get payslips for current user
 */
export const getMyPayslips = async (filters?: PayslipFilters): Promise<PayslipListResponse> => {
  const params = new URLSearchParams();
  if (filters?.skip) params.append('skip', filters.skip.toString());
  if (filters?.limit) params.append('limit', filters.limit.toString());
  if (filters?.month) params.append('month', filters.month.toString());
  if (filters?.year) params.append('year', filters.year.toString());

  const response = await api.get(`/payslips/me?${params.toString()}`);
  return response.data;
};

/**
 * Get payslips for a specific employee (HR only)
 */
export const getEmployeePayslips = async (
  employeeId: number,
  filters?: PayslipFilters
): Promise<PayslipListResponse> => {
  const params = new URLSearchParams();
  if (filters?.skip) params.append('skip', filters.skip.toString());
  if (filters?.limit) params.append('limit', filters.limit.toString());
  if (filters?.month) params.append('month', filters.month.toString());
  if (filters?.year) params.append('year', filters.year.toString());

  const response = await api.get(`/payslips/employee/${employeeId}?${params.toString()}`);
  return response.data;
};

/**
 * Get all payslips (HR only)
 */
export const getAllPayslips = async (filters?: PayslipFilters): Promise<PayslipListResponse> => {
  const params = new URLSearchParams();
  if (filters?.skip) params.append('skip', filters.skip.toString());
  if (filters?.limit) params.append('limit', filters.limit.toString());
  if (filters?.employee_id) params.append('employee_id', filters.employee_id.toString());
  if (filters?.month) params.append('month', filters.month.toString());
  if (filters?.year) params.append('year', filters.year.toString());

  const response = await api.get(`/payslips?${params.toString()}`);
  return response.data;
};

/**
 * Get payslip by ID
 */
export const getPayslipById = async (payslipId: number): Promise<PayslipResponse> => {
  const response = await api.get(`/payslips/${payslipId}`);
  return response.data;
};

/**
 * Create new payslip (HR only)
 */
export const createPayslip = async (data: PayslipCreateRequest): Promise<PayslipResponse> => {
  const response = await api.post('/payslips', data);
  return response.data;
};

/**
 * Generate monthly payslips for all employees (HR only)
 */
export const generateMonthlyPayslips = async (
  data: PayslipGenerateRequest
): Promise<PayslipResponse[]> => {
  const response = await api.post('/payslips/generate', data);
  return response.data;
};

/**
 * Update payslip (HR only)
 */
export const updatePayslip = async (
  payslipId: number,
  data: PayslipUpdateRequest
): Promise<PayslipResponse> => {
  const response = await api.put(`/payslips/${payslipId}`, data);
  return response.data;
};

/**
 * Delete payslip (HR only)
 */
export const deletePayslip = async (payslipId: number): Promise<{ message: string }> => {
  const response = await api.delete(`/payslips/${payslipId}`);
  return response.data;
};

/**
 * Upload payslip document (HR only)
 */
export const uploadPayslipDocument = async (
  payslipId: number,
  file: File
): Promise<{ message: string; payslip_id: number; file_path: string; file_name: string }> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post(`/payslips/${payslipId}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });

  return response.data;
};

/**
 * Download payslip document
 */
export const downloadPayslipDocument = async (payslipId: number): Promise<Blob> => {
  const response = await api.get(`/payslips/${payslipId}/download`, {
    responseType: 'blob'
  });

  return response.data;
};

/**
 * Get payslip statistics (HR only)
 */
export const getPayslipStats = async (): Promise<PayslipStatsResponse> => {
  const response = await api.get('/payslips/stats/summary');
  return response.data;
};

// ==================== Helper Functions ====================

/**
 * Format payslip date for display
 */
export const formatPayslipDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  });
};

/**
 * Format month/year for display
 */
export const formatPayPeriod = (month: number, year: number): string => {
  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];
  return `${monthNames[month - 1]} ${year}`;
};

/**
 * Format currency
 */
export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount);
};

/**
 * Download payslip as file
 */
export const downloadPayslip = async (payslipId: number, filename?: string): Promise<void> => {
  try {
    const blob = await downloadPayslipDocument(payslipId);
    
    // Create blob URL
    const url = window.URL.createObjectURL(blob);
    
    // Create download link
    const link = document.createElement('a');
    link.href = url;
    link.download = filename || `payslip_${payslipId}.pdf`;
    
    // Trigger download
    document.body.appendChild(link);
    link.click();
    
    // Cleanup
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Error downloading payslip:', error);
    throw error;
  }
};

/**
 * Get month options for filter
 */
export const getMonthOptions = (): Array<{ value: number; label: string }> => {
  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];
  
  return monthNames.map((name, index) => ({
    value: index + 1,
    label: name
  }));
};

/**
 * Get year options for filter
 */
export const getYearOptions = (startYear: number = 2020): Array<{ value: number; label: string }> => {
  const currentYear = new Date().getFullYear();
  const years: Array<{ value: number; label: string }> = [];
  
  for (let year = currentYear; year >= startYear; year--) {
    years.push({
      value: year,
      label: year.toString()
    });
  }
  
  return years;
};

/**
 * Calculate take-home percentage
 */
export const calculateTakeHomePercentage = (payslip: PayslipResponse): number => {
  if (payslip.gross_salary === 0) return 0;
  return (payslip.net_salary / payslip.gross_salary) * 100;
};

/**
 * Group payslips by year
 */
export const groupPayslipsByYear = (
  payslips: PayslipResponse[]
): Record<number, PayslipResponse[]> => {
  return payslips.reduce((acc, payslip) => {
    const year = payslip.year;
    if (!acc[year]) {
      acc[year] = [];
    }
    acc[year].push(payslip);
    return acc;
  }, {} as Record<number, PayslipResponse[]>);
};

/**
 * Sort payslips by date (newest first)
 */
export const sortPayslipsByDate = (payslips: PayslipResponse[]): PayslipResponse[] => {
  return [...payslips].sort((a, b) => {
    const dateA = new Date(a.pay_date);
    const dateB = new Date(b.pay_date);
    return dateB.getTime() - dateA.getTime();
  });
};

/**
 * Validate payslip create data
 */
export const validatePayslipData = (data: PayslipCreateRequest): string | null => {
  if (!data.employee_id || data.employee_id <= 0) {
    return 'Invalid employee ID';
  }
  
  if (!data.pay_period_start || !data.pay_period_end || !data.pay_date) {
    return 'Pay period and pay date are required';
  }
  
  const startDate = new Date(data.pay_period_start);
  const endDate = new Date(data.pay_period_end);
  const payDate = new Date(data.pay_date);
  
  if (endDate < startDate) {
    return 'Pay period end date must be after start date';
  }
  
  if (payDate < endDate) {
    return 'Pay date should be on or after pay period end date';
  }
  
  if (!data.basic_salary || data.basic_salary < 0) {
    return 'Invalid basic salary';
  }
  
  return null;
};

export default {
  getMyPayslips,
  getEmployeePayslips,
  getAllPayslips,
  getPayslipById,
  createPayslip,
  generateMonthlyPayslips,
  updatePayslip,
  deletePayslip,
  uploadPayslipDocument,
  downloadPayslipDocument,
  getPayslipStats,
  formatPayslipDate,
  formatPayPeriod,
  formatCurrency,
  downloadPayslip,
  getMonthOptions,
  getYearOptions,
  calculateTakeHomePercentage,
  groupPayslipsByYear,
  sortPayslipsByDate,
  validatePayslipData
};

