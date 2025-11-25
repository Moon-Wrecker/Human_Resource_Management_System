"""
Pytest configuration and shared fixtures for API tests
"""
import pytest
import requests
from typing import Dict

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE_URL = f"{BASE_URL}/api/v1"

# Test credentials
HR_EMAIL = "sarah.johnson@company.com"
MANAGER_EMAIL = "michael.chen@company.com"
EMPLOYEE_EMAIL = "john.anderson@company.com"
PASSWORD = "pass123"


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the API"""
    return BASE_URL


@pytest.fixture(scope="session")
def api_base_url():
    """API v1 base URL"""
    return API_BASE_URL


@pytest.fixture(scope="session")
def hr_token(api_base_url) -> str:
    """Get HR user authentication token"""
    response = requests.post(
        f"{api_base_url}/auth/login",
        json={"email": HR_EMAIL, "password": PASSWORD}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    return None


@pytest.fixture(scope="session")
def manager_token(api_base_url) -> str:
    """Get Manager user authentication token"""
    response = requests.post(
        f"{api_base_url}/auth/login",
        json={"email": MANAGER_EMAIL, "password": PASSWORD}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    return None


@pytest.fixture(scope="session")
def employee_token(api_base_url) -> str:
    """Get Employee user authentication token"""
    response = requests.post(
        f"{api_base_url}/auth/login",
        json={"email": EMPLOYEE_EMAIL, "password": PASSWORD}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    return None


@pytest.fixture(scope="session")
def hr_headers(hr_token) -> Dict[str, str]:
    """Headers with HR authentication"""
    if hr_token:
        return {
            "Authorization": f"Bearer {hr_token}",
            "Content-Type": "application/json"
        }
    return {"Content-Type": "application/json"}


@pytest.fixture(scope="session")
def manager_headers(manager_token) -> Dict[str, str]:
    """Headers with Manager authentication"""
    if manager_token:
        return {
            "Authorization": f"Bearer {manager_token}",
            "Content-Type": "application/json"
        }
    return {"Content-Type": "application/json"}


@pytest.fixture(scope="session")
def employee_headers(employee_token) -> Dict[str, str]:
    """Headers with Employee authentication"""
    if employee_token:
        return {
            "Authorization": f"Bearer {employee_token}",
            "Content-Type": "application/json"
        }
    return {"Content-Type": "application/json"}


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "health: Health and root endpoint tests"
    )
    config.addinivalue_line(
        "markers", "auth: Authentication tests"
    )
    config.addinivalue_line(
        "markers", "announcements: Announcements API tests"
    )
    config.addinivalue_line(
        "markers", "holidays: Holidays API tests"
    )
    config.addinivalue_line(
        "markers", "attendance: Attendance API tests"
    )
    config.addinivalue_line(
        "markers", "departments: Departments API tests"
    )
    config.addinivalue_line(
        "markers", "dashboard: Dashboard API tests"
    )
    config.addinivalue_line(
        "markers", "employees: Employees API tests"
    )
    config.addinivalue_line(
        "markers", "feedback: Feedback API tests"
    )
    config.addinivalue_line(
        "markers", "jobs: Job Listings API tests"
    )
    config.addinivalue_line(
        "markers", "goals: Goals API tests"
    )
    config.addinivalue_line(
        "markers", "leaves: Leaves API tests"
    )
    config.addinivalue_line(
        "markers", "applications: Applications API tests"
    )
    config.addinivalue_line(
        "markers", "organization: Organization/Hierarchy API tests"
    )
    config.addinivalue_line(
        "markers", "payslips: Payslips API tests"
    )
    config.addinivalue_line(
        "markers", "policies: Policies API tests"
    )
    config.addinivalue_line(
        "markers", "profile: Profile API tests"
    )
    config.addinivalue_line(
        "markers", "team_requests: Team Requests API tests"
    )
    config.addinivalue_line(
        "markers", "permissions: Permission/authorization tests"
    )
