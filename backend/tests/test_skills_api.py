"""
Skills/Modules Management API Tests (Pytest)
Run with: pytest backend/tests/test_skills_api.py -v
"""
import pytest
import requests
import uuid
from datetime import datetime, timedelta


@pytest.mark.skills
class TestSkillsAPI:
    """Test suite for Skills/Modules Management endpoints"""
    
    @pytest.fixture(scope="function")
    def skill_module_id(self, api_base_url, hr_token):
        """Create a test skill module and return its ID, cleanup after tests"""
        if not hr_token:
            yield None
            return
        
        # Create skill module with unique name
        unique_id = uuid.uuid4().hex[:8]
        module_data = {
            "name": f"Test Python Programming Module {unique_id}",
            "description": "Learn Python programming fundamentals",
            "category": "Programming",
            "difficulty_level": "beginner",
            "duration_hours": 40,
            "skill_areas": "Python, Programming, Backend"
        }
        
        response = requests.post(
            f"{api_base_url}/skills/modules",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=module_data
        )
        
        module_id = None
        if response.status_code == 201:
            module_id = response.json()["id"]
        
        yield module_id
        
        # Cleanup - delete module after tests
        if module_id:
            requests.delete(
                f"{api_base_url}/skills/modules/{module_id}",
                headers={"Authorization": f"Bearer {hr_token}"}
            )
    
    def test_create_skill_module(self, api_base_url, hr_token):
        """Test HR can create skill module"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        module_data = {
            "name": "Advanced JavaScript - Test",
            "description": "Master advanced JavaScript concepts",
            "category": "Programming",
            "difficulty_level": "advanced",
            "duration_hours": 60,
            "skill_areas": "JavaScript, Frontend, Web Development"
        }
        
        response = requests.post(
            f"{api_base_url}/skills/modules",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=module_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert data["name"] == module_data["name"]
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/skills/modules/{data['id']}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
    
    @pytest.mark.permissions
    def test_create_module_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot create skill module"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        module_data = {
            "name": "Unauthorized Module",
            "description": "This should not be created"
        }
        
        response = requests.post(
            f"{api_base_url}/skills/modules",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=module_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_all_modules(self, api_base_url, employee_token):
        """Test get all skill modules"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/skills/modules",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "modules" in data
        assert "total" in data
    
    def test_search_modules(self, api_base_url, employee_token):
        """Test search skill modules"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/skills/modules?search=python",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "modules" in data
    
    def test_filter_modules_by_category(self, api_base_url, employee_token):
        """Test filter modules by category"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/skills/modules?category=Programming",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "modules" in data
    
    def test_filter_modules_by_difficulty(self, api_base_url, employee_token):
        """Test filter modules by difficulty"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/skills/modules?difficulty=beginner",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "modules" in data
    
    def test_get_module_by_id(self, api_base_url, employee_token, skill_module_id):
        """Test get module by ID"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        if not skill_module_id:
            pytest.skip("Module ID not available (database not seeded)")

        response = requests.get(
            f"{api_base_url}/skills/modules/{skill_module_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == skill_module_id
    
    def test_update_skill_module(self, api_base_url, hr_token, skill_module_id):
        """Test HR can update skill module"""
        if not hr_token or not skill_module_id:
            pytest.skip("HR token or module not available (database not seeded)")
        
        update_data = {
            "description": "Updated description for Python module",
            "duration_hours": 50
        }
        
        response = requests.put(
            f"{api_base_url}/skills/modules/{skill_module_id}",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=update_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["description"] == update_data["description"]
    
    @pytest.mark.permissions
    def test_update_module_employee_forbidden(self, api_base_url, employee_token, skill_module_id):
        """Test employee cannot update skill module"""
        if not employee_token or not skill_module_id:
            pytest.skip("Employee token or module not available (database not seeded)")
        
        update_data = {"description": "Unauthorized update"}
        
        response = requests.put(
            f"{api_base_url}/skills/modules/{skill_module_id}",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=update_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_enroll_in_module(self, api_base_url, employee_token, skill_module_id):
        """Test employee can enroll in module"""
        if not employee_token or not skill_module_id:
            pytest.skip("Employee token or module not available (database not seeded)")
        
        enrollment_data = {
            "module_id": skill_module_id,
            "target_completion_date": (datetime.now() + timedelta(days=30)).date().isoformat()
        }
        
        response = requests.post(
            f"{api_base_url}/skills/enroll",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=enrollment_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert data["module_id"] == skill_module_id
    
    def test_get_my_enrollments(self, api_base_url, employee_token):
        """Test get my enrollments"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/skills/my-enrollments",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, list)
    
    def test_filter_my_enrollments_by_status(self, api_base_url, employee_token):
        """Test filter my enrollments by status"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/skills/my-enrollments?status=pending",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_all_enrollments(self, api_base_url, hr_token):
        """Test HR can get all enrollments"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/skills/enrollments",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "enrollments" in data
        assert "total" in data
    
    @pytest.mark.permissions
    def test_get_all_enrollments_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot get all enrollments"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/skills/enrollments",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_skill_stats(self, api_base_url, hr_token):
        """Test HR can get skill statistics"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/skills/stats",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict)
    
    @pytest.mark.permissions
    def test_get_stats_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot access skill statistics"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/skills/stats",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_delete_skill_module(self, api_base_url, hr_token):
        """Test HR can delete skill module"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        # Create module to delete
        create_response = requests.post(
            f"{api_base_url}/skills/modules",
            headers={"Authorization": f"Bearer {hr_token}"},
            json={
                "name": "Module for Delete Test",
                "description": "Will be deleted"
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create module for delete test")
        
        test_id = create_response.json()["id"]
        
        # Delete
        response = requests.delete(
            f"{api_base_url}/skills/modules/{test_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "message" in data
    
    @pytest.mark.permissions
    def test_delete_module_employee_forbidden(self, api_base_url, employee_token, skill_module_id):
        """Test employee cannot delete skill module"""
        if not employee_token or not skill_module_id:
            pytest.skip("Employee token or module not available (database not seeded)")
        
        response = requests.delete(
            f"{api_base_url}/skills/modules/{skill_module_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
