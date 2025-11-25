"""
Test script for Authentication API
Run this after starting the backend server to verify all endpoints work
"""
import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
HR_EMAIL = "sarah.johnson@company.com"
MANAGER_EMAIL = "michael.chen@company.com"
EMPLOYEE_EMAIL = "john.doe@company.com"
PASSWORD = "password123"

# ANSI Color codes
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Test counters
tests_passed = 0
tests_failed = 0

# Store tokens
hr_token = None
manager_token = None
employee_token = None
employee_refresh_token = None
employee_id = None


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_login_hr():
    """Test 1: HR can login successfully"""
    global tests_passed, tests_failed, hr_token
    test_name = "Test 1: HR Login"
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": HR_EMAIL, "password": PASSWORD}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        assert "access_token" in data, "Missing access_token"
        assert "refresh_token" in data, "Missing refresh_token"
        assert "token_type" in data, "Missing token_type"
        assert "user" in data, "Missing user"
        assert data["token_type"] == "bearer", "Token type should be bearer"
        assert data["user"]["role"] == "hr", "Role should be HR"
        
        hr_token = data["access_token"]
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   User: {data['user']['name']}, Role: {data['user']['role']}")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_login_manager():
    """Test 2: Manager can login successfully"""
    global tests_passed, tests_failed, manager_token
    test_name = "Test 2: Manager Login"
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": MANAGER_EMAIL, "password": PASSWORD}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        assert "access_token" in data, "Missing access_token"
        assert data["user"]["role"] == "manager", "Role should be manager"
        
        manager_token = data["access_token"]
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   User: {data['user']['name']}, Role: {data['user']['role']}")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_login_employee():
    """Test 3: Employee can login successfully"""
    global tests_passed, tests_failed, employee_token, employee_refresh_token, employee_id
    test_name = "Test 3: Employee Login"
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": EMPLOYEE_EMAIL, "password": PASSWORD}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        assert "access_token" in data, "Missing access_token"
        assert "refresh_token" in data, "Missing refresh_token"
        assert data["user"]["role"] == "employee", "Role should be employee"
        
        employee_token = data["access_token"]
        employee_refresh_token = data["refresh_token"]
        employee_id = data["user"]["id"]
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   User: {data['user']['name']}, Role: {data['user']['role']}")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_login_invalid_email():
    """Test 4: Invalid email returns 401"""
    global tests_passed, tests_failed
    test_name = "Test 4: Login - Invalid Email"
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": "nonexistent@company.com", "password": PASSWORD}
        )
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Correctly rejected invalid email with 401")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_login_wrong_password():
    """Test 5: Wrong password returns 401"""
    global tests_passed, tests_failed
    test_name = "Test 5: Login - Wrong Password"
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": EMPLOYEE_EMAIL, "password": "wrongpassword"}
        )
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Correctly rejected wrong password with 401")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_login_missing_field():
    """Test 6: Missing password field returns 422"""
    global tests_passed, tests_failed
    test_name = "Test 6: Login - Missing Password"
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": EMPLOYEE_EMAIL}
        )
        
        assert response.status_code == 422, f"Expected 422, got {response.status_code}"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Correctly rejected missing field with 422 validation error")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_get_current_user():
    """Test 7: Get current user with valid token"""
    global tests_passed, tests_failed
    test_name = "Test 7: Get Current User"
    
    try:
        assert employee_token is not None, "Employee token not available"
        
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        assert "name" in data, "Missing name"
        assert "email" in data, "Missing email"
        assert "role" in data, "Missing role"
        assert data["email"] == EMPLOYEE_EMAIL, f"Email mismatch"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   User: {data['name']}, Email: {data['email']}")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_get_current_user_no_token():
    """Test 8: Get current user without token returns 403"""
    global tests_passed, tests_failed
    test_name = "Test 8: Get Current User - No Token"
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me")
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Correctly blocked request without token (403)")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_get_current_user_invalid_token():
    """Test 9: Get current user with invalid token returns 401"""
    global tests_passed, tests_failed
    test_name = "Test 9: Get Current User - Invalid Token"
    
    try:
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Correctly rejected invalid token (401)")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_refresh_token():
    """Test 10: Refresh access token with valid refresh token"""
    global tests_passed, tests_failed
    test_name = "Test 10: Refresh Access Token"
    
    try:
        assert employee_refresh_token is not None, "Refresh token not available"
        
        response = requests.post(
            f"{BASE_URL}/auth/refresh",
            json={"refresh_token": employee_refresh_token}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        assert "access_token" in data, "Missing access_token"
        assert "token_type" in data, "Missing token_type"
        assert data["token_type"] == "bearer", "Token type should be bearer"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   New access token generated successfully")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_refresh_token_invalid():
    """Test 11: Invalid refresh token returns 401"""
    global tests_passed, tests_failed
    test_name = "Test 11: Refresh Token - Invalid"
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/refresh",
            json={"refresh_token": "invalid.refresh.token"}
        )
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Correctly rejected invalid refresh token (401)")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_change_password():
    """Test 12: Change password successfully"""
    global tests_passed, tests_failed, employee_token
    test_name = "Test 12: Change Password"
    
    try:
        assert employee_token is not None, "Employee token not available"
        
        # Change password
        response = requests.post(
            f"{BASE_URL}/auth/change-password",
            headers={"Authorization": f"Bearer {employee_token}"},
            json={
                "current_password": PASSWORD,
                "new_password": "newpassword456"
            }
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Verify can login with new password
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": EMPLOYEE_EMAIL, "password": "newpassword456"}
        )
        assert login_response.status_code == 200, "Cannot login with new password"
        
        # Revert password
        new_token = login_response.json()["access_token"]
        revert_response = requests.post(
            f"{BASE_URL}/auth/change-password",
            headers={"Authorization": f"Bearer {new_token}"},
            json={
                "current_password": "newpassword456",
                "new_password": PASSWORD
            }
        )
        assert revert_response.status_code == 200, "Could not revert password"
        
        # Update token
        employee_token = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": EMPLOYEE_EMAIL, "password": PASSWORD}
        ).json()["access_token"]
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Password changed and reverted successfully")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_change_password_wrong_current():
    """Test 13: Change password with wrong current password returns 400"""
    global tests_passed, tests_failed
    test_name = "Test 13: Change Password - Wrong Current"
    
    try:
        assert employee_token is not None, "Employee token not available"
        
        response = requests.post(
            f"{BASE_URL}/auth/change-password",
            headers={"Authorization": f"Bearer {employee_token}"},
            json={
                "current_password": "wrongpassword",
                "new_password": "newpassword456"
            }
        )
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Correctly rejected wrong current password (400)")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_reset_password_by_hr():
    """Test 14: HR can reset employee password"""
    global tests_passed, tests_failed
    test_name = "Test 14: HR Reset Password"
    
    try:
        assert hr_token is not None, "HR token not available"
        assert employee_id is not None, "Employee ID not available"
        
        # Reset password
        response = requests.post(
            f"{BASE_URL}/auth/reset-password",
            headers={"Authorization": f"Bearer {hr_token}"},
            json={
                "employee_id": employee_id,
                "new_password": "resetpassword123"
            }
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Verify can login with reset password
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": EMPLOYEE_EMAIL, "password": "resetpassword123"}
        )
        assert login_response.status_code == 200, "Cannot login with reset password"
        
        # Revert password
        reset_token = login_response.json()["access_token"]
        revert_response = requests.post(
            f"{BASE_URL}/auth/change-password",
            headers={"Authorization": f"Bearer {reset_token}"},
            json={
                "current_password": "resetpassword123",
                "new_password": PASSWORD
            }
        )
        assert revert_response.status_code == 200, "Could not revert password"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   HR reset password and reverted successfully")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_reset_password_by_manager():
    """Test 15: Manager can reset employee password"""
    global tests_passed, tests_failed
    test_name = "Test 15: Manager Reset Password"
    
    try:
        assert manager_token is not None, "Manager token not available"
        assert employee_id is not None, "Employee ID not available"
        
        # Reset password
        response = requests.post(
            f"{BASE_URL}/auth/reset-password",
            headers={"Authorization": f"Bearer {manager_token}"},
            json={
                "employee_id": employee_id,
                "new_password": "managerreset123"
            }
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Verify and revert
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": EMPLOYEE_EMAIL, "password": "managerreset123"}
        )
        assert login_response.status_code == 200, "Cannot login with reset password"
        
        reset_token = login_response.json()["access_token"]
        requests.post(
            f"{BASE_URL}/auth/change-password",
            headers={"Authorization": f"Bearer {reset_token}"},
            json={
                "current_password": "managerreset123",
                "new_password": PASSWORD
            }
        )
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Manager reset password successfully")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_reset_password_by_employee_forbidden():
    """Test 16: Employee cannot reset passwords (403)"""
    global tests_passed, tests_failed
    test_name = "Test 16: Employee Reset Password - Forbidden"
    
    try:
        # Get fresh employee token
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": EMPLOYEE_EMAIL, "password": PASSWORD}
        )
        emp_token = login_response.json()["access_token"]
        
        # Get HR ID
        hr_login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": HR_EMAIL, "password": PASSWORD}
        )
        hr_id = hr_login_response.json()["user"]["id"]
        
        # Try to reset
        response = requests.post(
            f"{BASE_URL}/auth/reset-password",
            headers={"Authorization": f"Bearer {emp_token}"},
            json={
                "employee_id": hr_id,
                "new_password": "hackedpassword"
            }
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Correctly blocked employee from resetting passwords (403)")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def test_logout():
    """Test 17: Logout endpoint"""
    global tests_passed, tests_failed
    test_name = "Test 17: Logout"
    
    try:
        response = requests.post(f"{BASE_URL}/auth/logout")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        print(f"{GREEN}PASS{RESET} {test_name}")
        print(f"   Logout successful")
        tests_passed += 1
        
    except AssertionError as e:
        print(f"{RED}FAIL{RESET} {test_name}: {str(e)}")
        tests_failed += 1
    except Exception as e:
        print(f"{RED}ERROR{RESET} {test_name}: {str(e)}")
        tests_failed += 1


def run_all_tests():
    """Run all authentication API tests"""
    global tests_passed, tests_failed
    
    print_section("AUTHENTICATION API TEST SUITE")
    print(f"Testing at: {BASE_URL}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all tests - each test handles its own errors
    test_login_hr()
    test_login_manager()
    test_login_employee()
    test_login_invalid_email()
    test_login_wrong_password()
    test_login_missing_field()
    test_get_current_user()
    test_get_current_user_no_token()
    test_get_current_user_invalid_token()
    test_refresh_token()
    test_refresh_token_invalid()
    test_change_password()
    test_change_password_wrong_current()
    test_reset_password_by_hr()
    test_reset_password_by_manager()
    test_reset_password_by_employee_forbidden()
    test_logout()
    
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
