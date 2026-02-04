#!/usr/bin/env python3
"""
Test script to verify that the fixed Taskie chatbot works correctly with CRUD operations
"""
import asyncio
import json
import requests
from datetime import datetime
import uuid

# Configuration
BASE_URL = "http://localhost:8000"
HEADERS = {
    "Content-Type": "application/json"
}

def test_chatbot_crud_operations():
    """Test the chatbot CRUD functionality after user login"""

    print("Testing Taskie chatbot CRUD operations after login...")

    # Step 1: Register a test user
    print("\n1. Registering test user...")
    user_email = f"test_user_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com"
    user_password = "SecurePassword123!"

    register_data = {
        "email": user_email,
        "password": user_password
    }

    try:
        register_response = requests.post(f"{BASE_URL}/auth/register",
                                       json=register_data,
                                       headers=HEADERS)
        print(f"Register response: {register_response.status_code}")

        if register_response.status_code == 400:
            # User might already exist, try login
            print("User might already exist, attempting login...")
        elif register_response.status_code not in [200, 201]:
            print(f"Failed to register user: {register_response.text}")
            return False
        else:
            print("User registered successfully")

    except Exception as e:
        print(f"Error registering user: {e}")
        return False

    # Step 2: Login the user
    print("\n2. Logging in user...")
    login_data = {
        "email": user_email,
        "password": user_password
    }

    try:
        login_response = requests.post(f"{BASE_URL}/auth/login",
                                    json=login_data,
                                    headers=HEADERS)
        print(f"Login response: {login_response.status_code}")

        if login_response.status_code != 200:
            print(f"Failed to login user: {login_response.text}")
            return False

        login_result = login_response.json()
        access_token = login_result.get("access_token")
        user_id = login_result.get("user_id")

        print(f"Access token received: {'Yes' if access_token else 'No'}")
        print(f"User ID: {user_id}")

        if not access_token:
            print("No access token received")
            return False

        # Add token to headers for subsequent requests
        auth_headers = HEADERS.copy()
        auth_headers["Authorization"] = f"Bearer {access_token}"

    except Exception as e:
        print(f"Error logging in user: {e}")
        return False

    # Step 3: Test chatbot CRUD functionality
    print("\n3. Testing chatbot CRUD functionality...")

    # Test 1: "hi" greeting
    print("\n3a. Testing greeting: 'hi'")
    chat_data = {
        "message": "hi"
    }

    try:
        chat_response = requests.post(f"{BASE_URL}/chat/",
                                   json=chat_data,
                                   headers=auth_headers)
        print(f"Chat response: {chat_response.status_code}")
        result = chat_response.json()
        print(f"Reply: {result.get('reply', 'No reply field')}")

        if chat_response.status_code != 200:
            print("Failed to get chat response for greeting")
            return False

        if "Taskie" not in result.get('reply', ''):
            print("Greeting response doesn't contain 'Taskie'")
        else:
            print("[PASS] Greeting response is correct")

    except Exception as e:
        print(f"Error testing greeting: {e}")
        return False

    # Test 2: Add task - "Add 'Buy milk'"
    print("\n3b. Testing task creation: 'Add Buy milk'")
    chat_data = {
        "message": "Add Buy milk"
    }

    try:
        chat_response = requests.post(f"{BASE_URL}/chat/",
                                   json=chat_data,
                                   headers=auth_headers)
        print(f"Chat response: {chat_response.status_code}")
        result = chat_response.json()
        print(f"Reply: {result.get('reply', 'No reply field')}")

        if chat_response.status_code != 200:
            print("Failed to get chat response for task creation")
            print(f"Response: {chat_response.text}")
            return False

        if "Buy milk" not in result.get('reply', ''):
            print("Task creation response doesn't contain 'Buy milk'")
        else:
            print("[PASS] Task creation response is correct")

    except Exception as e:
        print(f"Error testing task creation: {e}")
        return False

    # Test 3: Show tasks - "Show my tasks"
    print("\n3c. Testing task retrieval: 'Show my tasks'")
    chat_data = {
        "message": "Show my tasks"
    }

    try:
        chat_response = requests.post(f"{BASE_URL}/chat/",
                                   json=chat_data,
                                   headers=auth_headers)
        print(f"Chat response: {chat_response.status_code}")
        result = chat_response.json()
        print(f"Reply: {result.get('reply', 'No reply field')}")

        if chat_response.status_code != 200:
            print("Failed to get chat response for task retrieval")
            return False

        if "Buy milk" not in result.get('reply', ''):
            print("'Buy milk' not found in task list response")
        else:
            print("[PASS] Task list response contains 'Buy milk'")

    except Exception as e:
        print(f"Error testing task retrieval: {e}")
        return False

    # Test 4: Update task - "Update 'Buy milk' to 'Buy almond milk'"
    print("\n3d. Testing task update: 'Update Buy milk to Buy almond milk'")
    chat_data = {
        "message": "Update Buy milk to Buy almond milk"
    }

    try:
        chat_response = requests.post(f"{BASE_URL}/chat/",
                                   json=chat_data,
                                   headers=auth_headers)
        print(f"Chat response: {chat_response.status_code}")
        result = chat_response.json()
        print(f"Reply: {result.get('reply', 'No reply field')}")

        if chat_response.status_code != 200:
            print("Failed to get chat response for task update")
            return False

        if "almond milk" not in result.get('reply', '').lower():
            print("Task update response doesn't contain 'almond milk'")
        else:
            print("[PASS] Task update response is correct")

    except Exception as e:
        print(f"Error testing task update: {e}")
        return False

    # Test 5: Complete task - "Complete 'Buy almond milk'"
    print("\n3e. Testing task completion: 'Complete Buy almond milk'")
    chat_data = {
        "message": "Complete Buy almond milk"
    }

    try:
        chat_response = requests.post(f"{BASE_URL}/chat/",
                                   json=chat_data,
                                   headers=auth_headers)
        print(f"Chat response: {chat_response.status_code}")
        result = chat_response.json()
        print(f"Reply: {result.get('reply', 'No reply field')}")

        if chat_response.status_code != 200:
            print("Failed to get chat response for task completion")
            return False

        if "completed" not in result.get('reply', '').lower():
            print("Task completion response doesn't contain 'completed'")
        else:
            print("[PASS] Task completion response is correct")

    except Exception as e:
        print(f"Error testing task completion: {e}")
        return False

    # Test 6: Delete task - "Delete 'Buy almond milk'"
    print("\n3f. Testing task deletion: 'Delete Buy almond milk'")
    chat_data = {
        "message": "Delete Buy almond milk"
    }

    try:
        chat_response = requests.post(f"{BASE_URL}/chat/",
                                   json=chat_data,
                                   headers=auth_headers)
        print(f"Chat response: {chat_response.status_code}")
        result = chat_response.json()
        print(f"Reply: {result.get('reply', 'No reply field')}")

        if chat_response.status_code != 200:
            print("Failed to get chat response for task deletion")
            return False

        if "removed" not in result.get('reply', '').lower() and "deleted" not in result.get('reply', '').lower():
            print("Task deletion response doesn't contain 'removed' or 'deleted'")
        else:
            print("[PASS] Task deletion response is correct")

    except Exception as e:
        print(f"Error testing task deletion: {e}")
        return False

    print("\n[PASS] All CRUD tests passed! Taskie chatbot is working correctly after login.")
    return True

def test_unauthenticated_access():
    """Test that unauthenticated access is properly rejected"""
    print("\n4. Testing unauthenticated access...")

    chat_data = {
        "message": "Show my tasks"
    }

    try:
        chat_response = requests.post(f"{BASE_URL}/chat/",
                                   json=chat_data,
                                   headers=HEADERS)  # No auth header
        print(f"Unauthenticated chat response: {chat_response.status_code}")

        if chat_response.status_code == 401 or chat_response.status_code == 403:
            print("[PASS] Unauthenticated access properly rejected")
            return True
        else:
            print("[FAIL] Unauthenticated access should have been rejected")
            return False

    except Exception as e:
        print(f"Error testing unauthenticated access: {e}")
        return False

if __name__ == "__main__":
    print("Starting Taskie chatbot tests...")

    success1 = test_chatbot_crud_operations()
    success2 = test_unauthenticated_access()

    if success1 and success2:
        print("\n[SUCCESS] All tests passed! The Taskie chatbot is now working properly with CRUD operations.")
    else:
        print("\n[ERROR] Some tests failed. Please check the implementation.")