#!/usr/bin/env python3
"""
Test script to validate the registration error handling fix.
This script tests that the registration endpoint properly returns 
a 409 Conflict error with a meaningful message when trying to 
register with an existing email.
"""

import sys
import os

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from backend.src.database.database import get_db
from backend.src.api.auth import router as auth_router
from backend.src.models.user import User
from backend.src.schemas.user import UserRegistrationRequest
from backend.src.services.user_service import UserService

# Create an in-memory SQLite database for testing
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the test database tables
SQLModel.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Create a test app with just the auth router
app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_registration_conflict_error():
    """Test that registration with existing email returns 409 with proper message"""
    print("Testing registration conflict error handling...")
    
    # First, register a user successfully
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    
    if response.status_code != 201:
        print(f"X Failed to register initial user. Status: {response.status_code}")
        return False

    print("OK Successfully registered initial user")

    # Now try to register with the same email
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",  # Same email as before
            "password": "differentpassword123"
        }
    )

    # Check that we get a 409 Conflict status
    if response.status_code != 409:
        print(f"X Expected status 409, got {response.status_code}")
        return False

    print("OK Got 409 Conflict status as expected")

    # Check that the error message is meaningful
    response_data = response.json()
    if "detail" not in response_data:
        print("X Response doesn't contain 'detail' field")
        return False

    detail = response_data["detail"]
    expected_message = "A user with this email already exists"

    if expected_message not in detail:
        print(f"X Expected error message to contain '{expected_message}', got: {detail}")
        return False

    print(f"OK Got expected error message: {detail}")

    return True

def main():
    print("Testing registration error handling fix...")
    print("=" * 50)

    success = test_registration_conflict_error()

    print("=" * 50)
    if success:
        print("OK All tests passed! The registration error handling fix is working correctly.")
        return 0
    else:
        print("X Tests failed! There may be an issue with the error handling.")
        return 1

if __name__ == "__main__":
    sys.exit(main())