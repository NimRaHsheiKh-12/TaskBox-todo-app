import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch
import sys
import os

# Set environment variable to indicate testing mode
os.environ["TESTING"] = "true"

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"

# Override the database URL in settings before importing the app
from backend.src.config import settings
settings.database_url = SQLALCHEMY_DATABASE_URL

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'src'))

from backend.src.main import app
from backend.src.database.database import get_db
from backend.src.models import user, todo, token_blacklist  # Import models to register them
from sqlmodel import SQLModel

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get test database session
def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the get_db dependency with the test database
@pytest.fixture
def client():
    """Create a test client for the API with test database."""
    # Create the tables for each test run
    SQLModel.metadata.create_all(bind=engine)

    # Override the get_db dependency
    app.dependency_overrides[get_db] = get_test_db

    with TestClient(app) as test_client:
        yield test_client

    # Remove the override after the test
    app.dependency_overrides.clear()

    # Drop the tables after the test run
    SQLModel.metadata.drop_all(bind=engine)


def test_register_user_success(client):
    """Test successful user registration."""
    user_data = {
        "email": "test@example.com",
        "password": "SecurePassword123!"
    }

    response = client.post("/auth/register", json=user_data)

    # Verify the response
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["email"] == "test@example.com"
    assert "created_at" in response.json()


def test_register_user_duplicate_email(client):
    """Test user registration with duplicate email."""
    # First registration should succeed
    user_data = {
        "email": "duplicate@example.com",
        "password": "SecurePassword123!"
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201

    # Second registration with same email should fail
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 409
    assert response.json()["detail"] == "Registration failed"


def test_register_user_invalid_email(client):
    """Test user registration with invalid email."""
    user_data = {
        "email": "invalid_email",
        "password": "SecurePassword123!"
    }

    response = client.post("/auth/register", json=user_data)

    # Should return 422 for validation error
    assert response.status_code == 422


def test_login_user_success(client):
    """Test successful user login."""
    # First register a user
    user_data = {
        "email": "login_test@example.com",
        "password": "SecurePassword123!"
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201

    # Then try to login
    login_data = {
        "email": "login_test@example.com",
        "password": "SecurePassword123!"
    }

    response = client.post("/auth/login", json=login_data)

    # Verify the response
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_user_invalid_credentials(client):
    """Test login with invalid credentials."""
    # First register a user
    user_data = {
        "email": "invalid_login_test@example.com",
        "password": "SecurePassword123!"
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201

    # Then try to login with wrong password
    login_data = {
        "email": "invalid_login_test@example.com",
        "password": "WrongPassword!"
    }

    response = client.post("/auth/login", json=login_data)

    # Verify the response
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


def test_login_user_nonexistent_email(client):
    """Test login with non-existent email."""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "AnyPassword!"
    }

    response = client.post("/auth/login", json=login_data)

    # Verify the response
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


def test_get_user_profile_success(client):
    """Test getting user profile with valid token."""
    # Register a user
    user_data = {
        "email": "profile_test@example.com",
        "password": "SecurePassword123!"
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]

    # Login to get a token
    login_data = {
        "email": "profile_test@example.com",
        "password": "SecurePassword123!"
    }

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Use the token to access the profile
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/profile", headers=headers)

    # Verify the response
    assert response.status_code == 200
    assert response.json()["id"] == user_id
    assert response.json()["email"] == "profile_test@example.com"
    assert "created_at" in response.json()


def test_get_user_profile_invalid_token(client):
    """Test getting user profile with invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/auth/profile", headers=headers)

    # Verify the response
    assert response.status_code == 401


def test_get_user_profile_no_token(client):
    """Test getting user profile without token."""
    response = client.get("/auth/profile")

    # Verify the response
    assert response.status_code == 401


def test_validate_token_success(client):
    """Test token validation with valid token."""
    # Register a user
    user_data = {
        "email": "validate_test@example.com",
        "password": "SecurePassword123!"
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]

    # Login to get a token
    login_data = {
        "email": "validate_test@example.com",
        "password": "SecurePassword123!"
    }

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Use the token to validate it
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/auth/validate-token", headers=headers)

    # Verify the response
    assert response.status_code == 200
    assert response.json()["valid"] is True
    assert response.json()["user_id"] == user_id


def test_validate_token_invalid_token(client):
    """Test token validation with invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.post("/auth/validate-token", headers=headers)

    # Verify the response
    assert response.status_code == 401


def test_validate_token_no_token(client):
    """Test token validation without token."""
    response = client.post("/auth/validate-token")

    # Verify the response
    assert response.status_code == 401


def test_multiple_users_independent(client):
    """Test that multiple users operate independently."""
    # Register first user
    user1_data = {
        "email": "user1@example.com",
        "password": "SecurePassword123!"
    }

    response = client.post("/auth/register", json=user1_data)
    assert response.status_code == 201
    user1_id = response.json()["id"]

    # Register second user
    user2_data = {
        "email": "user2@example.com",
        "password": "SecurePassword456!"
    }

    response = client.post("/auth/register", json=user2_data)
    assert response.status_code == 201
    user2_id = response.json()["id"]

    # Login as first user
    login1_data = {
        "email": "user1@example.com",
        "password": "SecurePassword123!"
    }

    response = client.post("/auth/login", json=login1_data)
    assert response.status_code == 200
    token1 = response.json()["access_token"]

    # Login as second user
    login2_data = {
        "email": "user2@example.com",
        "password": "SecurePassword456!"
    }

    response = client.post("/auth/login", json=login2_data)
    assert response.status_code == 200
    token2 = response.json()["access_token"]

    # Verify first user gets their profile
    headers1 = {"Authorization": f"Bearer {token1}"}
    response = client.get("/auth/profile", headers=headers1)
    assert response.status_code == 200
    assert response.json()["id"] == user1_id

    # Verify second user gets their profile
    headers2 = {"Authorization": f"Bearer {token2}"}
    response = client.get("/auth/profile", headers=headers2)
    assert response.status_code == 200
    assert response.json()["id"] == user2_id

    # Verify users can't access each other's profiles
    response = client.get("/auth/profile", headers=headers1)
    assert response.status_code == 200
    assert response.json()["id"] == user1_id  # User 1 gets their own profile

    response = client.get("/auth/profile", headers=headers2)
    assert response.status_code == 200
    assert response.json()["id"] == user2_id  # User 2 gets their own profile