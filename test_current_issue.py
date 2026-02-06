#!/usr/bin/env python3
import requests
import json
import time

# Wait a moment for servers to be ready
time.sleep(2)

print("=" * 60)
print("TESTING BACKEND CHAT API")
print("=" * 60)

url = 'http://localhost:8000/chat/process_public'
test_cases = [
    {'message': 'add buy milk'},
    {'message': 'show my tasks'},
    {'message': 'delete buy milk'},
    {'message': 'hi'},
]

for test_payload in test_cases:
    print(f"\n📤 Sending: {json.dumps(test_payload)}")
    try:
        response = requests.post(url, json=test_payload, timeout=5)
        print(f"✓ Status: {response.status_code}")
        result = response.json()
        print(f"📥 Response:")
        print(f"   reply: {result.get('reply', 'N/A')}")
        print(f"   action_performed: {result.get('action_performed', 'N/A')}")
        print(f"   success: {result.get('success', 'N/A')}")
    except Exception as e:
        print(f"✗ Error: {e}")

print("\n" + "=" * 60)
