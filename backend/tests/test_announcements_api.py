"""
Test script for Announcements API
Run this after starting the backend server to verify all endpoints work
"""
import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
HR_EMAIL = "sarah.johnson@company.com"
EMPLOYEE_EMAIL = "john.doe@company.com"
PASSWORD = "password123"

# ANSI Color codes
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Test counters
tests_passed = 0
tests_failed = 0

# Store tokens and IDs
hr_token = None
employee_token = None
announcement_id = None


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_hr_login():
    """Test 1: HR can login"""
    global tests_passed, tests_failed, hr_token
    test_name = "Test 1: HR Login"
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": HR_EMAIL, "password": PASSWORD}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "access_token" in data
        
        hr_token = data["access_token"]
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   User: {data['user']['name']}")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_employee_login():
    """Test 2: Employee can login"""
    global tests_passed, tests_failed, employee_token
    test_name = "Test 2: Employee Login"
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": EMPLOYEE_EMAIL, "password": PASSWORD}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "access_token" in data
        
        employee_token = data["access_token"]
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   User: {data['user']['name']}")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_create_announcement():
    """Test 3: HR can create announcement"""
    global tests_passed, tests_failed, announcement_id
    test_name = "Test 3: Create Announcement (HR)"
    
    try:
        assert hr_token is not None, "HR token not available"
        
        expiry_date = (datetime.now() + timedelta(days=30)).isoformat()
        
        announcement_data = {
            "title": "Test Announcement - API Test",
            "message": "This is a test announcement created by the API test suite.",
            "link": "https://test.company.com/announcements",
            "is_urgent": False,
            "expiry_date": expiry_date
        }
        
        response = requests.post(
            f"{BASE_URL}/announcements",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=announcement_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert data["title"] == announcement_data["title"]
        
        announcement_id = data["id"]
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Announcement ID: {announcement_id}")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_create_announcement_employee_forbidden():
    """Test 4: Employee cannot create announcement"""
    global tests_passed, tests_failed
    test_name = "Test 4: Create Announcement - Employee Forbidden"
    
    try:
        assert employee_token is not None, "Employee token not available"
        
        announcement_data = {
            "title": "Unauthorized Announcement",
            "message": "This should fail"
        }
        
        response = requests.post(
            f"{BASE_URL}/announcements",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=announcement_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Correctly blocked employee from creating announcement")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_get_all_announcements():
    """Test 5: Get all announcements"""
    global tests_passed, tests_failed
    test_name = "Test 5: Get All Announcements"
    
    try:
        assert hr_token is not None, "HR token not available"
        
        response = requests.get(
            f"{BASE_URL}/announcements?limit=10",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "announcements" in data
        assert "total" in data
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Total: {data['total']}, Active: {data.get('active', 0)}")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_get_announcement_by_id():
    """Test 6: Get announcement by ID"""
    global tests_passed, tests_failed
    test_name = "Test 6: Get Announcement by ID"
    
    try:
        assert hr_token is not None, "HR token not available"
        assert announcement_id is not None, "Announcement ID not available"
        
        response = requests.get(
            f"{BASE_URL}/announcements/{announcement_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == announcement_id
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Title: {data['title']}")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_get_nonexistent_announcement():
    """Test 7: Get non-existent announcement returns 404"""
    global tests_passed, tests_failed
    test_name = "Test 7: Get Non-Existent Announcement"
    
    try:
        assert hr_token is not None, "HR token not available"
        
        response = requests.get(
            f"{BASE_URL}/announcements/99999",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Correctly returns 404 for non-existent announcement")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_update_announcement():
    """Test 8: HR can update announcement"""
    global tests_passed, tests_failed
    test_name = "Test 8: Update Announcement (HR)"
    
    try:
        assert hr_token is not None, "HR token not available"
        assert announcement_id is not None, "Announcement ID not available"
        
        update_data = {
            "title": "Updated Test Announcement - Modified",
            "is_urgent": True
        }
        
        response = requests.put(
            f"{BASE_URL}/announcements/{announcement_id}",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=update_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["is_urgent"] == update_data["is_urgent"]
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Updated title: {data['title']}")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_update_announcement_employee_forbidden():
    """Test 9: Employee cannot update announcement"""
    global tests_passed, tests_failed
    test_name = "Test 9: Update Announcement - Employee Forbidden"
    
    try:
        assert employee_token is not None, "Employee token not available"
        assert announcement_id is not None, "Announcement ID not available"
        
        update_data = {"title": "Unauthorized Update"}
        
        response = requests.put(
            f"{BASE_URL}/announcements/{announcement_id}",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=update_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Correctly blocked employee from updating")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_get_statistics():
    """Test 10: Get announcement statistics"""
    global tests_passed, tests_failed
    test_name = "Test 10: Get Announcement Statistics"
    
    try:
        assert hr_token is not None, "HR token not available"
        
        response = requests.get(
            f"{BASE_URL}/announcements/stats/summary",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "total" in data
        assert "active" in data
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Total: {data['total']}, Active: {data['active']}")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_employee_can_view_announcements():
    """Test 11: Employee can view announcements"""
    global tests_passed, tests_failed
    test_name = "Test 11: Employee Can View Announcements"
    
    try:
        assert employee_token is not None, "Employee token not available"
        
        response = requests.get(
            f"{BASE_URL}/announcements?limit=5",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "announcements" in data
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Employee can view {len(data['announcements'])} announcements")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_create_urgent_announcement():
    """Test 12: Create urgent announcement"""
    global tests_passed, tests_failed
    test_name = "Test 12: Create Urgent Announcement"
    
    try:
        assert hr_token is not None, "HR token not available"
        
        urgent_data = {
            "title": "URGENT: System Maintenance",
            "message": "Critical system maintenance tonight.",
            "is_urgent": True,
            "expiry_date": (datetime.now() + timedelta(days=1)).isoformat()
        }
        
        response = requests.post(
            f"{BASE_URL}/announcements",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=urgent_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert data["is_urgent"] == True
        
        # Clean up
        urgent_id = data["id"]
        requests.delete(
            f"{BASE_URL}/announcements/{urgent_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Urgent announcement created successfully")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_soft_delete_announcement():
    """Test 13: Soft delete announcement"""
    global tests_passed, tests_failed
    test_name = "Test 13: Soft Delete Announcement"
    
    try:
        assert hr_token is not None, "HR token not available"
        assert announcement_id is not None, "Announcement ID not available"
        
        response = requests.delete(
            f"{BASE_URL}/announcements/{announcement_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Verify it's not in active list
        list_response = requests.get(
            f"{BASE_URL}/announcements?limit=100",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        if list_response.status_code == 200:
            data = list_response.json()
            announcement_ids = [a["id"] for a in data["announcements"]]
            assert announcement_id not in announcement_ids, "Deleted announcement still in active list"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Announcement soft deleted (deactivated)")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_delete_announcement_employee_forbidden():
    """Test 14: Employee cannot delete announcement"""
    global tests_passed, tests_failed
    test_name = "Test 14: Delete Announcement - Employee Forbidden"
    
    try:
        assert employee_token is not None, "Employee token not available"
        
        # Create a test announcement first
        if hr_token:
            create_response = requests.post(
                f"{BASE_URL}/announcements",
                headers={"Authorization": f"Bearer {hr_token}"},
                json={
                    "title": "Test for Delete",
                    "message": "Test",
                    "expiry_date": (datetime.now() + timedelta(days=1)).isoformat()
                }
            )
            if create_response.status_code == 201:
                test_id = create_response.json()["id"]
                
                # Try to delete as employee
                response = requests.delete(
                    f"{BASE_URL}/announcements/{test_id}",
                    headers={"Authorization": f"Bearer {employee_token}"}
                )
                
                assert response.status_code == 403, f"Expected 403, got {response.status_code}"
                
                # Cleanup
                requests.delete(
                    f"{BASE_URL}/announcements/{test_id}",
                    headers={"Authorization": f"Bearer {hr_token}"}
                )
                
                print(f"{GREEN}PASS{RESET} {test_name}")
                print(f"   Correctly blocked employee from deleting")
                tests_passed += 1
                return
        
        print(f"{RED}FAIL{RESET} {test_name}: Could not set up test")
        tests_failed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def run_all_tests():
    """Run all announcements API tests"""
    global tests_passed, tests_failed
    
    print_section("ANNOUNCEMENTS API TEST SUITE")
    print(f"Testing at: {BASE_URL}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all tests
    test_hr_login()
    test_employee_login()
    test_create_announcement()
    test_create_announcement_employee_forbidden()
    test_get_all_announcements()
    test_get_announcement_by_id()
    test_get_nonexistent_announcement()
    test_update_announcement()
    test_update_announcement_employee_forbidden()
    test_get_statistics()
    test_employee_can_view_announcements()
    test_create_urgent_announcement()
    test_soft_delete_announcement()
    test_delete_announcement_employee_forbidden()
    
    # Print summary
    print_section("TEST SUMMARY")
    total_tests = tests_passed + tests_failed
    print(f"Total Tests: {total_tests}")
    print(f"{GREEN}PASSED{RESET}: {tests_passed}")
    print(f"{RED}FAILED{RESET}: {tests_failed}")
    print(f"Success Rate: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_failed == 0:
        print(f"\n{GREEN}All tests passed successfully!{RESET}")
    else:
        print(f"\n{RED}WARNING{RESET}: {tests_failed} test(s) failed. Please review the output above.")
    
    print("="*70)


if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print(f"\n{RED}ERROR{RESET}: Could not connect to backend server")
        print("Make sure the backend is running at http://localhost:8000")
    except Exception as e:
        print(f"\n{RED}ERROR{RESET} during testing: {str(e)}")
        import traceback
        traceback.print_exc()
