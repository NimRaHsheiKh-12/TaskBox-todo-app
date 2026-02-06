import requests
import json

# Test the backend API directly
BASE_URL = "http://localhost:8000"

# Test data
test_payload = {
    "user_id": "test_user_123",
    "message": "Add buy groceries",
    "current_tasks": []
}

headers = {
    "Content-Type": "application/json"
}

print("Testing /chat/process_public endpoint...")

try:
    response = requests.post(f"{BASE_URL}/chat/process_public", 
                           data=json.dumps(test_payload), 
                           headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test with a read command
test_payload_view = {
    "user_id": "test_user_123",
    "message": "Show my tasks",
    "current_tasks": [
        {
            "id": "task_1",
            "user_id": "test_user_123",
            "title": "Buy groceries",
            "description": "",
            "is_completed": False,
            "priority": "Medium",
            "category": "Personal",
            "due_date": None,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
    ]
}

print("\nTesting /chat/process_public endpoint with view command...")
try:
    response = requests.post(f"{BASE_URL}/chat/process_public", 
                           data=json.dumps(test_payload_view), 
                           headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")