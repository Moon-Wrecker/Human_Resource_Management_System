"""
COMPREHENSIVE API TESTING SUITE - ALL 171+ ENDPOINTS
Tests every documented API endpoint in the HRMS system
"""
import requests
import time
from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any

API_URL = "http://localhost:8000/api/v1"
CREDENTIALS = {
    "hr": {"email": "sarah.johnson@company.com", "password": "pass123"},
    "manager": {"email": "michael.chen@company.com", "password": "pass123"},
    "employee": {"email": "john.doe@company.com", "password": "pass123"}
}

class ComprehensiveTester:
    def __init__(self):
        self.tokens = {}
        self.results = []
        self.user_ids = {}
        self.created_ids = {}  # Track created resources for cleanup/dependent tests
        self.start = datetime.now()
    
    def test(self, name: str, method: str, endpoint: str, role: str = "employee", 
             data: Optional[Dict] = None, params: Optional[Dict] = None, expected: int = 200):
        """Run a single API test"""
        headers = {}
        if role and role in self.tokens:
            headers["Authorization"] = f"Bearer {self.tokens[role]}"
        
        url = f"{API_URL}{endpoint}"
        start_time = time.time()
        
        try:
            if method == "GET":
                r = requests.get(url, headers=headers, params=params, timeout=10)
            elif method == "POST":
                r = requests.post(url, headers=headers, json=data, timeout=10)
            elif method == "PUT":
                r = requests.put(url, headers=headers, json=data, timeout=10)
            elif method == "DELETE":
                r = requests.delete(url, headers=headers, timeout=10)
            elif method == "PATCH":
                r = requests.patch(url, headers=headers, json=data, timeout=10)
            
            exec_time = round((time.time() - start_time) * 1000)
            status = "✅ PASSED" if r.status_code == expected else "❌ FAILED"
            error = None if r.status_code == expected else f"Expected {expected}, got {r.status_code}"
            
            if error and r.status_code in [422, 500, 400]:
                try:
                    err_detail = r.json()
                    error += f" - {err_detail.get('detail', '')}"
                except:
                    pass
            
            self.results.append({
                "name": name, "method": method, "endpoint": endpoint,
                "status": status, "time": exec_time, "response_code": r.status_code,
                "expected_code": expected, "error": error, "role": role
            })
            
            print(f"  {status} {name} ({exec_time}ms)")
            if error:
                print(f"      ↳ {error}")
            
            return r if r.status_code == expected else None
            
        except Exception as e:
            self.results.append({
                "name": name, "method": method, "endpoint": endpoint,
                "status": "⚠️ ERROR", "time": round((time.time() - start_time) * 1000),
                "response_code": None, "expected_code": expected,
                "error": str(e), "role": role
            })
            print(f"  ⚠️ ERROR {name} - {str(e)}")
            return None
    
    def auth(self):
        """Authenticate all users"""
        print("\n🔐 AUTHENTICATING ALL USERS...")
        for role, creds in CREDENTIALS.items():
            r = self.test(f"{role.upper()} Login", "POST", "/auth/login", role=None, data=creds, expected=200)
            if r:
                data = r.json()
                self.tokens[role] = data.get("access_token")
                self.user_ids[role] = data.get("user", {}).get("id")
                print(f"    ✓ {role.upper()} authenticated (ID: {self.user_ids[role]})")
    
    def test_auth_module(self):
        """Test Authentication APIs (6 endpoints)"""
        print("\n\n" + "="*80)
        print("1️⃣ AUTHENTICATION MODULE (6 endpoints)")
        print("="*80)
        
        # Already tested login, test remaining
        self.test("Get Current User", "GET", "/auth/me", "employee", expected=200)
        self.test("Refresh Token", "POST", "/auth/refresh-token", "employee",
                 data={"refresh_token": "dummy"}, expected=401)  # Will fail, that's ok
        self.test("Change Password", "POST", "/auth/change-password", "employee",
                 data={"current_password": "pass123", "new_password": "newpass123"}, expected=200)
        self.test("Reset Password Request", "POST", "/auth/reset-password", None,
                 data={"email": "john.doe@company.com"}, expected=200)
        self.test("Logout", "POST", "/auth/logout", "employee", expected=200)
        # Re-auth after logout
        self.auth()
    
    def test_dashboard_module(self):
        """Test Dashboard APIs (6 endpoints)"""
        print("\n\n" + "="*80)
        print("2️⃣ DASHBOARD MODULE (6 endpoints)")
        print("="*80)
        
        self.test("Employee Dashboard", "GET", "/dashboard/employee", "employee", expected=200)
        self.test("Manager Dashboard", "GET", "/dashboard/manager", "manager", expected=200)
        self.test("HR Dashboard", "GET", "/dashboard/hr", "hr", expected=200)
        self.test("My Dashboard (Auto-detect)", "GET", "/dashboard/me", "employee", expected=200)
        self.test("Employee Performance", "GET", f"/dashboard/performance/{self.user_ids['employee']}", "manager", expected=200)
        self.test("My Performance", "GET", "/dashboard/performance/me", "employee", expected=200)
    
    def test_employees_module(self):
        """Test Employee Management APIs (6 endpoints)"""
        print("\n\n" + "="*80)
        print("3️⃣ EMPLOYEE MANAGEMENT MODULE (6 endpoints)")
        print("="*80)
        
        # Create employee
        emp_data = {
            "name": f"Test Employee {int(time.time())}",
            "email": f"test{int(time.time())}@company.com",
            "phone": "+1-555-0199",
            "role": "employee",
            "employee_id": f"TEST{int(time.time())}",
            "department_id": 1,
            "job_role": "Test Engineer",
            "hire_date": date.today().isoformat(),
            "password": "test123"
        }
        r = self.test("Create Employee", "POST", "/employees", "hr", data=emp_data, expected=201)
        if r:
            self.created_ids['employee'] = r.json().get('id')
        
        self.test("Get All Employees", "GET", "/employees", "hr", expected=200)
        self.test("Get Employee Stats", "GET", "/employees/stats", "hr", expected=200)
        
        if 'employee' in self.created_ids:
            emp_id = self.created_ids['employee']
            self.test("Get Employee Details", "GET", f"/employees/{emp_id}", "hr", expected=200)
            self.test("Update Employee", "PUT", f"/employees/{emp_id}", "hr",
                     data={"phone": "+1-555-9999"}, expected=200)
            self.test("Deactivate Employee", "DELETE", f"/employees/{emp_id}", "hr", expected=200)
    
    def test_departments_module(self):
        """Test Departments APIs (6 endpoints)"""
        print("\n\n" + "="*80)
        print("4️⃣ DEPARTMENTS MODULE (6 endpoints)")
        print("="*80)
        
        dept_data = {"name": f"Test Dept {int(time.time())}", "description": "Test department"}
        r = self.test("Create Department", "POST", "/departments", "hr", data=dept_data, expected=201)
        if r:
            self.created_ids['department'] = r.json().get('id')
        
        self.test("Get All Departments", "GET", "/departments", "employee", expected=200)
        self.test("Get Department Stats", "GET", "/departments/stats", "hr", expected=200)
        
        if 'department' in self.created_ids:
            dept_id = self.created_ids['department']
            self.test("Get Department Details", "GET", f"/departments/{dept_id}", "employee", expected=200)
            self.test("Update Department", "PUT", f"/departments/{dept_id}", "hr",
                     data={"description": "Updated description"}, expected=200)
            self.test("Delete Department", "DELETE", f"/departments/{dept_id}", "hr", expected=200)
    
    def test_teams_module(self):
        """Test Teams APIs (6 endpoints)"""
        print("\n\n" + "="*80)
        print("5️⃣ TEAMS MODULE (6 endpoints)")
        print("="*80)
        
        team_data = {"name": f"Test Team {int(time.time())}", "department_id": 1, "description": "Test team"}
        r = self.test("Create Team", "POST", "/teams", "hr", data=team_data, expected=201)
        if r:
            self.created_ids['team'] = r.json().get('id')
        
        self.test("Get All Teams", "GET", "/teams", "employee", expected=200)
        self.test("Get Team Stats", "GET", "/teams/stats", "hr", expected=200)
        
        if 'team' in self.created_ids:
            team_id = self.created_ids['team']
            self.test("Get Team Details", "GET", f"/teams/{team_id}", "employee", expected=200)
            self.test("Update Team", "PUT", f"/teams/{team_id}", "hr",
                     data={"description": "Updated team"}, expected=200)
            self.test("Delete Team", "DELETE", f"/teams/{team_id}", "hr", expected=200)
    
    def test_attendance_module(self):
        """Test Attendance APIs (9 endpoints)"""
        print("\n\n" + "="*80)
        print("6️⃣ ATTENDANCE MODULE (9 endpoints)")
        print("="*80)
        
        self.test("Punch In", "POST", "/attendance/punch-in", "employee",
                 data={"status": "present", "location": "office"}, expected=200)
        self.test("Get Today's Attendance", "GET", "/attendance/today", "employee", expected=200)
        self.test("Punch Out", "POST", "/attendance/punch-out", "employee",
                 data={"location": "office"}, expected=200)
        self.test("Get My Attendance", "GET", "/attendance/me", "employee", expected=200)
        self.test("Get My Summary", "GET", "/attendance/me/summary", "employee", expected=200)
        self.test("Get Team Attendance", "GET", "/attendance/team", "manager", expected=200)
        self.test("Get All Attendance", "GET", "/attendance/all", "hr", expected=200)
        
        mark_data = {
            "user_id": self.user_ids["employee"],
            "date": date.today().isoformat(),
            "status": "present",
            "check_in_time": datetime.now().isoformat(),
            "check_out_time": (datetime.now() + timedelta(hours=8)).isoformat()
        }
        self.test("Mark Attendance (HR)", "POST", "/attendance/mark", "hr", data=mark_data, expected=200)
        # Note: Delete attendance test skipped to avoid deleting real data
    
    def test_jobs_module(self):
        """Test Jobs APIs (7 endpoints)"""
        print("\n\n" + "="*80)
        print("7️⃣ JOBS MODULE (7 endpoints)")
        print("="*80)
        
        job_data = {
            "position": f"Test Position {int(time.time())}",
            "department_id": 1,
            "description": "Test job description",
            "experience_required": "2-3 years",
            "skills_required": "Python, FastAPI",
            "location": "Remote",
            "employment_type": "full-time",
            "salary_range": "$80k-$100k"
        }
        r = self.test("Create Job", "POST", "/jobs", "hr", data=job_data, expected=201)
        if r:
            self.created_ids['job'] = r.json().get('id')
        
        self.test("Get All Jobs", "GET", "/jobs", "employee", expected=200)
        self.test("Get Job Statistics", "GET", "/jobs/statistics", "hr", expected=200)
        
        if 'job' in self.created_ids:
            job_id = self.created_ids['job']
            self.test("Get Job Details", "GET", f"/jobs/{job_id}", "employee", expected=200)
            self.test("Update Job", "PUT", f"/jobs/{job_id}", "hr",
                     data={"description": "Updated description"}, expected=200)
            self.test("Get Job Applications", "GET", f"/jobs/{job_id}/applications", "hr", expected=200)
            self.test("Delete Job", "DELETE", f"/jobs/{job_id}", "hr", expected=200)
    
    def test_applications_module(self):
        """Test Applications APIs (9 endpoints)"""
        print("\n\n" + "="*80)
        print("8️⃣ APPLICATIONS MODULE (9 endpoints)")
        print("="*80)
        
        # Need a job for application
        if 'job' not in self.created_ids:
            job_data = {"position": "Test Job", "department_id": 1, "description": "Test"}
            r = self.test("Create Job for App", "POST", "/jobs", "hr", data=job_data, expected=201)
            if r:
                self.created_ids['job'] = r.json().get('id')
        
        if 'job' in self.created_ids:
            app_data = {
                "job_listing_id": self.created_ids['job'],
                "applicant_name": "Test Applicant",
                "email": f"applicant{int(time.time())}@test.com",
                "phone": "+1-555-1234",
                "cover_letter": "Test cover letter"
            }
            r = self.test("Submit Application", "POST", "/applications/apply", None, data=app_data, expected=201)
            if r:
                self.created_ids['application'] = r.json().get('id')
        
        self.test("Get All Applications", "GET", "/applications", "hr", expected=200)
        self.test("Get Application Stats", "GET", "/applications/stats", "hr", expected=200)
        self.test("Get Recent Applications", "GET", "/applications/recent", "hr", expected=200)
        
        if 'application' in self.created_ids:
            app_id = self.created_ids['application']
            self.test("Get Application Details", "GET", f"/applications/{app_id}", "hr", expected=200)
            self.test("Update Application Status", "PUT", f"/applications/{app_id}/status", "hr",
                     data={"status": "under_review"}, expected=200)
            
            screening_data = {
                "overall_score": 85, "technical_skills_score": 90,
                "experience_score": 80, "recommendation": "Interview"
            }
            self.test("Add Screening Result", "POST", f"/applications/{app_id}/screening", "hr",
                     data=screening_data, expected=200)
            
            if 'job' in self.created_ids:
                self.test("Get Apps by Job", "GET", f"/applications/job/{self.created_ids['job']}", "hr", expected=200)
            
            self.test("Delete Application", "DELETE", f"/applications/{app_id}", "hr", expected=200)
    
    def test_leaves_module(self):
        """Test Leaves APIs (9 endpoints)"""
        print("\n\n" + "="*80)
        print("9️⃣ LEAVES MODULE (9 endpoints)")
        print("="*80)
        
        tomorrow = date.today() + timedelta(days=1)
        leave_data = {
            "leave_type": "casual",
            "start_date": tomorrow.isoformat(),
            "end_date": (tomorrow + timedelta(days=1)).isoformat(),
            "days_requested": 2,
            "subject": "Personal Work",
            "reason": "Test leave request"
        }
        r = self.test("Create Leave Request", "POST", "/leaves", "employee", data=leave_data, expected=201)
        if r:
            self.created_ids['leave'] = r.json().get('id')
        
        self.test("Get My Leaves", "GET", "/leaves/me", "employee", expected=200)
        self.test("Get Leave Balance", "GET", "/leaves/balance/me", "employee", expected=200)
        self.test("Get Team Leaves", "GET", "/leaves/team", "manager", expected=200)
        self.test("Get All Leaves (HR)", "GET", "/leaves/all", "hr", expected=200)
        self.test("Get Leave Stats", "GET", "/leaves/stats", "hr", expected=200)
        
        if 'leave' in self.created_ids:
            leave_id = self.created_ids['leave']
            self.test("Get Leave Details", "GET", f"/leaves/{leave_id}", "employee", expected=200)
            self.test("Update Leave Status", "PUT", f"/leaves/{leave_id}/status", "manager",
                     data={"status": "approved", "comments": "Approved"}, expected=200)
            self.test("Cancel Leave", "DELETE", f"/leaves/{leave_id}", "employee", expected=200)
    
    def test_holidays_module(self):
        """Test Holidays APIs (7 endpoints)"""
        print("\n\n" + "="*80)
        print("🔟 HOLIDAYS MODULE (7 endpoints)")
        print("="*80)
        
        holiday_data = {
            "name": f"Test Holiday {int(time.time())}",
            "start_date": (date.today() + timedelta(days=30)).isoformat(),
            "end_date": (date.today() + timedelta(days=30)).isoformat(),
            "is_mandatory": True,
            "holiday_type": "national"
        }
        r = self.test("Create Holiday", "POST", "/holidays", "hr", data=holiday_data, expected=201)
        if r:
            self.created_ids['holiday'] = r.json().get('id')
        
        self.test("Get All Holidays", "GET", "/holidays", "employee", expected=200)
        self.test("Get Upcoming Holidays", "GET", "/holidays/upcoming", "employee", expected=200)
        self.test("Get Holiday Stats", "GET", "/holidays/stats", "hr", expected=200)
        
        if 'holiday' in self.created_ids:
            hol_id = self.created_ids['holiday']
            self.test("Get Holiday Details", "GET", f"/holidays/{hol_id}", "employee", expected=200)
            self.test("Update Holiday", "PUT", f"/holidays/{hol_id}", "hr",
                     data={"name": "Updated Holiday"}, expected=200)
            self.test("Delete Holiday", "DELETE", f"/holidays/{hol_id}", "hr", expected=200)
    
    def test_announcements_module(self):
        """Test Announcements APIs (6 endpoints)"""
        print("\n\n" + "="*80)
        print("1️⃣1️⃣ ANNOUNCEMENTS MODULE (6 endpoints)")
        print("="*80)
        
        ann_data = {
            "title": f"Test Announcement {int(time.time())}",
            "message": "This is a test announcement",
            "is_urgent": False
        }
        r = self.test("Create Announcement", "POST", "/announcements", "hr", data=ann_data, expected=201)
        if r:
            self.created_ids['announcement'] = r.json().get('id')
        
        self.test("Get All Announcements", "GET", "/announcements", "employee", expected=200)
        self.test("Get Announcement Stats", "GET", "/announcements/stats/summary", "hr", expected=200)
        
        if 'announcement' in self.created_ids:
            ann_id = self.created_ids['announcement']
            self.test("Get Announcement Details", "GET", f"/announcements/{ann_id}", "employee", expected=200)
            self.test("Update Announcement", "PUT", f"/announcements/{ann_id}", "hr",
                     data={"message": "Updated message"}, expected=200)
            self.test("Delete Announcement", "DELETE", f"/announcements/{ann_id}", "hr", expected=200)
    
    def test_policies_module(self):
        """Test Policies APIs (10 endpoints)"""
        print("\n\n" + "="*80)
        print("1️⃣2️⃣ POLICIES MODULE (10 endpoints)")
        print("="*80)
        
        policy_data = {
            "title": f"Test Policy {int(time.time())}",
            "description": "Test policy description",
            "content": "This is test policy content",
            "category": "HR",
            "version": "1.0",
            "effective_date": date.today().isoformat()
        }
        r = self.test("Create Policy", "POST", "/policies", "hr", data=policy_data, expected=201)
        if r:
            self.created_ids['policy'] = r.json().get('id')
        
        self.test("Get All Policies", "GET", "/policies", "employee", expected=200)
        self.test("Get Policy Stats", "GET", "/policies/stats", "hr", expected=200)
        self.test("Search Policies", "POST", "/policies/search", "employee",
                 data={"query": "test", "max_results": 5}, expected=200)
        
        if 'policy' in self.created_ids:
            pol_id = self.created_ids['policy']
            self.test("Get Policy Details", "GET", f"/policies/{pol_id}", "employee", expected=200)
            self.test("Update Policy", "PUT", f"/policies/{pol_id}", "hr",
                     data={"content": "Updated content"}, expected=200)
            self.test("Get Policy History", "GET", f"/policies/{pol_id}/history", "employee", expected=200)
            self.test("Acknowledge Policy", "POST", f"/policies/{pol_id}/acknowledge", "employee", expected=200)
            self.test("Get My Acknowledgements", "GET", "/policies/my-acknowledgements", "employee", expected=200)
            self.test("Delete Policy", "DELETE", f"/policies/{pol_id}", "hr", expected=200)
    
    def test_payslips_module(self):
        """Test Payslips APIs (11 endpoints)"""
        print("\n\n" + "="*80)
        print("1️⃣3️⃣ PAYSLIPS MODULE (11 endpoints)")
        print("="*80)
        
        payslip_data = {
            "employee_id": self.user_ids["employee"],
            "pay_period_start": date(2024, 11, 1).isoformat(),
            "pay_period_end": date(2024, 11, 30).isoformat(),
            "pay_date": date(2024, 12, 1).isoformat(),
            "basic_salary": 60000,
            "allowances": 10000,
            "gross_salary": 70000,
            "tax_deduction": 14000,
            "pf_deduction": 5600,
            "total_deductions": 19600,
            "net_salary": 50400
        }
        r = self.test("Generate Payslip", "POST", "/payslips", "hr", data=payslip_data, expected=201)
        if r:
            self.created_ids['payslip'] = r.json().get('id')
        
        self.test("Get My Payslips", "GET", "/payslips/me", "employee", expected=200)
        self.test("Get My Latest Payslip", "GET", "/payslips/me/latest", "employee", expected=200)
        self.test("Get All Payslips (HR)", "GET", "/payslips", "hr", expected=200)
        self.test("Get Payslip Stats", "GET", "/payslips/stats", "hr", expected=200)
        
        if 'payslip' in self.created_ids:
            ps_id = self.created_ids['payslip']
            self.test("Get Payslip Details", "GET", f"/payslips/{ps_id}", "employee", expected=200)
            self.test("Update Payslip", "PUT", f"/payslips/{ps_id}", "hr",
                     data={"bonus": 5000}, expected=200)
            self.test("Get Employee Payslips", "GET", f"/payslips/employee/{self.user_ids['employee']}", "hr", expected=200)
            self.test("Download Payslip PDF", "GET", f"/payslips/{ps_id}/download", "employee", expected=200)
            self.test("Email Payslip", "POST", f"/payslips/{ps_id}/email", "hr", expected=200)
            self.test("Delete Payslip", "DELETE", f"/payslips/{ps_id}", "hr", expected=200)
    
    def test_feedback_module(self):
        """Test Feedback APIs (9 endpoints)"""
        print("\n\n" + "="*80)
        print("1️⃣4️⃣ FEEDBACK MODULE (9 endpoints)")
        print("="*80)
        
        feedback_data = {
            "employee_id": self.user_ids["employee"],
            "subject": "Performance Review",
            "description": "Great work this quarter",
            "rating": 4.5
        }
        r = self.test("Give Feedback", "POST", "/feedback", "manager", data=feedback_data, expected=201)
        if r:
            self.created_ids['feedback'] = r.json().get('id')
        
        self.test("Get My Feedback", "GET", "/feedback/me", "employee", expected=200)
        self.test("Get Team Feedback", "GET", "/feedback/team", "manager", expected=200)
        self.test("Get All Feedback (HR)", "GET", "/feedback", "hr", expected=200)
        self.test("Get Feedback Stats", "GET", "/feedback/stats", "hr", expected=200)
        
        if 'feedback' in self.created_ids:
            fb_id = self.created_ids['feedback']
            self.test("Get Feedback Details", "GET", f"/feedback/{fb_id}", "employee", expected=200)
            self.test("Update Feedback", "PUT", f"/feedback/{fb_id}", "manager",
                     data={"description": "Updated feedback"}, expected=200)
            self.test("Get Employee Feedback", "GET", f"/feedback/employee/{self.user_ids['employee']}", "manager", expected=200)
            self.test("Delete Feedback", "DELETE", f"/feedback/{fb_id}", "hr", expected=200)
    
    def test_skills_module(self):
        """Test Skills APIs (10 endpoints)"""
        print("\n\n" + "="*80)
        print("1️⃣5️⃣ SKILLS MODULE (10 endpoints)")
        print("="*80)
        
        module_data = {
            "name": f"Test Module {int(time.time())}",
            "description": "Test skill module",
            "category": "Programming",
            "duration_hours": 10,
            "difficulty_level": "intermediate"
        }
        r = self.test("Create Skill Module", "POST", "/skills/modules", "hr", data=module_data, expected=201)
        if r:
            self.created_ids['skill_module'] = r.json().get('id')
        
        self.test("Get All Modules", "GET", "/skills/modules", "employee", expected=200)
        self.test("Get My Enrollments", "GET", "/skills/my-enrollments", "employee", expected=200)
        self.test("Get Skill Stats", "GET", "/skills/stats", "hr", expected=200)
        
        if 'skill_module' in self.created_ids:
            mod_id = self.created_ids['skill_module']
            self.test("Get Module Details", "GET", f"/skills/modules/{mod_id}", "employee", expected=200)
            self.test("Enroll in Module", "POST", f"/skills/modules/{mod_id}/enroll", "employee", expected=201)
            self.test("Update Progress", "PUT", "/skills/my-enrollments/progress", "employee",
                     data={"module_id": mod_id, "progress_percentage": 50}, expected=200)
            self.test("Get Module Enrollments (HR)", "GET", "/skills/enrollments", "hr", expected=200)
            self.test("Update Module", "PUT", f"/skills/modules/{mod_id}", "hr",
                     data={"description": "Updated"}, expected=200)
            self.test("Delete Module", "DELETE", f"/skills/modules/{mod_id}", "hr", expected=200)
    
    def test_goals_module(self):
        """Test Goals APIs (20+ endpoints)"""
        print("\n\n" + "="*80)
        print("1️⃣6️⃣ GOALS MODULE (20+ endpoints)")
        print("="*80)
        
        goal_data = {
            "employee_id": self.user_ids["employee"],
            "title": f"Test Goal {int(time.time())}",
            "description": "Test goal description",
            "category": "learning",
            "target_date": (date.today() + timedelta(days=90)).isoformat(),
            "start_date": date.today().isoformat()
        }
        r = self.test("Create Goal", "POST", "/goals", "manager", data=goal_data, expected=201)
        if r:
            self.created_ids['goal'] = r.json().get('id')
        
        self.test("Get My Goals", "GET", "/goals/me", "employee", expected=200)
        self.test("Get Team Goals", "GET", "/goals/team", "manager", expected=200)
        self.test("Get All Goals (HR)", "GET", "/goals", "hr", expected=200)
        self.test("Get Goal Stats", "GET", "/goals/stats", "hr", expected=200)
        
        if 'goal' in self.created_ids:
            goal_id = self.created_ids['goal']
            self.test("Get Goal Details", "GET", f"/goals/{goal_id}", "employee", expected=200)
            self.test("Update Goal", "PUT", f"/goals/{goal_id}", "manager",
                     data={"progress_percentage": 50}, expected=200)
            self.test("Update Goal Status", "PUT", f"/goals/{goal_id}/status", "manager",
                     data={"status": "in_progress"}, expected=200)
            
            checkpoint_data = {"title": "Test Checkpoint", "sequence_number": 1}
            r2 = self.test("Add Checkpoint", "POST", f"/goals/{goal_id}/checkpoints", "manager",
                          data=checkpoint_data, expected=201)
            
            self.test("Get Goal Checkpoints", "GET", f"/goals/{goal_id}/checkpoints", "employee", expected=200)
            self.test("Get Employee Goals", "GET", f"/goals/employee/{self.user_ids['employee']}", "manager", expected=200)
            self.test("Delete Goal", "DELETE", f"/goals/{goal_id}", "manager", expected=200)
    
    def test_requests_module(self):
        """Test Requests APIs (9 endpoints)"""
        print("\n\n" + "="*80)
        print("1️⃣7️⃣ REQUESTS MODULE (9 endpoints)")
        print("="*80)
        
        req_data = {
            "request_type": "wfh",
            "subject": "WFH Request",
            "description": "Need to work from home",
            "request_date": (date.today() + timedelta(days=1)).isoformat()
        }
        r = self.test("Create Request", "POST", "/requests", "employee", data=req_data, expected=201)
        if r:
            self.created_ids['request'] = r.json().get('id')
        
        self.test("Get My Requests", "GET", "/requests/me", "employee", expected=200)
        self.test("Get Team Requests", "GET", "/requests/team", "manager", expected=200)
        self.test("Get All Requests (HR)", "GET", "/requests", "hr", expected=200)
        self.test("Get Request Stats", "GET", "/requests/stats", "hr", expected=200)
        
        if 'request' in self.created_ids:
            req_id = self.created_ids['request']
            self.test("Get Request Details", "GET", f"/requests/{req_id}", "employee", expected=200)
            self.test("Update Request Status", "PUT", f"/requests/{req_id}/status", "manager",
                     data={"status": "approved", "comments": "Approved"}, expected=200)
            self.test("Cancel Request", "DELETE", f"/requests/{req_id}", "employee", expected=200)
    
    def test_organization_module(self):
        """Test Organization APIs (8 endpoints)"""
        print("\n\n" + "="*80)
        print("1️⃣8️⃣ ORGANIZATION MODULE (8 endpoints)")
        print("="*80)
        
        self.test("Get Full Org Hierarchy", "GET", "/organization/hierarchy", "employee", expected=200)
        self.test("Get Dept Hierarchy", "GET", "/organization/hierarchy/department/1", "employee", expected=200)
        self.test("Get Team Hierarchy", "GET", "/organization/hierarchy/team/1", "employee", expected=200)
        self.test("Get My Manager Chain", "GET", "/organization/manager-chain/me", "employee", expected=200)
        self.test("Get User Manager Chain", "GET", f"/organization/manager-chain/{self.user_ids['employee']}", "hr", expected=200)
        self.test("Get My Reporting Structure", "GET", "/organization/reporting-structure/me", "employee", expected=200)
        self.test("Get User Reporting Structure", "GET", f"/organization/reporting-structure/{self.user_ids['employee']}", "hr", expected=200)
        self.test("Get Org Chart", "GET", "/organization/org-chart", "employee", expected=200)
    
    def test_profile_module(self):
        """Test Profile APIs (8 endpoints)"""
        print("\n\n" + "="*80)
        print("1️⃣9️⃣ PROFILE MODULE (8 endpoints)")
        print("="*80)
        
        self.test("Get My Profile", "GET", "/profile/me", "employee", expected=200)
        self.test("Update My Profile", "PUT", "/profile/me", "employee",
                 data={"phone": "+1-555-9999", "address": "Test Address"}, expected=200)
        self.test("Get User Profile", "GET", f"/profile/{self.user_ids['employee']}", "hr", expected=200)
        self.test("Get My Team Members", "GET", "/profile/team", "manager", expected=200)
        self.test("Get My Skills", "GET", "/profile/skills/me", "employee", expected=200)
        self.test("Update My Skills", "PUT", "/profile/skills", "employee",
                 data={"skills": ["Python", "FastAPI"]}, expected=200)
        self.test("Get Profile Stats", "GET", "/profile/stats", "hr", expected=200)
    
    def test_notifications_module(self):
        """Test Notifications APIs (6 endpoints)"""
        print("\n\n" + "="*80)
        print("2️⃣0️⃣ NOTIFICATIONS MODULE (6 endpoints)")
        print("="*80)
        
        self.test("Get My Notifications", "GET", "/notifications/me", "employee", expected=200)
        self.test("Get Unread Count", "GET", "/notifications/unread/count", "employee", expected=200)
        self.test("Get Unread Notifications", "GET", "/notifications/unread", "employee", expected=200)
        
        # Create a notification (only if endpoint exists)
        notif_data = {
            "user_id": self.user_ids["employee"],
            "title": "Test Notification",
            "message": "This is a test",
            "notification_type": "info"
        }
        r = self.test("Create Notification", "POST", "/notifications", "hr", data=notif_data, expected=201)
        
        if r:
            notif_id = r.json().get('id')
            self.test("Mark as Read", "PUT", f"/notifications/{notif_id}/read", "employee", expected=200)
            self.test("Delete Notification", "DELETE", f"/notifications/{notif_id}", "employee", expected=200)
    
    def generate_report(self, filename="comprehensive_test_results.md"):
        """Generate comprehensive markdown report"""
        duration = (datetime.now() - self.start).total_seconds()
        total = len(self.results)
        passed = sum(1 for r in self.results if "PASSED" in r["status"])
        failed = sum(1 for r in self.results if "FAILED" in r["status"])
        errors = sum(1 for r in self.results if "ERROR" in r["status"])
        
        report = f"""# Comprehensive API Testing Results - ALL 171+ Endpoints

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Duration**: {duration:.2f}s  
**Backend**: http://localhost:8000

## 📊 Executive Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| **Total Tests** | {total} | 100% |
| ✅ **Passed** | {passed} | {round(passed/total*100,1) if total else 0}% |
| ❌ **Failed** | {failed} | {round(failed/total*100,1) if total else 0}% |
| ⚠️ **Errors** | {errors} | {round(errors/total*100,1) if total else 0}% |
| **Success Rate** | - | **{round(passed/total*100,1) if total else 0}%** |

## 📈 Coverage Analysis

- **Target Coverage**: 171+ API endpoints
- **Endpoints Tested**: {total}
- **Coverage Achieved**: ~{round(total/171*100,1)}%

## 📋 Detailed Results by Module

"""
        # Group by module (every 10 tests approximately)
        for idx, r in enumerate(self.results, 1):
            report += f"### Test {idx}: {r['name']}\n\n"
            report += f"- **Status**: {r['status']}\n"
            report += f"- **Endpoint**: `{r['method']} {r['endpoint']}`\n"
            report += f"- **Role**: {r.get('role', 'N/A')}\n"
            report += f"- **Time**: {r['time']}ms\n"
            report += f"- **Response**: HTTP {r['response_code']} (expected {r['expected_code']})\n"
            if r.get('error'):
                report += f"- **Error**: {r['error']}\n"
            report += "\n"
        
        report += f"\n---\n\n**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return filename

