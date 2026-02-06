#!/usr/bin/env python3
"""
Test script to validate the email normalization fix.
This script tests that emails with different cases or whitespace
are properly normalized and treated as the same email.
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

def test_email_case_normalization():
    """Test that emails with different cases are treated as the same"""
    print("Testing email case normalization...")
    
    # First, register a user with lowercase email
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
    
    print("OK Successfully registered user with lowercase email")
    
    # Now try to register with the same email but different case
    response = client.post(
        "/auth/register",
        json={
            "email": "TEST@EXAMPLE.COM",  # Same email but in uppercase
            "password": "differentpassword123"
        }
    )
    
    # Check that we get a 409 Conflict status (emails should be treated as same)
    if response.status_code != 409:
        print(f"X Expected status 409 for case-insensitive match, got {response.status_code}")
        return False
    
    print("OK Got 409 Conflict status for different case email (as expected)")
    
    # Check that the error message is meaningful
    response_data = response.json()
    expected_message = "A user with this email already exists"
    
    if expected_message not in response_data.get("detail", ""):
        print(f"X Expected error message to contain '{expected_message}', got: {response_data}")
        return False
    
    print(f"OK Got expected error message for case normalization")
    
    return True

def test_email_whitespace_normalization():
    """Test that emails with different whitespace are treated as the same"""
    print("Testing email whitespace normalization...")
    
    # Clear the database by recreating tables
    SQLModel.metadata.drop_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)
    
    # First, register a user with email that has no extra whitespace
    response = client.post(
        "/auth/register",
        json={
            "email": "test2@example.com",
            "password": "testpassword123"
        }
    )
    
    if response.status_code != 201:
        print(f"X Failed to register initial user. Status: {response.status_code}")
        return False
    
    print("OK Successfully registered user with clean email")
    
    # Now try to register with the same email but with extra whitespace
    response = client.post(
        "/auth/register",
        json={
            "email": "  test2@example.com  ",  # Same email but with leading/trailing spaces
            "password": "differentpassword123"
        }
    )
    
    # Check that we get a 409 Conflict status (emails should be treated as same)
    if response.status_code != 409:
        print(f"X Expected status 409 for whitespace-normalized match, got {response.status_code}")
        return False
    
    print("OK Got 409 Conflict status for email with extra whitespace (as expected)")
    
    # Check that the error message is meaningful
    response_data = response.json()
    expected_message = "A user with this email already exists"
    
    if expected_message not in response_data.get("detail", ""):
        print(f"X Expected error message to contain '{expected_message}', got: {response_data}")
        return False
    
    print(f"OK Got expected error message for whitespace normalization")
    
    return True

def test_successful_registration_with_normalization():
    """Test that a truly unique email (after normalization) can register successfully"""
    print("Testing successful registration with a unique email...")
    
    # Clear the database by recreating tables
    SQLModel.metadata.drop_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)
    
    # Register a user with an email
    response = client.post(
        "/auth/register",
        json={
            "email": "unique@example.com",
            "password": "testpassword123"
        }
    )
    
    if response.status_code != 201:
        print(f"X Failed to register user. Status: {response.status_code}")
        return False
    
    print("OK Successfully registered first user")
    
    # Try to register with a different email
    response = client.post(
        "/auth/register",
        json={
            "email": "different@example.com",
            "password": "anotherpassword123"
        }
    )
    
    # This should succeed since it's a different email
    if response.status_code != 201:
        print(f"X Expected successful registration for different email, got {response.status_code}")
        return False
    
    print("OK Successfully registered second user with different email")
    
    return True

def main():
    print("Testing email normalization functionality...")
    print("=" * 50)
    
    success1 = test_email_case_normalization()
    print()
    success2 = test_email_whitespace_normalization()
    print()
    success3 = test_successful_registration_with_normalization()
    
    print("=" * 50)
    if success1 and success2 and success3:
        print("OK All email normalization tests passed!")
        return 0
    else:
        print("X Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())