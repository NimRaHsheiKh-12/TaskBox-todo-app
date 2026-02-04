import requests
import json

# Test a direct POST request to see if CORS works for actual requests
try:
    response = requests.post('http://localhost:8000/auth/register',
                            headers={'Content-Type': 'application/json'},
                            json={"email": "test@example.com", "password": "testpassword"})
    
    print("POST Request - Status Code:", response.status_code)
    print("Headers:")
    for header, value in response.headers.items():
        print(f"  {header}: {value}")
    
    print("Response Body:", response.text)
        
except requests.exceptions.ConnectionError:
    print("Could not connect to the server. Is it running?")
except Exception as e:
    print(f"An error occurred: {e}")