"""
Dashboard API Tests (Pytest)
Run with: pytest backend/tests/test_dashboard_api.py -v
"""
import pytest
import requests


@pytest.mark.dashboard
class TestDashboardAPI:
    """Test suite for Dashboard endpoints"""
    
    def test_get_hr_dashboard(self, api_base_url, hr_token):
        """Test HR can access HR dashboard"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/dashboard/hr",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "departments" in data or "total_employees" in data
    
    @pytest.mark.permissions
    def test_get_hr_dashboard_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot access HR dashboard"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/dashboard/hr",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    @pytest.mark.permissions
    def test_get_hr_dashboard_manager_forbidden(self, api_base_url, manager_token):
        """Test manager cannot access HR dashboard"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/dashboard/hr",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_manager_dashboard(self, api_base_url, manager_token):
        """Test manager can access manager dashboard"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/dashboard/manager",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "personal_info" in data or "team_stats" in data or "today_attendance" in data
    
    @pytest.mark.permissions
    def test_get_manager_dashboard_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot access manager dashboard"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/dashboard/manager",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    @pytest.mark.permissions
    def test_get_manager_dashboard_hr_forbidden(self, api_base_url, hr_token):
        """Test HR cannot access manager dashboard"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/dashboard/manager",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_employee_dashboard(self, api_base_url, employee_token):
        """Test employee can access employee dashboard"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/dashboard/employee",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "employee_name" in data or "leave_balance" in data or "today_attendance" in data
    
    @pytest.mark.permissions
    def test_get_employee_dashboard_hr_forbidden(self, api_base_url, hr_token):
        """Test HR cannot access employee dashboard"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/dashboard/employee",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    @pytest.mark.permissions
    def test_get_employee_dashboard_manager_forbidden(self, api_base_url, manager_token):
        """Test manager cannot access employee dashboard"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/dashboard/employee",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_my_dashboard_hr(self, api_base_url, hr_token):
        """Test HR gets correct dashboard via /me endpoint"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/dashboard/me",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "role" in data
        assert data["role"] == "hr"
        assert "dashboard_data" in data
    
    def test_get_my_dashboard_manager(self, api_base_url, manager_token):
        """Test manager gets correct dashboard via /me endpoint"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/dashboard/me",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "role" in data
        assert data["role"] == "manager"
        assert "dashboard_data" in data
    
    def test_get_my_dashboard_employee(self, api_base_url, employee_token):
        """Test employee gets correct dashboard via /me endpoint"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/dashboard/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "role" in data
        assert data["role"] == "employee"
        assert "dashboard_data" in data
    
    def test_get_my_performance(self, api_base_url, employee_token):
        """Test get my performance metrics"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/dashboard/performance/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_my_performance_custom_months(self, api_base_url, employee_token):
        """Test get my performance with custom months parameter"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/dashboard/performance/me?months=6",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_employee_performance_own(self, api_base_url, employee_token):
        """Test employee can get their own performance"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        # Get employee ID
        me_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        if me_response.status_code != 200:
            pytest.skip("Could not get employee info")
        
        employee_id = me_response.json()["id"]
        
        response = requests.get(
            f"{api_base_url}/dashboard/performance/{employee_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict)
    
    @pytest.mark.permissions
    def test_get_employee_performance_other_forbidden(self, api_base_url, employee_token):
        """Test employee cannot view other employee's performance"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        # Try to access another employee's performance
        response = requests.get(
            f"{api_base_url}/dashboard/performance/99999",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        # Should be 403 or 404
        assert response.status_code in [403, 404], f"Expected 403 or 404, got {response.status_code}"
    
    def test_hr_can_view_any_performance(self, api_base_url, hr_token, employee_token):
        """Test HR can view any employee's performance"""
        if not hr_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Get employee ID
        me_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        if me_response.status_code != 200:
            pytest.skip("Could not get employee info")
        
        employee_id = me_response.json()["id"]
        
        response = requests.get(
            f"{api_base_url}/dashboard/performance/{employee_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict)
