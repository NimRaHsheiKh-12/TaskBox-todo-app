import requests

# Test the chat API
url = 'http://localhost:8000/chat/process_public'

# Test greeting
print("Testing greeting 'hi':")
data = {'message': 'hi'}
response = requests.post(url, json=data)
print('Status:', response.status_code)
print('Response:', response.json())
print()

# Test show my task
print("Testing 'show my task':")
data = {'message': 'show my task'}
response = requests.post(url, json=data)
print('Status:', response.status_code)
print('Response:', response.json())
print()

# Test add task
print("Testing 'add task':")
data = {'message': 'add task'}
response = requests.post(url, json=data)
print('Status:', response.status_code)
print('Response:', response.json())