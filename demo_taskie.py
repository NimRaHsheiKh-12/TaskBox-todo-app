"""
Simple demonstration of the TaskBox Chatbot Assistant (Taskie)
"""

from backend.src.services.chat_service import ChatService
from backend.src.schemas.chat import TaskSchema
from datetime import datetime


def demo_taskie():
    """Demonstrate Taskie's functionality"""
    print("TASKIE - Your AI Task Assistant!\n")
    
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

    # Simulate a conversation with Taskie
    conversation = [
        ("user", "Show my tasks"),
        ("user", "Mark 'Buy groceries' as completed"),
        ("user", "Add 'go for a run'"),
        ("user", "How can I better manage my tasks?"),
        ("user", "Complete task 2"),
    ]

    current_tasks = sample_tasks[:]

    for sender, message in conversation:
        print(f"[USER] {message}")

        # Process the message with Taskie
        result = chat_service.process_message(
            user_id="demo_user",
            message=message,
            current_tasks=current_tasks
        )

        print(f"[TASKIE] {result['reply']}")

        # Update the task list if there were changes
        if result['action_performed'] != 'READ' and result['action_performed'] != 'GUIDANCE':
            current_tasks = result['updated_tasks']

        print()

    print("[TASK LIST] Final tasks:")
    for i, task in enumerate(current_tasks, 1):
        status = "[DONE]" if task.is_completed else "[PENDING]"
        print(f"  {i}. {status} [{task.priority}] {task.category}: {task.title}")


if __name__ == "__main__":
    demo_taskie()