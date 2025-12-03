/**
 * Goal Service
 *
 * This service provides an interface for interacting with the backend's goal management endpoints.
 * It handles all aspects of goal and task management, including CRUD operations for goals,
 * checkpoints, comments, categories, and templates. It also provides functions for fetching
 * performance statistics.
 */

import api from "./api";
import { type AxiosResponse } from "axios";

// ==================== Enums ====================

export enum GoalStatus {
  NOT_STARTED = "not_started",
  IN_PROGRESS = "in_progress",
  COMPLETED = "completed",
  ON_HOLD = "on_hold",
  CANCELLED = "cancelled",
}

export enum GoalPriority {
  LOW = "low",
  MEDIUM = "medium",
  HIGH = "high",
  CRITICAL = "critical",
}

export enum CommentType {
  UPDATE = "update",
  FEEDBACK = "feedback",
  QUESTION = "question",
  BLOCKER = "blocker",
  MILESTONE = "milestone",
}

// ==================== Interfaces ====================

export interface Checkpoint {
  id: number;
  goal_id: number;
  title: string;
  description?: string;
  sequence_number: number;
  is_completed: boolean;
  completed_date?: string;
  completed_by?: number;
  created_at: string;
  updated_at?: string;
}

export interface GoalCategory {
  id: number;
  name: string;
  description?: string;
  color_code?: string;
  icon?: string;
  is_active: boolean;
  created_by?: number;
  created_at: string;
  updated_at?: string;
  goal_count?: number;
}

export interface GoalTemplate {
  id: number;
  name: string;
  description?: string;
  category_id?: number;
  priority: GoalPriority;
  default_duration_days?: number;
  checkpoint_template?: CheckpointTemplatePayload[];
  is_active: boolean;
  created_by?: number;
  created_at: string;
  updated_at?: string;
  usage_count: number;
}

export interface Goal {
  id: number;
  employee_id: number;
  employee_name?: string;
  employee_email?: string;
  title: string;
  description?: string;
  category_id?: number;
  priority: GoalPriority;
  start_date: string;
  target_date: string;
  status: GoalStatus;
  progress_percentage: number;
  completion_date?: string;
  is_personal: boolean;
  template_id?: number;
  assigned_by?: number;
  assigned_by_name?: string;
  category_name?: string;
  category_color?: string;
  checkpoints: Checkpoint[];
  total_checkpoints: number;
  completed_checkpoints: number;
  is_deleted: boolean;
  created_at: string;
  updated_at?: string;
  days_remaining?: number;
  is_overdue: boolean;
}

