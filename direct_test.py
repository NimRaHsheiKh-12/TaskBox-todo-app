#!/usr/bin/env python3
"""
Direct test of chatbot logic
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

# Mock database dependencies
class MockDB:
    pass

class MockTodoService:
    @staticmethod
    def get_todos_by_user(db, user_uuid):
        return []

# Mock the database module
import backend.src.database.database as db_module
db_module.get_db = lambda: MockDB()

import backend.src.services.todo_service as todo_module
todo_module.TodoService = MockTodoService

async def test_chatbot():
    try:
        from backend.src.services.chat_service import ChatService
        chat_service = ChatService()

        print("Testing chatbot responses...")

        # Test 1: Greeting
        print("\n1. Greeting test:")
        result = await chat_service.process_message("test_user", "hello", [])
        print(f"   Message: hello")
        print(f"   Reply: {result['reply']}")
        print(f"   Action: {result['action_performed']}")

        # Test 2: Task creation
        print("\n2. Task creation test:")
        result = await chat_service.process_message("test_user", "add buy groceries", [])
        print(f"   Message: add buy groceries")
        print(f"   Reply: {result['reply']}")
        print(f"   Action: {result['action_performed']}")
        tasks = result['updated_tasks']
        print(f"   Tasks created: {len(tasks)}")

        # Test 3: Task reading
        print("\n3. Task reading test:")
        result = await chat_service.process_message("test_user", "show my tasks", tasks)
        print(f"   Message: show my tasks")
        print(f"   Reply: {result['reply']}")
        print(f"   Action: {result['action_performed']}")

        # Test 4: General question
        print("\n4. General question test:")
        result = await chat_service.process_message("test_user", "how are you", tasks)
        print(f"   Message: how are you")
        print(f"   Reply: {result['reply']}")
        print(f"   Action: {result['action_performed']}")

        # Test 5: Task completion
        print("\n5. Task completion test:")
        result = await chat_service.process_message("test_user", "complete buy groceries", tasks)
        print(f"   Message: complete buy groceries")
        print(f"   Reply: {result['reply']}")
        print(f"   Action: {result['action_performed']}")
        tasks = result['updated_tasks']

        # Test 6: What can you do
        print("\n6. Help question test:")
        result = await chat_service.process_message("test_user", "what can you do", tasks)
        print(f"   Message: what can you do")
        print(f"   Reply: {result['reply'][:100]}...")
        print(f"   Action: {result['action_performed']}")

        print("\n✓ All tests completed successfully!")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_chatbot())