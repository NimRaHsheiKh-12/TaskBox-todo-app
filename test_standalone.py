#!/usr/bin/env python3
"""
Standalone test for chatbot core logic
"""
import asyncio
import sys
import os

# Mock the database and other dependencies
class MockDB:
    pass

class MockTodoService:
    @staticmethod
    def get_todos_by_user(db, user_uuid):
        return []

# Mock the imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

# Mock the database module
import backend.src.database.database as db_module
db_module.get_db = lambda: MockDB()

import backend.src.services.todo_service as todo_module
todo_module.TodoService = MockTodoService

try:
    from backend.src.services.chat_service import ChatService
    print("✓ ChatService imported successfully")

    async def test_chatbot():
        chat_service = ChatService()

        # Test greeting
        print("\n1. Testing greeting:")
        result = await chat_service.process_message("test_user", "hello", [])
        print(f"   Reply: {result['reply']}")
        print(f"   Action: {result['action_performed']}")

        # Test task creation
        print("\n2. Testing task creation:")
        result = await chat_service.process_message("test_user", "add buy groceries", [])
        print(f"   Reply: {result['reply']}")
        print(f"   Action: {result['action_performed']}")
        tasks = result['updated_tasks']
        print(f"   Tasks count: {len(tasks)}")

        # Test task reading
        print("\n3. Testing task reading:")
        result = await chat_service.process_message("test_user", "show my tasks", tasks)
        print(f"   Reply: {result['reply']}")
        print(f"   Action: {result['action_performed']}")

        # Test general query
        print("\n4. Testing general query:")
        result = await chat_service.process_message("test_user", "how are you", tasks)
        print(f"   Reply: {result['reply']}")
        print(f"   Action: {result['action_performed']}")

        print("\n✓ All tests completed successfully!")

    # Run the test
    asyncio.run(test_chatbot())

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()