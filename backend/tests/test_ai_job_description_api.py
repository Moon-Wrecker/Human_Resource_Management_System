"""
AI Job Description Generator API Tests (Pytest)
Tests for AI-powered job description generation using Google Gemini

Run with: pytest backend/tests/test_ai_job_description_api.py -v
"""
import pytest
import requests


@pytest.mark.ai_jd
class TestAIJobDescriptionAPI:
    """Test suite for AI Job Description Generator endpoints"""
    
    def _request_with_retry(self, method, url, **kwargs):
        """Helper to make requests with retry logic (60s delay)"""
        import time
        # Remove timeout if present as we are replacing it with retry
        if 'timeout' in kwargs:
            del kwargs['timeout']
            
        try:
            response = requests.request(method, url, **kwargs)
            # If service unavailable (503) or other transient error, retry
            if response.status_code == 503:
                time.sleep(60)
                return requests.request(method, url, **kwargs)
            return response
        except requests.exceptions.RequestException:
            time.sleep(60)
            return requests.request(method, url, **kwargs)
    
    def test_ai_service_status(self, api_base_url, employee_token):
        """Test AI service status endpoint"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = self._request_with_retry(
            "GET",
            f"{api_base_url}/ai/job-description/status",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        assert "available" in data
        # Service may or may not be configured with API key
        if data["available"]:
            assert "features" in data
            assert isinstance(data["features"], list)
    
    def test_generate_jd_preview_mode(self, api_base_url, hr_token):
        """Test generating JD in preview mode (no save)"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        request_data = {
            "job_title": "Senior Software Engineer",
            "job_level": "Senior",
            "department": "Engineering",
            "location": "Remote",
            "employment_type": "Full-time",
            "responsibilities": [
                "Design scalable systems",
                "Lead technical decisions"
            ],
            "requirements": [
                {"requirement": "5+ years experience", "is_required": True},
                {"requirement": "Python expertise", "is_required": True}
            ],
            "save_as_draft": False  # Preview mode
        }
        
        response = self._request_with_retry(
            "POST",
            f"{api_base_url}/ai/job-description/generate",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=request_data
        )
        
        # May be 503 if AI service not configured with API key, or 201 if successful
        assert response.status_code in [201, 503], f"Expected 201 or 503, got {response.status_code}"
        
        if response.status_code == 201:
            data = response.json()
            assert data["success"] == True
            assert "data" in data
            assert data["job_listing_id"] is None  # Not saved in preview mode
            
            # Verify JD structure
            jd_content = data["data"]
            assert "title" in jd_content
            assert "summary" in jd_content
            assert "key_responsibilities" in jd_content
            assert "required_qualifications" in jd_content
    
    def test_generate_jd_draft_mode(self, api_base_url, hr_token):
        """Test generating JD and saving as draft"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        request_data = {
            "job_title": "Backend Developer",
            "job_level": "Mid",
            "department": "Engineering",
            "location": "San Francisco",
            "employment_type": "Full-time",
            "save_as_draft": True  # Save as draft
        }
        
        response = self._request_with_retry(
            "POST",
            f"{api_base_url}/ai/job-description/generate",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=request_data
        )
        
        assert response.status_code in [201, 503], f"Expected 201 or 503, got {response.status_code}"
        
        if response.status_code == 201:
            data = response.json()
            assert data["success"] == True
            assert data["job_listing_id"] is not None  # Should have ID when saved
            assert "saved as draft" in data["message"].lower()
    
    def test_generate_jd_with_company_info(self, api_base_url, hr_token):
        """Test generating JD with company information"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        request_data = {
            "job_title": "Product Manager",
            "job_level": "Senior",
            "company_info": {
                "name": "TechCorp Inc",
                "description": "Leading technology company",
                "industry": "Software",
                "values": ["Innovation", "Collaboration", "Excellence"]
            },
            "save_as_draft": False
        }
        
        response = self._request_with_retry(
            "POST",
            f"{api_base_url}/ai/job-description/generate",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=request_data
        )
        
        assert response.status_code in [201, 503], f"Expected 201 or 503, got {response.status_code}"
    
    def test_generate_jd_with_salary_and_benefits(self, api_base_url, hr_token):
        """Test generating JD with salary range and benefits"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        request_data = {
            "job_title": "Data Scientist",
            "job_level": "Senior",
            "salary_range": "$120,000 - $160,000",
            "benefits": [
                "Health insurance",
                "401(k) matching",
                "Unlimited PTO"
            ],
            "save_as_draft": False
        }
        
        response = requests.post(
            f"{api_base_url}/ai/job-description/generate",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=request_data,
            timeout=30
        )
        
        assert response.status_code in [201, 503], f"Expected 201 or 503, got {response.status_code}"
    
    @pytest.mark.permissions
    def test_generate_jd_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot generate job descriptions"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        request_data = {
            "job_title": "Software Engineer",
            "job_level": "Mid"
        }
        
        response = self._request_with_retry(
            "POST",
            f"{api_base_url}/ai/job-description/generate",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=request_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    @pytest.mark.permissions
    def test_generate_jd_manager_forbidden(self, api_base_url, manager_token):
        """Test manager cannot generate job descriptions"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        request_data = {
            "job_title": "Software Engineer",
            "job_level": "Mid"
        }
        
        response = self._request_with_retry(
            "POST",
            f"{api_base_url}/ai/job-description/generate",
            headers={"Authorization": f"Bearer {manager_token}"},
            json=request_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_generate_jd_missing_required_fields(self, api_base_url, hr_token):
        """Test validation of required fields"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        # Missing job_title
        request_data = {
            "job_level": "Senior"
        }
        
        response = self._request_with_retry(
            "POST",
            f"{api_base_url}/ai/job-description/generate",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=request_data
        )
        
        assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    
    def test_extract_keywords(self, api_base_url, hr_token):
        """Test extracting SEO/ATS keywords from JD"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        job_description = """
        We are seeking a Senior Software Engineer with expertise in Python, 
        cloud computing, and microservices architecture. The ideal candidate 
        will have experience with AWS, Docker, and Kubernetes.
        """
        
        response = self._request_with_retry(
            "POST",
            f"{api_base_url}/ai/job-description/extract-keywords",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=job_description
        )
        
        assert response.status_code in [200, 503], f"Expected 200 or 503, got {response.status_code}"
        
        if response.status_code == 200:
            data = response.json()
            assert data["success"] == True
            assert "keywords" in data
            assert isinstance(data["keywords"], list)
            assert data["total"] >= 0
    
    @pytest.mark.permissions
    def test_extract_keywords_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot extract keywords"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = self._request_with_retry(
            "POST",
            f"{api_base_url}/ai/job-description/extract-keywords",
            headers={"Authorization": f"Bearer {employee_token}"},
            json="Sample job description"
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"


@pytest.mark.ai_jd
@pytest.mark.integration
class TestAIJobDescriptionIntegration:
    """Integration tests with real AI service (requires Gemini API key)"""
    
    @pytest.mark.skip(reason="Requires Gemini API key - run manually with --no-skip")
    def test_real_ai_generation_quality(self, api_base_url, hr_token):
        """Test actual AI generation quality (manual test only)"""
        if not hr_token:
            pytest.skip("HR token not available")
        
        request_data = {
            "job_title": "Senior Python Developer",
            "job_level": "Senior",
            "department": "Engineering",
            "responsibilities": ["Build APIs", "Write tests", "Code reviews"],
            "requirements": [
                {"requirement": "5+ years Python", "is_required": True},
                {"requirement": "FastAPI experience", "is_required": True}
            ],
            "save_as_draft": False
        }
        
        response = self._request_with_retry(
            "POST",
            f"{api_base_url}/ai/job-description/generate",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=request_data
        )
        
        # Should succeed with real AI
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        
        data = response.json()
        assert data["success"] == True
        
        # Verify AI generated substantial content
        jd_content = data["data"]
        assert len(jd_content["summary"]) > 50
        assert len(jd_content["key_responsibilities"]) >= 3
        assert len(jd_content["required_qualifications"]) >= 2
