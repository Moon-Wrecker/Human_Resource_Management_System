"""
Pydantic schemas for Organization/Hierarchy API
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Response Schemas
class UserHierarchyNode(BaseModel):
    """Schema for a user node in hierarchy"""
    id: int
    name: str
    email: str
    position: Optional[str]
    department: Optional[str]
    team: Optional[str]
    role: str
    profile_image: Optional[str]
    hierarchy_level: Optional[int]
    
    class Config:
        from_attributes = True


class ManagerChainResponse(BaseModel):
    """Schema for manager chain (reporting structure)"""
    employee: UserHierarchyNode
    manager: Optional[UserHierarchyNode]
    manager_of_manager: Optional[UserHierarchyNode]
    chain: List[UserHierarchyNode]  # Full chain from employee to CEO
    

class TeamHierarchyResponse(BaseModel):
    """Schema for team hierarchy"""
    id: int
    name: str
    description: Optional[str]
    department: str
    manager: Optional[UserHierarchyNode]
    members: List[UserHierarchyNode]
    member_count: int
    
    class Config:
        from_attributes = True


class DepartmentHierarchyResponse(BaseModel):
    """Schema for department hierarchy"""
    id: int
    name: str
    code: Optional[str]
    description: Optional[str]
    head: Optional[UserHierarchyNode]
    teams: List[TeamHierarchyResponse]
    employee_count: int
    team_count: int
    
    class Config:
        from_attributes = True


class OrganizationHierarchyResponse(BaseModel):
    """Schema for complete organization hierarchy"""
    total_employees: int
    total_departments: int
    total_teams: int
    departments: List[DepartmentHierarchyResponse]


class ReportingStructureResponse(BaseModel):
    """Schema for reporting structure (who reports to whom)"""
    employee: UserHierarchyNode
    direct_manager: Optional[UserHierarchyNode]
    skip_level_manager: Optional[UserHierarchyNode]  # Manager's manager
    direct_reports: List[UserHierarchyNode]  # If user is a manager
    peers: List[UserHierarchyNode]  # Same manager
    


class OrgChartNode(BaseModel):
    """Schema for org chart tree node"""
    user: UserHierarchyNode
    children: List['OrgChartNode'] = []  # Recursive structure
    
    class Config:
        from_attributes = True


# Allow forward references for recursive model
OrgChartNode.model_rebuild()

