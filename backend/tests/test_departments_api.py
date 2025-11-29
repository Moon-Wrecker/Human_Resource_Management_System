"""
Departments API Tests (Pytest)
Run with: pytest backend/tests/test_departments_api.py -v
"""
import pytest
import requests
import uuid


@pytest.mark.departments
class TestDepartmentsAPI:
    """Test suite for Departments endpoints"""
    
    @pytest.fixture(scope="class")
    def department_id(self, api_base_url, hr_token):
        """Create a test department and return its ID, cleanup after tests"""
        if not hr_token:
            yield None
            return
        
        department_data = {
            "name": "Test Department - Create Test" + str(uuid.uuid4().hex[:3]),
            "code": "TSTCREATE" + str(uuid.uuid4().hex[:3]),
            "description": "Test department for creation"
        }
              
        response = requests.post(
            f"{api_base_url}/departments",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=department_data
        )
        
        department_id = None
        if response.status_code == 201:
            department_id = response.json()["id"]
        
        yield department_id
        
        # Cleanup - delete department after tests
        if department_id:
            requests.delete(
                f"{api_base_url}/departments/{department_id}",
                headers={"Authorization": f"Bearer {hr_token}"}
            )
    
    def test_create_department(self, api_base_url, hr_token):
        """Test HR can create department"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        department_data = {
            "name": "Test Department - Create Test" + str(uuid.uuid4().hex[:3]),
            "code": "TSTCREATE" + str(uuid.uuid4().hex[:3]),
            "description": "Test department for creation"
        }
        
        response = requests.post(
            f"{api_base_url}/departments",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=department_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert data["name"] == department_data["name"]
        assert data["code"] == department_data["code"]
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/departments/{data['id']}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
    
    @pytest.mark.permissions
    def test_create_department_employee_forbidden(self, api_base_url, employee_token):
        """Test Employee cannot create department"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        department_data = {
            "name": "Unauthorized Department",
            "code": "UNAUTH"
        }
        
        response = requests.post(
            f"{api_base_url}/departments",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=department_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    @pytest.mark.permissions
    def test_create_department_manager_forbidden(self, api_base_url, manager_token):
        """Test Manager cannot create department"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        department_data = {
            "name": "Manager Department",
            "code": "MGR-DEPT"
        }
        
        response = requests.post(
            f"{api_base_url}/departments",
            headers={"Authorization": f"Bearer {manager_token}"},
            json=department_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_all_departments(self, api_base_url, employee_token):
        """Test get all departments"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/departments?page=1&page_size=50",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "departments" in data
        assert "total" in data
    
    def test_search_departments(self, api_base_url, employee_token):
        """Test search departments by name"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/departments?search=engineering",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "departments" in data
    
    def test_get_departments_with_pagination(self, api_base_url, employee_token):
        """Test departments pagination"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/departments?page=1&page_size=10",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "departments" in data
        assert "total" in data
    
    def test_get_department_by_id(self, api_base_url, employee_token, department_id):
        """Test get department by ID"""
        if not employee_token or not department_id:
            pytest.skip("Employee token or department not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/departments/{department_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == department_id
    
    def test_get_department_with_teams(self, api_base_url, employee_token, department_id):
        """Test get department with team details"""
        if not employee_token or not department_id:
            pytest.skip("Employee token or department not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/departments/{department_id}?include_teams=true",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == department_id
    
    def test_get_nonexistent_department(self, api_base_url, employee_token):
        """Test get non-existent department returns 404"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/departments/99999",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    def test_get_department_stats(self, api_base_url, hr_token):
        """Test get department statistics"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/departments/stats",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "total_departments" in data
    
    def test_get_department_stats_manager(self, api_base_url, manager_token):
        """Test manager can access department statistics"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/departments/stats",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "total_departments" in data
    
    @pytest.mark.permissions
    def test_get_department_stats_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot access department statistics"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/departments/stats",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_update_department(self, api_base_url, hr_token, department_id):
        """Test HR can update department"""
        if not hr_token or not department_id:
            pytest.skip("HR token or department not available (database not seeded)")
        
        update_data = {
            "name": "Updated Test Department" + str(uuid.uuid4().hex[:3]),
            "description": "Updated description"+ str(uuid.uuid4().hex[:3])
        }
        
        response = requests.put(
            f"{api_base_url}/departments/{department_id}",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=update_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]
    
    @pytest.mark.permissions
    def test_update_department_employee_forbidden(self, api_base_url, employee_token, department_id):
        """Test Employee cannot update department"""
        if not employee_token or not department_id:
            pytest.skip("Employee token or department not available (database not seeded)")
        
        update_data = {"name": "Unauthorized Update"}
        
        response = requests.put(
            f"{api_base_url}/departments/{department_id}",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=update_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    @pytest.mark.permissions
    def test_update_department_manager_forbidden(self, api_base_url, manager_token, department_id):
        """Test Manager cannot update department"""
        if not manager_token or not department_id:
            pytest.skip("Manager token or department not available (database not seeded)")
        
        update_data = {"name": "Manager Update"}
        
        response = requests.put(
            f"{api_base_url}/departments/{department_id}",
            headers={"Authorization": f"Bearer {manager_token}"},
            json=update_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_delete_department(self, api_base_url, hr_token):
        """Test HR can delete department"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        # Create a department to delete
        create_response = requests.post(
            f"{api_base_url}/departments",
            headers={"Authorization": f"Bearer {hr_token}"},
            json={
                "name": "Test for Delete" + str(uuid.uuid4().hex[:3]),
                "code": "TST-DEL" + str(uuid.uuid4().hex[:3]),
                "description": "Will be deleted"
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create department for delete test")
        
        test_id = create_response.json()["id"]
        
        # Delete
        response = requests.delete(
            f"{api_base_url}/departments/{test_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "message" in data
    
    @pytest.mark.permissions
    def test_delete_department_employee_forbidden(self, api_base_url, hr_token, employee_token):
        """Test Employee cannot delete department"""
        if not hr_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Create a test department
        create_response = requests.post(
            f"{api_base_url}/departments",
            headers={"Authorization": f"Bearer {hr_token}"},
            json={
                "name": "Test for Delete Permission"+str(uuid.uuid4().hex[:3]),
                "code": "TST-PERM"+str(uuid.uuid4().hex[:3]),
                "description": "Test"
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create department for delete test")
        
        test_id = create_response.json()["id"]
        
        # Try to delete as employee
        response = requests.delete(
            f"{api_base_url}/departments/{test_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/departments/{test_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
