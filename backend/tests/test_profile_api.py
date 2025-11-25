"""
Profile API Tests (Pytest)
Run with: pytest backend/tests/test_profile_api.py -v
"""
import pytest
import requests


@pytest.mark.profile
class TestProfileAPI:
    """Test suite for Profile endpoints"""
    
    def test_get_my_profile(self, api_base_url, employee_token):
        """Test get my profile"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/profile/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert "name" in data
        assert "email" in data
    
    def test_get_user_profile(self, api_base_url, hr_token, employee_token):
        """Test HR can get user profile by ID"""
        if not hr_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Get employee ID
        emp_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        if emp_response.status_code != 200:
            pytest.skip("Could not get employee info")
        
        employee_id = emp_response.json()["id"]
        
        response = requests.get(
            f"{api_base_url}/profile/{employee_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == employee_id
    
    @pytest.mark.permissions
    def test_get_user_profile_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot get other user's profile"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/profile/1",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_update_my_profile(self, api_base_url, employee_token):
        """Test update my profile"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        update_data = {
            "name": "Updated Name",
            "phone": "9999999999"
        }
        
        response = requests.put(
            f"{api_base_url}/profile/me",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=update_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["name"] == update_data["name"]
    
    def test_get_my_documents(self, api_base_url, employee_token):
        """Test get my documents"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/profile/documents",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_my_manager(self, api_base_url, employee_token):
        """Test get my manager"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/profile/manager",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        # May be 404 if no manager assigned
        assert response.status_code in [200, 404], f"Expected 200 or 404, got {response.status_code}"
    
    def test_get_my_team(self, api_base_url, manager_token):
        """Test manager can get their team"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/profile/team",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "team_members" in data or "members" in data
    
    def test_get_team_by_manager_id(self, api_base_url, hr_token, manager_token):
        """Test HR can get team by manager ID"""
        if not hr_token or not manager_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Get manager ID
        mgr_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        if mgr_response.status_code != 200:
            pytest.skip("Could not get manager info")
        
        manager_id = mgr_response.json()["id"]
        
        response = requests.get(
            f"{api_base_url}/profile/team/{manager_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "team_members" in data or "members" in data
    
    @pytest.mark.permissions
    def test_get_team_by_manager_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot get team by manager ID"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/profile/team/1",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_my_profile_stats(self, api_base_url, employee_token):
        """Test get my profile statistics"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/profile/stats",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_user_profile_stats(self, api_base_url, hr_token, employee_token):
        """Test HR can get user profile statistics"""
        if not hr_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Get employee ID
        emp_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        if emp_response.status_code != 200:
            pytest.skip("Could not get employee info")
        
        employee_id = emp_response.json()["id"]
        
        response = requests.get(
            f"{api_base_url}/profile/stats/{employee_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict)
    
    @pytest.mark.permissions
    def test_get_user_stats_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot get other user's statistics"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/profile/stats/1",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
