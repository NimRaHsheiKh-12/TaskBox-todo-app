import requests

# Test the OPTIONS request to check CORS headers on the test server with middleware
try:
    response = requests.options('http://localhost:8002/auth/register',
                               headers={'Access-Control-Request-Method': 'POST',
                                        'Access-Control-Request-Headers': 'Content-Type'})
    
    print("Test Server with Middleware - Status Code:", response.status_code)
    print("Headers:")
    for header, value in response.headers.items():
        print(f"  {header}: {value}")
        
    if 'access-control-allow-origin' in response.headers:
        print("\nCORS is properly configured on test server!")
    else:
        print("\nCORS header is missing on test server!")
        
except requests.exceptions.ConnectionError:
    print("Could not connect to the test server. Is it running?")
except Exception as e:
    print(f"An error occurred: {e}")