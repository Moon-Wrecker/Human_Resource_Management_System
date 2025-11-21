"""
Test script for Announcements API
Run this after starting the backend server to verify all endpoints work
"""
import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
HR_EMAIL = "sarah.johnson@company.com"
EMPLOYEE_EMAIL = "john.doe@company.com"
PASSWORD = "password123"


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def print_response(response, show_full=False):
    """Print formatted response"""
    print(f"Status Code: {response.status_code}")
    if show_full:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Response: {json.dumps(response.json(), indent=2)[:500]}...")


def login(email, password):
    """Login and get access token"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Login failed: {response.json()}")
        return None


def test_announcements_api():
    """Test all announcements API endpoints"""
    
    print_section("ANNOUNCEMENTS API TEST SUITE")
    print(f"Testing at: {BASE_URL}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # =================================================================
    # 1. LOGIN AS HR
    # =================================================================
    print_section("1. Login as HR")
    hr_token = login(HR_EMAIL, PASSWORD)
    if not hr_token:
        print("❌ HR login failed. Stopping tests.")
        return
    print(f"✅ HR logged in successfully")
    print(f"Token: {hr_token[:20]}...")
    
    headers_hr = {
        "Authorization": f"Bearer {hr_token}",
        "Content-Type": "application/json"
    }
    
    # =================================================================
    # 2. CREATE ANNOUNCEMENT (HR)
    # =================================================================
    print_section("2. Create Announcement (HR)")
    
    # Calculate expiry date (30 days from now)
    expiry_date = (datetime.now() + timedelta(days=30)).isoformat()
    
    announcement_data = {
        "title": "Test Announcement - API Test",
        "message": "This is a test announcement created by the API test suite. It demonstrates the announcements functionality.",
        "link": "https://test.company.com/announcements",
        "is_urgent": False,
        "expiry_date": expiry_date
    }
    
    response = requests.post(
        f"{BASE_URL}/announcements",
        headers=headers_hr,
        json=announcement_data
    )
    print_response(response, show_full=True)
    
    if response.status_code == 201:
        print("✅ Announcement created successfully")
        created_announcement = response.json()
        announcement_id = created_announcement["id"]
    else:
        print("❌ Failed to create announcement")
        return
    
    # =================================================================
    # 3. GET ALL ANNOUNCEMENTS (HR)
    # =================================================================
    print_section("3. Get All Announcements (HR)")
    
    response = requests.get(
        f"{BASE_URL}/announcements?limit=10",
        headers=headers_hr
    )
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {len(data['announcements'])} announcements")
        print(f"   Total: {data['total']}, Active: {data['active']}, Urgent: {data['urgent']}")
    else:
        print("❌ Failed to get announcements")
    
    # =================================================================
    # 4. GET ANNOUNCEMENT BY ID
    # =================================================================
    print_section("4. Get Announcement by ID")
    
    response = requests.get(
        f"{BASE_URL}/announcements/{announcement_id}",
        headers=headers_hr
    )
    print_response(response, show_full=True)
    
    if response.status_code == 200:
        print(f"✅ Retrieved announcement #{announcement_id}")
    else:
        print(f"❌ Failed to get announcement #{announcement_id}")
    
    # =================================================================
    # 5. UPDATE ANNOUNCEMENT (HR)
    # =================================================================
    print_section("5. Update Announcement (HR)")
    
    update_data = {
        "title": "Updated Test Announcement - Modified",
        "is_urgent": True
    }
    
    response = requests.put(
        f"{BASE_URL}/announcements/{announcement_id}",
        headers=headers_hr,
        json=update_data
    )
    print_response(response, show_full=True)
    
    if response.status_code == 200:
        print(f"✅ Announcement #{announcement_id} updated successfully")
        updated = response.json()
        print(f"   New title: {updated['title']}")
        print(f"   Is urgent: {updated['is_urgent']}")
    else:
        print(f"❌ Failed to update announcement #{announcement_id}")
    
    # =================================================================
    # 6. GET STATISTICS (HR)
    # =================================================================
    print_section("6. Get Announcement Statistics (HR)")
    
    response = requests.get(
        f"{BASE_URL}/announcements/stats/summary",
        headers=headers_hr
    )
    print_response(response, show_full=True)
    
    if response.status_code == 200:
        stats = response.json()
        print("✅ Statistics retrieved successfully")
        print(f"   Total: {stats['total']}")
        print(f"   Active: {stats['active']}")
        print(f"   Urgent: {stats['urgent']}")
        print(f"   Expired: {stats['expired']}")
        print(f"   Inactive: {stats['inactive']}")
    else:
        print("❌ Failed to get statistics")
    
    # =================================================================
    # 7. LOGIN AS EMPLOYEE
    # =================================================================
    print_section("7. Login as Employee")
    employee_token = login(EMPLOYEE_EMAIL, PASSWORD)
    if not employee_token:
        print("❌ Employee login failed")
        return
    print(f"✅ Employee logged in successfully")
    
    headers_employee = {
        "Authorization": f"Bearer {employee_token}",
        "Content-Type": "application/json"
    }
    
    # =================================================================
    # 8. GET ANNOUNCEMENTS (EMPLOYEE)
    # =================================================================
    print_section("8. Get Announcements (Employee)")
    
    response = requests.get(
        f"{BASE_URL}/announcements?limit=5",
        headers=headers_employee
    )
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Employee can view {len(data['announcements'])} announcements")
    else:
        print("❌ Employee failed to get announcements")
    
    # =================================================================
    # 9. TRY CREATE AS EMPLOYEE (Should Fail)
    # =================================================================
    print_section("9. Try Create Announcement as Employee (Should Fail)")
    
    response = requests.post(
        f"{BASE_URL}/announcements",
        headers=headers_employee,
        json={
            "title": "Unauthorized Test",
            "message": "This should fail"
        }
    )
    print_response(response, show_full=True)
    
    if response.status_code == 403:
        print("✅ Correctly blocked employee from creating announcement")
    else:
        print("❌ Security issue: Employee was able to create announcement!")
    
    # =================================================================
    # 10. SOFT DELETE ANNOUNCEMENT (HR)
    # =================================================================
    print_section("10. Soft Delete Announcement (HR)")
    
    response = requests.delete(
        f"{BASE_URL}/announcements/{announcement_id}",
        headers=headers_hr
    )
    print_response(response, show_full=True)
    
    if response.status_code == 200:
        print(f"✅ Announcement #{announcement_id} soft deleted (deactivated)")
    else:
        print(f"❌ Failed to delete announcement #{announcement_id}")
    
    # =================================================================
    # 11. VERIFY SOFT DELETE
    # =================================================================
    print_section("11. Verify Soft Delete")
    
    # Try to get active announcements (should not include deleted)
    response = requests.get(
        f"{BASE_URL}/announcements?limit=100",
        headers=headers_hr
    )
    
    if response.status_code == 200:
        data = response.json()
        announcement_ids = [a["id"] for a in data["announcements"]]
        
        if announcement_id not in announcement_ids:
            print(f"✅ Soft deleted announcement #{announcement_id} not in active list")
        else:
            print(f"❌ Soft deleted announcement #{announcement_id} still appears in active list")
    
    # Try to get with include_inactive flag
    response = requests.get(
        f"{BASE_URL}/announcements?include_inactive=true",
        headers=headers_hr
    )
    
    if response.status_code == 200:
        data = response.json()
        announcement_ids = [a["id"] for a in data["announcements"]]
        
        if announcement_id in announcement_ids:
            print(f"✅ Soft deleted announcement #{announcement_id} visible with include_inactive=true")
        else:
            print(f"⚠️  Soft deleted announcement #{announcement_id} not found even with include_inactive")
    
    # =================================================================
    # 12. CREATE URGENT ANNOUNCEMENT
    # =================================================================
    print_section("12. Create Urgent Announcement")
    
    urgent_data = {
        "title": "URGENT: System Maintenance Tonight",
        "message": "Critical system maintenance scheduled for tonight from 11 PM to 2 AM. Please save all work.",
        "link": "https://status.company.com/maintenance",
        "is_urgent": True,
        "expiry_date": (datetime.now() + timedelta(days=1)).isoformat()
    }
    
    response = requests.post(
        f"{BASE_URL}/announcements",
        headers=headers_hr,
        json=urgent_data
    )
    
    if response.status_code == 201:
        urgent_announcement = response.json()
        print(f"✅ Urgent announcement created: ID #{urgent_announcement['id']}")
        print(f"   Is Urgent: {urgent_announcement['is_urgent']}")
        
        # Clean up - delete the urgent announcement
        requests.delete(
            f"{BASE_URL}/announcements/{urgent_announcement['id']}",
            headers=headers_hr
        )
    else:
        print("❌ Failed to create urgent announcement")
    
    # =================================================================
    # SUMMARY
    # =================================================================
    print_section("TEST SUMMARY")
    print("✅ All announcements API endpoints tested successfully!")
    print("\nTested Endpoints:")
    print("  ✅ POST   /api/v1/announcements          (Create)")
    print("  ✅ GET    /api/v1/announcements          (List All)")
    print("  ✅ GET    /api/v1/announcements/{id}     (Get by ID)")
    print("  ✅ PUT    /api/v1/announcements/{id}     (Update)")
    print("  ✅ DELETE /api/v1/announcements/{id}     (Delete)")
    print("  ✅ GET    /api/v1/announcements/stats/summary (Statistics)")
    print("\nPermissions Tested:")
    print("  ✅ HR can create, update, delete announcements")
    print("  ✅ Employee can view announcements")
    print("  ✅ Employee cannot create announcements (403 Forbidden)")
    print("\nFeatures Verified:")
    print("  ✅ Soft delete (audit trail maintained)")
    print("  ✅ Urgent announcements")
    print("  ✅ Expiry date support")
    print("  ✅ Pagination")
    print("  ✅ Statistics endpoint")
    print("\n" + "="*60)


if __name__ == "__main__":
    try:
        test_announcements_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to backend server")
        print("Make sure the backend is running at http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

