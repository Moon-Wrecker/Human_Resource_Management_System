"""
Attendance API Tests (Pytest)
Run with: pytest backend/tests/test_attendance_api.py -v
"""
import pytest
import requests
from datetime import datetime, time, timedelta


@pytest.mark.attendance
class TestAttendanceAPI:
    """Test suite for Attendance endpoints"""
    
    @pytest.fixture(scope="class")
    def attendance_id(self, api_base_url, employee_token):
        """Create a test attendance record and return its ID, cleanup after tests"""
        if not employee_token:
            yield None
            return
        
        # Punch in
        punch_in_data = {
            "status": "present",
            "location": "office"
        }
        
        response = requests.post(
            f"{api_base_url}/attendance/punch-in",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=punch_in_data
        )
        
        attendance_id = None
        if response.status_code == 200:
            attendance_id = response.json()["attendance"]["id"]
        
        yield attendance_id
        
        # Note: Cleanup handled by delete test or manual cleanup if needed
    
    def test_punch_in(self, api_base_url, employee_token):
        """Test employee can punch in"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        punch_in_data = {
            "status": "present",
            "location": "office"
        }
        
        response = requests.post(
            f"{api_base_url}/attendance/punch-in",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=punch_in_data
        )
        
        # May be 200 even if already punched in
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "attendance" in data
        assert "message" in data
    
    def test_punch_in_wfh(self, api_base_url, employee_token):
        """Test employee can punch in with WFH status"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        punch_in_data = {
            "status": "wfh",
            "location": "home"
        }
        
        response = requests.post(
            f"{api_base_url}/attendance/punch-in",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=punch_in_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "attendance" in data
    
    def test_get_today_attendance(self, api_base_url, employee_token):
        """Test get today's attendance status"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/attendance/today",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        # May return null if not punched in today
    
    def test_punch_out(self, api_base_url, employee_token):
        """Test employee can punch out"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        # First ensure punched in
        punch_in_data = {"status": "present", "location": "office"}
        punch_in_response = requests.post(
            f"{api_base_url}/attendance/punch-in",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=punch_in_data
        )
        
        if punch_in_response.status_code != 200:
            pytest.skip("Could not punch in for punch out test")
        
        # Now punch out
        punch_out_data = {}
        
        response = requests.post(
            f"{api_base_url}/attendance/punch-out",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=punch_out_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "hours_worked" in data
        assert "attendance" in data
    
    def test_get_my_attendance_history(self, api_base_url, employee_token):
        """Test get my attendance history"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/attendance/me?page=1&page_size=30",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "records" in data
        assert "total" in data
        assert "page" in data
    
    def test_filter_attendance_by_status(self, api_base_url, employee_token):
        """Test filter attendance by status"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/attendance/me?status=present&page=1&page_size=30",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "records" in data
    
    def test_filter_attendance_by_date_range(self, api_base_url, employee_token):
        """Test filter attendance by date range"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        end_date = datetime.now().date().isoformat()
        start_date = (datetime.now() - timedelta(days=30)).date().isoformat()
        
        response = requests.get(
            f"{api_base_url}/attendance/me?start_date={start_date}&end_date={end_date}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "records" in data
    
    def test_get_my_attendance_summary(self, api_base_url, employee_token):
        """Test get monthly attendance summary"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        response = requests.get(
            f"{api_base_url}/attendance/me/summary?month={current_month}&year={current_year}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "total_days_present" in data or "total_present" in data
    
    def test_get_team_attendance(self, api_base_url, manager_token):
        """Test manager can get team attendance"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/attendance/team",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "records" in data
        assert "total_team_members" in data
    
    def test_get_team_attendance_specific_date(self, api_base_url, manager_token):
        """Test get team attendance for specific date"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        target_date = datetime.now().date().isoformat()
        
        response = requests.get(
            f"{api_base_url}/attendance/team?date={target_date}",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "records" in data
    
    @pytest.mark.permissions
    def test_get_team_attendance_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot access team attendance"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/attendance/team",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_all_attendance(self, api_base_url, hr_token):
        """Test HR can get all attendance records"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/attendance/all?page=1&page_size=50",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "records" in data
        assert "total_records" in data
        assert "total_employees" in data
    
    def test_filter_all_attendance_by_department(self, api_base_url, hr_token):
        """Test filter all attendance by department"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/attendance/all?department_id=1&page=1&page_size=50",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "records" in data
    
    @pytest.mark.permissions
    def test_get_all_attendance_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot access all attendance records"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/attendance/all",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_mark_attendance_manually(self, api_base_url, hr_token, employee_token):
        """Test HR can manually mark attendance"""
        if not hr_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Get employee ID
        employee_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        if employee_response.status_code != 200:
            pytest.skip("Could not get employee info")
        
        employee_id = employee_response.json()["id"]
        
        # Mark attendance for yesterday to avoid conflicts
        mark_date = (datetime.now()).replace(microsecond=0, second=0, hour=0, minute=0).isoformat()
        
        mark_data = {
            "employee_id": employee_id,
            "attendance_date": mark_date,
            "status": "present",
            "check_in_time": "2025-11-25T06:40:41.290Z",
            "check_out_time": "2025-11-25T18:00:00.290Z",
            "location": "office",
            "notes": "Manually marked by test"
        }
        
        response = requests.post(
            f"{api_base_url}/attendance/mark",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=mark_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "attendance" in data
        assert "marked_by" in data
    
    @pytest.mark.permissions
    def test_mark_attendance_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot manually mark attendance"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        mark_data = {
            "employee_id": 1,
            "attendance_date": datetime.now().date().isoformat(),
            "status": "present"
        }
        
        response = requests.post(
            f"{api_base_url}/attendance/mark",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=mark_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_delete_attendance_record(self, api_base_url, hr_token, employee_token):
        """Test HR can delete attendance record"""
        if not hr_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Create a test attendance record to delete
        employee_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        if employee_response.status_code != 200:
            pytest.skip("Could not get employee info")
        
        employee_id = employee_response.json()["id"]
        
        # Mark attendance for 2 days ago
        mark_date = (datetime.now() - timedelta(days=2)).date().isoformat()
        
        mark_response = requests.post(
            f"{api_base_url}/attendance/mark",
            headers={"Authorization": f"Bearer {hr_token}"},
            json={
                "employee_id": employee_id,
                "attendance_date": mark_date,
                "status": "present",
                "notes": "Test for deletion"
            }
        )
        
        if mark_response.status_code != 200:
            pytest.skip("Could not create attendance for delete test")
        
        attendance_id = mark_response.json()["attendance"]["id"]
        
        # Delete
        response = requests.delete(
            f"{api_base_url}/attendance/{attendance_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "message" in data
    
    @pytest.mark.permissions
    def test_delete_attendance_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot delete attendance records"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.delete(
            f"{api_base_url}/attendance/99999",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
