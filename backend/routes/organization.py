"""
Organization/Hierarchy API Routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import User
from schemas.organization_schemas import (
    ManagerChainResponse,
    TeamHierarchyResponse,
    DepartmentHierarchyResponse,
    OrganizationHierarchyResponse,
    ReportingStructureResponse,
    OrgChartNode
)
from services.organization_service import OrganizationService
from utils.dependencies import get_current_user

router = APIRouter(prefix="/organization", tags=["Organization/Hierarchy"])


@router.get("/hierarchy", response_model=OrganizationHierarchyResponse)
async def get_full_organization_hierarchy(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get complete organization hierarchy with all departments and teams.
    
    **Access**: All authenticated users
    
    **Returns**:
    - All departments with their teams
    - Department heads
    - Team managers and members
    - Total counts
    
    **Use Case**: For organization chart visualization, HR analytics
    """
    return OrganizationService.get_full_org_hierarchy(db)


@router.get("/hierarchy/department/{department_id}", response_model=DepartmentHierarchyResponse)
async def get_department_hierarchy(
    department_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get hierarchy for a specific department.
    
    **Access**: All authenticated users
    
    **Path Parameters**:
    - `department_id`: Department ID
    
    **Returns**:
    - Department details
    - Department head
    - All teams in department
    - Team managers and members
    
    **Use Case**: Department-specific org chart
    """
    return OrganizationService.get_department_hierarchy(db, department_id)


@router.get("/hierarchy/team/{team_id}", response_model=TeamHierarchyResponse)
async def get_team_hierarchy(
    team_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get hierarchy for a specific team.
    
    **Access**: All authenticated users
    
    **Path Parameters**:
    - `team_id`: Team ID
    
    **Returns**:
    - Team details
    - Team manager
    - All team members
    
    **Use Case**: Team-specific org chart
    """
    return OrganizationService.get_team_hierarchy(db, team_id)


@router.get("/manager-chain/me", response_model=ManagerChainResponse)
async def get_my_manager_chain(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get my manager chain (reporting structure).
    
    **Access**: All authenticated users
    
    **Returns**:
    - Employee (me)
    - Direct manager
    - Manager's manager (skip-level)
    - Full chain to CEO
    
    **Use Case**: For profile page showing "Reports to" section
    """
    return OrganizationService.get_manager_chain(db, current_user.id)


@router.get("/manager-chain/{user_id}", response_model=ManagerChainResponse)
async def get_user_manager_chain(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get manager chain for any user.
    
    **Access**: All authenticated users
    
    **Path Parameters**:
    - `user_id`: User ID
    
    **Returns**:
    - Employee details
    - Direct manager
    - Manager's manager
    - Full reporting chain to CEO
    
    **Use Case**: HR viewing any employee's reporting structure
    """
    return OrganizationService.get_manager_chain(db, user_id)


@router.get("/reporting-structure/me", response_model=ReportingStructureResponse)
async def get_my_reporting_structure(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get my complete reporting structure.
    
    **Access**: All authenticated users
    
    **Returns**:
    - Employee (me)
    - Direct manager
    - Skip-level manager
    - Direct reports (if I'm a manager)
    - Peers (same manager)
    
    **Use Case**: Comprehensive view of reporting relationships
    """
    return OrganizationService.get_reporting_structure(db, current_user.id)


@router.get("/reporting-structure/{user_id}", response_model=ReportingStructureResponse)
async def get_user_reporting_structure(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get complete reporting structure for any user.
    
    **Access**: All authenticated users
    
    **Path Parameters**:
    - `user_id`: User ID
    
    **Returns**:
    - Employee details
    - Managers
    - Direct reports
    - Peers
    
    **Use Case**: HR viewing any employee's complete reporting structure
    """
    return OrganizationService.get_reporting_structure(db, user_id)


@router.get("/org-chart", response_model=OrgChartNode)
async def get_organization_chart(
    root_user_id: Optional[int] = Query(None, description="Root user ID (defaults to CEO)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get organization chart as tree structure.
    
    **Access**: All authenticated users
    
    **Query Parameters**:
    - `root_user_id`: Starting point for tree (default: CEO)
    
    **Returns**: Tree structure with user nodes and children (direct reports)
    
    **Use Case**: 
    - Interactive org chart visualization
    - Tree-view of reporting structure
    - Can start from any manager to see their sub-tree
    
    **Note**: Returns recursive tree structure where each node has a user and children array
    """
    return OrganizationService.get_org_chart(db, root_user_id)

