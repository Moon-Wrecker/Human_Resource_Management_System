"""
Simplified API Testing Suite for HRMS
Tests key endpoints and generates markdown report
"""
import requests
import time
from datetime import datetime

API_URL = "http://localhost:8000/api/v1"
CREDENTIALS = {
    "hr": {"email": "sarah.johnson@company.com", "password": "pass123"},
    "manager": {"email": "michael.chen@company.com", "password": "pass123"},
    "employee": {"email": "john.doe@company.com", "password": "pass123"}
}

class Tester:
    def __init__(self):
        self.tokens = {}
        self.results = []
        self.start = datetime.now()
    
    def test(self, name, method, endpoint, role="employee", data=None, expected=200):
        """Run a single test"""
        headers = {}
        if role and role in self.tokens:
            headers["Authorization"] = f"Bearer {self.tokens[role]}"
        
        url = f"{API_URL}{endpoint}"
        start = time.time()
        
        try:
            if method == "GET":
                r = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                r = requests.post(url, headers=headers, json=data, timeout=10)
            elif method == "PUT":
                r = requests.put(url, headers=headers, json=data, timeout=10)
            elif method == "DELETE":
                r = requests.delete(url, headers=headers, timeout=10)
            
            exec_time = round((time.time() - start) * 1000)
            status = "✅ PASSED" if r.status_code == expected else "❌ FAILED"
            error = None if r.status_code == expected else f"Expected {expected}, got {r.status_code}"
            
            self.results.append({
                "name": name,
                "method": method,
                "endpoint": endpoint,
                "status": status,
                "time": exec_time,
                "response_code": r.status_code,
                "expected_code": expected,
                "error": error
            })
            
            print(f"  {status} {name} ({exec_time}ms)")
            if error:
                print(f"      ↳ {error}")
            
            return r if r.status_code == expected else None
            
        except Exception as e:
            self.results.append({
                "name": name,
                "method": method,
                "endpoint": endpoint,
                "status": "⚠️ ERROR",
                "time": round((time.time() - start) * 1000),
                "response_code": None,
                "expected_code": expected,
                "error": str(e)
            })
            print(f"  ⚠️ ERROR {name} - {str(e)}")
            return None
    
    def auth(self):
        """Authenticate all users"""
        print("\n🔐 AUTHENTICATING...")
        for role, creds in CREDENTIALS.items():
            r = self.test(f"{role.upper()} Login", "POST", "/auth/login", role=None, data=creds, expected=200)
            if r:
                data = r.json()
                self.tokens[role] = data.get("access_token")
                print(f"    ✓ {role.upper()} authenticated")
    
    def run_tests(self):
        """Run all tests"""
        print("\n╔════════════════════════════════════════════╗")
        print("║   HRMS API TESTING SUITE                 ║")
        print("╚════════════════════════════════════════════╝\n")
        
        self.auth()
        
        # Authentication Tests
        print("\n📝 AUTHENTICATION (3 tests)")
        self.test("Get Current User", "GET", "/auth/me", "employee", expected=200)
        self.test("Invalid Login", "POST", "/auth/login", None, {"email": "bad@test.com", "password": "wrong"}, 401)
        self.test("Logout", "POST", "/auth/logout", "employee", expected=200)
        
        # Dashboard Tests
        print("\n📊 DASHBOARDS (3 tests)")
        self.test("Employee Dashboard", "GET", "/dashboard/employee", "employee", expected=200)
        self.test("Manager Dashboard", "GET", "/dashboard/manager", "manager", expected=200)
        self.test("HR Dashboard", "GET", "/dashboard/hr", "hr", expected=200)
        
        # Employee Tests
        print("\n👥 EMPLOYEES (2 tests)")
        self.test("Get All Employees", "GET", "/employees", "hr", expected=200)
        self.test("Get Employee Stats", "GET", "/employees/stats", "hr", expected=200)
        
        # Attendance Tests
        print("\n📅 ATTENDANCE (4 tests)")
        self.test("Get My Attendance", "GET", "/attendance/me", "employee", expected=200)
        self.test("Punch In", "POST", "/attendance/punch-in", "employee", expected=200)
        self.test("Punch Out", "POST", "/attendance/punch-out", "employee", expected=200)
        self.test("Get Team Attendance", "GET", "/attendance/team", "manager", expected=200)
        
        # Jobs & Applications
        print("\n💼 JOBS & APPLICATIONS (3 tests)")
        self.test("Get All Jobs", "GET", "/jobs", "employee", expected=200)
        self.test("Get Job Stats", "GET", "/jobs/statistics", "hr", expected=200)
        self.test("Get Applications", "GET", "/applications", "hr", expected=200)
        
        # Departments
        print("\n🏢 DEPARTMENTS (2 tests)")
        self.test("Get All Departments", "GET", "/departments", "employee", expected=200)
        self.test("Get Dept Stats", "GET", "/departments/stats", "hr", expected=200)
        
        # Leaves
        print("\n🏖️ LEAVES (3 tests)")
        self.test("Get My Leaves", "GET", "/leaves/me", "employee", expected=200)
        self.test("Get Team Leaves", "GET", "/leaves/team", "manager", expected=200)
        self.test("Get Leave Balance", "GET", "/leaves/balance/me", "employee", expected=200)
        
        # Holidays
        print("\n🎉 HOLIDAYS (2 tests)")
        self.test("Get All Holidays", "GET", "/holidays", "employee", expected=200)
        self.test("Get Upcoming Holidays", "GET", "/holidays/upcoming", "employee", expected=200)
        
        # Announcements
        print("\n📢 ANNOUNCEMENTS (2 tests)")
        self.test("Get All Announcements", "GET", "/announcements", "employee", expected=200)
        self.test("Get Recent Announcements", "GET", "/announcements/recent", "employee", expected=200)
        
        # Policies
        print("\n📋 POLICIES (2 tests)")
        self.test("Get All Policies", "GET", "/policies", "employee", expected=200)
        self.test("Get Policy Categories", "GET", "/policies/categories", "employee", expected=200)
        
        # Payslips
        print("\n💰 PAYSLIPS (2 tests)")
        self.test("Get My Payslips", "GET", "/payslips/me", "employee", expected=200)
        self.test("Get Latest Payslip", "GET", "/payslips/me/latest", "employee", expected=200)
        
        # Feedback
        print("\n💬 FEEDBACK (2 tests)")
        self.test("Get My Feedback", "GET", "/feedback/me", "employee", expected=200)
        self.test("Get Team Feedback", "GET", "/feedback/team", "manager", expected=200)
        
        # Organization
        print("\n🏛️ ORGANIZATION (2 tests)")
        self.test("Get Org Hierarchy", "GET", "/organization/hierarchy", "employee", expected=200)
        self.test("Get Manager Chain", "GET", "/organization/manager-chain/me", "employee", expected=200)
        
        # Skills
        print("\n📚 SKILLS (3 tests)")
        self.test("Get All Modules", "GET", "/skills/modules", "employee", expected=200)
        self.test("Get My Enrollments", "GET", "/skills/my-enrollments", "employee", expected=200)
        self.test("Get Skill Stats", "GET", "/skills/stats", "hr", expected=200)
        
        # Goals (sample tests, full suite would have 20+)
        print("\n🎯 GOALS (2 tests)")
        self.test("Get My Goals", "GET", "/goals/me", "employee", expected=200)
        self.test("Get Team Goals", "GET", "/goals/team", "manager", expected=200)
        
    def generate_report(self, filename="ultimate_testing_results.md"):
        """Generate markdown report"""
        duration = (datetime.now() - self.start).total_seconds()
        total = len(self.results)
        passed = sum(1 for r in self.results if "PASSED" in r["status"])
        failed = sum(1 for r in self.results if "FAILED" in r["status"])
        errors = sum(1 for r in self.results if "ERROR" in r["status"])
        success_rate = round(passed / total * 100, 1) if total > 0 else 0
        
        report = f"""# Ultimate API Testing Results

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Test Duration**: {duration:.2f} seconds  
**Backend**: http://localhost:8000

---

## 📊 Executive Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| **Total Tests** | {total} | 100% |
| ✅ **Passed** | {passed} | {round(passed/total*100,1) if total else 0}% |
| ❌ **Failed** | {failed} | {round(failed/total*100,1) if total else 0}% |
| ⚠️ **Errors** | {errors} | {round(errors/total*100,1) if total else 0}% |
| **Success Rate** | - | **{success_rate}%** |

### Test Coverage

- **Test Execution Time**: {duration:.2f}s
- **Average Time per Test**: {round(duration/total*1000) if total else 0}ms
- **Modules Tested**: 15 core modules
- **API Categories**: Authentication, Dashboard, Employees, Attendance, Jobs, Departments, Leaves, Holidays, Announcements, Policies, Payslips, Feedback, Organization, Skills, Goals

---

## 📋 Detailed Test Results

"""
        
        current_module = None
        test_num = 1
        
        for r in self.results:
            # Group by endpoint pattern (first part after /api/v1/)
            module = r["endpoint"].split("/")[1] if "/" in r["endpoint"] else "other"
            if module != current_module:
                current_module = module
                report += f"\n### {module.title()} Module\n\n"
            
            report += f"#### Test {test_num}: {r['name']}\n\n"
            report += f"- **Status**: {r['status']}\n"
            report += f"- **Endpoint**: `{r['method']} {r['endpoint']}`\n"
            report += f"- **Execution time**: {r['time']}ms\n"
            report += f"- **Response**: HTTP {r['response_code']} (expected {r['expected_code']})\n"
            
            if r.get("error"):
                report += f"- **Error**: {r['error']}\n"
            
            report += "\n"
            test_num += 1
        
        # Performance metrics
        report += "\n---\n\n## ⚡ Performance Metrics\n\n"
        report += f"- **Fastest Test**: {min(r['time'] for r in self.results)}ms\n"
        report += f"- **Slowest Test**: {max(r['time'] for r in self.results)}ms\n"
        report += f"- **Average Test Time**: {round(sum(r['time'] for r in self.results) / len(self.results))}ms\n\n"
        
        # Coverage report
        report += "## 📈 Coverage Report\n\n"
        report += f"- **Total API Endpoints in System**: ~171+\n"
        report += f"- **Endpoints Tested**: {total}\n"
        report += f"- **Coverage Percentage**: ~{round(total/171*100,1)}%\n\n"
        report += "### Tested Modules\n\n"
        report += "- ✅ Authentication (6 endpoints documented, 3 tested)\n"
        report += "- ✅ Dashboards (6 endpoints)\n"
        report += "- ✅ Employees (6 endpoints, 2 tested)\n"
        report += "- ✅ Attendance (9 endpoints, 4 tested)\n"
        report += "- ✅ Jobs & Applications (16 endpoints, 3 tested)\n"
        report += "- ✅ Departments (6 endpoints, 2 tested)\n"
        report += "- ✅ Leaves (9 endpoints, 3 tested)\n"
        report += "- ✅ Holidays (7 endpoints, 2 tested)\n"
        report += "- ✅ Announcements (6 endpoints, 2 tested)\n"
        report += "- ✅ Policies (10 endpoints, 2 tested)\n"
        report += "- ✅ Payslips (11 endpoints, 2 tested)\n"
        report += "- ✅ Feedback (9 endpoints, 2 tested)\n"
        report += "- ✅ Organization (8 endpoints, 2 tested)\n"
        report += "- ✅ Skills (10 endpoints, 3 tested)\n"
        report += "- ✅ Goals (20+ endpoints, 2 tested)\n\n"
        
        report += "### Notes\n\n"
        report += "- This is a simplified test suite covering core endpoints\n"
        report += "- File upload tests were skipped as per user request\n"
        report += "- Tests use existing seed data from the database\n"
        report += "- Full comprehensive testing would cover all 171+ endpoints\n\n"
        
        report += "---\n\n"
        report += f"**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n"
        report += "**Testing Framework**: Python + requests library  \n"
        report += "**Backend Server**: http://localhost:8000\n"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return filename

if __name__ == "__main__":
    tester = Tester()
    tester.run_tests()
    
    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    
    total = len(tester.results)
    passed = sum(1 for r in tester.results if "PASSED" in r["status"])
    failed = sum(1 for r in tester.results if "FAILED" in r["status"])
    errors = sum(1 for r in tester.results if "ERROR" in r["status"])
    
    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⚠️ Errors: {errors}")
    print(f"🎯 Success Rate: {round(passed/total*100,1) if total else 0}%")
    
    print("\n📝 GENERATING REPORT...")
    report_file = tester.generate_report()
    print(f"✅ Report saved to: {report_file}")
    
    print("\n" + "="*50)
    print("✨ TESTING COMPLETE")
    print("="*50)
