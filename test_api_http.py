#!/usr/bin/env python3
"""
Simple HTTP test of the chat API to verify the fix works
"""
import requests
import json
import time
import subprocess
import sys

BACKEND_URL = "http://localhost:8000"

def test_api():
    """Test the chat API via HTTP"""
    
    print("\n" + "="*70)
    print("TESTING CHAT API ENDPOINT")
    print("="*70)
    print(f"\nTesting: POST {BACKEND_URL}/chat/process_public\n")
    
    tests = [
        ("hi", "NONE"),
        ("add buy milk", "CREATE"),
        ("show my tasks", "READ"),
        ("delete buy milk", "DELETE"),
    ]
    
    results = []
    
    for message, expected_action in tests:
        print(f"\n[TEST] Message: '{message}'")
        print(f"       Expected: {expected_action}")
        
        payload = {"message": message}
        print(f"       Payload: {json.dumps(payload)}")
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/chat/process_public",
                json=payload,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                action = data.get("action_performed", "NONE")
                reply = data.get("reply", "")[:80]
                
                success = (action == expected_action)
                status = "[PASS]" if success else "[FAIL]"
                
                print(f"       Status: {response.status_code}")
                print(f"       Action: {action}")
                print(f"       Reply: {reply}...")
                print(f"       {status}")
                
                results.append((message, expected_action, action, success))
            else:
                print(f"       Status: {response.status_code}")
                print(f"       Error: {response.text[:100]}")
                print(f"       [FAIL]")
                results.append((message, expected_action, "ERROR", False))
                
        except requests.exceptions.ConnectionError:
            print(f"       [ERROR] Backend not reachable at {BACKEND_URL}")
            print(f"              Start the backend first!")
            return False
        except Exception as e:
            print(f"       [ERROR] {e}")
            results.append((message, expected_action, "ERROR", False))
    
    # Summary
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    
    passed = sum(1 for _, _, _, success in results if success)
    total = len(results)
    
    for message, expected, actual, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status}: '{message}' (expected {expected}, got {actual})")
    
    print(f"\nPassed: {passed}/{total}")
    return passed == total

if __name__ == "__main__":
    try:
        success = test_api()
        exit(0 if success else 1)
    except Exception as e:
        print(f"[FATAL] {e}")
        exit(1)
