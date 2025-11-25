"""
Holidays API Tests (Pytest)
Run with: pytest backend/tests/test_holidays_api.py -v
"""
import pytest
import requests
from datetime import datetime, timedelta


@pytest.mark.holidays
class TestHolidaysAPI:
    """Test suite for Holidays endpoints"""
    
    @pytest.fixture(scope="class")
    def holiday_id(self, api_base_url, hr_token):
        """Create a test holiday and return its ID, cleanup after tests"""
        if not hr_token:
            yield None
            return
        
        # Create holiday 30 days from now
        start_date = (datetime.now() + timedelta(days=30)).date().isoformat()
        end_date = (datetime.now() + timedelta(days=30)).date().isoformat()
        
        holiday_data = {
            "name": "Test Holiday - API Test",
            "start_date": start_date,
            "end_date": end_date,
            "holiday_type": "company",
            "description": "This is a test holiday created by API tests",
            "is_mandatory": True
        }
        
        response = requests.post(
            f"{api_base_url}/holidays",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=holiday_data
        )
        
        holiday_id = None
        if response.status_code == 201:
            holiday_id = response.json()["id"]
        
        yield holiday_id
        
        # Cleanup - delete holiday after tests
        if holiday_id:
            requests.delete(
                f"{api_base_url}/holidays/{holiday_id}",
                headers={"Authorization": f"Bearer {hr_token}"}
            )
    
    def test_create_holiday(self, api_base_url, hr_token):
        """Test HR can create holiday"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        start_date = (datetime.now() + timedelta(days=30)).date().isoformat()
        end_date = (datetime.now() + timedelta(days=30)).date().isoformat()
        
        holiday_data = {
            "name": "Test Holiday - Create Test",
            "start_date": start_date,
            "end_date": end_date,
            "holiday_type": "company",
            "description": "Test holiday",
            "is_mandatory": True
        }
        
        response = requests.post(
            f"{api_base_url}/holidays",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=holiday_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert data["name"] == holiday_data["name"]
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/holidays/{data['id']}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
    
    @pytest.mark.permissions
    def test_create_holiday_employee_forbidden(self, api_base_url, employee_token):
        """Test Employee cannot create holiday"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        holiday_data = {
            "name": "Unauthorized Holiday",
            "start_date": datetime.now().date().isoformat(),
            "end_date": datetime.now().date().isoformat(),
            "holiday_type": "company"
        }
        
        response = requests.post(
            f"{api_base_url}/holidays",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=holiday_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_all_holidays(self, api_base_url, employee_token):
        """Test get all holidays"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/holidays?page=1&page_size=10",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "holidays" in data
        assert "total" in data
    
    def test_get_holiday_by_id(self, api_base_url, employee_token, holiday_id):
        """Test get holiday by ID"""
        if not employee_token or not holiday_id:
            pytest.skip("Employee token or holiday not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/holidays/{holiday_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == holiday_id
    
    def test_get_nonexistent_holiday(self, api_base_url, employee_token):
        """Test get non-existent holiday returns 404"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/holidays/99999",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    def test_get_upcoming_holidays(self, api_base_url, employee_token):
        """Test get upcoming holidays"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/holidays/upcoming?days_ahead=90&limit=10",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_holiday_stats(self, api_base_url, hr_token):
        """Test get holiday statistics (HR/Manager only)"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/holidays/stats",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "total_holidays" in data
    
    @pytest.mark.permissions
    def test_get_stats_employee_forbidden(self, api_base_url, employee_token):
        """Test Employee cannot access stats"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/holidays/stats",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_update_holiday(self, api_base_url, hr_token, holiday_id):
        """Test HR can update holiday"""
        if not hr_token or not holiday_id:
            pytest.skip("HR token or holiday not available (database not seeded)")
        
        update_data = {
            "name": "Updated Test Holiday - Modified",
            "is_mandatory": False
        }
        
        response = requests.put(
            f"{api_base_url}/holidays/{holiday_id}",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=update_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["is_mandatory"] == update_data["is_mandatory"]
    
    @pytest.mark.permissions
    def test_update_holiday_employee_forbidden(self, api_base_url, employee_token, holiday_id):
        """Test Employee cannot update holiday"""
        if not employee_token or not holiday_id:
            pytest.skip("Employee token or holiday not available (database not seeded)")
        
        update_data = {"name": "Unauthorized Update"}
        
        response = requests.put(
            f"{api_base_url}/holidays/{holiday_id}",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=update_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_filter_by_type(self, api_base_url, employee_token):
        """Test filter holidays by type"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/holidays?holiday_type=company",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "holidays" in data
    
    def test_filter_by_year(self, api_base_url, employee_token):
        """Test filter holidays by year"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        current_year = datetime.now().year
        response = requests.get(
            f"{api_base_url}/holidays?year={current_year}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "holidays" in data
    
    def test_delete_holiday(self, api_base_url, hr_token):
        """Test HR can delete holiday"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        # Create a holiday to delete
        create_response = requests.post(
            f"{api_base_url}/holidays",
            headers={"Authorization": f"Bearer {hr_token}"},
            json={
                "name": "Test for Delete",
                "start_date": datetime.now().date().isoformat(),
                "end_date": datetime.now().date().isoformat(),
                "holiday_type": "company"
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create holiday for delete test")
        
        test_id = create_response.json()["id"]
        
        # Delete
        response = requests.delete(
            f"{api_base_url}/holidays/{test_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "message" in data
    
    @pytest.mark.permissions
    def test_delete_holiday_employee_forbidden(self, api_base_url, hr_token, employee_token):
        """Test Employee cannot delete holiday"""
        if not hr_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Create a test holiday
        create_response = requests.post(
            f"{api_base_url}/holidays",
            headers={"Authorization": f"Bearer {hr_token}"},
            json={
                "name": "Test for Delete Permission",
                "start_date": datetime.now().date().isoformat(),
                "end_date": datetime.now().date().isoformat(),
                "holiday_type": "company"
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create holiday for delete test")
        
        test_id = create_response.json()["id"]
        
        # Try to delete as employee
        response = requests.delete(
            f"{api_base_url}/holidays/{test_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/holidays/{test_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
