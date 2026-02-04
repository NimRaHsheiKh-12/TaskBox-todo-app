#!/usr/bin/env python3
"""
Test to verify the UUID-as-message bug is fixed.
Tests all three chat endpoints with proper message and UUID isolation.
"""
import asyncio
import sys
import os

# Add backend src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from src.services.chat_service import ChatService
from src.utils.message_parser import MessageParser

async def test_message_parser():
    """Verify MessageParser correctly identifies intent from messages, not UUIDs."""
    print("\n" + "="*70)
    print("TEST 1: MessageParser - ensure it handles real messages, not UUIDs")
    print("="*70)
    
    parser = MessageParser()
    
    test_cases = [
        ("show my tasks", "READ"),
        ("add buy milk", "CREATE"),
        ("hello", None),  # Will be handled as greeting
        ("59d27b08-0e97-4481-943a-27e5d2d379d9", "NONE"),  # UUID should NOT match READ
    ]
    
    for message, expected_action in test_cases:
        result = parser.parse_intent(message, [])
        action_str = result.action.value if result else "NONE"
        status = "✓" if (expected_action is None or action_str == expected_action) else "✗"
        print(f"{status} Message: '{message}'")
        print(f"  → Action: {action_str}, Confidence: {result.confidence if result else 0}")

async def test_chat_service():
    """Verify ChatService receives the correct message and user_id separately."""
    print("\n" + "="*70)
    print("TEST 2: ChatService - ensure message and user_id are not confused")
    print("="*70)
    
    cs = ChatService()
    user_id = "59d27b08-0e97-4481-943a-27e5d2d379d9"
    
    test_cases = [
        ("hi", "greeting"),
        ("show my tasks", "read tasks"),
        ("add buy milk", "create task"),
    ]
    
    for message, desc in test_cases:
        print(f"\n  Testing: {desc}")
        print(f"    user_id: {user_id}")
        print(f"    message: '{message}'")
        
        result = await cs.process_message(
            db=None,
            user_id=user_id,
            message=message,
            current_tasks=None
        )
        
        reply = result.get("reply", "")
        action = result.get("action_performed", "")
        
        # Verify UUID is NOT in the reply
        if user_id in reply:
            print(f"    ✗ FAIL: UUID found in reply!")
            print(f"    Reply: {reply}")
        else:
            print(f"    ✓ UUID not in reply")
            print(f"    Action: {action}")
            print(f"    Reply (first 80 chars): {reply[:80]}...")

async def test_message_isolation():
    """Verify that if message is accidentally set to UUID, we handle it gracefully."""
    print("\n" + "="*70)
    print("TEST 3: Isolation - what happens if UUID is passed as message (bug scenario)")
    print("="*70)
    
    cs = ChatService()
    user_id = "59d27b08-0e97-4481-943a-27e5d2d379d9"
    bad_message = user_id  # Simulate the bug: UUID passed as message
    
    print(f"\n  Simulating bug: message = user_id")
    print(f"    message: '{bad_message}'")
    
    result = await cs.process_message(
        db=None,
        user_id=user_id,
        message=bad_message,
        current_tasks=None
    )
    
    reply = result.get("reply", "")
    
    # The bug would produce: "I'm not quite sure what you mean by '59d27b08...'"
    if "didn't quite understand" in reply or "not quite sure" in reply:
        print(f"  ✓ Fallback response triggered (expected, since UUID is not a valid command)")
        print(f"  Reply: {reply[:100]}...")
    else:
        print(f"  ? Unexpected reply: {reply}")

async def main():
    print("\n" + "█"*70)
    print("UUID BUG FIX VALIDATION TESTS")
    print("█"*70)
    
    await test_message_parser()
    await test_chat_service()
    await test_message_isolation()
    
    print("\n" + "█"*70)
    print("TESTS COMPLETE")
    print("█"*70)
    print("\nExpected behavior:")
    print("  ✓ Messages are correctly parsed as READ, CREATE, etc.")
    print("  ✓ UUIDs are never shown in chatbot replies")
    print("  ✓ User IDs are kept separate from messages at all layers")

if __name__ == "__main__":
    asyncio.run(main())
