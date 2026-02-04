"""
Quick test to verify Hugging Face MCP configuration
"""
import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.src.config import settings
from backend.app.src.services.hf_mcp_service import hf_mcp_service


def test_hf_config():
    print("Testing Hugging Face Configuration...")
    print(f"HF Token configured: {'Yes' if settings.hf_token else 'No'}")
    print(f"HF Model Name: {settings.hf_model_name}")
    print(f"HF Max Tokens: {settings.hf_max_tokens}")
    print(f"HF Temperature: {settings.hf_temperature}")

    print(f"\nService available: {hf_mcp_service.is_available()}")
    print(f"Service model name: {hf_mcp_service.model_name}")
    print(f"Service max tokens: {hf_mcp_service.max_tokens}")
    print(f"Service temperature: {hf_mcp_service.temperature}")

    print("\nConfiguration test completed successfully!")


if __name__ == "__main__":
    test_hf_config()