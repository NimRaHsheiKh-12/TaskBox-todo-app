#!/usr/bin/env python3
"""
Test to trace exactly where UUID is being treated as message.
Run this with the backend server running.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

test_cases = [
    ("show my tasks", "/chat/process_public"),
    ("add buy milk", "/chat/process_public"),
    ("hello", "/chat/process_public"),
]

print("\n" + "="*70)
print("TRACING UUID BUG - Testing all endpoints")
print("="*70 + "\n")

for message, endpoint in test_cases:
    url = f"{BASE_URL}{endpoint}"
    payload = {"message": message}
    
    print(f"Testing: {endpoint}")
    print(f"Message: '{message}'")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload)}")
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        print(f"Status: {response.status_code}")
        print(f"Reply: {data.get('reply', 'N/A')[:100]}...")
        print(f"Action: {data.get('action_performed', 'N/A')}")
        
        # Check if UUID appears in reply
        import re
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        if re.search(uuid_pattern, data.get('reply', '')):
            print(f"❌ UUID FOUND IN REPLY!")
        else:
            print(f"✓ No UUID in reply")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("-" * 70 + "\n")

print("Done!")
