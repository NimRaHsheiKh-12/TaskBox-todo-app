import asyncio
from backend.src.services.chat_service import ChatService
from backend.src.utils.message_parser import MessageParser

async def test_completion():
    # First, let's test the parser directly
    parser = MessageParser()
    
    # Create a sample task
    sample_tasks = [{
        'id': '1',
        'title': 'Buy groceries',
        'is_completed': False
    }]
    
    # Test the parser
    intent = parser.parse_intent('Mark buy groceries as completed', sample_tasks)
    print(f"Intent for 'Mark buy groceries as completed': {intent.action}, Confidence: {intent.confidence}")
    
    found_task = parser.find_task_by_title('Mark buy groceries as completed', sample_tasks)
    print(f"Found task: {found_task}")
    
    # Now test with the chat service
    chat_service = ChatService()
    
    # Add a task first
    result = await chat_service.process_message(
        user_id='test_user',
        message='Add buy groceries',
        current_tasks=[]
    )
    tasks_with_one_item = result['updated_tasks']
    
    print(f"\nBefore completion - Task completed status: {tasks_with_one_item[0]['is_completed']}")
    
    # Try to complete the task
    result = await chat_service.process_message(
        user_id='test_user',
        message='Mark buy groceries as completed',
        current_tasks=tasks_with_one_item
    )
    
    print(f"After completion attempt - Action: {result['action_performed']}")
    print(f"Reply: {result['reply'][:50]}...")
    
    if result['updated_tasks']:
        print(f"After completion - Task completed status: {result['updated_tasks'][0]['is_completed']}")

if __name__ == "__main__":
    asyncio.run(test_completion())