export interface GoalList {
  goals: Goal[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface GoalComment {
  id: number;
  goal_id: number;
  user_id: number;
  user_name?: string;
  user_role?: string;
  comment: string;
  comment_type: string;
  attachment_path?: string;
  created_at: string;
  updated_at?: string;
  is_deleted: boolean;
}

export interface GoalStats {
  total_goals: number;
  active_goals: number;
  completed_goals: number;
  overdue_goals: number;
  completion_rate: number;
  average_completion_days?: number;
  goals_by_priority: Record<string, number>;
  goals_by_category: Record<string, number>;
  goals_by_status: Record<string, number>;
}

export interface TeamGoalStats {
  total_team_goals: number;
  completed_team_goals: number;
  in_progress_team_goals: number;
  overdue_team_goals: number;
  team_completion_rate: number;
  team_members_stats: any[];
  top_performers: any[];
  needs_attention: any[];
}

export interface MessageResponse {
  message: string;
}

// ==================== Payload Interfaces ====================

export interface CheckpointTemplatePayload {
  title: string;
  description?: string;
}

export interface GetMyGoalsParams {
  skip?: number;
  limit?: number;
  status?: GoalStatus;
  priority?: GoalPriority;
  category_id?: number;
  is_overdue?: boolean;
}

export interface GetTeamGoalsParams {
  skip?: number;
  limit?: number;
  employee_id?: number;
  status?: GoalStatus;
  priority?: GoalPriority;
  is_overdue?: boolean;
}

export interface GetCategoriesParams {
  include_inactive?: boolean;
}

export interface GetTemplatesParams {
  include_inactive?: boolean;
}

export interface GoalCreatePayload {
  title: string;
  description?: string;
  category_id?: number;
  priority: GoalPriority;
  start_date: string;
  target_date: string;
  employee_id: number;
  is_personal?: boolean;
  template_id?: number;
  checkpoints?: {
    title: string;
    description?: string;
    sequence_number: number;
  }[];
}

export interface GoalUpdatePayload {
  title?: string;
  description?: string;
  category_id?: number;
  priority?: GoalPriority;
  start_date?: string;
  target_date?: string;
  status?: GoalStatus;
}

export interface GoalStatusUpdatePayload {
  status: GoalStatus;
}

export interface CheckpointCreatePayload {
  title: string;
  description?: string;
  sequence_number: number;
}

export interface CheckpointUpdatePayload {
  title?: string;
  description?: string;
  is_completed?: boolean;
}

export interface GoalCommentCreatePayload {
  comment: string;
  comment_type: CommentType;
}

export interface GoalCategoryCreatePayload {
  name: string;
  description?: string;
  color_code?: string;
  icon?: string;
}

export interface GoalCategoryUpdatePayload {
  name?: string;
  description?: string;
  color_code?: string;
  icon?: string;
  is_active?: boolean;
}

export interface GoalTemplateCreatePayload {
  name: string;
  description?: string;
  category_id?: number;
  priority: GoalPriority;
  default_duration_days?: number;
  checkpoint_template?: CheckpointTemplatePayload[];
}

/**
 * Goal Service Class
 */
class GoalService {
  private baseUrl = "/goals";

  // Goal CRUD
  createGoal(payload: GoalCreatePayload): Promise<Goal> {
    return api
      .post(this.baseUrl, payload)
      .then((res: AxiosResponse<Goal>) => res.data);
  }

  getMyGoals(params: GetMyGoalsParams): Promise<GoalList> {
    return api
      .get(`${this.baseUrl}/me`, { params })
      .then((res: AxiosResponse<GoalList>) => res.data);
  }

  getTeamGoals(params: GetTeamGoalsParams): Promise<GoalList> {
    return api
      .get(`${this.baseUrl}/team`, { params })
      .then((res: AxiosResponse<GoalList>) => res.data);
  }

  getGoalById(id: number): Promise<Goal> {
    return api
      .get(`${this.baseUrl}/${id}`)
      .then((res: AxiosResponse<Goal>) => res.data);
  }

  updateGoal(id: number, payload: GoalUpdatePayload): Promise<Goal> {
    return api
      .put(`${this.baseUrl}/${id}`, payload)
      .then((res: AxiosResponse<Goal>) => res.data);
  }

  updateGoalStatus(
    id: number,
    payload: GoalStatusUpdatePayload,
  ): Promise<Goal> {
    return api
      .patch(`${this.baseUrl}/${id}/status`, payload)
      .then((res: AxiosResponse<Goal>) => res.data);
  }

  deleteGoal(id: number): Promise<MessageResponse> {
    return api
      .delete(`${this.baseUrl}/${id}`)
      .then((res: AxiosResponse<MessageResponse>) => res.data);
  }

  // Checkpoints
  createCheckpoint(
    goalId: number,
    payload: CheckpointCreatePayload,
  ): Promise<Checkpoint> {
    return api
      .post(`${this.baseUrl}/${goalId}/checkpoints`, payload)
      .then((res: AxiosResponse<Checkpoint>) => res.data);
  }

  updateCheckpoint(
    id: number,
    payload: CheckpointUpdatePayload,
  ): Promise<Checkpoint> {
    return api
      .put(`${this.baseUrl}/checkpoints/${id}`, payload)
      .then((res: AxiosResponse<Checkpoint>) => res.data);
  }

  deleteCheckpoint(id: number): Promise<MessageResponse> {
    return api
      .delete(`/checkpoints/${id}`)
      .then((res: AxiosResponse<MessageResponse>) => res.data);
  }

  // Comments
  addComment(
    goalId: number,
    payload: GoalCommentCreatePayload,
  ): Promise<GoalComment> {
    return api
      .post(`${this.baseUrl}/${goalId}/comments`, payload)
      .then((res: AxiosResponse<GoalComment>) => res.data);
  }

  getComments(goalId: number): Promise<GoalComment[]> {
    return api
      .get(`${this.baseUrl}/${goalId}/comments`)
      .then((res: AxiosResponse<GoalComment[]>) => res.data);
  }

  // Categories and Templates
  getCategories(params: GetCategoriesParams = {}): Promise<GoalCategory[]> {
    return api
      .get(`${this.baseUrl}/categories`, { params })
      .then((res: AxiosResponse<GoalCategory[]>) => res.data);
  }

  createCategory(payload: GoalCategoryCreatePayload): Promise<GoalCategory> {
    return api
      .post(`${this.baseUrl}/categories`, payload)
      .then((res: AxiosResponse<GoalCategory>) => res.data);
  }

  updateCategory(
    id: number,
    payload: GoalCategoryUpdatePayload,
  ): Promise<GoalCategory> {
    return api
      .put(`${this.baseUrl}/categories/${id}`, payload)
      .then((res: AxiosResponse<GoalCategory>) => res.data);
  }

  getTemplates(params: GetTemplatesParams = {}): Promise<GoalTemplate[]> {
    return api
      .get(`${this.baseUrl}/templates`, { params })
      .then((res: AxiosResponse<GoalTemplate[]>) => res.data);
  }

  createTemplate(payload: GoalTemplateCreatePayload): Promise<GoalTemplate> {
    return api
      .post(`${this.baseUrl}/templates`, payload)
      .then((res: AxiosResponse<GoalTemplate>) => res.data);
  }

  getTemplateById(id: number): Promise<GoalTemplate> {
    return api
      .get(`${this.baseUrl}/templates/${id}`)
      .then((res: AxiosResponse<GoalTemplate>) => res.data);
  }

  // Stats
  getMyGoalStats(): Promise<GoalStats> {
    return api
      .get(`${this.baseUrl}/stats/me`)
      .then((res: AxiosResponse<GoalStats>) => res.data);
  }

  getTeamGoalStats(): Promise<TeamGoalStats> {
    return api
      .get(`${this.baseUrl}/stats/team`)
      .then((res: AxiosResponse<TeamGoalStats>) => res.data);
  }
}

// Export singleton instance
const goalService = new GoalService();
export default goalService;
