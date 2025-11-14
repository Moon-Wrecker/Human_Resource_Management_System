/**
 * Organization/Hierarchy Service - API calls for org structure
 */
import api from './api';

// Types
export interface UserHierarchyNode {
  id: number;
  name: string;
  email: string;
  position?: string;
  department?: string;
  team?: string;
  role: string;
  profile_image?: string;
  hierarchy_level?: number;
}

export interface ManagerChain {
  employee: UserHierarchyNode;
  manager?: UserHierarchyNode;
  manager_of_manager?: UserHierarchyNode;
  chain: UserHierarchyNode[];  // Full chain from employee to CEO
}

export interface TeamHierarchy {
  id: number;
  name: string;
  description?: string;
  department: string;
  manager?: UserHierarchyNode;
  members: UserHierarchyNode[];
  member_count: number;
}

export interface DepartmentHierarchy {
  id: number;
  name: string;
  code?: string;
  description?: string;
  head?: UserHierarchyNode;
  teams: TeamHierarchy[];
  employee_count: number;
  team_count: number;
}

export interface OrganizationHierarchy {
  total_employees: number;
  total_departments: number;
  total_teams: number;
  departments: DepartmentHierarchy[];
}

export interface ReportingStructure {
  employee: UserHierarchyNode;
  direct_manager?: UserHierarchyNode;
  skip_level_manager?: UserHierarchyNode;
  direct_reports: UserHierarchyNode[];  // If user is a manager
  peers: UserHierarchyNode[];  // Same manager
}

export interface OrgChartNode {
  user: UserHierarchyNode;
  children: OrgChartNode[];  // Recursive structure
}

// Organization Service
const organizationService = {
  /**
   * Get complete organization hierarchy
   */
  async getFullHierarchy(): Promise<OrganizationHierarchy> {
    const response = await api.get<OrganizationHierarchy>('/organization/hierarchy');
    return response.data;
  },

  /**
   * Get department hierarchy
   */
  async getDepartmentHierarchy(departmentId: number): Promise<DepartmentHierarchy> {
    const response = await api.get<DepartmentHierarchy>(`/organization/hierarchy/department/${departmentId}`);
    return response.data;
  },

  /**
   * Get team hierarchy
   */
  async getTeamHierarchy(teamId: number): Promise<TeamHierarchy> {
    const response = await api.get<TeamHierarchy>(`/organization/hierarchy/team/${teamId}`);
    return response.data;
  },

  /**
   * Get my manager chain (for logged-in user)
   */
  async getMyManagerChain(): Promise<ManagerChain> {
    const response = await api.get<ManagerChain>('/organization/manager-chain/me');
    return response.data;
  },

  /**
   * Get manager chain for any user
   */
  async getUserManagerChain(userId: number): Promise<ManagerChain> {
    const response = await api.get<ManagerChain>(`/organization/manager-chain/${userId}`);
    return response.data;
  },

  /**
   * Get my reporting structure (for logged-in user)
   */
  async getMyReportingStructure(): Promise<ReportingStructure> {
    const response = await api.get<ReportingStructure>('/organization/reporting-structure/me');
    return response.data;
  },

  /**
   * Get reporting structure for any user
   */
  async getUserReportingStructure(userId: number): Promise<ReportingStructure> {
    const response = await api.get<ReportingStructure>(`/organization/reporting-structure/${userId}`);
    return response.data;
  },

  /**
   * Get organization chart as tree
   * @param rootUserId - Optional starting point (defaults to CEO)
   */
  async getOrgChart(rootUserId?: number): Promise<OrgChartNode> {
    const response = await api.get<OrgChartNode>('/organization/org-chart', {
      params: rootUserId ? { root_user_id: rootUserId } : undefined
    });
    return response.data;
  }
};

export default organizationService;

