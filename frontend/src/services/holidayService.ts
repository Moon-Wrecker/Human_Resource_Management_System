/**
 * Holiday Service - API calls for holiday management
 */
import api from './api';

// Types
export interface Holiday {
  id: number;
  name: string;
  description?: string;
  start_date: string;
  end_date: string;
  is_mandatory: boolean;
  holiday_type?: string;
  is_active: boolean;
  created_by?: number;
  created_by_name?: string;
  created_at: string;
  duration_days: number;
}

export interface HolidayCreate {
  name: string;
  description?: string;
  start_date: string;  // Format: YYYY-MM-DD
  end_date: string;    // Format: YYYY-MM-DD
  is_mandatory: boolean;
  holiday_type?: 'national' | 'religious' | 'company' | 'regional' | 'optional';
}

export interface HolidayUpdate {
  name?: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  is_mandatory?: boolean;
  holiday_type?: string;
  is_active?: boolean;
}

export interface HolidayListResponse {
  holidays: Holiday[];
  total: number;
  page: number;
  page_size: number;
}

export interface HolidayStats {
  total_holidays: number;
  mandatory_holidays: number;
  optional_holidays: number;
  upcoming_holidays: number;
  holidays_this_month: number;
  holidays_this_year: number;
  by_type: Record<string, number>;
}

export interface HolidayFilters {
  page?: number;
  page_size?: number;
  include_inactive?: boolean;
  holiday_type?: string;
  year?: number;
  upcoming_only?: boolean;
}

// Holiday Service
const holidayService = {
  /**
   * Create a new holiday (HR only)
   */
  async createHoliday(data: HolidayCreate): Promise<Holiday> {
    const response = await api.post<Holiday>('/holidays', data);
    return response.data;
  },

  /**
   * Get all holidays with filters
   */
  async getHolidays(filters?: HolidayFilters): Promise<HolidayListResponse> {
    const response = await api.get<HolidayListResponse>('/holidays', { params: filters });
    return response.data;
  },

  /**
   * Get upcoming holidays (for dashboards)
   */
  async getUpcomingHolidays(daysAhead: number = 90, limit: number = 10): Promise<Holiday[]> {
    const response = await api.get<Holiday[]>('/holidays/upcoming', {
      params: { days_ahead: daysAhead, limit }
    });
    return response.data;
  },

  /**
   * Get holiday by ID
   */
  async getHolidayById(holidayId: number): Promise<Holiday> {
    const response = await api.get<Holiday>(`/holidays/${holidayId}`);
    return response.data;
  },

  /**
   * Update holiday (HR only)
   */
  async updateHoliday(holidayId: number, data: HolidayUpdate): Promise<Holiday> {
    const response = await api.put<Holiday>(`/holidays/${holidayId}`, data);
    return response.data;
  },

  /**
   * Delete holiday (HR only)
   */
  async deleteHoliday(holidayId: number): Promise<{ message: string }> {
    const response = await api.delete<{ message: string }>(`/holidays/${holidayId}`);
    return response.data;
  },

  /**
   * Get holiday statistics (HR/Manager)
   */
  async getHolidayStats(): Promise<HolidayStats> {
    const response = await api.get<HolidayStats>('/holidays/stats');
    return response.data;
  }
};

export default holidayService;

