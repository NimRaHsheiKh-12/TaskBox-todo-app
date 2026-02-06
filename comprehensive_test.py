import asyncio
from backend.src.services.chat_service import ChatService

async def test_comprehensive():
    chat_service = ChatService()
    
    # Start with empty tasks
    current_tasks = []
    
    print("=== Testing CREATE ===")
    # Test adding a task
    result = await chat_service.process_message(
        user_id='test_user',
        message='Add buy groceries',
        current_tasks=current_tasks
    )
    current_tasks = result['updated_tasks']
    print(f"Added task: {result['reply']}")
    print(f"Action: {result['action_performed']}")
    print(f"Task count: {len(current_tasks)}")
    
    print("\n=== Testing READ ===")
    # Test viewing tasks
    result = await chat_service.process_message(
        user_id='test_user',
        message='Show my tasks',
        current_tasks=current_tasks
    )
    print(f"View tasks: {result['reply'][:100]}...")  # Print first 100 chars
    print(f"Action: {result['action_performed']}")
    
    print("\n=== Testing UPDATE/COMPLETE ===")
    # Test completing a task
    result = await chat_service.process_message(
        user_id='test_user',
        message='Mark buy groceries as completed',
        current_tasks=current_tasks
    )
    current_tasks = result['updated_tasks']
    print(f"Completed task: {result['reply']}")
    print(f"Action: {result['action_performed']}")
    
    # Verify the task is actually marked as completed
    completed_task = next((task for task in current_tasks if task['title'] == 'Buy groceries'), None)
    if completed_task:
        print(f"Task completion status: {completed_task['is_completed']}")
    
    print("\n=== Testing DELETE ===")
    # Test deleting a task
    result = await chat_service.process_message(
        user_id='test_user',
        message='Delete buy groceries',
        current_tasks=current_tasks
    )
    current_tasks = result['updated_tasks']
    print(f"Deleted task: {result['reply']}")
    print(f"Action: {result['action_performed']}")
    print(f"Final task count: {len(current_tasks)}")

if __name__ == "__main__":
    asyncio.run(test_comprehensive())