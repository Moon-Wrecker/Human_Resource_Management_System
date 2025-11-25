"""
Authentication API Tests (Pytest)
Run with: pytest backend/tests/test_authentication_api.py -v
"""
import pytest
import requests


@pytest.mark.auth
class TestAuthenticationAPI:
    """Test suite for Authentication endpoints"""
    
    def test_hr_login(self, api_base_url):
        """Test HR can login successfully"""
        response = requests.post(
            f"{api_base_url}/auth/login",
            json={"email": "sarah.johnson@company.com", "password": "pass123"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        assert "access_token" in data
        assert "refresh_token" in data
        assert "token_type" in data
        assert "user" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["role"] == "hr"
    
    def test_manager_login(self, api_base_url):
        """Test Manager can login successfully"""
        response = requests.post(
            f"{api_base_url}/auth/login",
            json={"email": "michael.chen@company.com", "password": "pass123"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        assert "access_token" in data
        assert data["user"]["role"] == "manager"
    
    def test_employee_login(self, api_base_url):
        """Test Employee can login successfully"""
        response = requests.post(
            f"{api_base_url}/auth/login",
            json={"email": "john.anderson@company.com", "password": "pass123"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["user"]["role"] == "employee"
    
    @pytest.mark.permissions
    def test_login_invalid_email(self, api_base_url):
        """Test invalid email returns 401"""
        response = requests.post(
            f"{api_base_url}/auth/login",
            json={"email": "nonexistent@company.com", "password": "pass123"}
        )
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    
    @pytest.mark.permissions
    def test_login_wrong_password(self, api_base_url):
        """Test wrong password returns 401"""
        response = requests.post(
            f"{api_base_url}/auth/login",
            json={"email": "john.anderson@company.com", "password": "wrongpassword"}
        )
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    
    def test_login_missing_field(self, api_base_url):
        """Test missing password field returns 422"""
        response = requests.post(
            f"{api_base_url}/auth/login",
            json={"email": "john.anderson@company.com"}
        )
        
        assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    
    def test_get_current_user(self, api_base_url, employee_token):
        """Test get current user with valid token"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        assert "name" in data
        assert "email" in data
        assert "role" in data
        assert data["email"] == "john.anderson@company.com"
    
    @pytest.mark.permissions
    def test_get_current_user_no_token(self, api_base_url):
        """Test get current user without token returns 403"""
        response = requests.get(f"{api_base_url}/auth/me")
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    @pytest.mark.permissions
    def test_get_current_user_invalid_token(self, api_base_url):
        """Test get current user with invalid token returns 401"""
        response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    
    def test_refresh_token(self, api_base_url):
        """Test refresh access token with valid refresh token"""
        # First login to get refresh token
        login_response = requests.post(
            f"{api_base_url}/auth/login",
            json={"email": "john.anderson@company.com", "password": "pass123"}
        )
        
        if login_response.status_code != 200:
            pytest.skip("Login failed (database not seeded)")
        
        refresh_token = login_response.json()["refresh_token"]
        
        response = requests.post(
            f"{api_base_url}/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.permissions
    def test_refresh_token_invalid(self, api_base_url):
        """Test invalid refresh token returns 401"""
        response = requests.post(
            f"{api_base_url}/auth/refresh",
            json={"refresh_token": "invalid.refresh.token"}
        )
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    
    def test_change_password(self, api_base_url):
        """Test change password successfully"""
        # Login first
        login_response = requests.post(
            f"{api_base_url}/auth/login",
            json={"email": "john.anderson@company.com", "password": "pass123"}
        )
        
        if login_response.status_code != 200:
            pytest.skip("Login failed (database not seeded)")
        
        token = login_response.json()["access_token"]
        
        # Change password
        response = requests.post(
            f"{api_base_url}/auth/change-password",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "current_password": "pass123",
                "new_password": "newpassword456"
            }
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Verify can login with new password
        new_login = requests.post(
            f"{api_base_url}/auth/login",
            json={"email": "john.anderson@company.com", "password": "newpassword456"}
        )
        assert new_login.status_code == 200, "Cannot login with new password"
        
        # Revert password
        new_token = new_login.json()["access_token"]
        requests.post(
            f"{api_base_url}/auth/change-password",
            headers={"Authorization": f"Bearer {new_token}"},
            json={
                "current_password": "newpassword456",
                "new_password": "pass123"
            }
        )
    
    @pytest.mark.permissions
    def test_change_password_wrong_current(self, api_base_url, employee_token):
        """Test change password with wrong current password returns 400"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.post(
            f"{api_base_url}/auth/change-password",
            headers={"Authorization": f"Bearer {employee_token}"},
            json={
                "current_password": "wrongpassword",
                "new_password": "newpassword456"
            }
        )
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    @pytest.mark.permissions
    def test_reset_password_by_hr(self, api_base_url, hr_token):
        """Test HR can reset employee password"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        # Get employee ID
        employee_login = requests.post(
            f"{api_base_url}/auth/login",
            json={"email": "john.anderson@company.com", "password": "pass123"}
        )
        
        if employee_login.status_code != 200:
            pytest.skip("Employee login failed (database not seeded)")
        
        employee_id = employee_login.json()["user"]["id"]
        
        # Reset password
        response = requests.post(
            f"{api_base_url}/auth/reset-password",
            headers={"Authorization": f"Bearer {hr_token}"},
            json={
                "employee_id": employee_id,
                "new_password": "resetpassword123"
            }
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Verify and revert
        reset_login = requests.post(
            f"{api_base_url}/auth/login",
            json={"email": "john.anderson@company.com", "password": "resetpassword123"}
        )
        assert reset_login.status_code == 200, "Cannot login with reset password"
        
        # Revert
        reset_token = reset_login.json()["access_token"]
        requests.post(
            f"{api_base_url}/auth/change-password",
            headers={"Authorization": f"Bearer {reset_token}"},
            json={
                "current_password": "resetpassword123",
                "new_password": "pass123"
            }
        )
    
    @pytest.mark.permissions
    def test_reset_password_by_manager(self, api_base_url, manager_token):
        """Test Manager can reset employee password"""
        if not manager_token:
            pytest.skip("Manager token not available (database not seeded)")
        
        # Get employee ID
        employee_login = requests.post(
            f"{api_base_url}/auth/login",
            json={"email": "john.anderson@company.com", "password": "pass123"}
        )
        
        if employee_login.status_code != 200:
            pytest.skip("Employee login failed (database not seeded)")
        
        employee_id = employee_login.json()["user"]["id"]
        
        # Reset password
        response = requests.post(
            f"{api_base_url}/auth/reset-password",
            headers={"Authorization": f"Bearer {manager_token}"},
            json={
                "employee_id": employee_id,
                "new_password": "managerreset123"
            }
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Revert
        reset_login = requests.post(
            f"{api_base_url}/auth/login",
            json={"email": "john.anderson@company.com", "password": "managerreset123"}
        )
        
        if reset_login.status_code == 200:
            reset_token = reset_login.json()["access_token"]
            requests.post(
                f"{api_base_url}/auth/change-password",
                headers={"Authorization": f"Bearer {reset_token}"},
                json={
                    "current_password": "managerreset123",
                    "new_password": "pass123"
                }
            )
    
    @pytest.mark.permissions
    def test_reset_password_employee_forbidden(self, api_base_url, employee_token, hr_token):
        """Test Employee cannot reset passwords (403)"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        # Get HR ID
        hr_login = requests.post(
            f"{api_base_url}/auth/login",
            json={"email": "sarah.johnson@company.com", "password": "pass123"}
        )
        
        if hr_login.status_code != 200:
            pytest.skip("HR login failed (database not seeded)")
        
        hr_id = hr_login.json()["user"]["id"]
        
        # Try to reset as employee
        response = requests.post(
            f"{api_base_url}/auth/reset-password",
            headers={"Authorization": f"Bearer {employee_token}"},
            json={
                "employee_id": hr_id,
                "new_password": "hackedpassword"
            }
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_logout(self, api_base_url):
        """Test logout endpoint"""
        response = requests.post(f"{api_base_url}/auth/logout")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
