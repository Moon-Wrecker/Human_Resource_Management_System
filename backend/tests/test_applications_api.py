"""
Applications API Tests (Pytest)
Run with: pytest backend/tests/test_applications_api.py -v
"""
import pytest
import requests
from datetime import datetime


@pytest.mark.applications
class TestApplicationsAPI:
    """Test suite for Job Applications endpoints"""
    
    @pytest.fixture(scope="class")
    def application_id(self, api_base_url, employee_token):
        """Create a test application and return its ID, cleanup after tests"""
        if not employee_token:
            yield None
            return
        
        # Create application
        application_data = {
            "job_id": 1,
            "applicant_name": "Test Applicant",
            "applicant_email": "test.applicant@example.com",
            "applicant_phone": "1234567890",
            "cover_letter": "I am very interested in this position.",
            "source": "self-applied"
        }
        
        response = requests.post(
            f"{api_base_url}/applications",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=application_data
        )
        
        application_id = None
        if response.status_code == 201:
            application_id = response.json()["id"]
        
        yield application_id
        
        # Cleanup - delete application after tests
        if application_id:
            requests.delete(
                f"{api_base_url}/applications/{application_id}",
                headers={"Authorization": f"Bearer {employee_token}"}
            )
    
    def test_create_application(self, api_base_url, employee_token):
        """Test create job application"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        application_data = {
            "job_id": 1,
            "applicant_name": "John Doe",
            "applicant_email": "john.doe.test@example.com",
            "applicant_phone": "9876543210",
            "cover_letter": "I am excited to apply for this position.",
            "source": "self-applied"
        }
        
        response = requests.post(
            f"{api_base_url}/applications",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=application_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert data["applicant_name"] == application_data["applicant_name"]
        assert data["applicant_email"] == application_data["applicant_email"]
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/applications/{data['id']}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
    
    def test_create_application_public(self, api_base_url):
        """Test public can create application without authentication"""
        application_data = {
            "job_id": 1,
            "applicant_name": "External Applicant",
            "applicant_email": "external.test@example.com",
            "applicant_phone": "5555555555",
            "source": "self-applied"
        }
        
        response = requests.post(
            f"{api_base_url}/applications",
            json=application_data
        )
        
        # Should work without auth
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
    
    def test_get_my_applications(self, api_base_url, employee_token):
        """Test get my applications"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/applications/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "applications" in data
        assert "total" in data
        assert "page" in data
    
    def test_get_all_applications(self, api_base_url, hr_token):
        """Test HR can get all applications"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/applications?page=1&page_size=20",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "applications" in data
        assert "total" in data
    
    @pytest.mark.permissions
    def test_get_all_applications_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot get all applications"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/applications",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_filter_applications_by_job(self, api_base_url, hr_token):
        """Test filter applications by job ID"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/applications?job_id=1",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "applications" in data
    
    def test_filter_applications_by_status(self, api_base_url, hr_token):
        """Test filter applications by status"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/applications?status=pending",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "applications" in data
    
    def test_search_applications(self, api_base_url, hr_token):
        """Test search applications by name/email"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/applications?search=test",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "applications" in data
    
    def test_get_application_by_id(self, api_base_url, employee_token, application_id):
        """Test get application by ID"""
        if not employee_token or not application_id:
            pytest.skip("Employee token or application not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/applications/{application_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == application_id
    
    def test_get_application_statistics(self, api_base_url, hr_token):
        """Test HR can get application statistics"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/applications/statistics",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "total_applications" in data or "total" in data
    
    @pytest.mark.permissions
    def test_get_statistics_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot access application statistics"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/applications/statistics",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_update_application_status(self, api_base_url, hr_token, employee_token):
        """Test HR can update application status"""
        if not hr_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Create application to update
        create_response = requests.post(
            f"{api_base_url}/applications",
            headers={"Authorization": f"Bearer {employee_token}"},
            json={
                "job_id": 1,
                "applicant_name": "Status Test",
                "applicant_email": "status.test@example.com",
                "source": "self-applied"
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create application for status test")
        
        test_id = create_response.json()["id"]
        
        # Update status
        status_data = {
            "status": "reviewed",
            "screening_notes": "Good candidate",
            "screening_score": 85
        }
        
        response = requests.put(
            f"{api_base_url}/applications/{test_id}/status",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=status_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["status"] == "reviewed"
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/applications/{test_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
    
    @pytest.mark.permissions
    def test_update_status_employee_forbidden(self, api_base_url, employee_token, application_id):
        """Test employee cannot update application status"""
        if not employee_token or not application_id:
            pytest.skip("Employee token or application not available (database not seeded)")
        
        status_data = {"status": "reviewed"}
        
        response = requests.put(
            f"{api_base_url}/applications/{application_id}/status",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=status_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_delete_application(self, api_base_url, employee_token):
        """Test employee can delete pending application"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        # Create application to delete
        create_response = requests.post(
            f"{api_base_url}/applications",
            headers={"Authorization": f"Bearer {employee_token}"},
            json={
                "job_id": 1,
                "applicant_name": "Delete Test",
                "applicant_email": "delete.test@example.com",
                "source": "self-applied"
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create application for delete test")
        
        test_id = create_response.json()["id"]
        
        # Delete
        response = requests.delete(
            f"{api_base_url}/applications/{test_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "message" in data
    
    @pytest.mark.permissions
    def test_delete_reviewed_application_forbidden(self, api_base_url, hr_token, employee_token):
        """Test employee cannot delete reviewed application"""
        if not hr_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Create and review application
        create_response = requests.post(
            f"{api_base_url}/applications",
            headers={"Authorization": f"Bearer {employee_token}"},
            json={
                "job_id": 1,
                "applicant_name": "Review Delete Test",
                "applicant_email": "review.delete@example.com",
                "source": "self-applied"
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create application")
        
        test_id = create_response.json()["id"]
        
        # Review it
        requests.put(
            f"{api_base_url}/applications/{test_id}/status",
            headers={"Authorization": f"Bearer {hr_token}"},
            json={"status": "reviewed"}
        )
        
        # Try to delete as employee
        response = requests.delete(
            f"{api_base_url}/applications/{test_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/applications/{test_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
