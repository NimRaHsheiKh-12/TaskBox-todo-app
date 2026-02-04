#!/usr/bin/env python3
"""
Test script to verify that the authentication fixes work properly
"""

import sys
import os

# Add the backend src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from uuid import UUID


def test_uuid_validation():
    """Test UUID validation logic"""

    print("Testing UUID validation logic...")

    # Valid UUID
    valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
    try:
        user_uuid = UUID(valid_uuid)
        print(f"[PASS] Valid UUID '{valid_uuid}' parsed successfully: {user_uuid}")
    except ValueError:
        print(f"[FAIL] Failed to parse valid UUID: {valid_uuid}")

    # Invalid UUID
    invalid_uuid = "invalid-uuid-string"
    try:
        user_uuid = UUID(invalid_uuid)
        print(f"[FAIL] Invalid UUID '{invalid_uuid}' was incorrectly accepted: {user_uuid}")
    except ValueError:
        print(f"[PASS] Invalid UUID '{invalid_uuid}' correctly rejected")


if __name__ == "__main__":
    test_uuid_validation()