import requests
import json

# Test basic server functionality
BASE_URL = "http://localhost:8000"

# Test the root endpoint
print("Testing root endpoint...")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"Root endpoint response: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error testing root endpoint: {e}")

# Test the chat endpoint without authentication to confirm it rejects unauthorized access
print("\nTesting chat endpoint without authentication...")
try:
    response = requests.post(f"{BASE_URL}/chat/", json={"message": "hi"})
    print(f"Unauthenticated chat response: {response.status_code}")
    if response.status_code != 403 and response.status_code != 401:
        print("Unexpected response for unauthenticated request")
    else:
        print("Correctly rejected unauthenticated request")
except Exception as e:
    print(f"Error testing unauthenticated chat: {e}")

# Test registration
print("\nTesting registration...")
try:
    register_data = {
        "email": "test@example.com",
        "password": "SecurePassword123!"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Registration response: {response.status_code}")
    print(f"Registration response data: {response.json()}")
except Exception as e:
    print(f"Error testing registration: {e}")

# Test login
print("\nTesting login...")
try:
    login_data = {
        "email": "test@example.com",
        "password": "SecurePassword123!"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login response: {response.status_code}")
    if response.status_code == 200:
        login_data = response.json()
        print(f"Login response data: {login_data}")
        access_token = login_data.get('access_token')
        if access_token:
            print("Successfully obtained access token")
            
            # Test authenticated chat
            print("\nTesting authenticated chat...")
            headers = {"Authorization": f"Bearer {access_token}"}
            chat_data = {"message": "hi"}
            response = requests.post(f"{BASE_URL}/chat/", json=chat_data, headers=headers)
            print(f"Authenticated chat response: {response.status_code}")
            if response.status_code == 200:
                chat_response = response.json()
                print(f"Chat response: {json.dumps(chat_response, indent=2)}")
            else:
                print(f"Chat request failed: {response.text}")
        else:
            print("No access token in login response")
    else:
        print(f"Login failed: {response.text}")
except Exception as e:
    print(f"Error testing login: {e}")