#!/usr/bin/env python3
"""
Test the /chat API endpoints to verify they work correctly
"""
import requests
import json

BASE_URL = 'http://localhost:8000'

def test_chat_endpoints():
    print('Testing /chat API endpoints...')

    # Test greeting
    print('\n1. Testing greeting...')
    test_data = {'message': 'hello', 'user_id': 'test-user-123'}
    try:
        response = requests.post(f'{BASE_URL}/chat/process_public', json=test_data, timeout=5)
        print(f'   Status: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print(f'   Response: {data}')
            if 'reply' in data and data['reply']:
                print('   ✓ Greeting test passed')
            else:
                print('   ❌ Greeting test failed - no reply field')
        else:
            print(f'   ❌ Greeting test failed - status {response.status_code}')
    except Exception as e:
        print(f'   ❌ Greeting test failed - exception: {e}')

    # Test CREATE
    print('\n2. Testing CREATE...')
    test_data = {'message': 'add buy coffee', 'user_id': 'test-user-123'}
    try:
        response = requests.post(f'{BASE_URL}/chat/process_public', json=test_data, timeout=5)
        print(f'   Status: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print(f'   Response: {data}')
            if 'reply' in data and data['reply']:
                print('   ✓ CREATE test passed')
            else:
                print('   ❌ CREATE test failed - no reply field')
        else:
            print(f'   ❌ CREATE test failed - status {response.status_code}')
    except Exception as e:
        print(f'   ❌ CREATE test failed - exception: {e}')

    # Test READ
    print('\n3. Testing READ...')
    test_data = {'message': 'show my tasks', 'user_id': 'test-user-123'}
    try:
        response = requests.post(f'{BASE_URL}/chat/process_public', json=test_data, timeout=5)
        print(f'   Status: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print(f'   Response: {data}')
            if 'reply' in data and data['reply']:
                print('   ✓ READ test passed')
            else:
                print('   ❌ READ test failed - no reply field')
        else:
            print(f'   ❌ READ test failed - status {response.status_code}')
    except Exception as e:
        print(f'   ❌ READ test failed - exception: {e}')

    print('\nAPI endpoint testing completed.')

if __name__ == '__main__':
    test_chat_endpoints()