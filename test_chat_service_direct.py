#!/usr/bin/env python3
"""
Direct test of the chat service without requiring the web server.
This tests the intent parsing directly with the fixed frontend payload.
"""

import sys
import asyncio
sys.path.insert(0, r'c:\fullstack TODO\todo_fullstack_app\backend')

from src.services.chat_service import ChatService

async def test_chat_service():
    """Test the chat service directly with the corrected frontend payload."""
    
    print("\n" + "="*70)
    print("FRONTEND CHAT API FIX - DIRECT SERVICE TEST")
    print("="*70)
    print("\nTesting that backend correctly parses intent when")
    print("receiving ONLY { message } payload from frontend\n")
    
    chat_service = ChatService()
    
    test_cases = [
        ("hi", "NONE", "greeting"),
        ("hello", "NONE", "greeting"),
        ("add buy milk", "CREATE", "create task"),
        ("add task: call mom", "CREATE", "create task"),
        ("show my tasks", "READ", "read tasks"),
        ("what are my tasks", "READ", "read tasks"),
        ("delete buy milk", "DELETE", "delete task"),
        ("what is 2+2?", "NONE", "general question"),
    ]
    
    results = []
    
    for message, expected_action, description in test_cases:
        print(f"\n{'-'*70}")
        print(f"Test: {description}")
        print(f"Input:  message = '{message}'")
        print(f"Expected action: {expected_action}")
        print(f"{'-'*70}")
        
        try:
            # Call the service with ONLY the message (simulating the fixed frontend)
            response = await chat_service.process_message(
                user_id="test_user",
                message=message,
                current_tasks=[]
            )
            
            action = response.get("action_performed", "NONE")
            reply = response.get("reply", "")
            
            print(f"Output:")
            print(f"  action_performed: {action}")
            print(f"  reply: {reply[:100]}..." if len(reply) > 100 else f"  reply: {reply}")
            
            success = (action == expected_action)
            status = "[PASS]" if success else "[FAIL]"
            print(f"\nResult: {status}")
            
            if not success:
                print(f"  Expected: {expected_action}, Got: {action}")
            
            results.append((message, expected_action, action, success))
            
        except Exception as e:
            print(f"[ERROR] Exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((message, expected_action, "ERROR", False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, _, _, success in results if success)
    total = len(results)
    
    for message, expected, actual, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status}: '{message}' (expected {expected}, got {actual})")
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] Backend correctly handles frontend payload!")
        print("         All intent parsing tests passed!")
        return True
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(test_chat_service())
        exit(0 if success else 1)
    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()
        exit(1)
