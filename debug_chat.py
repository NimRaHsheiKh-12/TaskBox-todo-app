#!/usr/bin/env python3
"""
Test script to debug the chatbot functionality
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.services.chat_service import ChatService
from backend.src.utils.message_parser import MessageParser
from backend.src.utils.task_enums import TaskAction

def test_chat_service():
    print("Testing chat service...")
    
    # Test the message parser
    print("\n1. Testing message parser...")
    parser = MessageParser()
    message = "Add buy groceries to my list"
    current_tasks = []
    
    intent_result = parser.parse_intent(message, current_tasks)
    print(f"Intent: {intent_result.action}, Confidence: {intent_result.confidence}")
    
    # Test extracting task title
    task_title = parser.extract_task_title(message)
    print(f"Extracted task title: {task_title}")
    
    # Test the chat service
    print("\n2. Testing chat service...")
    chat_service = ChatService()
    
    # Test with asyncio
    import asyncio
    
    async def run_tests():
        print("Running async tests...")
        
        # Test creating a task
        result = await chat_service.process_message('test_user_123', message, current_tasks)
        print(f"Process message result: {result}")
        
        # Test reading tasks
        read_result = await chat_service.process_message('test_user_123', 'Show my tasks', result.get('updated_tasks', []))
        print(f"Read tasks result: {read_result}")
        
        # Test completing a task if one exists
        if result.get('updated_tasks'):
            task_title = result['updated_tasks'][0]['title']
            complete_result = await chat_service.process_message('test_user_123', f'Complete {task_title}', result['updated_tasks'])
            print(f"Complete task result: {complete_result}")
    
    asyncio.run(run_tests())
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_chat_service()