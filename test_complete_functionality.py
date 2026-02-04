#!/usr/bin/env python3
"""
Test script to check the complete functionality
"""
import asyncio
from backend.src.services.chat_service import ChatService
from backend.src.utils.message_parser import MessageParser


async def test_complete_functionality():
    """Test the complete functionality"""
    chat_service = ChatService()
    parser = MessageParser()
    
    # Test the find_task_by_title function specifically
    message = "Mark 'Buy groceries' as completed"
    tasks = [
        {
            "id": "task1",
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
    
    found_task = parser.find_task_by_title(message, tasks)
    print(f"Message: {message}")
    print(f"Found task: {found_task}")
    
    # Test the full flow
    result = await chat_service.process_message("test_user_123", message, tasks)
    print(f"Complete result: {result}")


if __name__ == "__main__":
    asyncio.run(test_complete_functionality())