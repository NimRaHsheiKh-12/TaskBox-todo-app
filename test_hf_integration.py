"""
Test script to verify Hugging Face MCP integration
"""
import asyncio
import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.src.services.hf_mcp_service import hf_mcp_service


async def test_hf_integration():
    print("Testing Hugging Face MCP Integration...")
    print(f"Service available: {hf_mcp_service.is_available()}")
    print(f"Model name: {hf_mcp_service.model_name}")
    
    # Test basic text generation
    print("\n--- Testing Text Generation ---")
    try:
        response = await hf_mcp_service.generate_text(
            prompt="Hello, how are you?",
            max_tokens=50,
            temperature=0.7
        )
        print(f"Generated response: {response}")
    except Exception as e:
        print(f"Text generation failed: {e}")
    
    # Test with a task-related prompt
    print("\n--- Testing Task-Related Prompt ---")
    try:
        response = await hf_mcp_service.generate_text(
            prompt="How can I organize my daily tasks effectively?",
            max_tokens=100,
            temperature=0.7
        )
        print(f"Task-related response: {response}")
    except Exception as e:
        print(f"Task-related generation failed: {e}")
    
    # Test chat completion if available
    print("\n--- Testing Chat Completion ---")
    try:
        messages = [
            {"role": "user", "content": "What is the weather like today?"},
            {"role": "assistant", "content": "I'm sorry, I don't have access to real-time weather information."},
            {"role": "user", "content": "Can you help me manage my tasks?"}
        ]
        response = await hf_mcp_service.chat_completion(
            messages=messages,
            max_tokens=80,
            temperature=0.7
        )
        print(f"Chat completion response: {response}")
    except Exception as e:
        print(f"Chat completion failed: {e}")
    
    print("\n--- Testing Completed ---")


if __name__ == "__main__":
    asyncio.run(test_hf_integration())