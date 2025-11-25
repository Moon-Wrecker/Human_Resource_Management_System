"""
Test script for Health and Root API endpoints
Run this after starting the backend server to verify basic endpoints work
"""
import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"

# ANSI Color codes
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Test counters
tests_passed = 0
tests_failed = 0


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_root_endpoint():
    """Test 1: Root endpoint returns correct structure"""
    global tests_passed, tests_failed
    test_name = "Test 1: Root Endpoint"
    
    try:
        response = requests.get(f"{BASE_URL}/")
        
        # Assert status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        # Assert response structure
        assert "success" in data, "Missing 'success' field"
        assert data["success"] == True, "'success' should be True"
        assert "data" in data, "Missing 'data' field"
        
        # Assert data fields
        endpoint_data = data["data"]
        assert "name" in endpoint_data, "Missing 'name' field"
        assert "version" in endpoint_data, "Missing 'version' field"
        assert "environment" in endpoint_data, "Missing 'environment' field"
        assert "status" in endpoint_data, "Missing 'status' field"
        assert endpoint_data["status"] == "running", "Status should be 'running'"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   App: {endpoint_data['name']} v{endpoint_data['version']}")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_health_endpoint():
    """Test 2: Health endpoint returns healthy status"""
    global tests_passed, tests_failed
    test_name = "Test 2: Health Endpoint"
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        
        # Assert status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        # Assert response structure
        assert "success" in data, "Missing 'success' field"
        assert data["success"] == True, "'success' should be True"
        assert "data" in data, "Missing 'data' field"
        
        # Assert health data
        health_data = data["data"]
        assert "status" in health_data, "Missing 'status' field"
        assert health_data["status"] == "healthy", "Status should be 'healthy'"
        assert "environment" in health_data, "Missing 'environment' field"
        assert "version" in health_data, "Missing 'version' field"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Status: {health_data['status']}, Env: {health_data['environment']}")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_api_v1_root():
    """Test 3: API v1 root returns endpoints and documentation"""
    global tests_passed, tests_failed
    test_name = "Test 3: API v1 Root"
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1")
        
        # Assert status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        # Assert response structure
        assert "success" in data, "Missing 'success' field"
        assert data["success"] == True, "'success' should be True"
        assert "data" in data, "Missing 'data' field"
        
        # Assert API data
        api_data = data["data"]
        assert "version" in api_data, "Missing 'version' field"
        assert "message" in api_data, "Missing 'message' field"
        assert "endpoints" in api_data, "Missing 'endpoints' field"
        assert "documentation" in api_data, "Missing 'documentation' field"
        
        # Assert key endpoints exist
        endpoints = api_data["endpoints"]
        required_endpoints = ["auth", "profile", "dashboard", "employees"]
        for endpoint in required_endpoints:
            assert endpoint in endpoints, f"Missing '{endpoint}' endpoint"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Version: {api_data['version']}, Endpoints: {len(endpoints)}")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_swagger_ui():
    """Test 4: Swagger UI is accessible"""
    global tests_passed, tests_failed
    test_name = "Test 4: Swagger UI"
    
    try:
        response = requests.get(f"{BASE_URL}/api/docs")
        
        # Assert status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Assert content type
        content_type = response.headers.get('content-type', '')
        assert 'html' in content_type.lower(), f"Expected HTML, got {content_type}"
        
        # Assert content exists
        assert len(response.text) > 0, "Empty response"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Content-Type: {content_type}, Size: {len(response.text)} bytes")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_redoc():
    """Test 5: ReDoc is accessible"""
    global tests_passed, tests_failed
    test_name = "Test 5: ReDoc"
    
    try:
        response = requests.get(f"{BASE_URL}/api/redoc")
        
        # Assert status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Assert content type
        content_type = response.headers.get('content-type', '')
        assert 'html' in content_type.lower(), f"Expected HTML, got {content_type}"
        
        # Assert content exists
        assert len(response.text) > 0, "Empty response"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Content-Type: {content_type}, Size: {len(response.text)} bytes")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_openapi_json():
    """Test 6: OpenAPI JSON specification is valid"""
    global tests_passed, tests_failed
    test_name = "Test 6: OpenAPI JSON"
    
    try:
        response = requests.get(f"{BASE_URL}/api/openapi.json")
        
        # Assert status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Assert can parse JSON
        openapi_spec = response.json()
        
        # Assert OpenAPI structure
        assert "openapi" in openapi_spec, "Missing 'openapi' field"
        assert "info" in openapi_spec, "Missing 'info' field"
        assert "paths" in openapi_spec, "Missing 'paths' field"
        
        # Assert info fields
        info = openapi_spec["info"]
        assert "title" in info, "Missing 'title' in info"
        assert "version" in info, "Missing 'version' in info"
        
        # Assert paths exist
        paths_count = len(openapi_spec["paths"])
        assert paths_count > 0, "No paths defined"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   OpenAPI: {openapi_spec['openapi']}, Paths: {paths_count}")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_404_handling():
    """Test 7: Non-existent endpoints return 404"""
    global tests_passed, tests_failed
    test_name = "Test 7: 404 Handling"
    
    try:
        response = requests.get(f"{BASE_URL}/non-existent-endpoint")
        
        # Assert 404 status
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Non-existent endpoint correctly returns 404")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def run_all_tests():
    """Run all health and root API tests"""
    global tests_passed, tests_failed
    
    print_section("HEALTH & ROOT API TEST SUITE")
    print(f"Testing at: {BASE_URL}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all tests
    test_root_endpoint()
    test_health_endpoint()
    test_api_v1_root()
    test_swagger_ui()
    test_redoc()
    test_openapi_json()
    test_404_handling()
    
    # Print summary
    print_section("TEST SUMMARY")
    total_tests = tests_passed + tests_failed
    print(f"Total Tests: {total_tests}")
    print(f"PASSED: {tests_passed}")
    print(f"FAILED: {tests_failed}")
    print(f"Success Rate: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_failed == 0:
        print("\nAll tests passed successfully!")
    else:
        print(f"\nWARNING: {tests_failed} test(s) failed. Please review the output above.")
    
    print("=" * 60)


if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to backend server")
        print("Make sure the backend is running at http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
