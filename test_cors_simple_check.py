import requests

# Test the OPTIONS request to check CORS headers on the simple server
try:
    response = requests.options('http://localhost:8001/test-register',
                               headers={'Access-Control-Request-Method': 'POST',
                                        'Access-Control-Request-Headers': 'Content-Type'})
    
    print("Simple Server - Status Code:", response.status_code)
    print("Headers:")
    for header, value in response.headers.items():
        print(f"  {header}: {value}")
        
    if 'access-control-allow-origin' in response.headers:
        print("\nCORS is properly configured on simple server!")
    else:
        print("\nCORS header is missing on simple server!")
        
except requests.exceptions.ConnectionError:
    print("Could not connect to the simple server. Is it running?")
except Exception as e:
    print(f"An error occurred: {e}")