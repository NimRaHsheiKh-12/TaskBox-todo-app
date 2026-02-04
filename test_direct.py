import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import asyncio
from backend.src.services.chat_service import ChatService

async def test_process_message():
    print("Testing process_message function directly...")
    
    chat_service = ChatService()
    
    # Test the exact scenario that's failing
    result = await chat_service.process_message(
        user_id='test_user_123',
        message='Add buy groceries to my list',
        current_tasks=[]
    )
    
    print(f"Result: {result}")
    print("Direct test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_process_message())