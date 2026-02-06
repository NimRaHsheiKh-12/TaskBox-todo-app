import asyncio
import json
from backend.src.services.chat_service import ChatService

async def test_chatbot():
    chat_service = ChatService()

    # Test initial tasks
    initial_tasks = []

    print("Testing ADD functionality...")
    # Test adding a task
    result = await chat_service.process_message(
        user_id='test_user',
        message='Add buy groceries',
        current_tasks=initial_tasks
    )
    print('Add task result:', repr(result['reply']))  # Using repr to handle emojis
    updated_tasks = result['updated_tasks']
    print('Number of tasks after adding:', len(updated_tasks))

    print("\nTesting VIEW functionality...")
    # Test viewing tasks
    result = await chat_service.process_message(
        user_id='test_user',
        message='Show my tasks',
        current_tasks=updated_tasks
    )
    print('View tasks result:', repr(result['reply']))

    print("\nTesting COMPLETE functionality...")
    # Test completing a task
    result = await chat_service.process_message(
        user_id='test_user',
        message='Mark buy groceries as completed',
        current_tasks=updated_tasks
    )
    print('Complete task result:', repr(result['reply']))
    updated_tasks = result['updated_tasks']
    print('Number of tasks after completing:', len(updated_tasks))

    # Verify the task is completed
    completed_task = next((task for task in updated_tasks if task['title'] == 'Buy groceries'), None)
    if completed_task:
        print('Task completion status:', completed_task['is_completed'])

    print("\nTesting DELETE functionality...")
    # Test deleting a task
    result = await chat_service.process_message(
        user_id='test_user',
        message='Delete buy groceries',
        current_tasks=updated_tasks
    )
    print('Delete task result:', repr(result['reply']))
    updated_tasks = result['updated_tasks']
    print('Number of tasks after deleting:', len(updated_tasks))

if __name__ == "__main__":
    asyncio.run(test_chatbot())