import asyncio
import aiohttp
import json

async def test_chatbot():
    """Test the chatbot functionality directly"""
    
    base_url = "http://localhost:8000"
    
    # Test 1: Test the public chat endpoint
    print("Testing public chat endpoint...")
    
    async with aiohttp.ClientSession() as session:
        # Test creating a task
        print("\n1. Testing task creation...")
        create_payload = {
            "user_id": "test_user_123",
            "message": "Add buy groceries to my list",
            "current_tasks": []
        }
        
        try:
            async with session.post(f"{base_url}/chat/process_public", json=create_payload) as response:
                result = await response.json()
                print(f"Status: {response.status}")
                print(f"Response: {json.dumps(result, indent=2)}")
                
                if response.status == 200:
                    print("[PASS] Task creation test passed")
                else:
                    print("[FAIL] Task creation test failed")
                    
        except Exception as e:
            print(f"[ERROR] Error during task creation test: {e}")
            
        # Test reading tasks
        print("\n2. Testing task reading...")
        read_payload = {
            "user_id": "test_user_123",
            "message": "Show my tasks",
            "current_tasks": result.get("updated_tasks", []) if 'result' in locals() else []
        }
        
        try:
            async with session.post(f"{base_url}/chat/process_public", json=read_payload) as response:
                result = await response.json()
                print(f"Status: {response.status}")
                print(f"Response: {json.dumps(result, indent=2)}")
                
                if response.status == 200:
                    print("[PASS] Task reading test passed")
                else:
                    print("[FAIL] Task reading test failed")
                    
        except Exception as e:
            print(f"[ERROR] Error during task reading test: {e}")
            
        # Test completing a task
        print("\n3. Testing task completion...")
        if 'result' in locals() and result.get("updated_tasks"):
            complete_payload = {
                "user_id": "test_user_123",
                "message": f"Complete {result['updated_tasks'][0]['title']}",
                "current_tasks": result.get("updated_tasks", [])
            }
            
            try:
                async with session.post(f"{base_url}/chat/process_public", json=complete_payload) as response:
                    result = await response.json()
                    print(f"Status: {response.status}")
                    print(f"Response: {json.dumps(result, indent=2)}")
                    
                    if response.status == 200:
                        print("[PASS] Task completion test passed")
                    else:
                        print("[FAIL] Task completion test failed")
                        
            except Exception as e:
                print(f"[ERROR] Error during task completion test: {e}")
        else:
            print("Cannot test task completion - no tasks available")
            
        # Test updating a task
        print("\n4. Testing task update...")
        if 'result' in locals() and result.get("updated_tasks"):
            update_payload = {
                "user_id": "test_user_123",
                "message": f"Update {result['updated_tasks'][0]['title']} to buy groceries and household items",
                "current_tasks": result.get("updated_tasks", [])
            }
            
            try:
                async with session.post(f"{base_url}/chat/process_public", json=update_payload) as response:
                    result = await response.json()
                    print(f"Status: {response.status}")
                    print(f"Response: {json.dumps(result, indent=2)}")
                    
                    if response.status == 200:
                        print("[PASS] Task update test passed")
                    else:
                        print("[FAIL] Task update test failed")
                        
            except Exception as e:
                print(f"[ERROR] Error during task update test: {e}")
        else:
            print("Cannot test task update - no tasks available")
            
        # Test deleting a task
        print("\n5. Testing task deletion...")
        if 'result' in locals() and result.get("updated_tasks"):
            delete_payload = {
                "user_id": "test_user_123",
                "message": f"Delete {result['updated_tasks'][0]['title']}",
                "current_tasks": result.get("updated_tasks", [])
            }
            
            try:
                async with session.post(f"{base_url}/chat/process_public", json=delete_payload) as response:
                    result = await response.json()
                    print(f"Status: {response.status}")
                    print(f"Response: {json.dumps(result, indent=2)}")
                    
                    if response.status == 200:
                        print("[PASS] Task deletion test passed")
                    else:
                        print("[FAIL] Task deletion test failed")
                        
            except Exception as e:
                print(f"[ERROR] Error during task deletion test: {e}")
        else:
            print("Cannot test task deletion - no tasks available")

if __name__ == "__main__":
    asyncio.run(test_chatbot())