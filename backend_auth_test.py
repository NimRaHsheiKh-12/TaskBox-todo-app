import requests
import json

# Test the backend API directly with the authenticated endpoint
# but without a token to simulate what might happen on the frontend
BASE_URL = "http://localhost:8000"

# Test data - similar to what frontend sends
test_payload = {
    "user_id": "test_user_123",
    "message": "Add buy groceries",
    "current_tasks": []
}

headers = {
    "Content-Type": "application/json"
    # No Authorization header to simulate unauthenticated request
}

print("Testing /chat/process endpoint WITHOUT authentication...")

try:
    response = requests.post(f"{BASE_URL}/chat/process", 
                           data=json.dumps(test_payload), 
                           headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Also test with a simple greeting
test_payload_greeting = {
    "user_id": "test_user_123",
    "message": "Hi",
    "current_tasks": []
}

print("\nTesting /chat/process endpoint with greeting WITHOUT authentication...")
try:
    response = requests.post(f"{BASE_URL}/chat/process", 
                           data=json.dumps(test_payload_greeting), 
                           headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")