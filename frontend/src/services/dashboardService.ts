/**
 * Dashboard Service
 * API calls for dashboard data for all roles (HR, Manager, Employee)
 */

import api from '@/services/api';

// ==================== Type Definitions ====================

export interface HolidayInfo {
  id: number;
  name: string;
  description?: string;
  start_date: string;
  end_date: string;
  is_mandatory: boolean;
  holiday_type?: string;
}

export interface AttendanceInfo {
  date: string;
  check_in_time?: string;
  check_out_time?: string;
  status: string;
  hours_worked?: number;
}

export interface LeaveBalanceInfo {
  casual_leave: number;
  sick_leave: number;
  annual_leave: number;
  wfh_balance: number;
}

// HR Dashboard Types
export interface DepartmentEmployeeCount {
  department_id: number;
  department_name: string;
  employee_count: number;
}

export interface DepartmentAttendance {
  department_id: number;
  department_name: string;
  present_percentage: number;
  absent_percentage: number;
}

export interface DepartmentModulesCompleted {
  department_id: number;
  department_name: string;
  modules_completed: number;
}

export interface ActiveApplicationInfo {
  application_id: number;
  applicant_name: string;
  applied_role: string;
  applied_date: string;
  status: string;
  source?: string;
}

export interface HRDashboardData {
  departments: DepartmentEmployeeCount[];
  department_attendance: DepartmentAttendance[];
  department_modules: DepartmentModulesCompleted[];
  active_applications: ActiveApplicationInfo[];
  total_employees: number;
  total_departments: number;
  total_active_applications: number;
}

// Manager Dashboard Types
export interface TeamMemberAttendance {
  employee_id: number;
  employee_name: string;
  present_percentage: number;
  absent_percentage: number;
}

export interface TeamMemberModules {
  employee_id: number;
  employee_name: string;
  modules_completed: number;
}

export interface TeamGoalsStats {
  total_goals: number;
  completed_goals: number;
  in_progress_goals: number;
  not_started_goals: number;
  completion_percentage: number;
}

export interface TeamStats {
  team_id: number;
  team_name: string;
  total_members: number;
  team_training_hours: number;
  team_performance_score: number;
}

export interface ManagerDashboardData {
  personal_info: LeaveBalanceInfo;
  today_attendance?: AttendanceInfo;
  upcoming_holidays: HolidayInfo[];
  team_stats?: TeamStats;
  team_goals: TeamGoalsStats;
  team_attendance: TeamMemberAttendance[];
  team_modules_leaderboard: TeamMemberModules[];
  learner_rank?: number;
}

// Employee Dashboard Types
export interface GoalStats {
  total_goals: number;
  completed_goals: number;
  pending_goals: number;
  completion_percentage: number;
}

export interface EmployeeDashboardData {
  employee_name: string;
  leave_balance: LeaveBalanceInfo;
  today_attendance?: AttendanceInfo;
  upcoming_holidays: HolidayInfo[];
  learning_goals: GoalStats;
  learner_rank?: number;
}

// Performance Metrics Types
export interface MonthlyModulesCompleted {
  month: string;
  modules_completed: number;
}

export interface PerformanceMetrics {
  employee_id: number;
  employee_name: string;
  monthly_modules: MonthlyModulesCompleted[];
  total_modules_completed: number;
  attendance_rate: number;
  goals_completion_rate: number;
}

// ==================== Dashboard Service ====================

class DashboardService {
  /**
   * Get HR Dashboard Data
   * @returns HR dashboard data
   */
  async getHRDashboard(): Promise<HRDashboardData> {
    const response = await api.get('/dashboard/hr');
    return response.data;
  }

  /**
   * Get Manager Dashboard Data
   * @returns Manager dashboard data
   */
  async getManagerDashboard(): Promise<ManagerDashboardData> {
    const response = await api.get('/dashboard/manager');
    return response.data;
  }

  /**
   * Get Employee Dashboard Data
   * @returns Employee dashboard data
   */
  async getEmployeeDashboard(): Promise<EmployeeDashboardData> {
    const response = await api.get('/dashboard/employee');
    return response.data;
  }

  /**
   * Get Dashboard Data for Current User (auto-routes based on role)
   * @returns Dashboard data based on user role
   */
  async getMyDashboard(): Promise<{
    role: string;
    dashboard_data: HRDashboardData | ManagerDashboardData | EmployeeDashboardData;
  }> {
    const response = await api.get('/dashboard/me');
    return response.data;
  }

  /**
   * Get Employee Performance Metrics
   * @param employeeId - Employee ID
   * @param months - Number of months of data (1-24, default: 12)
   * @returns Performance metrics
   */
  async getEmployeePerformance(
    employeeId: number,
    months: number = 12
  ): Promise<PerformanceMetrics> {
    const response = await api.get(`/dashboard/performance/${employeeId}`, {
      params: { months }
    });
    return response.data;
  }

  /**
   * Get My Performance Metrics
   * @param months - Number of months of data (1-24, default: 12)
   * @returns Performance metrics
   */
  async getMyPerformance(months: number = 12): Promise<PerformanceMetrics> {
    const response = await api.get('/dashboard/performance/me', {
      params: { months }
    });
    return response.data;
  }
}

// Export singleton instance
export const dashboardService = new DashboardService();
export default dashboardService;