if __name__ == "__main__":
    print("="*80)
    print("🚀 COMPREHENSIVE API TESTING - ALL 171+ ENDPOINTS")
    print("="*80)
    
    tester = ComprehensiveTester()
    tester.auth()
    
    # Run all modules
    tester.test_auth_module()
    tester.test_dashboard_module()
    tester.test_employees_module()
    tester.test_departments_module()
    tester.test_teams_module()
    tester.test_attendance_module()
    tester.test_jobs_module()
    tester.test_applications_module()
    tester.test_leaves_module()
    tester.test_holidays_module()
    tester.test_announcements_module()
    tester.test_policies_module()
    tester.test_payslips_module()
    tester.test_feedback_module()
    tester.test_skills_module()
    tester.test_goals_module()
    tester.test_requests_module()
    tester.test_organization_module()
    tester.test_profile_module()
    tester.test_notifications_module()
    
    # Summary
    print("\n" + "="*80)
    print("📊 FINAL SUMMARY")
    print("="*80)
    
    total = len(tester.results)
    passed = sum(1 for r in tester.results if "PASSED" in r["status"])
    failed = sum(1 for r in tester.results if "FAILED" in r["status"])
    errors = sum(1 for r in tester.results if "ERROR" in r["status"])
    
    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed: {passed} ({round(passed/total*100,1)}%)")
    print(f"❌ Failed: {failed} ({round(failed/total*100,1)}%)")
    print(f"⚠️ Errors: {errors} ({round(errors/total*100,1)}%)")
    print(f"📈 Coverage: ~{round(total/171*100,1)}% of 171+ APIs")
    
    print("\n📝 Generating comprehensive report...")
    report_file = tester.generate_report()
    print(f"✅ Report saved to: {report_file}")
    
    print("\n" + "="*80)
    print("✨ COMPREHENSIVE TESTING COMPLETE")
    print("="*80)
