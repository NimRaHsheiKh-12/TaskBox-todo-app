#!/usr/bin/env python3
"""
Test the authenticated /chat/process endpoint.
This tests what happens when JWT token is used.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Create a test with a fake JWT to see if it works
# For testing, we'll just test the public endpoint again but trace the flow

print("\n" + "="*70)
print("TESTING - Check if bug appears in specific scenarios")
print("="*70 + "\n")

# Test 1: Test what happens if the frontend sends userId in the request body
print("TEST 1: What if frontend sends userId in request body (malformed request)?")
url = f"{BASE_URL}/chat/process_public"
payload = {"message": "show my tasks", "user_id": "59d27b08-0e97-4481-943a-27e5d2d379d9"}
print(f"Payload: {json.dumps(payload)}")

try:
    response = requests.post(url, json=payload, timeout=5)
    data = response.json()
    print(f"Reply: {data.get('reply', 'N/A')[:120]}...")
    print(f"Action: {data.get('action_performed', 'N/A')}")
    
    if "59d27b08" in data.get('reply', ''):
        print("❌ UUID FOUND IN REPLY - This is the bug!")
    else:
        print("✓ UUID not in reply")
except Exception as e:
    print(f"Error: {str(e)}")

print("\n" + "-"*70 + "\n")

# Test 2: Check if middleware is modifying the message
print("TEST 2: Send valid message and check server output for DEBUG logs")
url = f"{BASE_URL}/chat/process_public"
payload = {"message": "test message"}
print(f"Payload: {json.dumps(payload)}")

try:
    response = requests.post(url, json=payload, timeout=5)
    data = response.json()
    print(f"Reply: {data.get('reply', 'N/A')[:120]}...")
    print(f"Action: {data.get('action_performed', 'N/A')}")
    print(f"\nCheck server logs (stderr) for DEBUG lines")
except Exception as e:
    print(f"Error: {str(e)}")

print("\nDone!")
