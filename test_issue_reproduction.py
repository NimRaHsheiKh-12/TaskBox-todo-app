#!/usr/bin/env python3
"""
Test script to reproduce the CRUD actions issue
"""
import asyncio
from backend.src.services.chat_service import ChatService
from backend.src.utils.message_parser import MessageParser
from backend.src.utils.task_enums import TaskAction


async def test_intent_parsing():
    """Test if intent parsing works correctly"""
    parser = MessageParser()

    # Test different messages
    test_messages = [
        "Add buy groceries",
        "Add 'Buy groceries' to my list",  # This is the problematic case from the test
        "Create finish project report",
        "Show my tasks",
        "List all tasks",
        "Update buy groceries to buy organic groceries",
        "Delete buy groceries",
        "Remove buy groceries",
        "Complete buy groceries"
    ]

    print("Testing intent parsing:")
    for msg in test_messages:
        intent_result = parser.parse_intent(msg, [])
        print(f"Message: '{msg}' -> Action: {intent_result.action}, Confidence: {intent_result.confidence}")

        # Also test extract_task_title for create messages
        if intent_result.action == TaskAction.CREATE:
            title = parser.extract_task_title(msg)
            print(f"  Extracted title: '{title}'")


async def test_chat_service():
    """Test the full ChatService flow"""
    chat_service = ChatService()

    # Simulate empty task list
    current_tasks = []

    print("\nTesting ChatService:")

    # Test create
    result = await chat_service.process_message("user1", "Add buy groceries", current_tasks)
    print(f"Create result: {result['action_performed']}, Success: {result['success']}")

    # Test read with some tasks
    tasks_with_data = [
        {
            "id": "1",
            "user_id": "user1",
            "title": "buy groceries",
            "description": "",
            "is_completed": False,
            "priority": "Medium",
            "category": "Personal",
            "due_date": None,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
    ]

    result = await chat_service.process_message("user1", "Show my tasks", tasks_with_data)
    print(f"Read result: {result['action_performed']}, Success: {result['success']}")

    # Test delete
    result = await chat_service.process_message("user1", "Delete buy groceries", tasks_with_data)
    print(f"Delete result: {result['action_performed']}, Success: {result['success']}")

    # Test update
    result = await chat_service.process_message("user1", "Update buy groceries to buy organic groceries", tasks_with_data)
    print(f"Update result: {result['action_performed']}, Success: {result['success']}")


async def test_extract_functions():
    """Test the extract functions in MessageParser"""
    parser = MessageParser()

    print("\nTesting extract functions:")

    # Test extract_task_title for create
    create_msg = "Add buy groceries"
    title = parser.extract_task_title(create_msg)
    print(f"Extract title from '{create_msg}': '{title}'")

    # Test extract_task_title for delete (this might be problematic)
    delete_msg = "Delete buy groceries"
    title = parser.extract_task_title(delete_msg)
    print(f"Extract title from '{delete_msg}' (using extract_task_title): '{title}'")

    # Test find_task_by_title for delete
    delete_msg = "Delete buy groceries"
    tasks = [{"id": "1", "title": "buy groceries", "user_id": "user1"}]
    task = parser.find_task_by_title(delete_msg, tasks)
    print(f"Find task from '{delete_msg}': {task}")


if __name__ == "__main__":
    asyncio.run(test_intent_parsing())
    asyncio.run(test_chat_service())
    asyncio.run(test_extract_functions())