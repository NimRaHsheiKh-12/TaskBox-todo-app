# Data Model: User Authentication

## User Entity

### Fields
- **id**: UUID (Primary Key)
  - Type: UUID (database) / str (Python)
  - Constraints: Unique, Not Null, Auto-generated
  - Description: Unique identifier for each user

- **email**: User's email address
  - Type: String
  - Constraints: Unique, Not Null, Valid email format
  - Max Length: 255 characters
  - Description: User's unique email used for authentication

- **password_hash**: Hashed password
  - Type: String
  - Constraints: Not Null
  - Max Length: 255 characters
  - Description: Securely hashed password using bcrypt

- **created_at**: Account creation timestamp
  - Type: DateTime (UTC)
  - Constraints: Not Null, Auto-generated on creation
  - Description: Timestamp when the user account was created

- **updated_at**: Last update timestamp
  - Type: DateTime (UTC)
  - Constraints: Not Null, Auto-updated on modification
  - Description: Timestamp when the user account was last updated

### Relationships
- No relationships needed for the User entity in this authentication module
- Future task entities will have a foreign key relationship to User.id

### Validation Rules
- Email must follow standard email format (using Pydantic EmailStr)
- Email must be unique across all users
- Password must be securely hashed before storing (never store plaintext)
- Email cannot be changed after account creation (for simplicity and security)

### State Transitions
- User account is created in 'active' state upon successful registration
- No state transitions required in this initial implementation
- Future enhancements might include 'suspended' or 'deleted' states

## JWT Token Structure

### Access Token Payload
- **sub**: Subject (user's UUID)
- **email**: User's email address
- **exp**: Expiration timestamp
- **iat**: Issued at timestamp
- **jti**: JWT ID for potential revocation

### Token Configuration
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Secret**: Environment variable (JWT_SECRET_KEY)
- **Expiration**: 15 minutes (900 seconds) for access tokens
- **Refresh Token**: 7 days (604800 seconds) - to be implemented in future iteration

## Database Schema

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for efficient email lookups during authentication
CREATE INDEX idx_users_email ON users(email);
```

## SQLAlchemy Model

```python
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
```

## Pydantic Models

### User Registration Request
```python
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegistrationRequest(BaseModel):
    email: EmailStr
    password: str  # Will be validated for minimum length and complexity
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePassword123!"
            }
        }
```

### User Login Request
```python
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePassword123!"
            }
        }
```

### User Response (without sensitive data)
```python
from datetime import datetime

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
```

### Token Response
```python
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
```