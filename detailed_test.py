import requests
import json

# Test basic server functionality
BASE_URL = "http://localhost:8000"

# Test with a known user account or create a new one with a unique email
import uuid
unique_email = f"test_user_{uuid.uuid4()}@example.com"

print(f"Testing with unique email: {unique_email}")

# Register a new user
print("\nTesting registration with unique email...")
try:
    register_data = {
        "email": unique_email,
        "password": "SecurePassword123!"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Registration response: {response.status_code}")
    if response.status_code == 200 or response.status_code == 201:
        print(f"Registration response data: {response.json()}")
    else:
        print(f"Registration failed: {response.text}")
except Exception as e:
    print(f"Error testing registration: {e}")

# Login with the new user
print(f"\nTesting login with {unique_email}...")
try:
    login_data = {
        "email": unique_email,
        "password": "SecurePassword123!"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login response: {response.status_code}")
    if response.status_code == 200:
        login_data = response.json()
        print(f"Login response data: {json.dumps(login_data, indent=2)}")
        access_token = login_data.get('access_token')
        user_id = login_data.get('user_id')
        print(f"Access token: {'Yes' if access_token else 'No'}")
        print(f"User ID: {user_id}")
        
        if access_token:
            print("Successfully obtained access token")
            
            # Test authenticated chat - greeting
            print("\nTesting authenticated chat - greeting...")
            headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
            chat_data = {"message": "hi"}
            response = requests.post(f"{BASE_URL}/chat/", json=chat_data, headers=headers)
            print(f"Greeting chat response: {response.status_code}")
            if response.status_code == 200:
                chat_response = response.json()
                print(f"Greeting response: {json.dumps(chat_response, indent=2)}")
            else:
                print(f"Greeting chat request failed: {response.text}")
            
            # Test authenticated chat - add task
            print("\nTesting authenticated chat - add task...")
            chat_data = {"message": "Add Buy milk"}
            response = requests.post(f"{BASE_URL}/chat/", json=chat_data, headers=headers)
            print(f"Add task chat response: {response.status_code}")
            if response.status_code == 200:
                chat_response = response.json()
                print(f"Add task response: {json.dumps(chat_response, indent=2)}")
            else:
                print(f"Add task chat request failed: {response.text}")
                
            # Test authenticated chat - show tasks
            print("\nTesting authenticated chat - show tasks...")
            chat_data = {"message": "Show my tasks"}
            response = requests.post(f"{BASE_URL}/chat/", json=chat_data, headers=headers)
            print(f"Show tasks chat response: {response.status_code}")
            if response.status_code == 200:
                chat_response = response.json()
                print(f"Show tasks response: {json.dumps(chat_response, indent=2)}")
            else:
                print(f"Show tasks chat request failed: {response.text}")
                
            # Test authenticated chat - update task
            print("\nTesting authenticated chat - update task...")
            chat_data = {"message": "Update Buy milk to Buy almond milk"}
            response = requests.post(f"{BASE_URL}/chat/", json=chat_data, headers=headers)
            print(f"Update task chat response: {response.status_code}")
            if response.status_code == 200:
                chat_response = response.json()
                print(f"Update task response: {json.dumps(chat_response, indent=2)}")
            else:
                print(f"Update task chat request failed: {response.text}")
                
            # Test authenticated chat - complete task
            print("\nTesting authenticated chat - complete task...")
            chat_data = {"message": "Complete Buy almond milk"}
            response = requests.post(f"{BASE_URL}/chat/", json=chat_data, headers=headers)
            print(f"Complete task chat response: {response.status_code}")
            if response.status_code == 200:
                chat_response = response.json()
                print(f"Complete task response: {json.dumps(chat_response, indent=2)}")
            else:
                print(f"Complete task chat request failed: {response.text}")
                
            # Test authenticated chat - delete task
            print("\nTesting authenticated chat - delete task...")
            chat_data = {"message": "Delete Buy almond milk"}
            response = requests.post(f"{BASE_URL}/chat/", json=chat_data, headers=headers)
            print(f"Delete task chat response: {response.status_code}")
            if response.status_code == 200:
                chat_response = response.json()
                print(f"Delete task response: {json.dumps(chat_response, indent=2)}")
            else:
                print(f"Delete task chat request failed: {response.text}")
        else:
            print("No access token in login response")
    else:
        print(f"Login failed: {response.text}")
except Exception as e:
    print(f"Error testing login: {e}")
    import traceback
    traceback.print_exc()