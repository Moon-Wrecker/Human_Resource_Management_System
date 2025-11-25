"""
Employees API Tests (Pytest)
Run with: pytest backend/tests/test_employees_api.py -v
"""
import pytest
import requests
import uuid
from datetime import datetime


@pytest.mark.employees
class TestEmployeesAPI:
    """Test suite for Employees endpoints"""
    
    @pytest.fixture(scope="class")
    def employee_id(self, api_base_url, hr_token):
        """Create a test employee and return its ID, cleanup after tests"""
        if not hr_token:
            yield None
            return
        
        # Create employee
        employee_data = {
            "name": "Test Employee - API Test",
            "email": "test.employee.api@company.com",
            "password": "testpass123",
            "employee_id": "TST-EMP-001",
            "position": "Test Engineer",
            "role": "employee"
        }
        
        response = requests.post(
            f"{api_base_url}/employees",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=employee_data
        )
        
        employee_id = None
        if response.status_code == 201:
            employee_id = response.json()["id"]
        
        yield employee_id
        
        # Cleanup - deactivate employee after tests
        if employee_id:
            requests.delete(
                f"{api_base_url}/employees/{employee_id}",
                headers={"Authorization": f"Bearer {hr_token}"}
            )

    def test_create_employee(self, api_base_url, hr_token):
        """Test HR can create a full employee record with all fields"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")

        # Generate unique email to avoid conflicts
        unique_email = f"test.create.{uuid.uuid4().hex[:8]}@company.com"

        today = datetime.now().date().isoformat()

        employee_data = {
            "name": "Test Employee - Create Test",
            "email": unique_email,
            "password": "testpass123",
            "phone": "9876543210",
            "employee_id": "EMP016",
            "position": "Software Engineer",
            "department_id": 1,         
            "team_id": 1,                
            "manager_id": 3,             
            "role": "employee",
            "hierarchy_level": 10,
            "date_of_birth": today,
            "join_date": today,
            "salary": 50000,
            "emergency_contact": "9999999999",
            "casual_leave_balance": 12,
            "sick_leave_balance": 10,
            "annual_leave_balance": 15,
            "wfh_balance": 52
        }

        # Create employee
        response = requests.post(
            f"{api_base_url}/employees",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=employee_data
        )

        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()

        # Assertions
        assert "id" in data
        assert data["name"] == employee_data["name"]
        assert data["email"] == employee_data["email"]
        assert data["employee_id"] == employee_data["employee_id"]
        assert data["position"] == employee_data["position"]
        assert data["role"] == "employee"

        # Cleanup (delete created employee)
        requests.delete(
            f"{api_base_url}/employees/{data['id']}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )

    @pytest.mark.permissions
    def test_create_employee_manager_forbidden(self, api_base_url, manager_token):
        """Test Manager cannot create employee"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        employee_data = {
            "name": "Unauthorized Employee",
            "email": "unauth@company.com",
            "password": "password123"
        }
        
        response = requests.post(
            f"{api_base_url}/employees",
            headers={"Authorization": f"Bearer {manager_token}"},
            json=employee_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    @pytest.mark.permissions
    def test_create_employee_employee_forbidden(self, api_base_url, employee_token):
        """Test Employee cannot create employee"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        employee_data = {
            "name": "Unauthorized Employee",
            "email": "unauth2@company.com",
            "password": "password123"
        }
        
        response = requests.post(
            f"{api_base_url}/employees",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=employee_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_all_employees(self, api_base_url, hr_token):
        """Test get all employees"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/employees?page=1&page_size=50",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "employees" in data
        assert "total" in data
        assert "page" in data
        assert "total_pages" in data
    
    def test_search_employees(self, api_base_url, hr_token):
        """Test search employees"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/employees?search=john",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "employees" in data
    
    def test_filter_employees_by_department(self, api_base_url, hr_token):
        """Test filter employees by department"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/employees?department_id=1",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "employees" in data
    
    def test_filter_employees_by_role(self, api_base_url, hr_token):
        """Test filter employees by role"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/employees?role=employee",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "employees" in data
    
    def test_filter_employees_by_active_status(self, api_base_url, hr_token):
        """Test filter employees by active status"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/employees?is_active=true",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "employees" in data
    
    @pytest.mark.permissions
    def test_get_all_employees_employee_forbidden(self, api_base_url, employee_token):
        """Test Employee cannot get all employees list"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/employees",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_employee_stats(self, api_base_url, hr_token):
        """Test get employee statistics"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/employees/stats",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "total_employees" in data
    
    @pytest.mark.permissions
    def test_get_employee_stats_employee_forbidden(self, api_base_url, employee_token):
        """Test Employee cannot access employee stats"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/employees/stats",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_employee_by_id(self, api_base_url, hr_token, employee_id):
        """Test get employee by ID"""
        if not hr_token or not employee_id:
            pytest.skip("HR token or employee not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/employees/{employee_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == employee_id
    
    def test_get_nonexistent_employee(self, api_base_url, hr_token):
        """Test get non-existent employee returns 404"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/employees/99999",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    @pytest.mark.permissions
    def test_get_employee_by_id_employee_forbidden(self, api_base_url, employee_token):
        """Test Employee cannot get employee by ID"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/employees/1",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_update_employee(self, api_base_url, hr_token, employee_id):
        """Test HR can update employee"""
        if not hr_token or not employee_id:
            pytest.skip("HR token or employee not available (database not seeded)")
        
        update_data = {
            "name": "Updated Test Employee",
            "position": "Senior Test Engineer"
        }
        
        response = requests.put(
            f"{api_base_url}/employees/{employee_id}",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=update_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["position"] == update_data["position"]
    
    @pytest.mark.permissions
    def test_update_employee_manager_forbidden(self, api_base_url, manager_token, employee_id):
        """Test Manager cannot update employee"""
        if not manager_token or not employee_id:
            pytest.skip("Manager token or employee not available (database not seeded)")
        
        update_data = {"name": "Unauthorized Update"}
        
        response = requests.put(
            f"{api_base_url}/employees/{employee_id}",
            headers={"Authorization": f"Bearer {manager_token}"},
            json=update_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    @pytest.mark.permissions
    def test_update_employee_employee_forbidden(self, api_base_url, employee_token, employee_id):
        """Test Employee cannot update employee"""
        if not employee_token or not employee_id:
            pytest.skip("Employee token or employee not available (database not seeded)")
        
        update_data = {"name": "Unauthorized Update"}
        
        response = requests.put(
            f"{api_base_url}/employees/{employee_id}",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=update_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_deactivate_employee(self, api_base_url, hr_token):
        """Test HR can deactivate employee"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        # Create an employee to deactivate
        create_response = requests.post(
            f"{api_base_url}/employees",
            headers={"Authorization": f"Bearer {hr_token}"},
            json={
                "name": "Test for Deactivation",
                "email": "test.deactivate@company.com",
                "password": "testpass123",
                "employee_id": "TST-DEACT-001"
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create employee for deactivation test")
        
        test_id = create_response.json()["id"]
        
        # Deactivate
        response = requests.delete(
            f"{api_base_url}/employees/{test_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "message" in data
    
    @pytest.mark.permissions
    def test_deactivate_employee_manager_forbidden(self, api_base_url, hr_token, manager_token):
        """Test Manager cannot deactivate employee"""
        if not hr_token or not manager_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Create a test employee
        create_response = requests.post(
            f"{api_base_url}/employees",
            headers={"Authorization": f"Bearer {hr_token}"},
            json={
                "name": "Test for Delete Permission",
                "email": "test.perm.del@company.com",
                "password": "testpass123",
                "employee_id": "TST-PERM-DEL"
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create employee for delete test")
        
        test_id = create_response.json()["id"]
        
        # Try to deactivate as manager
        response = requests.delete(
            f"{api_base_url}/employees/{test_id}",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/employees/{test_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
    
    @pytest.mark.permissions
    def test_deactivate_employee_employee_forbidden(self, api_base_url, employee_token):
        """Test Employee cannot deactivate employee"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.delete(
            f"{api_base_url}/employees/1",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
