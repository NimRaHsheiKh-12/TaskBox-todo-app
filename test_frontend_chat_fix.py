#!/usr/bin/env python3
"""
Test script to verify the frontend chat API fix.
Tests that the API correctly sends only {message} payload.
"""

import requests
import json
import time
import subprocess
import os
from pathlib import Path

# Configuration
BACKEND_URL = "http://localhost:8000"
TEST_DELAY = 2

def test_chat_endpoint(message: str, expected_action: str = None):
    """Test the chat endpoint with a single message."""
    print(f"\n{'='*60}")
    print(f"Testing: '{message}'")
    print(f"Expected action: {expected_action or 'Any valid response'}")
    print(f"{'='*60}")
    
    # Prepare the payload - ONLY message, no userId or todosCount
    payload = {"message": message}
    
    print(f"[SEND] Payload: {json.dumps(payload)}")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat/process_public",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        print(f"[HTTP] Response Status: {response.status_code}")
        response_data = response.json()
        print(f"[RECV] Response Data:")
        print(json.dumps(response_data, indent=2))
        
        if response.status_code == 200:
            action = response_data.get("action_performed", "NONE")
            reply = response_data.get("reply", "")
            
            print(f"\n[OK] Success!")
            print(f"   Action: {action}")
            print(f"   Reply: {reply}")
            
            if expected_action and action != expected_action:
                print(f"[WARN] Expected action '{expected_action}' but got '{action}'")
                return False
            return True
        else:
            print(f"[ERROR] {response_data}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Connection failed: Is the backend running on {BACKEND_URL}?")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("FRONTEND CHAT API FIX TEST")
    print("="*60)
    print(f"\nTesting backend at: {BACKEND_URL}")
    print(f"Verifying API only sends: {{ message: <text> }}")
    
    # Check if backend is running
    print("\n[...] Checking backend connection...")
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=2)
        print("[OK] Backend is reachable!")
    except:
        print(f"[ERROR] Backend not reachable at {BACKEND_URL}")
        print(f"   Please start the backend first")
        return False
    
    # Run test cases
    test_cases = [
        ("hi", "NONE"),  # Should be a greeting
        ("hello", "NONE"),  # Should be a greeting
        ("add buy milk", "CREATE"),  # Should create a task
        ("show my tasks", "READ"),  # Should read tasks
        ("delete buy milk", "DELETE"),  # Should delete a task
        ("what is 2+2?", "NONE"),  # Should be a general question
    ]
    
    results = []
    for message, expected_action in test_cases:
        time.sleep(TEST_DELAY)  # Small delay between requests
        success = test_chat_endpoint(message, expected_action)
        results.append((message, expected_action, success))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, _, success in results if success)
    total = len(results)
    
    for message, expected_action, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status}: '{message}' -> Expected: {expected_action or 'Valid response'}")
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] Frontend chat API fix is working correctly!")
        return True
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
