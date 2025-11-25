"""
Quick script to test if AI endpoints are loaded
"""
import requests
import json

try:
    response = requests.get("http://localhost:8000/api/openapi.json")
    data = response.json()
    
    paths = data.get('paths', {})
    total = len(paths)
    
    # Find AI endpoints
    ai_endpoints = [p for p in paths if '/ai/' in p]
    
    print(f"✅ Total API endpoints: {total}")
    print(f"🤖 AI endpoints: {len(ai_endpoints)}\n")
    
    if ai_endpoints:
        print("AI Endpoints Found:")
        for endpoint in sorted(ai_endpoints):
            # Get methods for this endpoint
            methods = list(paths[endpoint].keys())
            print(f"  - {endpoint:60} [{', '.join(m.upper() for m in methods if m != 'parameters')}]")
    else:
        print("❌ NO AI ENDPOINTS FOUND!")
        print("\nThis means AI routes are not being loaded.")
        print("Check:")
        print("  1. AI dependencies installed: pip install -r requirements_ai.txt")
        print("  2. Server logs for import errors")
        print("  3. main.py AI_ROUTES_AVAILABLE flag")
    
    # Check tags
    tags = data.get('tags', [])
    ai_tags = [t['name'] for t in tags if 'AI' in t['name'] or 'GenAI' in t.get('description', '')]
    print(f"\n🏷️  AI Tags: {len(ai_tags)}")
    for tag in ai_tags:
        print(f"  - {tag}")

except Exception as e:
    print(f"❌ Error: {e}")
    print("\nMake sure the server is running: python main.py")

