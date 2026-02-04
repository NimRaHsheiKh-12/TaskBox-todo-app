#!/usr/bin/env python3
"""
Final verification test for the intent parsing fix
"""
import sys
import os

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from utils.message_parser import MessageParser
from utils.task_enums import TaskAction

def test_original_issue_fixed():
    """Test that the original issue has been fixed"""
    parser = MessageParser()
    
    # Test the exact examples from the issue description
    test_cases = [
        ("add task buy milk", TaskAction.CREATE),
        ("create todo read book", TaskAction.CREATE),
        ("show my tasks", TaskAction.READ),
        ("delete task buy milk", TaskAction.DELETE),
    ]
    
    print("Testing that the original issue has been fixed:")
    print("=" * 60)
    
    all_passed = True
    
    for message, expected_action in test_cases:
        intent_result = parser.parse_intent(message, [])
        actual_action = intent_result.action
        
        status = "✅ PASS" if actual_action == expected_action else "❌ FAIL"
        if actual_action != expected_action:
            all_passed = False
            
        print(f"{status} Message: '{message}' -> Expected: {expected_action}, Got: {actual_action}")
    
    print("=" * 60)
    
    # Test that greetings don't trigger CRUD operations anymore
    greeting_tests = [
        ("hello", [TaskAction.CREATE, TaskAction.READ, TaskAction.UPDATE, TaskAction.DELETE]),
        ("hi", [TaskAction.CREATE, TaskAction.READ, TaskAction.UPDATE, TaskAction.DELETE]),
        ("hey there", [TaskAction.CREATE, TaskAction.READ, TaskAction.UPDATE, TaskAction.DELETE])
    ]
    
    print("\nTesting that greetings don't trigger CRUD operations:")
    print("=" * 60)
    
    for message, forbidden_actions in greeting_tests:
        intent_result = parser.parse_intent(message, [])
        actual_action = intent_result.action
        
        # Check if the action is one of the forbidden CRUD actions
        is_crud_action = actual_action in forbidden_actions
        status = "❌ FAIL" if is_crud_action else "✅ PASS"
        
        if is_crud_action:
            all_passed = False
            
        print(f"{status} Message: '{message}' -> Action: {actual_action} (should not be CRUD)")
    
    print("=" * 60)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED! The issue has been fixed.")
    else:
        print("⚠️  Some tests failed. The issue may not be fully resolved.")
    
    return all_passed

if __name__ == "__main__":
    test_original_issue_fixed()