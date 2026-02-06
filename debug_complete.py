#!/usr/bin/env python3
"""
Debug script to check what's happening with the complete task test
"""
import asyncio
from backend.src.services.chat_service import ChatService


async def debug_complete_task():
    """Debug the complete task functionality"""
    chat_service = ChatService()
    
    # Replicate the test scenario
    current_tasks = [
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
    
    # Test with the same user_id as the test
    result = await chat_service.process_message("test_user_123", "Mark 'Buy groceries' as completed", current_tasks)
    print(f"Success: {result.get('success')}")
    print(f"Action performed: {result.get('action_performed')}")
    print(f"Reply length: {len(result.get('reply', ''))}")
    print(f"Reply starts with: {repr(result.get('reply', '')[:50])}")


if __name__ == "__main__":
    asyncio.run(debug_complete_task())