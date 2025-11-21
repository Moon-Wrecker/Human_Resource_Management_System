/**
 * Announcement Service
 * Service layer for announcements API calls
 */

import api from './api';

// Types
export interface Announcement {
  id: number;
  title: string;
  message: string;
  link?: string;
  target_departments?: string;
  target_roles?: string;
  is_urgent: boolean;
  created_by: number;
  created_by_name?: string;
  created_at: string;
  published_date: string;
  expiry_date?: string;
  is_active: boolean;
  is_expired: boolean;
}

export interface AnnouncementListResponse {
  announcements: Announcement[];
  total: number;
  active: number;
  urgent: number;
}

export interface CreateAnnouncementData {
  title: string;
  message: string;
  link?: string;
  target_departments?: string;
  target_roles?: string;
  is_urgent?: boolean;
  expiry_date?: string;
}

export interface UpdateAnnouncementData {
  title?: string;
  message?: string;
  link?: string;
  target_departments?: string;
  target_roles?: string;
  is_urgent?: boolean;
  expiry_date?: string;
  is_active?: boolean;
}

export interface AnnouncementStats {
  total: number;
  active: number;
  urgent: number;
  expired: number;
  inactive: number;
}

/**
 * Announcement Service Class
 */
class AnnouncementService {
  private baseUrl = '/announcements';

  /**
   * Get all announcements
   * @param params Query parameters for filtering and pagination
   * @returns List of announcements with metadata
   */
  async getAnnouncements(params?: {
    include_expired?: boolean;
    include_inactive?: boolean;
    skip?: number;
    limit?: number;
  }): Promise<AnnouncementListResponse> {
    try {
      const response = await api.get<AnnouncementListResponse>(this.baseUrl, {
        params: params || {},
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching announcements:', error);
      throw error;
    }
  }

  /**
   * Get announcement by ID
   * @param id Announcement ID
   * @returns Announcement object
   */
  async getAnnouncementById(id: number): Promise<Announcement> {
    try {
      const response = await api.get<Announcement>(`${this.baseUrl}/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching announcement ${id}:`, error);
      throw error;
    }
  }

  /**
   * Create a new announcement (HR/Manager only)
   * @param data Announcement data
   * @returns Created announcement
   */
  async createAnnouncement(data: CreateAnnouncementData): Promise<Announcement> {
    try {
      const response = await api.post<Announcement>(this.baseUrl, data);
      return response.data;
    } catch (error) {
      console.error('Error creating announcement:', error);
      throw error;
    }
  }

  /**
   * Update an announcement (HR/Manager only)
   * @param id Announcement ID
   * @param data Update data
   * @returns Updated announcement
   */
  async updateAnnouncement(
    id: number,
    data: UpdateAnnouncementData
  ): Promise<Announcement> {
    try {
      const response = await api.put<Announcement>(`${this.baseUrl}/${id}`, data);
      return response.data;
    } catch (error) {
      console.error(`Error updating announcement ${id}:`, error);
      throw error;
    }
  }

  /**
   * Delete an announcement (HR/Manager only)
   * @param id Announcement ID
   * @param hardDelete Whether to permanently delete (default: false)
   * @returns Success message
   */
  async deleteAnnouncement(
    id: number,
    hardDelete: boolean = false
  ): Promise<{ message: string }> {
    try {
      const response = await api.delete<{ message: string }>(
        `${this.baseUrl}/${id}`,
        {
          params: { hard_delete: hardDelete },
        }
      );
      return response.data;
    } catch (error) {
      console.error(`Error deleting announcement ${id}:`, error);
      throw error;
    }
  }

  /**
   * Get announcement statistics (HR/Manager only)
   * @returns Statistics object
   */
  async getStatistics(): Promise<AnnouncementStats> {
    try {
      const response = await api.get<AnnouncementStats>(
        `${this.baseUrl}/stats/summary`
      );
      return response.data;
    } catch (error) {
      console.error('Error fetching announcement statistics:', error);
      throw error;
    }
  }

  /**
   * Get recent announcements (helper method)
   * @param limit Number of announcements to fetch (default: 5)
   * @returns Recent announcements
   */
  async getRecentAnnouncements(limit: number = 5): Promise<Announcement[]> {
    try {
      const response = await this.getAnnouncements({ limit });
      return response.announcements;
    } catch (error) {
      console.error('Error fetching recent announcements:', error);
      throw error;
    }
  }

  /**
   * Get urgent announcements (helper method)
   * @returns Urgent announcements only
   */
  async getUrgentAnnouncements(): Promise<Announcement[]> {
    try {
      const response = await this.getAnnouncements({ limit: 100 });
      return response.announcements.filter((a) => a.is_urgent);
    } catch (error) {
      console.error('Error fetching urgent announcements:', error);
      throw error;
    }
  }

  /**
   * Check if announcement is expired
   * @param announcement Announcement object
   * @returns True if expired
   */
  isExpired(announcement: Announcement): boolean {
    if (!announcement.expiry_date) return false;
    return new Date(announcement.expiry_date) < new Date();
  }

  /**
   * Format announcement date for display
   * @param dateString ISO date string
   * @returns Formatted date string
   */
  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    });
  }

  /**
   * Format announcement datetime for display
   * @param dateString ISO datetime string
   * @returns Formatted datetime string
   */
  formatDateTime(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  }
}

// Export singleton instance
const announcementService = new AnnouncementService();
export default announcementService;

