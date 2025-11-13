/**
 * Attendance Service
 * API calls for attendance management
 */

import api, { handleApiError } from './api';

// Types/Interfaces
export type AttendanceRecord = {
  id: number;
  employee_id: number;
  employee_name?: string;
  employee_employee_id?: string;
  date: string;
  status: 'present' | 'absent' | 'leave' | 'wfh' | 'holiday';
  check_in_time?: string;
  check_out_time?: string;
  hours_worked?: number;
  location?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export type PunchInRequest = {
  location?: string;
  status?: 'present' | 'wfh';
  notes?: string;
}

export type PunchInResponse = {
  message: string;
  attendance: AttendanceRecord;
  already_punched_in: boolean;
}

export type PunchOutRequest = {
  notes?: string;
}

export type PunchOutResponse = {
  message: string;
  attendance: AttendanceRecord;
  hours_worked: number;
}

export type AttendanceHistoryResponse = {
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  records: AttendanceRecord[];
}

export type AttendanceSummary = {
  employee_id: number;
  employee_name: string;
  month: number;
  year: number;
  total_present: number;
  total_absent: number;
  total_leave: number;
  total_wfh: number;
  total_holiday: number;
  total_working_days: number;
  total_hours_worked: number;
  average_hours_per_day: number;
  late_arrivals: number;
  early_departures: number;
  attendance_percentage: number;
  from_date: string;
  to_date: string;
}

export type TeamAttendanceRecord = {
  employee_id: number;
  employee_name: string;
  employee_employee_id: string;
  job_role?: string;
  date: string;
  status: string;
  check_in_time?: string;
  check_out_time?: string;
  hours_worked?: number;
  location?: string;
}

export type TeamAttendanceResponse = {
  date: string;
  total_team_members: number;
  present: number;
  absent: number;
  on_leave: number;
  wfh: number;
  records: TeamAttendanceRecord[];
}

export type DepartmentAttendanceStats = {
  department_id: number;
  department_name: string;
  total_employees: number;
  present: number;
  absent: number;
  on_leave: number;
  wfh: number;
  attendance_percentage: number;
}

export type AllAttendanceResponse = {
  date: string;
  total_employees: number;
  present: number;
  absent: number;
  on_leave: number;
  wfh: number;
  department_stats: DepartmentAttendanceStats[];
  records: AttendanceRecord[];
  total_records: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export type MarkAttendanceRequest = {
  employee_id: number;
  attendance_date: string;
  status: 'present' | 'absent' | 'leave' | 'wfh' | 'holiday';
  check_in_time?: string;
  check_out_time?: string;
  location?: string;
  notes?: string;
}

export type MarkAttendanceResponse = {
  message: string;
  attendance: AttendanceRecord;
  marked_by: string;
}

export type AttendanceFilters = {
  start_date?: string;
  end_date?: string;
  status?: string;
  page?: number;
  page_size?: number;
}

export type AllAttendanceFilters = {
  date?: string;
  start_date?: string;
  end_date?: string;
  department_id?: number;
  team_id?: number;
  status?: string;
  page?: number;
  page_size?: number;
}

class AttendanceService {
  /**
   * Punch in for the day
   */
  async punchIn(data: PunchInRequest = {}): Promise<PunchInResponse> {
    try {
      const response = await api.post('/attendance/punch-in', {
        location: data.location || 'office',
        status: data.status || 'present',
        notes: data.notes
      });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Punch out for the day
   */
  async punchOut(data: PunchOutRequest = {}): Promise<PunchOutResponse> {
    try {
      const response = await api.post('/attendance/punch-out', {
        notes: data.notes
      });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get today's attendance status
   */
  async getTodayAttendance(): Promise<AttendanceRecord | null> {
    try {
      const response = await api.get('/attendance/today');
      return response.data;
    } catch (error) {
      // Return null if not found (404)
      if ((error as any)?.response?.status === 404) {
        return null;
      }
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get my attendance history
   */
  async getMyAttendance(filters: AttendanceFilters = {}): Promise<AttendanceHistoryResponse> {
    try {
      const params = new URLSearchParams();
      
      if (filters.start_date) params.append('start_date', filters.start_date);
      if (filters.end_date) params.append('end_date', filters.end_date);
      if (filters.status) params.append('status', filters.status);
      if (filters.page) params.append('page', filters.page.toString());
      if (filters.page_size) params.append('page_size', filters.page_size.toString());

      const response = await api.get(`/attendance/me?${params.toString()}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get monthly attendance summary
   */
  async getMySummary(month?: number, year?: number): Promise<AttendanceSummary> {
    try {
      const params = new URLSearchParams();
      
      if (month) params.append('month', month.toString());
      if (year) params.append('year', year.toString());

      const response = await api.get(`/attendance/me/summary?${params.toString()}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get team attendance (Manager only)
   */
  async getTeamAttendance(date?: string): Promise<TeamAttendanceResponse> {
    try {
      const params = new URLSearchParams();
      if (date) params.append('date', date);

      const response = await api.get(`/attendance/team?${params.toString()}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Get all attendance (HR only)
   */
  async getAllAttendance(filters: AllAttendanceFilters = {}): Promise<AllAttendanceResponse> {
    try {
      const params = new URLSearchParams();
      
      if (filters.date) params.append('date', filters.date);
      if (filters.start_date) params.append('start_date', filters.start_date);
      if (filters.end_date) params.append('end_date', filters.end_date);
      if (filters.department_id) params.append('department_id', filters.department_id.toString());
      if (filters.team_id) params.append('team_id', filters.team_id.toString());
      if (filters.status) params.append('status', filters.status);
      if (filters.page) params.append('page', filters.page.toString());
      if (filters.page_size) params.append('page_size', filters.page_size.toString());

      const response = await api.get(`/attendance/all?${params.toString()}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Manually mark attendance (HR only)
   */
  async markAttendance(data: MarkAttendanceRequest): Promise<MarkAttendanceResponse> {
    try {
      const response = await api.post('/attendance/mark', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Delete attendance record (HR only)
   */
  async deleteAttendance(attendanceId: number): Promise<{ message: string; success: boolean }> {
    try {
      const response = await api.delete(`/attendance/${attendanceId}`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  }

  /**
   * Format date for API (YYYY-MM-DD)
   */
  formatDate(date: Date): string {
    return date.toISOString().split('T')[0];
  }

  /**
   * Format time for display (HH:MM AM/PM)
   */
  formatTime(dateTimeString?: string): string {
    if (!dateTimeString) return '--:--';
    
    const date = new Date(dateTimeString);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: true 
    });
  }

  /**
   * Format duration (hours) for display
   */
  formatDuration(hours?: number): string {
    if (!hours) return '0h 0m';
    
    const h = Math.floor(hours);
    const m = Math.round((hours - h) * 60);
    
    return `${h}h ${m}m`;
  }

  /**
   * Get status color for UI
   */
  getStatusColor(status: string): string {
    const colors: Record<string, string> = {
      present: 'bg-green-100 text-green-800',
      absent: 'bg-red-100 text-red-800',
      leave: 'bg-yellow-100 text-yellow-800',
      wfh: 'bg-blue-100 text-blue-800',
      holiday: 'bg-purple-100 text-purple-800',
    };
    
    return colors[status] || 'bg-gray-100 text-gray-800';
  }

  /**
   * Get status label for display
   */
  getStatusLabel(status: string): string {
    const labels: Record<string, string> = {
      present: 'Present',
      absent: 'Absent',
      leave: 'On Leave',
      wfh: 'Work From Home',
      holiday: 'Holiday',
    };
    
    return labels[status] || status;
  }
}

// Export singleton instance
const attendanceService = new AttendanceService();
export default attendanceService;

// Also export the class for testing
export { AttendanceService };

