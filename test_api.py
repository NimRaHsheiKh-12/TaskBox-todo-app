import requests
import json

# Test the chat API
url = 'http://localhost:8000/chat/process_public'
data = {
    'user_id': 'temp_123456',
    'message': 'Add buy groceries'
}

try:
    response = requests.post(url, json=data)
    print('Status Code:', response.status_code)
    if response.status_code == 500:
        print('Error Response:', response.text)
    else:
        print('Response:', response.json())
except Exception as e:
    print('Error:', str(e))