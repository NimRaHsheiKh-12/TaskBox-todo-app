#!/usr/bin/env python3
"""
Simple test script for ChatService to verify the fixes work
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

async def test_chat_service():
    try:
        from backend.src.services.chat_service import ChatService
        from backend.src.utils.task_enums import TaskAction

        # Create ChatService instance
        cs = ChatService()

        # Test data
        user_id = "test-user-123"
        current_tasks = [
            {
                "id": "task-1",
                "user_id": user_id,
                "title": "Buy groceries",
                "description": "",
                "is_completed": False,
                "priority": "Medium",
                "category": "Personal",
                "due_date": None,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        ]

        # Test greeting
        print("Testing greeting...")
        result = await cs.process_message(user_id, "hello", current_tasks)
        print(f"Greeting result: {result}")
        assert "reply" in result
        assert result["reply"] != ""
        print("✓ Greeting test passed")

        # Test CREATE intent
        print("\nTesting CREATE intent...")
        result = await cs.process_message(user_id, "add buy milk", current_tasks)
        print(f"Create result: {result}")
        assert "reply" in result
        assert result["reply"] != ""
        assert result.get("action_performed") == TaskAction.CREATE.value
        assert result.get("success") == True
        assert len(result.get("updated_tasks", [])) == 2  # Original + new task
        print("✓ CREATE test passed")

        # Test READ intent
        print("\nTesting READ intent...")
        result = await cs.process_message(user_id, "show my tasks", current_tasks)
        print(f"Read result: {result}")
        assert "reply" in result
        assert result["reply"] != ""
        assert result.get("action_performed") == TaskAction.READ.value
        print("✓ READ test passed")

        # Test COMPLETE intent
        print("\nTesting COMPLETE intent...")
        result = await cs.process_message(user_id, "complete buy groceries", current_tasks)
        print(f"Complete result: {result}")
        assert "reply" in result
        assert result["reply"] != ""
        assert result.get("action_performed") == TaskAction.COMPLETE.value
        assert result.get("success") == True
        print("✓ COMPLETE test passed")

        # Test DELETE intent
        print("\nTesting DELETE intent...")
        result = await cs.process_message(user_id, "delete buy groceries", current_tasks)
        print(f"Delete result: {result}")
        assert "reply" in result
        assert result["reply"] != ""
        assert result.get("action_performed") == TaskAction.DELETE.value
        assert result.get("success") == True
        print("✓ DELETE test passed")

        print("\n🎉 All ChatService tests passed!")

    except Exception as e:
        import traceback
        print(f"❌ Test failed: {e}")
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(test_chat_service())
    sys.exit(0 if success else 1)