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


def test_logout_success(client):
    """Test successful user logout."""
    # Register a user
    user_data = {
        "email": "logout_test@example.com",
        "password": "SecurePassword123!"
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201

    # Login to get a token
    login_data = {
        "email": "logout_test@example.com",
        "password": "SecurePassword123!"
    }

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Use the token to access the profile (should work before logout)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/profile", headers=headers)
    assert response.status_code == 200

    # Logout
    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out"

    # Try to access the profile again (should fail after logout)
    response = client.get("/auth/profile", headers=headers)
    assert response.status_code == 401


def test_logout_with_invalid_token(client):
    """Test logout with invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.post("/auth/logout", headers=headers)

    # Should return 400 for invalid token or 401 for unauthorized
    assert response.status_code in [400, 401]


def test_logout_without_token(client):
    """Test logout without token."""
    response = client.post("/auth/logout")

    # Should return 401 for unauthorized
    assert response.status_code == 401


def test_logout_twice_same_token(client):
    """Test that logging out the same token twice works for the first time but fails the second."""
    # Register a user
    user_data = {
        "email": "logout_twice_test@example.com",
        "password": "SecurePassword123!"
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201

    # Login to get a token
    login_data = {
        "email": "logout_twice_test@example.com",
        "password": "SecurePassword123!"
    }

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # First logout should succeed
    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out"

    # Second logout with same token should fail
    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 401  # Token is now blacklisted