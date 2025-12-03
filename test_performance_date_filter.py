#!/usr/bin/env python3
"""
Test script to verify the date filter functionality for the /performance/me endpoint
"""
import requests
import json
from datetime import date, timedelta

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

def test_performance_date_filters():
    """Test the performance endpoint with date filters"""
    
    # First, let's get a token (using seeded test data)
    login_data = {
        "email": "sarah.johnson@company.com",  # HR manager credentials from seed data
        "password": "pass123"
    }
    
    print("🔐 Attempting to login...")
    try:
        login_response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return False
        
        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login successful")
        
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return False
    
    # Test 1: Default behavior (should work as before)
    print("\n📊 Test 1: Default behavior (no date filters)")
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard/performance/me", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Default request works - got {len(data.get('monthly_modules', []))} monthly records")
        else:
            print(f"❌ Default request failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Using months parameter (backward compatibility)
    print("\n📊 Test 2: Using months parameter (6 months)")
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard/performance/me?months=6", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Months parameter works - got {len(data.get('monthly_modules', []))} monthly records")
        else:
            print(f"❌ Months parameter failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: Using date range (new functionality)
    print("\n📊 Test 3: Using date range (last 30 days)")
    try:
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        response = requests.get(
            f"{API_BASE_URL}/dashboard/performance/me?start_date={start_date}&end_date={end_date}",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        print(f"Date range: {start_date} to {end_date}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Date range works - got {len(data.get('monthly_modules', []))} monthly records")
            print(f"Total modules in period: {data.get('total_modules_completed', 0)}")
            print(f"Attendance rate: {data.get('attendance_rate', 0)}%")
            print(f"Goals completion rate: {data.get('goals_completion_rate', 0)}%")
        else:
            print(f"❌ Date range failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 4: Using only start_date 
    print("\n📊 Test 4: Using only start_date (last 7 days to today)")
    try:
        start_date = date.today() - timedelta(days=7)
        
        response = requests.get(
            f"{API_BASE_URL}/dashboard/performance/me?start_date={start_date}",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        print(f"Start date: {start_date} (end_date defaults to today)")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Start date only works - got {len(data.get('monthly_modules', []))} monthly records")
        else:
            print(f"❌ Start date only failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n🎉 Performance date filter tests completed!")
    return True

if __name__ == "__main__":
    test_performance_date_filters()