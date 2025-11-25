"""
Leaves API Tests (Pytest)
Run with: pytest backend/tests/test_leaves_api.py -v
"""
import pytest
import requests
from datetime import datetime, timedelta


@pytest.mark.leaves
class TestLeavesAPI:
    """Test suite for Leave Management endpoints"""
    
    @pytest.fixture(scope="class")
    def leave_id(self, api_base_url, employee_token):
        """Create a test leave request and return its ID, cleanup after tests"""
        if not employee_token:
            yield None
            return
        
        # Create leave request
        start_date = (datetime.now() + timedelta(days=7)).date().isoformat()
        end_date = (datetime.now() + timedelta(days=9)).date().isoformat()
        
        leave_data = {
            "leave_type": "casual",
            "start_date": start_date,
            "end_date": end_date,
            "subject": "Test Leave Request",
            "reason": "Personal work",
            "description": "This is a test leave request"
        }
        
        response = requests.post(
            f"{api_base_url}/leaves",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=leave_data
        )
        
        leave_id = None
        if response.status_code == 201:
            leave_id = response.json()["id"]
        
        yield leave_id
        
        # Cleanup - cancel leave after tests if still pending
        if leave_id:
            requests.delete(
                f"{api_base_url}/leaves/{leave_id}",
                headers={"Authorization": f"Bearer {employee_token}"}
            )
    
    def test_apply_for_leave(self, api_base_url, employee_token):
        """Test employee can apply for leave"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        start_date = (datetime.now() + timedelta(days=10)).date().isoformat()
        end_date = (datetime.now() + timedelta(days=12)).date().isoformat()
        
        leave_data = {
            "leave_type": "sick",
            "start_date": start_date,
            "end_date": end_date,
            "subject": "Medical Leave",
            "reason": "Doctor appointment",
            "description": "Need to visit doctor for checkup"
        }
        
        response = requests.post(
            f"{api_base_url}/leaves",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=leave_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert data["leave_type"] == leave_data["leave_type"]
        assert data["status"] == "pending"
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/leaves/{data['id']}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
    
    def test_get_my_leave_requests(self, api_base_url, employee_token):
        """Test get my leave requests"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/leaves/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "leaves" in data
        assert "total" in data
        assert "page" in data
    
    def test_filter_my_leaves_by_status(self, api_base_url, employee_token):
        """Test filter my leaves by status"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/leaves/me?status=pending",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "leaves" in data
    
    def test_filter_my_leaves_by_type(self, api_base_url, employee_token):
        """Test filter my leaves by type"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/leaves/me?leave_type=casual",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "leaves" in data
    
    def test_get_my_leave_balance(self, api_base_url, employee_token):
        """Test get my leave balance"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/leaves/balance/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_team_leave_requests(self, api_base_url, manager_token):
        """Test manager can get team leave requests"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/leaves/team",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "leaves" in data
        assert "total" in data
    
    @pytest.mark.permissions
    def test_get_team_leaves_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot access team leaves"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/leaves/team",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_all_leave_requests(self, api_base_url, hr_token):
        """Test HR can get all leave requests"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/leaves/all",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "leaves" in data
        assert "total" in data
    
    @pytest.mark.permissions
    def test_get_all_leaves_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot access all leaves"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/leaves/all",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_employee_leave_balance(self, api_base_url, manager_token, employee_token):
        """Test manager can get employee leave balance"""
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
            f"{api_base_url}/leaves/balance/{employee_id}",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_leave_by_id(self, api_base_url, employee_token, leave_id):
        """Test get leave request by ID"""
        if not employee_token or not leave_id:
            pytest.skip("Employee token or leave not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/leaves/{leave_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == leave_id
    
    def test_update_leave_request(self, api_base_url, employee_token, leave_id):
        """Test employee can update pending leave request"""
        if not employee_token or not leave_id:
            pytest.skip("Employee token or leave not available (database not seeded)")
        
        update_data = {
            "subject": "Updated Leave Request",
            "reason": "Updated reason"
        }
        
        response = requests.put(
            f"{api_base_url}/leaves/{leave_id}",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=update_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["subject"] == update_data["subject"]
    
    def test_approve_leave_request(self, api_base_url, manager_token, employee_token):
        """Test manager can approve leave request"""
        if not manager_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Create a leave request to approve
        start_date = (datetime.now() + timedelta(days=15)).date().isoformat()
        end_date = (datetime.now() + timedelta(days=17)).date().isoformat()
        
        create_response = requests.post(
            f"{api_base_url}/leaves",
            headers={"Authorization": f"Bearer {employee_token}"},
            json={
                "leave_type": "annual",
                "start_date": start_date,
                "end_date": end_date,
                "subject": "Test Approval"
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create leave for approval test")
        
        test_id = create_response.json()["id"]
        
        # Approve
        status_data = {"status": "approved"}
        
        response = requests.patch(
            f"{api_base_url}/leaves/{test_id}/status",
            headers={"Authorization": f"Bearer {manager_token}"},
            json=status_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["status"] == "approved"
    
    def test_reject_leave_request(self, api_base_url, manager_token, employee_token):
        """Test manager can reject leave request"""
        if not manager_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Create a leave request to reject
        start_date = (datetime.now() + timedelta(days=20)).date().isoformat()
        end_date = (datetime.now() + timedelta(days=22)).date().isoformat()
        
        create_response = requests.post(
            f"{api_base_url}/leaves",
            headers={"Authorization": f"Bearer {employee_token}"},
            json={
                "leave_type": "casual",
                "start_date": start_date,
                "end_date": end_date,
                "subject": "Test Rejection"
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create leave for rejection test")
        
        test_id = create_response.json()["id"]
        
        # Reject
        status_data = {
            "status": "rejected",
            "rejection_reason": "Insufficient staffing during this period"
        }
        
        response = requests.patch(
            f"{api_base_url}/leaves/{test_id}/status",
            headers={"Authorization": f"Bearer {manager_token}"},
            json=status_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["status"] == "rejected"
    
    @pytest.mark.permissions
    def test_approve_leave_employee_forbidden(self, api_base_url, employee_token, leave_id):
        """Test employee cannot approve leave"""
        if not employee_token or not leave_id:
            pytest.skip("Employee token or leave not available (database not seeded)")
        
        status_data = {"status": "approved"}
        
        response = requests.patch(
            f"{api_base_url}/leaves/{leave_id}/status",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=status_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_cancel_leave_request(self, api_base_url, employee_token):
        """Test employee can cancel pending leave request"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        # Create a leave request to cancel
        start_date = (datetime.now() + timedelta(days=25)).date().isoformat()
        end_date = (datetime.now() + timedelta(days=27)).date().isoformat()
        
        create_response = requests.post(
            f"{api_base_url}/leaves",
            headers={"Authorization": f"Bearer {employee_token}"},
            json={
                "leave_type": "casual",
                "start_date": start_date,
                "end_date": end_date,
                "subject": "Test Cancellation"
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create leave for cancellation test")
        
        test_id = create_response.json()["id"]
        
        # Cancel
        response = requests.delete(
            f"{api_base_url}/leaves/{test_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "message" in data
    
    def test_get_leave_stats(self, api_base_url, hr_token):
        """Test HR can get leave statistics"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/leaves/stats/summary",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, dict)
    
    @pytest.mark.permissions
    def test_get_leave_stats_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot access leave statistics"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/leaves/stats/summary",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
