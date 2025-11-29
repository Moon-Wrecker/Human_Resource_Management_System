"""
Organization/Hierarchy Service - Business logic for org structure and hierarchy
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import User, Department, Team
from schemas.organization_schemas import (
    UserHierarchyNode,
    ManagerChainResponse,
    TeamHierarchyResponse,
    DepartmentHierarchyResponse,
    OrganizationHierarchyResponse,
    ReportingStructureResponse,
    OrgChartNode,
)
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class OrganizationService:
    """Service class for organization hierarchy operations"""

    @staticmethod
    def get_manager_chain(db: Session, user_id: int) -> ManagerChainResponse:
        """
        Get the manager chain (reporting structure) for a user.
        Returns employee, immediate manager, manager's manager, and full chain to top.
        """
        user = db.query(User).filter(User.id == user_id, User.is_active == True).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found",
            )

        # Build full chain
        chain = []
        current_user = user
        visited_ids = set()  # Prevent infinite loops

        while current_user:
            # Add current user to chain
            chain.append(OrganizationService._format_user_node(current_user, db))

            # Check for circular reference
            if current_user.id in visited_ids:
                logger.warning(
                    f"Circular reference detected in manager chain for user {user_id}"
                )
                break
            visited_ids.add(current_user.id)

            # Move to manager
            if current_user.manager_id:
                current_user = (
                    db.query(User)
                    .filter(User.id == current_user.manager_id, User.is_active == True)
                    .first()
                )
            else:
                break

        # Extract specific levels
        employee = chain[0] if len(chain) > 0 else None
        manager = chain[1] if len(chain) > 1 else None
        manager_of_manager = chain[2] if len(chain) > 2 else None

        return ManagerChainResponse(
            employee=employee,
            manager=manager,
            manager_of_manager=manager_of_manager,
            chain=chain,
        )

    @staticmethod
    def get_reporting_structure(
        db: Session, user_id: int
    ) -> ReportingStructureResponse:
        """
        Get complete reporting structure for a user.
        Includes direct reports (if manager), peers, and management chain.
        """
        user = db.query(User).filter(User.id == user_id, User.is_active == True).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found",
            )

        # Get employee and managers
        employee_node = OrganizationService._format_user_node(user, db)

        direct_manager = None
        if user.manager_id:
            manager = (
                db.query(User)
                .filter(User.id == user.manager_id, User.is_active == True)
                .first()
            )
            if manager:
                direct_manager = OrganizationService._format_user_node(manager, db)

        skip_level_manager = None
        if user.manager_id:
            manager = db.query(User).filter(User.id == user.manager_id).first()
            if manager and manager.manager_id:
                skip_level = (
                    db.query(User)
                    .filter(User.id == manager.manager_id, User.is_active == True)
                    .first()
                )
                if skip_level:
                    skip_level_manager = OrganizationService._format_user_node(
                        skip_level, db
                    )

        # Get direct reports (if user is a manager)
        direct_reports_users = (
            db.query(User)
            .filter(User.manager_id == user_id, User.is_active == True)
            .all()
        )
        direct_reports = [
            OrganizationService._format_user_node(u, db) for u in direct_reports_users
        ]

        # Get peers (same manager)
        peers = []
        if user.manager_id:
            peers_users = (
                db.query(User)
                .filter(
                    User.manager_id == user.manager_id,
                    User.id != user_id,
                    User.is_active == True,
                )
                .all()
            )
            peers = [OrganizationService._format_user_node(u, db) for u in peers_users]

        return ReportingStructureResponse(
            employee=employee_node,
            direct_manager=direct_manager,
            skip_level_manager=skip_level_manager,
            direct_reports=direct_reports,
            peers=peers,
        )

    @staticmethod
    def get_full_org_hierarchy(db: Session) -> OrganizationHierarchyResponse:
        """
        Get complete organization hierarchy with all departments and teams.
        """
        departments = db.query(Department).filter(Department.is_active == True).all()

        dept_hierarchies = []
        for dept in departments:
            dept_hierarchy = OrganizationService._build_department_hierarchy(dept, db)
            dept_hierarchies.append(dept_hierarchy)

        # Get totals
        total_employees = db.query(User).filter(User.is_active == True).count()
        total_departments = len(departments)
        total_teams = db.query(Team).filter(Team.is_active == True).count()

        return OrganizationHierarchyResponse(
            total_employees=total_employees,
            total_departments=total_departments,
            total_teams=total_teams,
            departments=dept_hierarchies,
        )

    @staticmethod
    def get_department_hierarchy(
        db: Session, department_id: int
    ) -> DepartmentHierarchyResponse:
        """Get hierarchy for a specific department"""
        department = (
            db.query(Department)
            .filter(Department.id == department_id, Department.is_active == True)
            .first()
        )

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with ID {department_id} not found",
            )

        return OrganizationService._build_department_hierarchy(department, db)

    @staticmethod
    def get_team_hierarchy(db: Session, team_id: int) -> TeamHierarchyResponse:
        """Get hierarchy for a specific team"""
        team = db.query(Team).filter(Team.id == team_id, Team.is_active == True).first()

        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Team with ID {team_id} not found",
            )

        return OrganizationService._build_team_hierarchy(team, db)

    @staticmethod
    def get_org_chart(db: Session, root_user_id: Optional[int] = None) -> OrgChartNode:
        """
        Get organization chart as tree structure.
        If root_user_id is None, finds the CEO (user with no manager).
        """
        if root_user_id:
            root_user = (
                db.query(User)
                .filter(User.id == root_user_id, User.is_active == True)
                .first()
            )

            if not root_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with ID {root_user_id} not found",
                )
        else:
            # Find CEO (user with lowest hierarchy_level or no manager)
            root_user = (
                db.query(User)
                .filter(User.is_active == True, User.manager_id.is_(None))
                .order_by(User.hierarchy_level)
                .first()
            )

            if not root_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No root user (CEO) found in organization",
                )

        # Build tree recursively
        return OrganizationService._build_org_tree(root_user, db, set())

    @staticmethod
    def _build_org_tree(user: User, db: Session, visited: set) -> OrgChartNode:
        """Recursively build org chart tree"""
        # Prevent circular references
        if user.id in visited:
            return OrgChartNode(
                user=OrganizationService._format_user_node(user, db), children=[]
            )

        visited.add(user.id)

        # Get direct reports
        direct_reports = (
            db.query(User)
            .filter(User.manager_id == user.id, User.is_active == True)
            .all()
        )

        # Build children recursively
        children = [
            OrganizationService._build_org_tree(report, db, visited.copy())
            for report in direct_reports
        ]

        return OrgChartNode(
            user=OrganizationService._format_user_node(user, db), children=children
        )

    @staticmethod
    def _build_department_hierarchy(
        department: Department, db: Session
    ) -> DepartmentHierarchyResponse:
        """Build department hierarchy with teams"""
        # Get department head
        head = None
        if department.head_id:
            head_user = (
                db.query(User)
                .filter(User.id == department.head_id, User.is_active == True)
                .first()
            )
            if head_user:
                head = OrganizationService._format_user_node(head_user, db)

        # Get teams
        teams = (
            db.query(Team)
            .filter(Team.department_id == department.id, Team.is_active == True)
            .all()
        )

        team_hierarchies = [
            OrganizationService._build_team_hierarchy(team, db) for team in teams
        ]

        # Count employees
        employee_count = (
            db.query(User)
            .filter(User.department_id == department.id, User.is_active == True)
            .count()
        )

        return DepartmentHierarchyResponse(
            id=department.id,
            name=department.name,
            code=department.code,
            description=department.description,
            head=head,
            teams=team_hierarchies,
            employee_count=employee_count,
            team_count=len(team_hierarchies),
        )

    @staticmethod
    def _build_team_hierarchy(team: Team, db: Session) -> TeamHierarchyResponse:
        """Build team hierarchy with members"""
        # Get department name
        department_name = "Unknown"
        if team.department_id:
            dept = (
                db.query(Department).filter(Department.id == team.department_id).first()
            )
            if dept:
                department_name = dept.name

        # Get manager
        manager = None
        if team.manager_id:
            manager_user = (
                db.query(User)
                .filter(User.id == team.manager_id, User.is_active == True)
                .first()
            )
            if manager_user:
                manager = OrganizationService._format_user_node(manager_user, db)

        # Get members
        members_users = (
            db.query(User).filter(User.team_id == team.id, User.is_active == True).all()
        )

        members = [OrganizationService._format_user_node(u, db) for u in members_users]

        return TeamHierarchyResponse(
            id=team.id,
            name=team.name,
            description=team.description,
            department=department_name,
            manager=manager,
            members=members,
            member_count=len(members),
        )

    @staticmethod
    def _format_user_node(user: User, db: Session) -> UserHierarchyNode:
        """Format user to hierarchy node"""
        # Get department name
        department_name = None
        if user.department_id:
            dept = (
                db.query(Department).filter(Department.id == user.department_id).first()
            )
            if dept:
                department_name = dept.name

        # Get team name
        team_name = None
        if user.team_id:
            team = db.query(Team).filter(Team.id == user.team_id).first()
            if team:
                team_name = team.name

        return UserHierarchyNode(
            id=user.id,
            name=user.name,
            email=user.email,
            position=user.job_role,
            department=department_name,
            team=team_name,
            role=user.role.value if user.role else "employee",
            profile_image=user.profile_image_path,
            hierarchy_level=user.hierarchy_level,
        )
