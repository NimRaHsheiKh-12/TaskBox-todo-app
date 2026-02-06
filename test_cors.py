import requests

# Test the OPTIONS request to check CORS headers
try:
    response = requests.options('http://localhost:8000/auth/register',
                               headers={'Access-Control-Request-Method': 'POST',
                                        'Access-Control-Request-Headers': 'Content-Type'})
    
    print("Status Code:", response.status_code)
    print("Headers:")
    for header, value in response.headers.items():
        print(f"  {header}: {value}")
        
    if 'access-control-allow-origin' in response.headers:
        print("\nCORS is properly configured!")
    else:
        print("\nCORS header is missing!")
        
except requests.exceptions.ConnectionError:
    print("Could not connect to the server. Is it running?")
except Exception as e:
    print(f"An error occurred: {e}")