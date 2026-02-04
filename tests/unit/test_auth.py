import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import Mock, patch
import sys
import os

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'src'))

# Import using the full module path
from backend.src.schemas.user import UserRegistrationRequest
from backend.src.services.user_service import UserService
from backend.src.utils.password import hash_password, verify_password
from backend.src.utils.token import create_access_token, verify_token
from datetime import timedelta


# Test User Registration Request Schema
def test_user_registration_request_valid():
    """Test that UserRegistrationRequest validates correctly with valid data."""
    user_data = UserRegistrationRequest(email="test@example.com", password="SecurePassword123!")
    assert user_data.email == "test@example.com"
    assert user_data.password == "SecurePassword123!"


def test_user_registration_request_invalid_email():
    """Test that UserRegistrationRequest fails validation with invalid email."""
    with pytest.raises(ValueError):
        UserRegistrationRequest(email="invalid_email", password="SecurePassword123!")


# Test Password Utilities
def test_password_hashing():
    """Test that password hashing works correctly."""
    plain_password = "SecurePassword123!"
    hashed = hash_password(plain_password)
    
    # Verify the password can be verified against the hash
    assert verify_password(plain_password, hashed)
    
    # Verify a different password doesn't match
    assert not verify_password("DifferentPassword", hashed)


def test_password_verification():
    """Test that password verification works correctly."""
    plain_password = "SecurePassword123!"
    wrong_password = "WrongPassword456!"
    hashed = hash_password(plain_password)
    
    # Correct password should verify
    assert verify_password(plain_password, hashed)
    
    # Wrong password should not verify
    assert not verify_password(wrong_password, hashed)


# Test Token Utilities
def test_create_and_verify_token():
    """Test that tokens can be created and verified."""
    data = {"sub": "user123", "email": "test@example.com"}
    token = create_access_token(data)
    
    # Verify the token
    payload = verify_token(token)
    
    # Check that the payload contains the expected data
    assert payload is not None
    assert payload["sub"] == "user123"
    assert payload["email"] == "test@example.com"
    
    # Check that expiration is included
    assert "exp" in payload


def test_token_verification_with_expiration():
    """Test that tokens expire correctly."""
    data = {"sub": "user123", "email": "test@example.com"}
    # Create a token that expires in 1 second
    token = create_access_token(data, expires_delta=timedelta(seconds=1))
    
    # Immediately verify - should work
    payload = verify_token(token)
    assert payload is not None
    
    # Wait for expiration and verify - should fail
    import time
    time.sleep(2)  # Wait 2 seconds to ensure expiration
    
    payload_after_expiration = verify_token(token)
    assert payload_after_expiration is None


def test_invalid_token():
    """Test that invalid tokens are rejected."""
    invalid_token = "invalid.token.here"
    payload = verify_token(invalid_token)
    assert payload is None


# Test User Service
def test_create_user():
    """Test that users can be created correctly."""
    # Create a mock database session
    mock_db = Mock()

    # Mock user data
    user_data = UserRegistrationRequest(email="test@example.com", password="SecurePassword123!")

    # Call the create_user method
    created_user = UserService.create_user(mock_db, user_data)

    # Verify the database methods were called correctly
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    # Verify the created user has the correct email
    assert created_user.email == "test@example.com"
    # Verify the created user has an ID and created_at timestamp
    assert created_user.id is not None
    assert created_user.created_at is not None


def test_get_user_by_email():
    """Test that users can be retrieved by email."""
    # Create a mock database session
    mock_db = Mock()

    # Mock user object
    mock_user = Mock()
    mock_user.id = "123"
    mock_user.email = "test@example.com"
    mock_user.password_hash = "hashed_password"

    # Set up the mock to return our mock user
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = mock_user
    mock_db.execute.return_value = mock_result

    # Call the get_user_by_email method
    result = UserService.get_user_by_email(mock_db, "test@example.com")

    # Verify the database query was called correctly
    mock_db.execute.assert_called_once()

    # Verify the returned user is correct
    assert result == mock_user


def test_authenticate_user_success():
    """Test successful user authentication."""
    from datetime import datetime

    # Create a mock database session
    mock_db = Mock()

    # Mock user object with a hashed password
    plain_password = "SecurePassword123!"
    hashed_password = hash_password(plain_password)

    # Create a mock user with required attributes
    mock_user = Mock()
    mock_user.id = "123"
    mock_user.email = "test@example.com"
    mock_user.password_hash = hashed_password
    mock_user.created_at = datetime.utcnow()  # Add the created_at field

    # Mock the get_user_by_email method to return our mock user
    with patch.object(UserService, 'get_user_by_email', return_value=mock_user):
        # Call the authenticate_user method
        result = UserService.authenticate_user(mock_db, "test@example.com", plain_password)

        # Verify the authentication was successful
        assert result.email == "test@example.com"
        assert result.id == "123"


def test_authenticate_user_wrong_password():
    """Test authentication failure with wrong password."""
    # Create a mock database session
    mock_db = Mock()

    # Mock user object with a hashed password
    correct_password = "SecurePassword123!"
    hashed_password = hash_password(correct_password)

    # Create a mock user with required attributes
    mock_user = Mock()
    mock_user.id = "123"
    mock_user.email = "test@example.com"
    mock_user.password_hash = hashed_password

    # Mock the get_user_by_email method to return our mock user
    with patch.object(UserService, 'get_user_by_email', return_value=mock_user):
        # Call the authenticate_user method with wrong password
        result = UserService.authenticate_user(mock_db, "test@example.com", "WrongPassword!")

        # Verify the authentication failed
        assert result is None


def test_authenticate_user_nonexistent_email():
    """Test authentication failure with non-existent email."""
    # Create a mock database session
    mock_db = Mock()

    # Mock the get_user_by_email method to return None
    with patch.object(UserService, 'get_user_by_email', return_value=None):
        # Call the authenticate_user method
        result = UserService.authenticate_user(mock_db, "nonexistent@example.com", "AnyPassword!")

        # Verify the authentication failed
        assert result is None