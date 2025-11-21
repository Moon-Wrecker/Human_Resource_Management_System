/**
 * API Configuration
 * Base URLs and API endpoints configuration
 */

// Backend API base URL
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// API version prefix
export const API_V1_PREFIX = '/api/v1';

// Full API URL
export const API_URL = `${API_BASE_URL}${API_V1_PREFIX}`;

// API Endpoints
export const API_ENDPOINTS = {
  // Authentication
  AUTH: {
    LOGIN: '/auth/login',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh',
    ME: '/auth/me',
    CHANGE_PASSWORD: '/auth/change-password',
    RESET_PASSWORD: '/auth/reset-password',
  },
  
  // Users
  USERS: {
    ME: '/users/me',
    BY_ID: (id: number) => `/users/${id}`,
    UPLOAD_PROFILE: (id: number) => `/users/${id}/upload-profile`,
    UPLOAD_DOCUMENT: (id: number) => `/users/${id}/upload-document`,
    DOCUMENTS: (id: number) => `/users/${id}/documents`,
  },
  
  // Dashboard
  DASHBOARD: {
    HR: '/dashboard/hr',
    EMPLOYEE: '/dashboard/employee',
    MANAGER: '/dashboard/manager',
  },
  
  // Employees
  EMPLOYEES: {
    LIST: '/employees',
    BY_ID: (id: number) => `/employees/${id}`,
    SEARCH: '/employees/search',
    HIERARCHY: '/employees/hierarchy',
  },
  
  // Jobs
  JOBS: {
    LIST: '/jobs',
    BY_ID: (id: number) => `/jobs/${id}`,
    PUBLISH: (id: number) => `/jobs/${id}/publish`,
    CLOSE: (id: number) => `/jobs/${id}/close`,
  },
  
  // Applications
  APPLICATIONS: {
    LIST: '/applications',
    BY_ID: (id: number) => `/applications/${id}`,
    STATUS: (id: number) => `/applications/${id}/status`,
    SCREEN: (id: number) => `/applications/${id}/screen`,
  },
  
  // Attendance
  ATTENDANCE: {
    PUNCH_IN: '/attendance/punch-in',
    PUNCH_OUT: '/attendance/punch-out',
    LIST: '/attendance',
    MY_RECORDS: '/attendance/my-records',
    SUMMARY: '/attendance/summary',
  },
  
  // Leaves
  LEAVES: {
    LIST: '/leaves',
    BY_ID: (id: number) => `/leaves/${id}`,
    APPROVE: (id: number) => `/leaves/${id}/approve`,
    REJECT: (id: number) => `/leaves/${id}/reject`,
    BALANCE: '/leaves/balance',
    PENDING: '/leaves/pending',
  },
  
  // Goals
  GOALS: {
    LIST: '/goals',
    BY_ID: (id: number) => `/goals/${id}`,
    PROGRESS: (id: number) => `/goals/${id}/progress`,
    CHECKPOINT: (id: number) => `/goals/${id}/checkpoint`,
  },
  
  // Skills
  SKILLS: {
    MODULES: '/skills/modules',
    ENROLL: '/skills/enroll',
    MY_ENROLLMENTS: '/skills/my-enrollments',
    PROGRESS: (id: number) => `/skills/enrollments/${id}/progress`,
  },
  
  // Feedback
  FEEDBACK: {
    LIST: '/feedback',
    BY_ID: (id: number) => `/feedback/${id}`,
    SUMMARY: '/feedback/summary',
  },
  
  // Announcements
  ANNOUNCEMENTS: {
    LIST: '/announcements',
    BY_ID: (id: number) => `/announcements/${id}`,
  },
  
  // Policies
  POLICIES: {
    LIST: '/policies',
    BY_ID: (id: number) => `/policies/${id}`,
    DOWNLOAD: (id: number) => `/policies/${id}/download`,
  },
  
  // Payslips
  PAYSLIPS: {
    LIST: '/payslips',
    BY_ID: (id: number) => `/payslips/${id}`,
    DOWNLOAD: (id: number) => `/payslips/${id}/download`,
  },
  
  // Notifications
  NOTIFICATIONS: {
    LIST: '/notifications',
    UNREAD_COUNT: '/notifications/unread-count',
    READ: (id: number) => `/notifications/${id}/read`,
    READ_ALL: '/notifications/read-all',
  },
  
  // Teams
  TEAMS: {
    LIST: '/teams',
    BY_ID: (id: number) => `/teams/${id}`,
    MEMBERS: (id: number) => `/teams/${id}/members`,
  },
  
  // Departments
  DEPARTMENTS: {
    LIST: '/departments',
    BY_ID: (id: number) => `/departments/${id}`,
  },
  
  // Holidays
  HOLIDAYS: {
    LIST: '/holidays',
    BY_ID: (id: number) => `/holidays/${id}`,
  },
  
  // Requests
  REQUESTS: {
    LIST: '/requests',
    BY_ID: (id: number) => `/requests/${id}`,
    APPROVE: (id: number) => `/requests/${id}/approve`,
    REJECT: (id: number) => `/requests/${id}/reject`,
    PENDING: '/requests/pending',
  },
};

export default {
  API_BASE_URL,
  API_URL,
  API_ENDPOINTS,
};


