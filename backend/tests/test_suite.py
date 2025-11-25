"""
Comprehensive API Test Suite Runner (Pytest)

This script runs all API tests using pytest with colored output and detailed reporting.

Usage:
    python3 backend/tests/test_suite.py           # Run all API tests
    python3 backend/tests/test_suite.py -v        # Verbose output
    python3 backend/tests/test_suite.py -k health # Run only health tests

Or use pytest directly:
    pytest backend/tests/test_*_api.py            # Run all API tests
    pytest backend/tests/ -v                      # Verbose
    pytest backend/tests/ -v --tb=short          # Short traceback
    pytest backend/tests/ -m health              # Run health tests only
    pytest backend/tests/ -n auto                # Parallel execution
"""
import sys
import subprocess
import os


def run_tests():
    """Run all API tests using pytest"""
    
    # Change to tests directory
    os.chdir(os.path.dirname(__file__))
    
    # Default pytest arguments - only run *_api.py files
    pytest_args = [
        "pytest",
        "test_health_api.py",
        "test_authentication_api.py",
        "test_announcements_api.py",
        "test_holidays_api.py",
        "test_attendance_api.py",
        "test_departments_api.py",
        "test_dashboard_api.py",  # Added
        "-v",  # Verbose
        "--tb=short",  # Short traceback
        "--color=yes",  # Colored output
        "-ra",  # Show summary of all test outcomes
    ]
    
    # Add any additional arguments passed to this script
    if len(sys.argv) > 1:
        # Remove the converted file names and use custom args
        pytest_args = ["pytest"] + sys.argv[1:] + ["test_*_api.py"]
    
    print("="*70)
    print("  COMPREHENSIVE API TEST SUITE (Pytest)")
    print("="*70)
    print(f"Running: {' '.join(pytest_args)}")
    print("="*70)
    print()
    
    # Run pytest
    result = subprocess.run(pytest_args)
    
    return result.returncode


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
