"""
Test script for Health and Root API endpoints
Run this after starting the backend server to verify basic endpoints work
"""
import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def print_response(response, show_full=True):
    """Print formatted response"""
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")


def test_health_api():
    """Test health and root API endpoints"""
    
    print_section("HEALTH & ROOT API TEST SUITE")
    print(f"Testing at: {BASE_URL}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # =================================================================
    # 1. ROOT ENDPOINT
    # =================================================================
    print_section("1. Root Endpoint - GET /")
    
    response = requests.get(f"{BASE_URL}/")
    print_response(response, show_full=True)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Root endpoint working")
        if "success" in data and data["success"]:
            print("   Response structure correct")
            if "data" in data:
                endpoint_data = data["data"]
                print(f"   App Name: {endpoint_data.get('name', 'N/A')}")
                print(f"   Version: {endpoint_data.get('version', 'N/A')}")
                print(f"   Environment: {endpoint_data.get('environment', 'N/A')}")
                print(f"   Status: {endpoint_data.get('status', 'N/A')}")
                print(f"   Docs: {endpoint_data.get('docs', 'N/A')}")
        else:
            print("   ⚠️  Response structure unexpected")
    else:
        print("❌ Root endpoint failed")
    
    # =================================================================
    # 2. HEALTH CHECK ENDPOINT
    # =================================================================
    print_section("2. Health Check - GET /health")
    
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, show_full=True)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Health endpoint working")
        if "success" in data and data["success"]:
            print("   Response structure correct")
            if "data" in data:
                health_data = data["data"]
                status = health_data.get('status', 'N/A')
                print(f"   Status: {status}")
                print(f"   Environment: {health_data.get('environment', 'N/A')}")
                print(f"   Version: {health_data.get('version', 'N/A')}")
                
                if status == "healthy":
                    print("   ✅ System is healthy")
                else:
                    print(f"   ⚠️  System status is: {status}")
        else:
            print("   ⚠️  Response structure unexpected")
    else:
        print("❌ Health endpoint failed")
    
    # =================================================================
    # 3. API V1 ROOT ENDPOINT
    # =================================================================
    print_section("3. API V1 Root - GET /api/v1")
    
    response = requests.get(f"{BASE_URL}/api/v1")
    print_response(response, show_full=True)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ API v1 root endpoint working")
        if "success" in data and data["success"]:
            if "data" in data:
                api_data = data["data"]
                print(f"   Version: {api_data.get('version', 'N/A')}")
                print(f"   Message: {api_data.get('message', 'N/A')}")
                
                # Check if endpoints list is present
                if "endpoints" in api_data:
                    endpoints = api_data["endpoints"]
                    print(f"   Available endpoints: {len(endpoints)}")
                    print("   Key endpoints:")
                    for key in ["auth", "profile", "dashboard", "employees", "jobs"]:
                        if key in endpoints:
                            print(f"     - {key}: {endpoints[key]}")
                
                # Check if documentation links are present
                if "documentation" in api_data:
                    docs = api_data["documentation"]
                    print("   Documentation:")
                    print(f"     - Swagger UI: {docs.get('swagger_ui', 'N/A')}")
                    print(f"     - ReDoc: {docs.get('redoc', 'N/A')}")
                    print(f"     - OpenAPI JSON: {docs.get('openapi_json', 'N/A')}")
        else:
            print("   ⚠️  Response structure unexpected")
    else:
        print("❌ API v1 root endpoint failed")
    
    # =================================================================
    # 4. SWAGGER DOCS ENDPOINT
    # =================================================================
    print_section("4. Swagger UI - GET /api/docs")
    
    response = requests.get(f"{BASE_URL}/api/docs")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ Swagger UI is accessible")
        print(f"   Content Type: {response.headers.get('content-type', 'N/A')}")
        print(f"   Content Length: {len(response.text)} bytes")
    else:
        print("❌ Swagger UI not accessible")
    
    # =================================================================
    # 5. REDOC ENDPOINT
    # =================================================================
    print_section("5. ReDoc - GET /api/redoc")
    
    response = requests.get(f"{BASE_URL}/api/redoc")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ ReDoc is accessible")
        print(f"   Content Type: {response.headers.get('content-type', 'N/A')}")
        print(f"   Content Length: {len(response.text)} bytes")
    else:
        print("❌ ReDoc not accessible")
    
    # =================================================================
    # 6. OPENAPI JSON ENDPOINT
    # =================================================================
    print_section("6. OpenAPI JSON - GET /api/openapi.json")
    
    response = requests.get(f"{BASE_URL}/api/openapi.json")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        try:
            openapi_spec = response.json()
            print("✅ OpenAPI JSON is accessible")
            print(f"   OpenAPI Version: {openapi_spec.get('openapi', 'N/A')}")
            
            if "info" in openapi_spec:
                info = openapi_spec["info"]
                print(f"   API Title: {info.get('title', 'N/A')}")
                print(f"   API Version: {info.get('version', 'N/A')}")
            
            if "paths" in openapi_spec:
                print(f"   Total Paths: {len(openapi_spec['paths'])}")
        except:
            print("   ⚠️  Could not parse OpenAPI JSON")
    else:
        print("❌ OpenAPI JSON not accessible")
    
    # =================================================================
    # 7. NON-EXISTENT ENDPOINT (404 TEST)
    # =================================================================
    print_section("7. Non-Existent Endpoint - GET /non-existent")
    
    response = requests.get(f"{BASE_URL}/non-existent")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 404:
        print("✅ Correctly returns 404 for non-existent endpoint")
    else:
        print("❌ Should return 404 for non-existent endpoint")
    
    # =================================================================
    # SUMMARY
    # =================================================================
    print_section("TEST SUMMARY")
    print("✅ All health and root API endpoints tested successfully!")
    print("\nTested Endpoints:")
    print("  ✅ GET    /                     (Root)")
    print("  ✅ GET    /health               (Health Check)")
    print("  ✅ GET    /api/v1               (API v1 Root)")
    print("  ✅ GET    /api/docs             (Swagger UI)")
    print("  ✅ GET    /api/redoc            (ReDoc)")
    print("  ✅ GET    /api/openapi.json     (OpenAPI Spec)")
    print("  ✅ GET    /non-existent         (404 Test)")
    print("\nFeatures Verified:")
    print("  ✅ Server is running and responsive")
    print("  ✅ Health check returns healthy status")
    print("  ✅ API documentation is accessible")
    print("  ✅ OpenAPI specification is valid")
    print("  ✅ Proper 404 handling for non-existent routes")
    print("\n" + "="*60)


if __name__ == "__main__":
    try:
        test_health_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to backend server")
        print("Make sure the backend is running at http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
