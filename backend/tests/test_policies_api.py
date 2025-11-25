"""
Policies API Tests (Pytest) - Non-AI endpoints
Run with: pytest backend/tests/test_policies_api.py -v
"""
import pytest
import requests
from datetime import datetime, timedelta


@pytest.mark.policies
class TestPoliciesAPI:
    """Test suite for Policies endpoints (excluding AI features)"""
    
    @pytest.fixture(scope="class")
    def policy_id(self, api_base_url, hr_token):
        """Create a test policy and return its ID, cleanup after tests"""
        if not hr_token:
            yield None
            return
        
        # Create policy
        effective_date = (datetime.now() + timedelta(days=1)).date().isoformat()
        policy_data = {
            "title": "Test Policy - API Test",
            "description": "This is a test policy for API testing",
            "content": "Policy content goes here. This is the full text of the policy.",
            "category": "HR",
            "version": "1.0",
            "effective_date": effective_date,
            "require_acknowledgment": True
        }
        
        response = requests.post(
            f"{api_base_url}/policies",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=policy_data
        )
        
        policy_id = None
        if response.status_code == 201:
            policy_id = response.json()["id"]
        
        yield policy_id
        
        # Cleanup - delete policy after tests
        if policy_id:
            requests.delete(
                f"{api_base_url}/policies/{policy_id}",
                headers={"Authorization": f"Bearer {hr_token}"}
            )
    
    def test_create_policy(self, api_base_url, hr_token):
        """Test HR can create policy"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        effective_date = (datetime.now() + timedelta(days=7)).date().isoformat()
        policy_data = {
            "title": "Test Policy - Create Test",
            "description": "Policy for testing creation",
            "content": "This is the policy content that employees must follow.",
            "category": "IT",
            "version": "1.0",
            "effective_date": effective_date,
            "require_acknowledgment": False
        }
        
        response = requests.post(
            f"{api_base_url}/policies",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=policy_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert data["title"] == policy_data["title"]
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/policies/{data['id']}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
    
    @pytest.mark.permissions
    def test_create_policy_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot create policy"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        policy_data = {
            "title": "Unauthorized Policy",
            "content": "This should not be created",
            "effective_date": datetime.now().date().isoformat()
        }
        
        response = requests.post(
            f"{api_base_url}/policies",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=policy_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_all_policies(self, api_base_url, employee_token):
        """Test get all policies"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/policies",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "policies" in data
        assert "total" in data
    
    def test_filter_policies_by_category(self, api_base_url, employee_token):
        """Test filter policies by category"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/policies?category=HR",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "policies" in data
    
    def test_get_policy_by_id(self, api_base_url, employee_token, policy_id):
        """Test get policy by ID"""
        if not employee_token or not policy_id:
            pytest.skip("Employee token or policy not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/policies/{policy_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == policy_id
    
    def test_get_nonexistent_policy(self, api_base_url, employee_token):
        """Test get non-existent policy returns 404"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/policies/99999",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    def test_update_policy(self, api_base_url, hr_token, policy_id):
        """Test HR can update policy"""
        if not hr_token or not policy_id:
            pytest.skip("HR token or policy not available (database not seeded)")
        
        update_data = {
            "title": "Updated Test Policy",
            "version": "1.1"
        }
        
        response = requests.put(
            f"{api_base_url}/policies/{policy_id}",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=update_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["title"] == update_data["title"]
    
    @pytest.mark.permissions
    def test_update_policy_employee_forbidden(self, api_base_url, employee_token, policy_id):
        """Test employee cannot update policy"""
        if not employee_token or not policy_id:
            pytest.skip("Employee token or policy not available (database not seeded)")
        
        update_data = {"title": "Unauthorized Update"}
        
        response = requests.put(
            f"{api_base_url}/policies/{policy_id}",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=update_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_acknowledge_policy(self, api_base_url, employee_token, policy_id):
        """Test employee can acknowledge policy"""
        if not employee_token or not policy_id:
            pytest.skip("Employee token or policy not available (database not seeded)")
        
        response = requests.post(
            f"{api_base_url}/policies/{policy_id}/acknowledge",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert data["policy_id"] == policy_id
    
    def test_get_policy_acknowledgments(self, api_base_url, hr_token, policy_id):
        """Test HR can get policy acknowledgments"""
        if not hr_token or not policy_id:
            pytest.skip("HR token or policy not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/policies/{policy_id}/acknowledgments",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "acknowledgments" in data
        assert "total" in data
    
    @pytest.mark.permissions
    def test_get_acknowledgments_employee_forbidden(self, api_base_url, employee_token, policy_id):
        """Test employee cannot get policy acknowledgments"""
        if not employee_token or not policy_id:
            pytest.skip("Employee token or policy not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/policies/{policy_id}/acknowledgments",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_policy_stats(self, api_base_url, hr_token):
        """Test HR can get policy statistics"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/policies/stats/summary",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "total" in data or "active" in data
    
    @pytest.mark.permissions
    def test_get_policy_stats_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot access policy statistics"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/policies/stats/summary",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_soft_delete_policy(self, api_base_url, hr_token):
        """Test HR can soft delete policy"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        # Create policy to delete
        effective_date = datetime.now().date().isoformat()
        create_response = requests.post(
            f"{api_base_url}/policies",
            headers={"Authorization": f"Bearer {hr_token}"},
            json={
                "title": "Test for Soft Delete",
                "content": "Will be soft deleted",
                "effective_date": effective_date
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create policy for delete test")
        
        test_id = create_response.json()["id"]
        
        # Soft delete (default)
        response = requests.delete(
            f"{api_base_url}/policies/{test_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "message" in data
    
    @pytest.mark.permissions
    def test_delete_policy_employee_forbidden(self, api_base_url, employee_token, policy_id):
        """Test employee cannot delete policy"""
        if not employee_token or not policy_id:
            pytest.skip("Employee token or policy not available (database not seeded)")
        
        response = requests.delete(
            f"{api_base_url}/policies/{policy_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
