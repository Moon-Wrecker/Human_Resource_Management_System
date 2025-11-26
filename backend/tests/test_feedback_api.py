"""
Feedback API Tests (Pytest)
Run with: pytest backend/tests/test_feedback_api.py -v
"""
import pytest
import requests
from datetime import datetime


@pytest.mark.feedback
class TestFeedbackAPI:
    """Test suite for Feedback endpoints"""
    
    @pytest.fixture(scope="class")
    def feedback_id(self, api_base_url, manager_token, employee_token):
        """Create a test feedback and return its ID, cleanup after tests"""
        if not manager_token or not employee_token:
            yield None
            return
        
        # Get employee ID
        emp_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        if emp_response.status_code != 200:
            yield None
            return
        
        employee_id = emp_response.json()["id"]
        
        # Create feedback
        feedback_data = {
            "employee_id": employee_id,
            "feedback_type": "positive",
            "description": "Great work on the recent project!",
            "subject": "Feedback for recent project",
            "rating": 5
        }
        
        response = requests.post(
            f"{api_base_url}/feedback",
            headers={"Authorization": f"Bearer {manager_token}"},
            json=feedback_data
        )
        
        feedback_id = None
        if response.status_code == 201:
            feedback_id = response.json()["id"]
        
        yield feedback_id
        
        # Cleanup - delete feedback after tests
        if feedback_id:
            requests.delete(
                f"{api_base_url}/feedback/{feedback_id}",
                headers={"Authorization": f"Bearer {manager_token}"}
            )
    
    def test_create_feedback(self, api_base_url, manager_token, employee_token):
        """Test manager can create feedback"""
        if not manager_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Get employee ID
        emp_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        if emp_response.status_code != 200:
            pytest.skip("Could not get employee info")
        
        employee_id = emp_response.json()["id"]
        
        feedback_data = {
            "employee_id": employee_id,
            "subject": "Feedback for recent project",
            "feedback_type": "constructive",
            "description": "Consider improving time management skills",
            "rating": 4
        }
        
        response = requests.post(
            f"{api_base_url}/feedback",
            headers={"Authorization": f"Bearer {manager_token}"},
            json=feedback_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert data["description"] == feedback_data["description"]
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/feedback/{data['id']}",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
    
    @pytest.mark.permissions
    def test_create_feedback_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot create feedback"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        feedback_data = {
            "employee_id": 1,
            "feedback_type": "positive",
            "description": "Unauthorized feedback",
            "subject": "Feedback for recent project",
            "rating": 4
        }
        
        response = requests.post(
            f"{api_base_url}/feedback",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=feedback_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_my_feedback(self, api_base_url, employee_token):
        """Test employee can get their own feedback"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/feedback/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "feedback" in data
        assert "total" in data
    
    def test_get_my_feedback_with_filters(self, api_base_url, employee_token):
        """Test get my feedback with type filter"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/feedback/me?feedback_type=positive",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "feedback" in data
    
    def test_get_employee_feedback(self, api_base_url, manager_token, employee_token):
        """Test manager can get employee feedback"""
        if not manager_token or not employee_token:
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
            f"{api_base_url}/feedback/employee/{employee_id}",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "feedback" in data
        assert "total" in data
    
    def test_get_feedback_given(self, api_base_url, manager_token):
        """Test manager can get feedback they gave"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/feedback/given",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "feedback" in data
        assert "total" in data
    
    @pytest.mark.permissions
    def test_get_feedback_given_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot access feedback given endpoint"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/feedback/given",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_all_feedback(self, api_base_url, hr_token):
        """Test HR can get all feedback"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/feedback",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "feedback" in data
        assert "total" in data
    
    def test_get_all_feedback_with_filters(self, api_base_url, hr_token):
        """Test get all feedback with filters"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/feedback?feedback_type=positive",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "feedback" in data
    
    @pytest.mark.permissions
    def test_get_all_feedback_manager_forbidden(self, api_base_url, manager_token):
        """Test manager cannot get all feedback"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/feedback",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_feedback_by_id(self, api_base_url, employee_token, feedback_id):
        """Test get feedback by ID"""
        if not employee_token or not feedback_id:
            pytest.skip("Employee token or feedback not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/feedback/{feedback_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == feedback_id
    
    def test_get_nonexistent_feedback(self, api_base_url, employee_token):
        """Test get non-existent feedback returns 404"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/feedback/99999",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    def test_update_feedback(self, api_base_url, manager_token, feedback_id):
        """Test manager can update their own feedback"""
        if not manager_token or not feedback_id:
            pytest.skip("Manager token or feedback not available (database not seeded)")
        
        update_data = {
            "description": "Updated feedback description",
            "rating": 4
        }
        
        response = requests.put(
            f"{api_base_url}/feedback/{feedback_id}",
            headers={"Authorization": f"Bearer {manager_token}"},
            json=update_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["description"] == update_data["description"]
    
    @pytest.mark.permissions
    def test_update_feedback_employee_forbidden(self, api_base_url, employee_token, feedback_id):
        """Test employee cannot update feedback"""
        if not employee_token or not feedback_id:
            pytest.skip("Employee token or feedback not available (database not seeded)")
        
        update_data = {"description": "Unauthorized update"}
        
        response = requests.put(
            f"{api_base_url}/feedback/{feedback_id}",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=update_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_feedback_stats(self, api_base_url, manager_token):
        """Test get feedback statistics"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/feedback/stats/summary",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "total_feedback" in data or "total" in data
    
    def test_get_feedback_stats_for_employee(self, api_base_url, manager_token, employee_token):
        """Test get feedback stats for specific employee"""
        if not manager_token or not employee_token:
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
            f"{api_base_url}/feedback/stats/summary?employee_id={employee_id}",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict)
    
    @pytest.mark.permissions
    def test_get_feedback_stats_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot access feedback stats"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/feedback/stats/summary",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_delete_feedback(self, api_base_url, manager_token, employee_token):
        """Test manager can delete their own feedback"""
        if not manager_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Get employee ID
        emp_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        if emp_response.status_code != 200:
            pytest.skip("Could not get employee info")
        
        employee_id = emp_response.json()["id"]
        
        # Create feedback to delete
        create_response = requests.post(
            f"{api_base_url}/feedback",
            headers={"Authorization": f"Bearer {manager_token}"},
            json={
                "employee_id": employee_id,
                "feedback_type": "general",
                "description": "Test for deletion",
                "subject": "Feedback for deletion",
                "rating": 4
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create feedback for delete test")
        
        test_id = create_response.json()["id"]
        
        # Delete
        response = requests.delete(
            f"{api_base_url}/feedback/{test_id}",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "message" in data
    
    @pytest.mark.permissions
    def test_delete_feedback_employee_forbidden(self, api_base_url, employee_token, feedback_id):
        """Test employee cannot delete feedback"""
        if not employee_token or not feedback_id:
            pytest.skip("Employee token or feedback not available (database not seeded)")
        
        response = requests.delete(
            f"{api_base_url}/feedback/{feedback_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
