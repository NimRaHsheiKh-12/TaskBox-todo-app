#!/usr/bin/env python3
"""
Final integration test: verify the chatbot backend handles all critical cases.
- Test MessageParser with "show my tasks"
- Test ChatService.process_message with None current_tasks
- Test the public chat endpoint payload handling
"""
import asyncio
import sys
import json

sys.path.insert(0, 'backend')

def test_parser():
    """Test that MessageParser correctly identifies READ intent for 'show my tasks'."""
    from src.utils.message_parser import MessageParser
    parser = MessageParser()
    result = parser.parse_intent('show my tasks', [])
    print(f"✓ Parser test: 'show my tasks' → {result.action} (confidence: {result.confidence})")
    assert str(result.action) == 'TaskAction.READ', f"Expected READ, got {result.action}"
    return True

def test_chat_service():
    """Test that ChatService.process_message handles None current_tasks."""
    from src.services.chat_service import ChatService
    cs = ChatService()
    # Call with db=None, user_id as dummy UUID, message='show my tasks', current_tasks=None
    res = asyncio.run(cs.process_message(
        db=None,
        user_id='00000000-0000-0000-0000-000000000000',
        message='show my tasks',
        current_tasks=None  # This was the bug—should now be handled
    ))
    print(f"✓ ChatService test: result = {json.dumps({k: v for k, v in res.items() if k != 'reply'}, indent=2)}")
    assert res.get('success'), "Expected success=True"
    assert 'reply' in res, "Expected reply in response"
    # We expect either a READ response (since we now have keyword fallback) or a fallback with no tasks
    print(f"  Reply: {res['reply'][:80]}...")
    return True

def test_schemas():
    """Test that ChatMessageRequest with current_tasks=None is valid."""
    from src.schemas.chat import ChatMessageRequest
    req = ChatMessageRequest(message='show my tasks', user_id=None, current_tasks=None)
    print(f"✓ Schema test: ChatMessageRequest accepts current_tasks=None")
    assert req.message == 'show my tasks'
    assert req.current_tasks is None
    return True

def main():
    print("=" * 60)
    print("FINAL INTEGRATION TEST")
    print("=" * 60)
    
    try:
        test_parser()
        test_schemas()
        test_chat_service()
        print("\n✓ ALL TESTS PASSED")
        return 0
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
