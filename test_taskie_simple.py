"""
Simple test of the TaskBox Chatbot Assistant (Taskie) functionality
"""

import sys
import os
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

from backend.src.services.chat_service import ChatService
from backend.src.schemas.chat import TaskSchema
from datetime import datetime


def test_taskie():
    """Test Taskie's functionality"""
    print("Testing Taskie - Your AI Task Assistant!\n")
    
    # Initialize the chat service
    chat_service = ChatService()
    
    # Create some sample tasks
    sample_tasks = [
        TaskSchema(
            id="1",
            title="Buy groceries",
            description="Milk, bread, eggs, fruits",
            is_completed=False,
            priority="Medium",
            category="Personal",
            due_date="2024-01-20",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        TaskSchema(
            id="2",
            title="Finish project proposal",
            description="Complete the Q1 project proposal for client",
            is_completed=False,
            priority="High",
            category="Work",
            due_date="2024-01-18",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        TaskSchema(
            id="3",
            title="Call dentist",
            description="Schedule annual checkup",
            is_completed=True,
            priority="Low",
            category="Personal",
            due_date=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ]
    
    print("[TASK LIST] Initial tasks:")
    for i, task in enumerate(sample_tasks, 1):
        status = "[DONE]" if task.is_completed else "[PENDING]"
        print(f"  {i}. {status} [{task.priority}] {task.category}: {task.title}")
    print()
    
    # Test different functionalities
    test_cases = [
        ("Show my tasks", "Should list all tasks"),
        ("Mark 'Buy groceries' as completed", "Should mark task as completed"),
        ("Add 'go for a run'", "Should add a new task"),
        ("How can I better manage my tasks?", "Should provide guidance"),
        ("Complete task 2", "Should mark task 2 as completed"),
    ]
    
    current_tasks = sample_tasks[:]
    
    for message, description in test_cases:
        print(f"[INPUT] {message} - {description}")
        
        # Process the message with Taskie
        result = chat_service.process_message(
            user_id="demo_user",
            message=message,
            current_tasks=current_tasks
        )
        
        # Print result without emojis by replacing them
        reply = result['reply']
        import re
        # Remove emojis using regex
        reply_clean = re.sub(r'[^\x00-\x7F]+', '', reply)
        print(f"[OUTPUT] {reply_clean or result['reply'][:50]}...")  # Fallback to first 50 chars if all emojis
        print(f"[ACTION] {result['action_performed']}")
        
        # Update the task list if there were changes
        if result['action_performed'] != 'READ' and result['action_performed'] != 'GUIDANCE':
            current_tasks = result['updated_tasks']
            print(f"[STATUS] Tasks updated. Total tasks now: {len(current_tasks)}")
        else:
            print(f"[STATUS] No task changes. Total tasks: {len(current_tasks)}")
        
        print()
    
    print("[TASK LIST] Final tasks:")
    for i, task in enumerate(current_tasks, 1):
        status = "[DONE]" if task.is_completed else "[PENDING]"
        print(f"  {i}. {status} [{task.priority}] {task.category}: {task.title}")
    
    print("\n✅ Taskie functionality test completed successfully!")


if __name__ == "__main__":
    test_taskie()