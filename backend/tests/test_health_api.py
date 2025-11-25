"""
Health and Root API Tests (Pytest)
Run with: pytest backend/tests/test_health_api.py -v
"""
import pytest
import requests


@pytest.mark.health
class TestHealthAPI:
    """Test suite for Health and Root endpoints"""
    
    def test_root_endpoint(self, base_url):
        """Test root endpoint returns correct structure"""
        response = requests.get(f"{base_url}/")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "success" in data and data["success"] == True
        assert "data" in data
        
        endpoint_data = data["data"]
        assert "name" in endpoint_data
        assert "version" in endpoint_data
        assert "status" in endpoint_data
        assert endpoint_data["status"] == "running"
    
    def test_health_endpoint(self, base_url):
        """Test health endpoint returns healthy status"""
        response = requests.get(f"{base_url}/health")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "success" in data and data["success"] == True
        assert "data" in data
        
        health_data = data["data"]
        assert "status" in health_data
        assert health_data["status"] == "healthy"
    
    def test_api_v1_root(self, base_url):
        """Test API v1 root returns endpoints and documentation"""
        response = requests.get(f"{base_url}/api/v1")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "success" in data and data["success"] == True
        assert "data" in data
        
        api_data = data["data"]
        assert "endpoints" in api_data
        assert "documentation" in api_data
        
        endpoints = api_data["endpoints"]
        required_endpoints = ["auth", "profile", "dashboard", "employees"]
        for endpoint in required_endpoints:
            assert endpoint in endpoints, f"Missing '{endpoint}' endpoint"
    
    def test_swagger_ui(self, base_url):
        """Test Swagger UI is accessible"""
        response = requests.get(f"{base_url}/api/docs")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        content_type = response.headers.get('content-type', '')
        assert 'html' in content_type.lower(), f"Expected HTML, got {content_type}"
        assert len(response.text) > 0
    
    def test_redoc(self, base_url):
        """Test ReDoc is accessible"""
        response = requests.get(f"{base_url}/api/redoc")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        content_type = response.headers.get('content-type', '')
        assert 'html' in content_type.lower()
        assert len(response.text) > 0
    
    def test_openapi_json(self, base_url):
        """Test OpenAPI JSON specification is valid"""
        response = requests.get(f"{base_url}/api/openapi.json")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        openapi_spec = response.json()
        assert "openapi" in openapi_spec
        assert "info" in openapi_spec
        assert "paths" in openapi_spec
        
        paths_count = len(openapi_spec["paths"])
        assert paths_count > 0
    
    def test_404_handling(self, base_url):
        """Test non-existent endpoints return 404"""
        response = requests.get(f"{base_url}/non-existent-endpoint")
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
