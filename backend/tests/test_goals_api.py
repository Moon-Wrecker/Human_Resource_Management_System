"""
Goals API Tests (Pytest)
Run with: pytest backend/tests/test_goals_api.py -v
"""
import pytest
import requests
from datetime import datetime, timedelta


@pytest.mark.goals
class TestGoalsAPI:
    """Test suite for Goals & Task Management endpoints"""
    
    @pytest.fixture(scope="class")
    def goal_id(self, api_base_url, manager_token, employee_token):
        """Create a test goal and return its ID, cleanup after tests"""
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
        
        # Create goal
        target_date = (datetime.now() + timedelta(days=30)).date().isoformat()
        goal_data = {
            "title": "Test Goal - API Test",
            "description": "This is a test goal for API testing",
            "employee_id": employee_id,
            "target_date": target_date,
            "priority": "medium",
            "is_personal": False
        }
        
        response = requests.post(
            f"{api_base_url}/goals",
            headers={"Authorization": f"Bearer {manager_token}"},
            json=goal_data
        )
        
        goal_id = None
        if response.status_code == 201:
            goal_id = response.json()["id"]
        
        yield goal_id
        
        # Cleanup - delete goal after tests
        if goal_id:
            requests.delete(
                f"{api_base_url}/goals/{goal_id}",
                headers={"Authorization": f"Bearer {manager_token}"}
            )
    
    def test_create_goal_manager_assigned(self, api_base_url, manager_token, employee_token):
        """Test manager can create goal for team member"""
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
        
        target_date = (datetime.now() + timedelta(days=30)).date().isoformat()
        goal_data = {
            "title": "Complete Project Documentation",
            "description": "Write comprehensive documentation for the project",
            "employee_id": employee_id,
            "target_date": target_date,
            "priority": "high",
            "is_personal": False,
            "start_date": (datetime.now() - timedelta(days=1)).date().isoformat(),
            "end_date": (datetime.now() + timedelta(days=30)).date().isoformat()
        }
        
        response = requests.post(
            f"{api_base_url}/goals",
            headers={"Authorization": f"Bearer {manager_token}"},
            json=goal_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert data["title"] == goal_data["title"]
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/goals/{data['id']}",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
    
    def test_create_personal_goal(self, api_base_url, employee_token):
        """Test employee can create personal goal"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        # Get employee ID
        emp_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        if emp_response.status_code != 200:
            pytest.skip("Could not get employee info")
        
        employee_id = emp_response.json()["id"]
        
        target_date = (datetime.now() + timedelta(days=60)).date().isoformat()
        goal_data = {
            "title": "Learn Python Advanced Concepts",
            "description": "Master decorators, generators, and async programming",
            "employee_id": employee_id,
            "target_date": target_date,
            "priority": "medium",
            "is_personal": True
        }
        
        response = requests.post(
            f"{api_base_url}/goals",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=goal_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/goals/{data['id']}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
    
    def test_get_my_goals(self, api_base_url, employee_token):
        """Test get my goals"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/goals/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "goals" in data
        assert "total" in data
    
    def test_filter_my_goals_by_status(self, api_base_url, employee_token):
        """Test filter my goals by status"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/goals/me?status=in_progress",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "goals" in data
    
    def test_get_team_goals(self, api_base_url, manager_token):
        """Test manager can get team goals"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/goals/team",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "goals" in data
        assert "total" in data
    
    @pytest.mark.permissions
    def test_get_team_goals_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot access team goals"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/goals/team",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_goal_by_id(self, api_base_url, employee_token, goal_id):
        """Test get goal by ID"""
        if not employee_token or not goal_id:
            pytest.skip("Employee token or goal not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/goals/{goal_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == goal_id
    
    def test_update_goal(self, api_base_url, manager_token, goal_id):
        """Test manager can update goal"""
        if not manager_token or not goal_id:
            pytest.skip("Manager token or goal not available (database not seeded)")
        
        update_data = {
            "title": "Updated Test Goal",
            "priority": "high"
        }
        
        response = requests.put(
            f"{api_base_url}/goals/{goal_id}",
            headers={"Authorization": f"Bearer {manager_token}"},
            json=update_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["title"] == update_data["title"]
    
    def test_update_goal_status(self, api_base_url, employee_token, goal_id):
        """Test update goal status"""
        if not employee_token or not goal_id:
            pytest.skip("Employee token or goal not available (database not seeded)")
        
        status_data = {"status": "in_progress"}
        
        response = requests.patch(
            f"{api_base_url}/goals/{goal_id}/status",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=status_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["status"] == "in_progress"
    
    def test_get_my_goal_stats(self, api_base_url, employee_token):
        """Test get my goal statistics"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/goals/stats/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_team_goal_stats(self, api_base_url, manager_token):
        """Test manager can get team goal statistics"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/goals/stats/team",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict)
    
    @pytest.mark.permissions
    def test_get_team_stats_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot access team goal stats"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/goals/stats/team",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_create_checkpoint(self, api_base_url, employee_token, goal_id):
        """Test create checkpoint for goal"""
        if not employee_token or not goal_id:
            pytest.skip("Employee token or goal not available (database not seeded)")
        
        checkpoint_data = {
            "title": "Complete research phase",
            "description": "Research and document findings"
        }
        
        response = requests.post(
            f"{api_base_url}/goals/{goal_id}/checkpoints",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=checkpoint_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert data["title"] == checkpoint_data["title"]
    
    def test_add_comment(self, api_base_url, employee_token, goal_id):
        """Test add comment to goal"""
        if not employee_token or not goal_id:
            pytest.skip("Employee token or goal not available (database not seeded)")
        
        comment_data = {
            "content": "Making good progress on this goal",
            "comment_type": "update"
        }
        
        response = requests.post(
            f"{api_base_url}/goals/{goal_id}/comments",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=comment_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert data["content"] == comment_data["content"]
    
    def test_get_comments(self, api_base_url, employee_token, goal_id):
        """Test get goal comments"""
        if not employee_token or not goal_id:
            pytest.skip("Employee token or goal not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/goals/{goal_id}/comments",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_categories(self, api_base_url, employee_token):
        """Test get goal categories"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/goals/categories",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_templates(self, api_base_url, employee_token):
        """Test get goal templates"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/goals/templates",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, list)
    
    def test_delete_goal(self, api_base_url, manager_token, employee_token):
        """Test manager can delete goal"""
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
        
        # Create goal to delete
        target_date = (datetime.now() + timedelta(days=30)).date().isoformat()
        create_response = requests.post(
            f"{api_base_url}/goals",
            headers={"Authorization": f"Bearer {manager_token}"},
            json={
                "title": "Test for Delete",
                "employee_id": employee_id,
                "target_date": target_date,
                "is_personal": False
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create goal for delete test")
        
        test_id = create_response.json()["id"]
        
        # Delete
        response = requests.delete(
            f"{api_base_url}/goals/{test_id}",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "message" in data
