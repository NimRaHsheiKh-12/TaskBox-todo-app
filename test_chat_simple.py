#!/usr/bin/env python3
"""
Test script to verify that the Taskie chatbot fixes work properly
"""

import asyncio
import sys
import os

# Add the backend src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from backend.src.services.chat_service import ChatService
from backend.src.utils.message_parser import MessageParser
from backend.src.utils.task_enums import TaskAction


async def test_chatbot_fixes():
    """Test the chatbot fixes"""
    
    print("Testing Taskie chatbot fixes...")
    
    # Initialize the chat service
    chat_service = ChatService()
    
    # Test 1: Greeting message should return a proper response
    print("\n1. Testing greeting message:")
    try:
        greeting_result = await chat_service.process_message(
            user_id="test-user-id",
            message="hi",
            current_tasks=[]
        )
        print(f"   Reply: {greeting_result.get('reply', 'No reply field')[:100]}...")  # Limit length
        print(f"   Action: {greeting_result.get('action_performed', 'No action field')}")
        print(f"   Success: {greeting_result.get('success', 'No success field')}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    # Test 2: Create task message should work
    print("\n2. Testing create task message:")
    try:
        create_result = await chat_service.process_message(
            user_id="test-user-id",
            message="Add 'Buy milk' to my list",
            current_tasks=[]
        )
        print(f"   Reply: {create_result.get('reply', 'No reply field')[:100]}...")  # Limit length
        print(f"   Action: {create_result.get('action_performed', 'No action field')}")
        print(f"   Success: {create_result.get('success', 'No success field')}")
        print(f"   Updated tasks count: {len(create_result.get('updated_tasks', []))}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    # Test 3: Show tasks message should work
    print("\n3. Testing show tasks message:")
    sample_tasks = [
        {
            "id": "1",
            "user_id": "test-user-id",
            "title": "Buy milk",
            "description": "",
            "is_completed": False,
            "priority": "Medium",
            "category": "Personal",
            "due_date": None,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
    ]
    try:
        show_result = await chat_service.process_message(
            user_id="test-user-id",
            message="Show my tasks",
            current_tasks=sample_tasks
        )
        print(f"   Reply: {show_result.get('reply', 'No reply field')[:100]}...")  # Limit length
        print(f"   Action: {show_result.get('action_performed', 'No action field')}")
        print(f"   Success: {show_result.get('success', 'No success field')}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    # Test 4: Delete task message should work
    print("\n4. Testing delete task message:")
    try:
        delete_result = await chat_service.process_message(
            user_id="test-user-id",
            message="Delete 'Buy milk'",
            current_tasks=sample_tasks
        )
        print(f"   Reply: {delete_result.get('reply', 'No reply field')[:100]}...")  # Limit length
        print(f"   Action: {delete_result.get('action_performed', 'No action field')}")
        print(f"   Success: {delete_result.get('success', 'No success field')}")
        print(f"   Updated tasks count: {len(delete_result.get('updated_tasks', []))}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    # Test 5: Unrecognized message should return a friendly response
    print("\n5. Testing unrecognized message:")
    try:
        unrecognized_result = await chat_service.process_message(
            user_id="test-user-id",
            message="This is an unrecognized message",
            current_tasks=[]
        )
        print(f"   Reply: {unrecognized_result.get('reply', 'No reply field')[:100]}...")  # Limit length
        print(f"   Action: {unrecognized_result.get('action_performed', 'No action field')}")
        print(f"   Success: {unrecognized_result.get('success', 'No success field')}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    print("\nAll tests completed!")


if __name__ == "__main__":
    asyncio.run(test_chatbot_fixes())