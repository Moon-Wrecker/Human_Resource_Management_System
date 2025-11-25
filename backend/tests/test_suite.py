"""
Comprehensive API Test Suite Runner
Runs all API tests from individual test modules

Test Modules:
- test_health_api.py (7 tests)
- test_authentication_api.py (17 tests)
- test_announcements_api.py (14 tests)

Run: python3 backend/tests/test_suite.py
"""
import sys
from datetime import datetime

# ANSI Color codes
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Import test modules
from test_health_api import (
    test_root_endpoint,
    test_health_endpoint,
    test_api_v1_root,
    test_swagger_ui,
    test_redoc,
    test_openapi_json,
    test_404_handling,
    tests_passed as health_passed,
    tests_failed as health_failed
)

from test_authentication_api import (
    test_login_hr,
    test_login_manager,
    test_login_employee,
    test_login_invalid_email,
    test_login_wrong_password,
    test_login_missing_field,
    test_get_current_user,
    test_get_current_user_no_token,
    test_get_current_user_invalid_token,
    test_refresh_token,
    test_refresh_token_invalid,
    test_change_password,
    test_change_password_wrong_current,
    test_reset_password_by_hr,
    test_reset_password_by_manager,
    test_reset_password_by_employee_forbidden,
    test_logout,
    tests_passed as auth_passed,
    tests_failed as auth_failed
)

from test_announcements_api import (
    test_hr_login as test_announcements_hr_login,
    test_employee_login as test_announcements_employee_login,
    test_create_announcement,
    test_create_announcement_employee_forbidden,
    test_get_all_announcements,
    test_get_announcement_by_id,
    test_get_nonexistent_announcement,
    test_update_announcement,
    test_update_announcement_employee_forbidden,
    test_get_statistics,
    test_employee_can_view_announcements,
    test_create_urgent_announcement,
    test_soft_delete_announcement,
    test_delete_announcement_employee_forbidden,
    tests_passed as announcements_passed,
    tests_failed as announcements_failed
)


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def print_subsection(title):
    """Print a formatted subsection header"""
    print("\n" + "-"*70)
    print(f"  {title}")
    print("-"*70)


def run_comprehensive_test_suite():
    """Run all API tests from all modules"""
    
    print_section("COMPREHENSIVE API TEST SUITE")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # ========================================================================
    # HEALTH & ROOT TESTS
    # ========================================================================
    print_subsection("HEALTH & ROOT API TESTS (7 Tests)")
    
    test_root_endpoint()
    test_health_endpoint()
    test_api_v1_root()
    test_swagger_ui()
    test_redoc()
    test_openapi_json()
    test_404_handling()
    
    # Get health test results
    import test_health_api
    health_tests_passed = test_health_api.tests_passed
    health_tests_failed = test_health_api.tests_failed
    
    # ========================================================================
    # AUTHENTICATION TESTS
    # ========================================================================
    print_subsection("AUTHENTICATION API TESTS (17 Tests)")
    
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
    
    # Get auth test results
    import test_authentication_api
    auth_tests_passed = test_authentication_api.tests_passed
    auth_tests_failed = test_authentication_api.tests_failed
    
    # ========================================================================
    # ANNOUNCEMENTS TESTS
    # ========================================================================
    print_subsection("ANNOUNCEMENTS API TESTS (14 Tests)")
    
    test_announcements_hr_login()
    test_announcements_employee_login()
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
    
    # Get announcements test results
    import test_announcements_api
    announcements_tests_passed = test_announcements_api.tests_passed
    announcements_tests_failed = test_announcements_api.tests_failed
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print_section("FINAL TEST SUMMARY")
    
    total_passed = health_tests_passed + auth_tests_passed + announcements_tests_passed
    total_failed = health_tests_failed + auth_tests_failed + announcements_tests_failed
    total_tests = total_passed + total_failed
    
    print(f"\nOverall Results:")
    print(f"  Total Tests: {total_tests}")
    print(f"  {GREEN}PASSED{RESET}: {total_passed}")
    print(f"  {RED}FAILED{RESET}: {total_failed}")
    print(f"  Success Rate: {(total_passed/total_tests)*100:.1f}%")
    
    print(f"\nBreakdown by Module:")
    print(f"  Health & Root API:")
    print(f"    {GREEN}PASSED{RESET}: {health_tests_passed}/7")
    print(f"    {RED}FAILED{RESET}: {health_tests_failed}/7")
    
    print(f"  Authentication API:")
    print(f"    {GREEN}PASSED{RESET}: {auth_tests_passed}/17")
    print(f"    {RED}FAILED{RESET}: {auth_tests_failed}/17")
    
    print(f"  Announcements API:")
    print(f"    {GREEN}PASSED{RESET}: {announcements_tests_passed}/14")
    print(f"    {RED}FAILED{RESET}: {announcements_tests_failed}/14")
    
    if total_failed == 0:
        print(f"\n{GREEN}All tests passed successfully!{RESET}")
        print("="*70)
        return 0
    else:
        print(f"\n{RED}WARNING{RESET}: {total_failed} test(s) failed. Please review the output above.")
        print("="*70)
        return 1


if __name__ == "__main__":
    try:
        exit_code = run_comprehensive_test_suite()
        sys.exit(exit_code)
    except ImportError as e:
        print(f"\n❌ Error: Could not import test modules")
        print(f"Details: {str(e)}")
        print("Make sure you're running from the tests directory or use:")
        print("  cd backend/tests && python3 test_suite.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
