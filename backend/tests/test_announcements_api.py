"""
Announcements API Tests (Pytest)
Run with: pytest backend/tests/test_announcements_api.py -v
"""
import pytest
import requests
from datetime import datetime, timedelta


@pytest.mark.announcements
class TestAnnouncementsAPI:
    """Test suite for Announcements endpoints"""
    
    @pytest.fixture(scope="class")
    def announcement_id(self, api_base_url, hr_token):
        """Create a test announcement and return its ID, cleanup after tests"""
        if not hr_token:
            yield None
            return
        
        # Create announcement
        expiry_date = (datetime.now() + timedelta(days=30)).replace(microsecond=0).isoformat()
        announcement_data = {
            "title": "Test Announcement - API Test",
            "message": "This is a test announcement created by the API test suite.",
            "link": "https://test.company.com/announcements",
            "is_urgent": False,
            "expiry_date": expiry_date
        }
        
        response = requests.post(
            f"{api_base_url}/announcements",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=announcement_data
        )
        
        announcement_id = None
        if response.status_code == 201:
            announcement_id = response.json()["id"]
        
        yield announcement_id
        
        # Cleanup - delete announcement after tests
        if announcement_id:
            requests.delete(
                f"{api_base_url}/announcements/{announcement_id}",
                headers={"Authorization": f"Bearer {hr_token}"}
            )
    
    def test_create_announcement(self, api_base_url, hr_token):
        """Test HR can create announcement"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        expiry_date = (datetime.now() + timedelta(days=30)).replace(microsecond=0).isoformat()
        announcement_data = {
            "title": "Test Announcement - Create Test",
            "message": "This is a test announcement.",
            "link": "https://test.company.com",
            "is_urgent": False,
            "expiry_date": expiry_date
        }
        
        response = requests.post(
            f"{api_base_url}/announcements",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=announcement_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert data["title"] == announcement_data["title"]
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/announcements/{data['id']}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
    
    @pytest.mark.permissions
    def test_create_announcement_employee_forbidden(self, api_base_url, employee_token):
        """Test Employee cannot create announcement"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        announcement_data = {
            "title": "Unauthorized Announcement",
            "message": "This should fail"
        }
        
        response = requests.post(
            f"{api_base_url}/announcements",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=announcement_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_all_announcements(self, api_base_url, hr_token):
        """Test get all announcements"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/announcements?limit=10",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "announcements" in data
        assert "total" in data
    
    def test_get_announcement_by_id(self, api_base_url, hr_token, announcement_id):
        """Test get announcement by ID"""
        if not hr_token or not announcement_id:
            pytest.skip("HR token or announcement not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/announcements/{announcement_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == announcement_id
    
    def test_get_nonexistent_announcement(self, api_base_url, hr_token):
        """Test get non-existent announcement returns 404"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/announcements/99999",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    def test_update_announcement(self, api_base_url, hr_token, announcement_id):
        """Test HR can update announcement"""
        if not hr_token or not announcement_id:
            pytest.skip("HR token or announcement not available (database not seeded)")
        
        update_data = {
            "title": "Updated Test Announcement - Modified",
            "is_urgent": True
        }
        
        response = requests.put(
            f"{api_base_url}/announcements/{announcement_id}",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=update_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["is_urgent"] == update_data["is_urgent"]
    
    @pytest.mark.permissions
    def test_update_announcement_employee_forbidden(self, api_base_url, employee_token, announcement_id):
        """Test Employee cannot update announcement"""
        if not employee_token or not announcement_id:
            pytest.skip("Employee token or announcement not available (database not seeded)")
        
        update_data = {"title": "Unauthorized Update"}
        
        response = requests.put(
            f"{api_base_url}/announcements/{announcement_id}",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=update_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_statistics(self, api_base_url, hr_token):
        """Test get announcement statistics"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/announcements/stats/summary",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "total" in data
        assert "active" in data
    
    def test_employee_can_view_announcements(self, api_base_url, employee_token):
        """Test Employee can view announcements"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/announcements?limit=5",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "announcements" in data
    
    def test_create_urgent_announcement(self, api_base_url, hr_token):
        """Test create urgent announcement"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        urgent_data = {
            "title": "URGENT: System Maintenance",
            "message": "Critical system maintenance tonight.",
            "is_urgent": True,
            "expiry_date": (datetime.now() + timedelta(days=1)).isoformat()
        }
        
        response = requests.post(
            f"{api_base_url}/announcements",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=urgent_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert data["is_urgent"] == True
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/announcements/{data['id']}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
    
    def test_soft_delete_announcement(self, api_base_url, hr_token):
        """Test soft delete announcement"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        # Create announcement to delete
        create_response = requests.post(
            f"{api_base_url}/announcements",
            headers={"Authorization": f"Bearer {hr_token}"},
            json={
                "title": "Test for Delete",
                "message": "Will be deleted",
                "expiry_date": (datetime.now() + timedelta(days=1)).isoformat()
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create announcement for delete test")
        
        announcement_id = create_response.json()["id"]
        
        # Delete
        response = requests.delete(
            f"{api_base_url}/announcements/{announcement_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Verify it's not in active list
        list_response = requests.get(
            f"{api_base_url}/announcements?limit=100",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        if list_response.status_code == 200:
            data = list_response.json()
            announcement_ids = [a["id"] for a in data["announcements"]]
            assert announcement_id not in announcement_ids, "Deleted announcement still in active list"
    
    @pytest.mark.permissions
    def test_delete_announcement_employee_forbidden(self, api_base_url, hr_token, employee_token):
        """Test Employee cannot delete announcement"""
        if not hr_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Create announcement
        create_response = requests.post(
            f"{api_base_url}/announcements",
            headers={"Authorization": f"Bearer {hr_token}"},
            json={
                "title": "Test for Delete Permission",
                "message": "Test",
                "expiry_date": (datetime.now() + timedelta(days=1)).isoformat()
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create announcement for delete test")
        
        test_id = create_response.json()["id"]
        
        # Try to delete as employee
        response = requests.delete(
            f"{api_base_url}/announcements/{test_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/announcements/{test_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
