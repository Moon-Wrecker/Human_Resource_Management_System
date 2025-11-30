"""
Comprehensive API Test Suite Runner (Pytest)

This script runs all API tests using pytest with colored output and detailed reporting.
Test outputs are automatically saved to test_reports/{timestamp}.txt

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
from datetime import datetime
from pathlib import Path


def run_tests():
    """Run all API tests using pytest and save output to timestamped file"""
    
    # Create test_reports directory if it doesn't exist
    project_root = Path(__file__).parent.parent.parent  # Go up from tests/backend to project root
    reports_dir = project_root / "test_reports"
    reports_dir.mkdir(exist_ok=True)
    
    # Generate timestamp for the report file
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    report_file = reports_dir / f"{timestamp}.txt"
    
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
        "test_dashboard_api.py",
        "test_employees_api.py",
        "test_feedback_api.py",
        "test_jobs_listings_api.py",  
        "test_goals_api.py",
        "test_leaves_api.py",
        "test_applications_api.py",
        "test_organization_api.py",
        "test_payslips_api.py",
        "test_policies_api.py",
        "test_profile_api.py",
        "test_team_requests_api.py",
        "test_skills_api.py",
        "test_ai_apis_comprehensive.py",  # AI services comprehensive tests
        "-v",  # Verbose
        "--tb=short",  # Short traceback
        "--color=yes",  # Colored output
        "-ra",  # Show summary of all test outcomes
    ]
    
    # Add any additional arguments passed to this script
    if len(sys.argv) > 1:
        # Remove the converted file names and use custom args
        pytest_args = ["pytest"] + sys.argv[1:] + ["test_*_api.py"]
    
    header = "=" * 70
    print(header)
    print("  COMPREHENSIVE API TEST SUITE (Pytest)")
    print(header)
    print(f"Running: {' '.join(pytest_args)}")
    print(f"Report will be saved to: {report_file}")
    print(header)
    print()
    
    # Run pytest and capture output to both console and file
    with open(report_file, 'w') as f:
        # Write header to file
        f.write(header + "\n")
        f.write("  COMPREHENSIVE API TEST SUITE (Pytest)\n")
        f.write(header + "\n")
        f.write(f"Running: {' '.join(pytest_args)}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(header + "\n\n")
        f.flush()
        
        # Run pytest with Tee-like behavior (output to both console and file)
        process = subprocess.Popen(
            pytest_args, 
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Read output line by line and write to both console and file
        for line in process.stdout:
            print(line, end='')  # Print to console
            f.write(line)  # Write to file
            f.flush()  # Ensure immediate write
        
        process.wait()
        
        # Write footer
        footer = f"\n{header}\nTest report saved to: {report_file}\n{header}\n"
        print(footer)
        f.write(footer)
    
    print(f"\n✅ Test report saved to: {report_file}")
    
    return process.returncode


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
