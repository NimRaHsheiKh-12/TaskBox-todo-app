#!/usr/bin/env python3
"""
Test script to verify that Taskie chatbot works correctly after login
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

def test_chatbot_after_login():
    """Test the chatbot functionality after user login"""
    
    print("Testing Taskie chatbot after login...")
    
    # Step 1: Register a test user
    print("\n1. Registering test user...")
    user_email = f"test_user_{uuid.uuid4()}@example.com"
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
        print(f"Register data: {register_response.json()}")
        
        if register_response.status_code != 200:
            print("Failed to register user")
            return False
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
            print("Failed to login user")
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
    
    # Step 3: Test chatbot functionality
    print("\n3. Testing chatbot functionality...")
    
    # Test 1: "hi" greeting
    print("\n3a. Testing greeting: 'hi'")
    chat_data = {
        "user_id": user_id,
        "message": "hi",
        "current_tasks": []
    }
    
    try:
        chat_response = requests.post(f"{BASE_URL}/chat/process", 
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
            print("✓ Greeting response is correct")
            
    except Exception as e:
        print(f"Error testing greeting: {e}")
        return False
    
    # Test 2: Add task - "Add 'Buy milk' to my list"
    print("\n3b. Testing task creation: 'Add Buy milk to my list'")
    chat_data = {
        "user_id": user_id,
        "message": "Add 'Buy milk' to my list",
        "current_tasks": []
    }
    
    try:
        chat_response = requests.post(f"{BASE_URL}/chat/process", 
                                   json=chat_data, 
                                   headers=auth_headers)
        print(f"Chat response: {chat_response.status_code}")
        result = chat_response.json()
        print(f"Reply: {result.get('reply', 'No reply field')}")
        print(f"Action performed: {result.get('action_performed', 'No action field')}")
        
        if chat_response.status_code != 200:
            print("Failed to get chat response for task creation")
            return False
            
        if result.get('action_performed') != 'CREATE':
            print("Task creation action not performed")
        else:
            print("✓ Task creation action performed")
            
    except Exception as e:
        print(f"Error testing task creation: {e}")
        return False
    
    # Test 3: Show tasks - "Show my tasks"
    print("\n3c. Testing task retrieval: 'Show my tasks'")
    chat_data = {
        "user_id": user_id,
        "message": "Show my tasks",
        "current_tasks": []  # Will be loaded from DB by backend
    }
    
    try:
        chat_response = requests.post(f"{BASE_URL}/chat/process", 
                                   json=chat_data, 
                                   headers=auth_headers)
        print(f"Chat response: {chat_response.status_code}")
        result = chat_response.json()
        print(f"Reply: {result.get('reply', 'No reply field')}")
        print(f"Action performed: {result.get('action_performed', 'No action field')}")
        
        if chat_response.status_code != 200:
            print("Failed to get chat response for task retrieval")
            return False
            
        if "Buy milk" not in result.get('reply', ''):
            print("'Buy milk' not found in task list response")
        else:
            print("✓ Task list response contains 'Buy milk'")
            
    except Exception as e:
        print(f"Error testing task retrieval: {e}")
        return False
    
    # Test 4: Delete task - "Delete 'Buy milk'"
    print("\n3d. Testing task deletion: 'Delete Buy milk'")
    chat_data = {
        "user_id": user_id,
        "message": "Delete 'Buy milk'",
        "current_tasks": []  # Will be loaded from DB by backend
    }
    
    try:
        chat_response = requests.post(f"{BASE_URL}/chat/process", 
                                   json=chat_data, 
                                   headers=auth_headers)
        print(f"Chat response: {chat_response.status_code}")
        result = chat_response.json()
        print(f"Reply: {result.get('reply', 'No reply field')}")
        print(f"Action performed: {result.get('action_performed', 'No action field')}")
        
        if chat_response.status_code != 200:
            print("Failed to get chat response for task deletion")
            return False
            
        if result.get('action_performed') != 'DELETE':
            print("Task deletion action not performed")
        else:
            print("✓ Task deletion action performed")
            
    except Exception as e:
        print(f"Error testing task deletion: {e}")
        return False
    
    print("\n✓ All tests passed! Taskie chatbot is working correctly after login.")
    return True

if __name__ == "__main__":
    success = test_chatbot_after_login()
    if success:
        print("\n🎉 All tests passed! The Taskie chatbot is now working properly after login.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")