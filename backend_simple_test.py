import requests
import json

# Test the simple /chat/ endpoint
BASE_URL = "http://localhost:8000"

# Test data - similar to what might be sent to the simple endpoint
test_payload = {
    "message": "Add buy groceries",
    "current_tasks": []
}

headers = {
    "Content-Type": "application/json"
    # No Authorization header, as this might be how it's being called
}

print("Testing /chat/ endpoint (simple endpoint)...")

try:
    response = requests.post(f"{BASE_URL}/chat/", 
                           data=json.dumps(test_payload), 
                           headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test with a greeting
test_payload_greeting = {
    "message": "Hi",
    "current_tasks": []
}

print("\nTesting /chat/ endpoint with greeting...")
try:
    response = requests.post(f"{BASE_URL}/chat/", 
                           data=json.dumps(test_payload_greeting), 
                           headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")