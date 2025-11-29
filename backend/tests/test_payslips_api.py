"""
Payslips API Tests (Pytest)
Run with: pytest backend/tests/test_payslips_api.py -v
"""
import pytest
import requests
from datetime import datetime


@pytest.mark.payslips
class TestPayslipsAPI:
    """Test suite for Payslips endpoints"""
    
    @pytest.fixture(scope="class")
    def payslip_id(self, api_base_url, hr_token, employee_token):
        """Create a test payslip and return its ID, cleanup after tests"""
        if not hr_token or not employee_token:
            yield None
            return
        
        # Get employee ID
        emp_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        if emp_response.status_code != 200:
            yield None
            return
        
        employee_id = emp_response.json()["id"]
        
        # Create payslip
        current_date = datetime.now()
        payslip_data = {
            "employee_id": employee_id,
            "pay_period_start": f"{current_date.year}-{current_date.month:02d}-01",
            "pay_period_end": f"{current_date.year}-{current_date.month:02d}-28",
            "pay_date": f"{current_date.year}-{current_date.month:02d}-28",
            "basic_salary": 50000.0,
            "allowances": 10000.0,
            "overtime_pay": 5000.0,
            "bonus": 0.0,
            "tax_deduction": 9750.0,
            "pf_deduction": 6000.0,
            "insurance_deduction": 1000.0,
            "other_deductions": 0.0
        }
        
        response = requests.post(
            f"{api_base_url}/payslips",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=payslip_data
        )
        
        payslip_id = None
        if response.status_code == 201:
            payslip_id = response.json()["id"]
        
        yield payslip_id
        
        # Cleanup - delete payslip after tests
        if payslip_id:
            requests.delete(
                f"{api_base_url}/payslips/{payslip_id}",
                headers={"Authorization": f"Bearer {hr_token}"}
            )
    
    def test_create_payslip(self, api_base_url, hr_token, employee_token):
        """Test HR can create payslip"""
        if not hr_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Get employee ID
        emp_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        if emp_response.status_code != 200:
            pytest.skip("Could not get employee info")
        
        employee_id = emp_response.json()["id"]
        
        current_date = datetime.now()
        payslip_data = {
            "employee_id": employee_id,
            "pay_period_start": f"{current_date.year}-{current_date.month:02d}-01",
            "pay_period_end": f"{current_date.year}-{current_date.month:02d}-28",
            "pay_date": f"{current_date.year}-{current_date.month:02d}-28",
            "basic_salary": 60000.0,
            "allowances": 12000.0,
            "overtime_pay": 0.0,
            "bonus": 5000.0,
            "tax_deduction": 11550.0,
            "pf_deduction": 7200.0,
            "insurance_deduction": 1500.0,
            "other_deductions": 0.0
        }
        
        response = requests.post(
            f"{api_base_url}/payslips",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=payslip_data
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data
        assert data["employee_id"] == employee_id
        
        # Cleanup
        requests.delete(
            f"{api_base_url}/payslips/{data['id']}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
    
    @pytest.mark.permissions
    def test_create_payslip_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot create payslip"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        payslip_data = {
            "employee_id": 1,
            "pay_period_start": "2025-01-01",
            "pay_period_end": "2025-01-31",
            "pay_date": "2025-01-31",
            "basic_salary": 50000.0
        }
        
        response = requests.post(
            f"{api_base_url}/payslips",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=payslip_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_my_payslips(self, api_base_url, employee_token):
        """Test get my payslips"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/payslips/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "payslips" in data
        assert "total" in data
    
    def test_filter_my_payslips_by_month(self, api_base_url, employee_token):
        """Test filter my payslips by month"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        current_month = datetime.now().month
        
        response = requests.get(
            f"{api_base_url}/payslips/me?month={current_month}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "payslips" in data
    
    def test_filter_my_payslips_by_year(self, api_base_url, employee_token):
        """Test filter my payslips by year"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        current_year = datetime.now().year
        
        response = requests.get(
            f"{api_base_url}/payslips/me?year={current_year}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "payslips" in data
    
    def test_get_employee_payslips(self, api_base_url, hr_token, employee_token):
        """Test HR can get employee payslips"""
        if not hr_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Get employee ID
        emp_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        if emp_response.status_code != 200:
            pytest.skip("Could not get employee info")
        
        employee_id = emp_response.json()["id"]
        
        response = requests.get(
            f"{api_base_url}/payslips/employee/{employee_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "payslips" in data
        assert "total" in data
    
    @pytest.mark.permissions
    def test_get_employee_payslips_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot get other employee's payslips"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/payslips/employee/1",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_all_payslips(self, api_base_url, hr_token):
        """Test HR can get all payslips"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/payslips",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "payslips" in data
        assert "total" in data
    
    @pytest.mark.permissions
    def test_get_all_payslips_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot get all payslips"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/payslips",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_payslip_by_id(self, api_base_url, employee_token, payslip_id):
        """Test get payslip by ID"""
        if not employee_token or not payslip_id:
            pytest.skip("Employee token or payslip not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/payslips/{payslip_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == payslip_id
    
    def test_update_payslip(self, api_base_url, hr_token, payslip_id):
        """Test HR can update payslip"""
        if not hr_token or not payslip_id:
            pytest.skip("HR token or payslip not available (database not seeded)")
        
        update_data = {
            "bonus": 10000.0,
            "overtime_pay": 7500.0
        }
        
        response = requests.put(
            f"{api_base_url}/payslips/{payslip_id}",
            headers={"Authorization": f"Bearer {hr_token}"},
            json=update_data
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["bonus"] == update_data["bonus"]
    
    @pytest.mark.permissions
    def test_update_payslip_employee_forbidden(self, api_base_url, employee_token, payslip_id):
        """Test employee cannot update payslip"""
        if not employee_token or not payslip_id:
            pytest.skip("Employee token or payslip not available (database not seeded)")
        
        update_data = {"bonus": 50000.0}
        
        response = requests.put(
            f"{api_base_url}/payslips/{payslip_id}",
            headers={"Authorization": f"Bearer {employee_token}"},
            json=update_data
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_get_payslip_stats(self, api_base_url, hr_token):
        """Test HR can get payslip statistics"""
        if not hr_token:
            pytest.skip("HR token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/payslips/stats/summary",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "total_payslips" in data or "total" in data
    
    @pytest.mark.permissions
    def test_get_payslip_stats_employee_forbidden(self, api_base_url, employee_token):
        """Test employee cannot access payslip statistics"""
        if not employee_token:
            pytest.skip("Employee token not available (database not seeded)")
        
        response = requests.get(
            f"{api_base_url}/payslips/stats/summary",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_delete_payslip(self, api_base_url, hr_token, employee_token):
        """Test HR can delete payslip"""
        if not hr_token or not employee_token:
            pytest.skip("Tokens not available (database not seeded)")
        
        # Get employee ID
        emp_response = requests.get(
            f"{api_base_url}/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        if emp_response.status_code != 200:
            pytest.skip("Could not get employee info")
        
        employee_id = emp_response.json()["id"]
        
        # Create payslip to delete
        current_date = datetime.now()
        create_response = requests.post(
            f"{api_base_url}/payslips",
            headers={"Authorization": f"Bearer {hr_token}"},
            json={
                "employee_id": employee_id,
                "pay_period_start": f"{current_date.year}-{current_date.month:02d}-01",
                "pay_period_end": f"{current_date.year}-{current_date.month:02d}-15",
                "pay_date": f"{current_date.year}-{current_date.month:02d}-15",
                "basic_salary": 40000.0
            }
        )
        
        if create_response.status_code != 201:
            pytest.skip("Could not create payslip for delete test")
        
        test_id = create_response.json()["id"]
        
        # Delete
        response = requests.delete(
            f"{api_base_url}/payslips/{test_id}",
            headers={"Authorization": f"Bearer {hr_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "message" in data
    
    @pytest.mark.permissions
    def test_delete_payslip_employee_forbidden(self, api_base_url, employee_token, payslip_id):
        """Test employee cannot delete payslip"""
        if not employee_token or not payslip_id:
            pytest.skip("Employee token or payslip not available (database not seeded)")
        
        response = requests.delete(
            f"{api_base_url}/payslips/{payslip_id}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
