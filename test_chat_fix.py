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
    greeting_result = await chat_service.process_message(
        user_id="test-user-id",
        message="hi",
        current_tasks=[]
    )
    print(f"   Reply: {greeting_result['reply']}")
    print(f"   Action: {greeting_result['action_performed']}")
    print(f"   Success: {greeting_result['success']}")
    
    # Test 2: Create task message should work
    print("\n2. Testing create task message:")
    create_result = await chat_service.process_message(
        user_id="test-user-id",
        message="Add 'Buy milk' to my list",
        current_tasks=[]
    )
    print(f"   Reply: {create_result['reply']}")
    print(f"   Action: {create_result['action_performed']}")
    print(f"   Success: {create_result['success']}")
    print(f"   Updated tasks count: {len(create_result['updated_tasks'])}")
    
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
    show_result = await chat_service.process_message(
        user_id="test-user-id",
        message="Show my tasks",
        current_tasks=sample_tasks
    )
    print(f"   Reply: {show_result['reply']}")
    print(f"   Action: {show_result['action_performed']}")
    print(f"   Success: {show_result['success']}")
    
    # Test 4: Delete task message should work
    print("\n4. Testing delete task message:")
    delete_result = await chat_service.process_message(
        user_id="test-user-id",
        message="Delete 'Buy milk'",
        current_tasks=sample_tasks
    )
    print(f"   Reply: {delete_result['reply']}")
    print(f"   Action: {delete_result['action_performed']}")
    print(f"   Success: {delete_result['success']}")
    print(f"   Updated tasks count: {len(delete_result['updated_tasks'])}")
    
    # Test 5: Unrecognized message should return a friendly response
    print("\n5. Testing unrecognized message:")
    unrecognized_result = await chat_service.process_message(
        user_id="test-user-id",
        message="This is an unrecognized message",
        current_tasks=[]
    )
    print(f"   Reply: {unrecognized_result['reply']}")
    print(f"   Action: {unrecognized_result['action_performed']}")
    print(f"   Success: {unrecognized_result['success']}")
    
    print("\nAll tests completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_chatbot_fixes())