"""
Team Requests API Tests (Pytest)
Tests for the Team Requests management API (WFH, equipment, travel, etc.)
Run with: pytest backend/tests/test_team_requests_api.py -v
"""
import pytest
import requests
from datetime import datetime, timedelta


@pytest.mark.team_requests
class TestTeamRequestsAPI:
    """Test suite for Team Requests endpoints"""
    
    @pytest.fixture(scope="class")
    def team_request_id(self, api_base_url, employee_token):
        """Create a test team request and return its ID, cleanup after tests"""
        if not employee_token:
            yield None
            return
        
        # Create team request
        request_data = {
            "request_type": "wfh",
            "subject": "Work from Home Request",
            "description": "Need to work from home for personal reasons",
            "start_date": (datetime.now() + timedelta(days=1)).date().isoformat(),
            "end_date": (datetime.now() + timedelta(days=3)).date().isoformat()
        }
        
        response = requests.post(
            f"{api_base_url}/requests",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=request_data
        )
        
        request_id = None
        if response.status_code == 201:
            request_id = response.json()["id"]
        
        yield request_id
        
        # Cleanup - delete request after tests
        if request_id:
            requests.delete(
                f"{api_base_url}/requests/{request_id}",
                headers={"Authorization": f"Bearer {employee_token}"}
            )
    
    def test_submit_request(self, api_base_url, employee_token):
        """Test employee can submit request"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        request_data = {
            "request_type": "equipment",
            "subject": "New Laptop Request",
            "description": "Need a new laptop for development work",
            "start_date": datetime.now().date().isoformat()
        }
        
        response = requests.post(
            f"{api_base_url}/requests",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=request_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert data["request_type"] == request_data["request_type"]
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/requests/{data['id']}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
    
    def test_get_my_requests(self, api_base_url, employee_token):
        """Test get my requests"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/requests/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "requests" in data
        assert "total" in data
    
    def test_filter_my_requests_by_type(self, api_base_url, employee_token):
        """Test filter my requests by type"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/requests/me?request_type=wfh",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "requests" in data
    
    def test_filter_my_requests_by_status(self, api_base_url, employee_token):
        """Test filter my requests by status"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/requests/me?status=pending",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "requests" in data
    
    def test_get_team_requests(self, api_base_url, manager_token):
        """Test manager can get team requests"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/requests/team",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "requests" in data
        assert "total" in data
    
    @pytest.mark.permissions
    def test_get_team_requests_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot get team requests"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/requests/team",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_all_requests(self, api_base_url, hr_token):
        """Test HR can get all requests"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/requests/all",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "requests" in data
        assert "total" in data
    
    @pytest.mark.permissions
    def test_get_all_requests_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot get all requests"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/requests/all",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_search_all_requests(self, api_base_url, hr_token):
        """Test HR can search requests"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/requests/all?search=laptop",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "requests" in data
    
    def test_get_request_by_id(self, api_base_url, employee_token, team_request_id):
        """Test get request by ID"""
        if not employee_token or not team_request_id:
            pytest.skip("Employee token or request not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/requests/{team_request_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == team_request_id
    
    def test_update_request(self, api_base_url, employee_token, team_request_id):
        """Test employee can update pending request"""
        if not employee_token or not team_request_id:
            pytest.skip("Employee token or request not available (database not seeded)")
        
        update_data = {
            "subject": "Updated WFH Request",
            "description": "Updated description for work from home"
        }
        
        response = requests.put(
            f"{api_base_url}/requests/{team_request_id}",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=update_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["subject"] == update_data["subject"]
    
    def test_approve_request(self, api_base_url, manager_token, employee_token):
        """Test manager can approve request"""
        if not manager_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Create request to approve
        create_response = requests.post(
            f"{api_base_url}/requests",
            headers={"Authorization": f"Bearer {employee_token}"},
            json={
                "request_type": "travel",
                "subject": "Travel Request for Approval",
                "description": "Business travel to client site",
                "start_date": (datetime.now() + timedelta(days=5)).date().isoformat()
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create request for approval test")
        
        test_id = create_response.json()["id"]
        
        # Approve
        status_data = {
            "status": "approved",
            "remarks": "Approved by manager"
        }
        
        response = requests.put(
            f"{api_base_url}/requests/{test_id}/status",
            headers={"Authorization": f"Bearer {manager_token}"},
            json=status_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["status"] == "approved"
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/requests/{test_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
    
    def test_reject_request(self, api_base_url, manager_token, employee_token):
        """Test manager can reject request"""
        if not manager_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Create request to reject
        create_response = requests.post(
            f"{api_base_url}/requests",
            headers={"Authorization": f"Bearer {employee_token}"},
            json={
                "request_type": "other",
                "subject": "Request for Rejection Test",
                "description": "This will be rejected",
                "start_date": datetime.now().date().isoformat()
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create request for rejection test")
        
        test_id = create_response.json()["id"]
        
        # Reject
        status_data = {
            "status": "rejected",
            "remarks": "Not approved at this time"
        }
        
        response = requests.put(
            f"{api_base_url}/requests/{test_id}/status",
            headers={"Authorization": f"Bearer {manager_token}"},
            json=status_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["status"] == "rejected"
    
    @pytest.mark.permissions
    def test_approve_request_employee_forbidden(self, api_base_url, employee_token, team_request_id):
        """Test employee cannot approve requests"""
        if not employee_token or not team_request_id:
            pytest.skip("Employee token or request not available (database not seeded)")
        
        status_data = {"status": "approved"}
        
        response = requests.put(
            f"{api_base_url}/requests/{team_request_id}/status",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=status_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_request_statistics(self, api_base_url, employee_token):
        """Test get request statistics"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/requests/stats",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict)
    
    def test_delete_request(self, api_base_url, employee_token):
        """Test employee can delete pending request"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        # Create request to delete
        create_response = requests.post(
            f"{api_base_url}/requests",
            headers={"Authorization": f"Bearer {employee_token}"},
            json={
                "request_type": "wfh",
                "subject": "Request for Delete Test",
                "description": "Will be deleted",
                "start_date": datetime.now().date().isoformat()
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create request for delete test")
        
        test_id = create_response.json()["id"]
        
        # Delete
        response = requests.delete(
            f"{api_base_url}/requests/{test_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "message" in data
