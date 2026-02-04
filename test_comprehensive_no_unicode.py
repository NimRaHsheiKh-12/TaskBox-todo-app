import requests
import json

BASE_URL = "http://localhost:8000"

def test_chatbot_crud():
    """Test all CRUD operations of the chatbot"""
    user_id = "test_user_123"
    
    print("=== Testing Chatbot CRUD Operations ===\n")
    
    # Test 1: Create a task
    print("1. Testing CREATE operation...")
    create_response = requests.post(f"{BASE_URL}/chat/process_public", json={
        "user_id": user_id,
        "message": "Add buy groceries to my list",
        "current_tasks": []
    })
    print(f"   Status: {create_response.status_code}")
    create_data = create_response.json()
    print(f"   Action: {create_data.get('action_performed', 'N/A')}")
    print(f"   Success: {create_data.get('success', 'N/A')}")
    print(f"   Tasks count: {len(create_data.get('updated_tasks', []))}")
    
    # Store the created task for later operations
    updated_tasks = create_data.get('updated_tasks', [])
    
    # Test 2: Read tasks
    print("\n2. Testing READ operation...")
    read_response = requests.post(f"{BASE_URL}/chat/process_public", json={
        "user_id": user_id,
        "message": "Show my tasks",
        "current_tasks": updated_tasks
    })
    print(f"   Status: {read_response.status_code}")
    read_data = read_response.json()
    print(f"   Action: {read_data.get('action_performed', 'N/A')}")
    print(f"   Success: {read_data.get('success', 'N/A')}")
    
    # Test 3: Update a task (if one exists)
    print("\n3. Testing UPDATE operation...")
    if updated_tasks:
        task_title = updated_tasks[0]['title']
        update_response = requests.post(f"{BASE_URL}/chat/process_public", json={
            "user_id": user_id,
            "message": f"Update {task_title} to buy groceries and household items",
            "current_tasks": updated_tasks
        })
        print(f"   Status: {update_response.status_code}")
        update_data = update_response.json()
        print(f"   Action: {update_data.get('action_performed', 'N/A')}")
        print(f"   Success: {update_data.get('success', 'N/A')}")
        updated_tasks = update_data.get('updated_tasks', [])
    else:
        print("   Skipping update test - no tasks available")
    
    # Test 4: Complete a task (if one exists)
    print("\n4. Testing COMPLETE operation...")
    if updated_tasks:
        task_title = updated_tasks[0]['title']
        complete_response = requests.post(f"{BASE_URL}/chat/process_public", json={
            "user_id": user_id,
            "message": f"Complete {task_title}",
            "current_tasks": updated_tasks
        })
        print(f"   Status: {complete_response.status_code}")
        complete_data = complete_response.json()
        print(f"   Action: {complete_data.get('action_performed', 'N/A')}")
        print(f"   Success: {complete_data.get('success', 'N/A')}")
        updated_tasks = complete_data.get('updated_tasks', [])
    else:
        print("   Skipping completion test - no tasks available")
    
    # Test 5: Delete a task (if one exists)
    print("\n5. Testing DELETE operation...")
    if updated_tasks:
        task_title = updated_tasks[0]['title']
        delete_response = requests.post(f"{BASE_URL}/chat/process_public", json={
            "user_id": user_id,
            "message": f"Delete {task_title}",
            "current_tasks": updated_tasks
        })
        print(f"   Status: {delete_response.status_code}")
        delete_data = delete_response.json()
        print(f"   Action: {delete_data.get('action_performed', 'N/A')}")
        print(f"   Success: {delete_data.get('success', 'N/A')}")
    else:
        print("   Skipping deletion test - no tasks available")
    
    print("\n=== All tests completed ===")

if __name__ == "__main__":
    test_chatbot_crud()