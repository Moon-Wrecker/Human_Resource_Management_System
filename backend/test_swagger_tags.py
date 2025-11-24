"""
Test script to verify all router tags match openapi_tags in main.py
Run this to check for any tag mismatches that would break Swagger UI
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

def check_tags():
    """Check if all router tags match openapi_tags in main.py"""
    
    print("=" * 70)
    print("SWAGGER TAGS VALIDATION")
    print("=" * 70)
    print()
    
    # Expected tags from main.py openapi_tags
    expected_tags = {
        "Root",
        "Health",
        "API",
        "Authentication",
        "Dashboard",
        "Employee Management",
        "Profile",
        "Attendance",
        "Leave Management",
        "Job Listings",
        "Applications",
        "Feedback",
        "Payslips",
        "Goals & Task Management",
        "Skills/Modules Management",
        "Policies",
        "Announcements",
        "Holidays",
        "Departments",
        "Organization/Hierarchy",
        "Team Requests",
        "AI - Policy RAG",
        "AI - Resume Screener",
        "AI - Job Description Generator",
        "AI Performance Reports"
    }
    
    # Try to import all routers and check their tags
    router_tags = {}
    errors = []
    
    router_imports = [
        ("routes.auth", "auth_router", "Authentication"),
        ("routes.dashboard", "dashboard_router", "Dashboard"),
        ("routes.profile", "profile_router", "Profile"),
        ("routes.attendance", "attendance_router", "Attendance"),
        ("routes.jobs", "jobs_router", "Job Listings"),
        ("routes.applications", "applications_router", "Applications"),
        ("routes.announcements", "announcements_router", "Announcements"),
        ("routes.policies", "policies_router", "Policies"),
        ("routes.feedback", "feedback_router", "Feedback"),
        ("routes.payslips", "payslips_router", "Payslips"),
        ("routes.holidays", "holidays_router", "Holidays"),
        ("routes.departments", "departments_router", "Departments"),
        ("routes.organization", "organization_router", "Organization/Hierarchy"),
        ("routes.employees", "employees_router", "Employee Management"),
        ("routes.leaves", "leaves_router", "Leave Management"),
        ("routes.skills", "skills_router", "Skills/Modules Management"),
        ("routes.requests", "requests_router", "Team Requests"),
        ("routes.goals", "goals_router", "Goals & Task Management"),
    ]
    
    print("📋 Checking Standard Routes:")
    print("-" * 70)
    
    for module_name, router_name, expected_tag in router_imports:
        try:
            module = __import__(module_name, fromlist=[router_name])
            router = getattr(module, "router")
            actual_tags = router.tags if hasattr(router, 'tags') else []
            
            if actual_tags:
                actual_tag = actual_tags[0]
                router_tags[module_name] = actual_tag
                
                if actual_tag == expected_tag:
                    print(f"✅ {module_name:<30} → {actual_tag}")
                else:
                    print(f"❌ {module_name:<30} → {actual_tag} (Expected: {expected_tag})")
                    errors.append(f"{module_name}: Tag mismatch - '{actual_tag}' vs '{expected_tag}'")
            else:
                print(f"⚠️  {module_name:<30} → No tags found")
                errors.append(f"{module_name}: No tags defined")
                
        except ImportError as e:
            print(f"❌ {module_name:<30} → Import Error: {str(e)}")
            errors.append(f"{module_name}: Import failed - {str(e)}")
        except Exception as e:
            print(f"❌ {module_name:<30} → Error: {str(e)}")
            errors.append(f"{module_name}: Error - {str(e)}")
    
    print()
    print("🤖 Checking AI Routes:")
    print("-" * 70)
    
    ai_router_imports = [
        ("routes.ai_policy_rag", "ai_policy_rag_router", "AI - Policy RAG"),
        ("routes.ai_resume_screener", "ai_resume_screener_router", "AI - Resume Screener"),
        ("routes.ai_job_description", "ai_job_description_router", "AI - Job Description Generator"),
        ("routes.ai_performance_report", "ai_performance_report_router", "AI Performance Reports"),
    ]
    
    for module_name, router_name, expected_tag in ai_router_imports:
        try:
            module = __import__(module_name, fromlist=[router_name])
            router = getattr(module, "router")
            actual_tags = router.tags if hasattr(router, 'tags') else []
            
            if actual_tags:
                actual_tag = actual_tags[0]
                router_tags[module_name] = actual_tag
                
                if actual_tag == expected_tag:
                    print(f"✅ {module_name:<30} → {actual_tag}")
                else:
                    print(f"❌ {module_name:<30} → {actual_tag} (Expected: {expected_tag})")
                    errors.append(f"{module_name}: Tag mismatch - '{actual_tag}' vs '{expected_tag}'")
            else:
                print(f"⚠️  {module_name:<30} → No tags found")
                errors.append(f"{module_name}: No tags defined")
                
        except ImportError as e:
            print(f"⚠️  {module_name:<30} → Not available (AI dependencies not installed)")
        except Exception as e:
            print(f"❌ {module_name:<30} → Error: {str(e)}")
            errors.append(f"{module_name}: Error - {str(e)}")
    
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    
    if errors:
        print(f"❌ Found {len(errors)} issue(s):")
        print()
        for error in errors:
            print(f"  • {error}")
        print()
        print("🔧 Fix these issues to ensure Swagger UI displays all routes correctly!")
        return False
    else:
        print("✅ All router tags match openapi_tags correctly!")
        print()
        print("All routes should now be visible in Swagger UI at:")
        print("  → http://localhost:8000/api/docs")
        return True

if __name__ == "__main__":
    success = check_tags()
    sys.exit(0 if success else 1)

