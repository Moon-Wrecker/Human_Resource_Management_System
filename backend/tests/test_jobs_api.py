"""
Job Listings API Tests (Pytest)
Run with: pytest backend/tests/test_jobs_api.py -v
"""
import pytest
import requests
from datetime import datetime, timedelta


@pytest.mark.jobs
class TestJobListingsAPI:
    """Test suite for Job Listings endpoints"""
    
    @pytest.fixture(scope="class")
    def job_id(self, api_base_url, hr_token):
        """Create a test job listing and return its ID, cleanup after tests"""
        if not hr_token:
            yield None
            return
        
        # Create job
        deadline = (datetime.now() + timedelta(days=30)).date().isoformat()
        job_data = {
            "position": "Test Software Engineer",
            "department_id": 1,
            "description": "This is a test job posting",
            "experience_required": "2-3 years",
            "skills_required": "Python, FastAPI, PostgreSQL",
            "location": "Remote",
            "employment_type": "full-time",
            "salary_range": "$80,000 - $100,000",
            "application_deadline": deadline
        }
        
        response = requests.post(
            f"{api_base_url}/jobs",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=job_data
        )
        
        job_id = None
        if response.status_code == 201:
            job_id = response.json()["id"]
        
        yield job_id
        
        # Cleanup - delete job after tests
        if job_id:
            requests.delete(
                f"{api_base_url}/jobs/{job_id}",
                headers={"Authorization": f"Bearer {hr_token}"}
            )
    
    def test_create_job(self, api_base_url, hr_token):
        """Test HR can create job listing"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        deadline = (datetime.now() + timedelta(days=30)).date().isoformat()
        job_data = {
            "position": "Senior Backend Developer",
            "department_id": 1,
            "description": "Looking for experienced backend developer",
            "experience_required": "5+ years",
            "skills_required": "Python, FastAPI, Docker",
            "location": "San Francisco",
            "employment_type": "full-time",
            "application_deadline": deadline
        }
        
        response = requests.post(
            f"{api_base_url}/jobs",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=job_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert data["position"] == job_data["position"]
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/jobs/{data['id']}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
    
    @pytest.mark.permissions
    def test_create_job_employee_forbidden(self, api_base_url, employee_token):
        """Test Employee cannot create job listing"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        job_data = {
            "position": "Unauthorized Job",
            "department_id": 1,
            "description": "This should fail"
        }
        
        response = requests.post(
            f"{api_base_url}/jobs",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=job_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    @pytest.mark.permissions
    def test_create_job_manager_forbidden(self, api_base_url, manager_token):
        """Test Manager cannot create job listing"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        job_data = {
            "position": "Manager Job",
            "department_id": 1,
            "description": "This should fail"
        }
        
        response = requests.post(
            f"{api_base_url}/jobs",
            headers={"Authorization": f"Bearer {manager_token}"},
            json=job_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_all_jobs(self, api_base_url, employee_token):
        """Test get all job listings"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/jobs?page=1&page_size=20",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "jobs" in data
        assert "total" in data
        assert "page" in data
    
    def test_filter_jobs_by_department(self, api_base_url, employee_token):
        """Test filter job listings by department"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/jobs?department_id=1",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "jobs" in data
    
    def test_filter_jobs_by_location(self, api_base_url, employee_token):
        """Test filter job listings by location"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/jobs?location=Remote",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "jobs" in data
    
    def test_search_jobs(self, api_base_url, employee_token):
        """Test search job listings"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/jobs?search=engineer",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "jobs" in data
    
    def test_filter_jobs_by_active_status(self, api_base_url, employee_token):
        """Test filter job listings by active status"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/jobs?is_active=true",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "jobs" in data
    
    def test_get_job_by_id(self, api_base_url, employee_token, job_id):
        """Test get job listing by ID"""
        if not employee_token or not job_id:
            pytest.skip("Employee token or job listing not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/jobs/{job_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == job_id
    
    def test_get_nonexistent_job(self, api_base_url, employee_token):
        """Test get non-existent job listing returns 404"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/jobs/99999",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    def test_get_job_statistics(self, api_base_url, hr_token):
        """Test get job listing statistics"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/jobs/statistics",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "total_jobs" in data or "total" in data
    
    @pytest.mark.permissions
    def test_get_job_statistics_employee_forbidden(self, api_base_url, employee_token):
        """Test Employee cannot access job listing statistics"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/jobs/statistics",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_update_job(self, api_base_url, hr_token, job_id):
        """Test HR can update job listing"""
        if not hr_token or not job_id:
            pytest.skip("HR token or job listing not available (database not seeded)")
        
        update_data = {
            "position": "Updated Test Software Engineer",
            "description": "Updated description"
        }
        
        response = requests.put(
            f"{api_base_url}/jobs/{job_id}",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=update_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["position"] == update_data["position"]
    
    @pytest.mark.permissions
    def test_update_job_employee_forbidden(self, api_base_url, employee_token, job_id):
        """Test Employee cannot update job listing"""
        if not employee_token or not job_id:
            pytest.skip("Employee token or job listing not available (database not seeded)")
        
        update_data = {"position": "Unauthorized Update"}
        
        response = requests.put(
            f"{api_base_url}/jobs/{job_id}",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=update_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_job_applications(self, api_base_url, hr_token, job_id):
        """Test HR can get job listing applications"""
        if not hr_token or not job_id:
            pytest.skip("HR token or job listing not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/jobs/{job_id}/applications",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, list)
    
    @pytest.mark.permissions
    def test_get_job_applications_employee_forbidden(self, api_base_url, employee_token, job_id):
        """Test Employee cannot get job listing applications"""
        if not employee_token or not job_id:
            pytest.skip("Employee token or job listing not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/jobs/{job_id}/applications",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_delete_job(self, api_base_url, hr_token):
        """Test HR can delete job listing"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        # Create a job to delete
        deadline = (datetime.now() + timedelta(days=30)).date().isoformat()
        create_response = requests.post(
            f"{api_base_url}/jobs",
            headers={"Authorization": f"Bearer {hr_token}"},
            json={
                "position": "Test for Delete",
                "department_id": 1,
                "description": "Will be deleted",
                "application_deadline": deadline
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create job listing for delete test")
        
        test_id = create_response.json()["id"]
        
        # Delete
        response = requests.delete(
            f"{api_base_url}/jobs/{test_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "message" in data
    
    @pytest.mark.permissions
    def test_delete_job_employee_forbidden(self, api_base_url, hr_token, employee_token):
        """Test Employee cannot delete job listing"""
        if not hr_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Create a test job listing
        deadline = (datetime.now() + timedelta(days=30)).date().isoformat()
        create_response = requests.post(
            f"{api_base_url}/jobs",
            headers={"Authorization": f"Bearer {hr_token}"},
            json={
                "position": "Test for Delete Permission",
                "department_id": 1,
                "description": "Test",
                "application_deadline": deadline
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create job listing for delete test")
        
        test_id = create_response.json()["id"]
        
        # Try to delete as employee
        response = requests.delete(
            f"{api_base_url}/jobs/{test_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/jobs/{test_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
