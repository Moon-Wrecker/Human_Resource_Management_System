"""
Organization/Hierarchy API Tests (Pytest)
Run with: pytest backend/tests/test_organization_api.py -v
"""

import pytest
import requests


@pytest.mark.organization
class TestOrganizationAPI:
    """Test suite for Organization/Hierarchy endpoints"""

    def test_get_full_organization_hierarchy(self, api_base_url, employee_token):
        """Test get complete organization hierarchy"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")

        response = requests.get(
            f"{api_base_url}/organization/hierarchy",
            headers={"Authorization": f"Bearer {employee_token}"},
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "departments" in data or "total_departments" in data

    def test_get_department_hierarchy(self, api_base_url, employee_token):
        """Test get department hierarchy"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")

        response = requests.get(
            f"{api_base_url}/organization/hierarchy/department/1",
            headers={"Authorization": f"Bearer {employee_token}"},
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "head" in data or "id" in data or "teams" in data

    def test_get_nonexistent_department_hierarchy(self, api_base_url, employee_token):
        """Test get non-existent department returns 404"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")

        response = requests.get(
            f"{api_base_url}/organization/hierarchy/department/99999",
            headers={"Authorization": f"Bearer {employee_token}"},
        )

        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    def test_get_team_hierarchy(self, api_base_url, employee_token):
        """Test get team hierarchy"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")

        response = requests.get(
            f"{api_base_url}/organization/hierarchy/team/1",
            headers={"Authorization": f"Bearer {employee_token}"},
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert (
            "id" in data
            or "manager" in data
            or "members" in data
            or "member_count" in data
        )

    def test_get_nonexistent_team_hierarchy(self, api_base_url, employee_token):
        """Test get non-existent team returns 404"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")

        response = requests.get(
            f"{api_base_url}/organization/hierarchy/team/99999",
            headers={"Authorization": f"Bearer {employee_token}"},
        )

        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    def test_get_my_manager_chain(self, api_base_url, employee_token):
        """Test get my manager chain"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")

        response = requests.get(
            f"{api_base_url}/organization/manager-chain/me",
            headers={"Authorization": f"Bearer {employee_token}"},
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "employee" in data or "manager_chain" in data

    def test_get_user_manager_chain(self, api_base_url, hr_token, employee_token):
        """Test get manager chain for specific user"""
        if not hr_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")

        # Get employee ID
        emp_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"},
        )

        if emp_response.status_code != 200:
            pytest.skip("Could not get employee info")

        employee_id = emp_response.json()["id"]

        response = requests.get(
            f"{api_base_url}/organization/manager-chain/{employee_id}",
            headers={"Authorization": f"Bearer {hr_token}"},
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "employee" in data or "manager_chain" in data

    def test_get_my_reporting_structure(self, api_base_url, employee_token):
        """Test get my reporting structure"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")

        response = requests.get(
            f"{api_base_url}/organization/reporting-structure/me",
            headers={"Authorization": f"Bearer {employee_token}"},
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "employee" in data or "direct_manager" in data

    def test_get_user_reporting_structure(self, api_base_url, hr_token, employee_token):
        """Test get reporting structure for specific user"""
        if not hr_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")

        # Get employee ID
        emp_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"},
        )

        if emp_response.status_code != 200:
            pytest.skip("Could not get employee info")

        employee_id = emp_response.json()["id"]

        response = requests.get(
            f"{api_base_url}/organization/reporting-structure/{employee_id}",
            headers={"Authorization": f"Bearer {hr_token}"},
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "employee" in data or "direct_manager" in data

    def test_get_organization_chart(self, api_base_url, employee_token):
        """Test get organization chart"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")

        response = requests.get(
            f"{api_base_url}/organization/org-chart",
            headers={"Authorization": f"Bearer {employee_token}"},
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "user" in data or "children" in data

    def test_get_organization_chart_with_root(self, api_base_url, employee_token):
        """Test get organization chart with specific root user"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")

        # Get employee ID
        emp_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"},
        )

        if emp_response.status_code != 200:
            pytest.skip("Could not get employee info")

        employee_id = emp_response.json()["id"]

        response = requests.get(
            f"{api_base_url}/organization/org-chart?root_user_id={employee_id}",
            headers={"Authorization": f"Bearer {employee_token}"},
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "user" in data

    @pytest.mark.permissions
    def test_hierarchy_requires_authentication(self, api_base_url):
        """Test hierarchy endpoints require authentication"""
        response = requests.get(f"{api_base_url}/organization/hierarchy")

        assert response.status_code == 403, f"Expected 403, got {response.status_code}"

    @pytest.mark.permissions
    def test_manager_chain_requires_authentication(self, api_base_url):
        """Test manager chain requires authentication"""
        response = requests.get(f"{api_base_url}/organization/manager-chain/me")

        assert response.status_code == 403, f"Expected 403, got {response.status_code}"

    @pytest.mark.permissions
    def test_reporting_structure_requires_authentication(self, api_base_url):
        """Test reporting structure requires authentication"""
        response = requests.get(f"{api_base_url}/organization/reporting-structure/me")

        assert response.status_code == 403, f"Expected 403, got {response.status_code}"

    @pytest.mark.permissions
    def test_org_chart_requires_authentication(self, api_base_url):
        """Test org chart requires authentication"""
        response = requests.get(f"{api_base_url}/organization/org-chart")

        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
