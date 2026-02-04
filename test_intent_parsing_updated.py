#!/usr/bin/env python3
"""
Test script to debug the intent parsing issue - Updated version
"""
import sys
import os

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

# Import the modules directly from the file content
import re
from typing import List, Dict, NamedTuple
from enum import Enum

class TaskAction(Enum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    COMPLETE = "COMPLETE"
    NONE = "NONE"

class IntentResult(NamedTuple):
    action: TaskAction
    confidence: float  # 0.0 to 1.0

class MessageParser:
    def __init__(self):
        # Define patterns for different intents
        self.create_patterns = [
            r"(add|create|make|new)\s+(?:a\s+|an\s+|the\s+)?(.+)",
            r"(add|create|make|new)\s+(?:a\s+|an\s+|the\s+)?(.+)\s+(to\s+my\s+)?(?:task|todo|to-do)\s+list",
            r"i\s+need\s+to\s+(.+)",
            r"don'?t\s+forget\s+to\s+(.+)",
            r"remind\s+me\s+to\s+(.+)"
        ]

        self.read_patterns = [
            r"(show|display|list|view|see|what.*have|what.*got)\s+(?:my\s+)?(?:tasks|todos|to-dos|list)",
            r"(what|which)\s+(?:tasks|todos|to-dos)\s+(?:do\s+i\s+have|are\s+on\s+my\s+list)",
            r"my\s+(?:current\s+)?(?:tasks|todos|to-dos)",
            r"help\s+me\s+organize",
            r"what\s+should\s+i\s+do"
        ]

        self.complete_patterns = [
            r"(complete|finish|done|completed|finished)\s+(?:the\s+)?(.+?)",
            r"(mark|set)\s+(?:the\s+)?(.+?)\s+(?:as\s+)?(complete|done|finished)",
            r"i\s+(?:have\s+)?(completed|finished|done)\s+(?:the\s+)?(.+?)",
            r"cross\s+(?:the\s+)?(.+?)\s+off\s+(?:my\s+)?(?:list|tasks)"
        ]

        self.update_patterns = [
            r"(change|update|edit|modify)\s+(?:the\s+)?(.+?)\s+(?:to|as)\s+(.+)",
            r"(update|change|edit|modify)\s+(?:the\s+)?(.+?)",
            r"rename\s+(?:the\s+)?(.+?)\s+(?:to|as)\s+(.+)"
        ]

        self.delete_patterns = [
            r"(delete|remove|eliminate|get rid of)\s+(?:the\s+)?(.+?)",
            r"(delete|remove|eliminate|get rid of)\s+(?:task|todo|to-do)\s+(?:named|called|titled)\s+(.+?)"
        ]

    def parse_intent(self, message: str, current_tasks: List[Dict]) -> IntentResult:
        """
        Parse the user's message to determine the intent
        """
        try:
            if not message:
                return IntentResult(action=TaskAction.NONE, confidence=0.1)

            message_lower = message.lower().strip()

            # Rule-based intent detection with keyword matching
            # If message contains "add" or "create" → create_todo
            if any(keyword in message_lower for keyword in ["add", "create"]):
                return IntentResult(action=TaskAction.CREATE, confidence=0.9)

            # If message contains "show" or "list" → list_todos
            if any(keyword in message_lower for keyword in ["show", "list"]):
                return IntentResult(action=TaskAction.READ, confidence=0.9)

            # If message contains "update" or "edit" → update_todo
            if any(keyword in message_lower for keyword in ["update", "edit"]):
                return IntentResult(action=TaskAction.UPDATE, confidence=0.9)

            # If message contains "delete" or "remove" → delete_todo
            if any(keyword in message_lower for keyword in ["delete", "remove"]):
                return IntentResult(action=TaskAction.DELETE, confidence=0.9)

            # Check for create intent (backup using regex patterns)
            for pattern in self.create_patterns:
                if re.search(pattern, message_lower):
                    return IntentResult(action=TaskAction.CREATE, confidence=0.9)

            # Check for read/view intent (backup using regex patterns)
            for pattern in self.read_patterns:
                if re.search(pattern, message_lower):
                    return IntentResult(action=TaskAction.READ, confidence=0.9)

            # Check for complete intent (backup using regex patterns)
            for pattern in self.complete_patterns:
                if re.search(pattern, message_lower):
                    return IntentResult(action=TaskAction.COMPLETE, confidence=0.9)

            # Check for update intent (backup using regex patterns)
            for pattern in self.update_patterns:
                if re.search(pattern, message_lower):
                    return IntentResult(action=TaskAction.UPDATE, confidence=0.9)

            # Check for delete intent (backup using regex patterns)
            for pattern in self.delete_patterns:
                if re.search(pattern, message_lower):
                    return IntentResult(action=TaskAction.DELETE, confidence=0.9)

            # Default to no specific action
            return IntentResult(action=TaskAction.NONE, confidence=0.5)
        except Exception as e:
            import traceback
            print(f"Error in parse_intent: {str(e)}")
            print(traceback.format_exc())
            # Return a safe default
            return IntentResult(action=TaskAction.NONE, confidence=0.1)

def test_intent_parsing():
    parser = MessageParser()
    
    # Test messages from the requirements
    test_messages = [
        "add task buy milk",
        "create todo read book", 
        "show my tasks",
        "delete task buy milk",
        "hello",  # This should not trigger CRUD operations
        "hi there",  # This should not trigger CRUD operations
        "update task buy milk to buy almond milk"  # This should trigger update
    ]
    
    print("Testing intent parsing for the following messages:")
    print("-" * 60)
    
    for message in test_messages:
        # Note: parse_intent requires current_tasks as second parameter
        intent_result = parser.parse_intent(message, [])
        
        print(f"Message: '{message}'")
        print(f"Intent Action: {intent_result.action}")
        print(f"Confidence: {intent_result.confidence}")
        print("-" * 40)

if __name__ == "__main__":
    test_intent_parsing()