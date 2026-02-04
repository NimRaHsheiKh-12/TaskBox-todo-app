# Authentication Module Documentation

## Overview
The authentication module provides user registration, login, and protected route access functionality for the Todo Fullstack Application. It uses JWT tokens for authentication and bcrypt for password hashing.

## Features

### User Registration
- Allows new users to create an account with email and password
- Secure password hashing using bcrypt
- Email uniqueness validation
- Returns user profile information upon successful registration

### User Login
- Authenticates users with email and password
- Generates JWT access tokens upon successful authentication
- Secure credential validation
- Returns appropriate error messages for invalid credentials

### Protected Route Access
- Restricts access to protected application features using JWT tokens
- Validates JWT tokens for authorization
- Provides user profile access for authenticated users
- Token validation endpoint to verify token validity

## API Endpoints

### Registration
- **Endpoint**: `POST /auth/register`
- **Description**: Register a new user with email and password
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }
  ```
- **Response**: 201 Created with user information
- **Error Responses**: 400 Bad Request, 409 Conflict

### Login
- **Endpoint**: `POST /auth/login`
- **Description**: Authenticate user and return JWT token
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }
  ```
- **Response**: 200 OK with JWT token
- **Error Responses**: 400 Bad Request, 401 Unauthorized

### User Profile (Protected)
- **Endpoint**: `GET /auth/profile`
- **Description**: Get authenticated user's profile information
- **Authentication**: JWT token required in Authorization header
- **Response**: 200 OK with user information
- **Error Responses**: 401 Unauthorized

### Token Validation (Protected)
- **Endpoint**: `POST /auth/validate-token`
- **Description**: Validate JWT token without returning user data
- **Authentication**: JWT token required in Authorization header
- **Response**: 200 OK with validation result
- **Error Responses**: 401 Unauthorized

## Security Features

### Password Security
- Passwords are hashed using bcrypt before storage
- No plaintext passwords are stored in the database
- Secure password verification process

### JWT Token Security
- JWT tokens are signed using HS256 algorithm
- Tokens have a configurable expiration time (default 30 minutes)
- Secure token validation process

### Rate Limiting
- Registration: 5 requests per hour per IP
- Login: 10 attempts per 15 minutes per IP
- All other endpoints: 1000 requests per hour per user

## Configuration

The authentication module can be configured using environment variables:

- `DATABASE_URL`: PostgreSQL database connection string
- `JWT_SECRET_KEY`: Secret key for signing JWT tokens
- `JWT_ALGORITHM`: Algorithm used for signing (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes

## Implementation Details

### Tech Stack
- FastAPI: Web framework with automatic API documentation
- SQLAlchemy: ORM for database operations
- PostgreSQL: Relational database
- Pydantic: Data validation and settings management
- Python-Jose: JWT token handling
- Passlib: Password hashing utilities

### Database Schema
The authentication module uses a single `users` table with the following fields:
- `id`: UUID primary key
- `email`: Unique email address
- `password_hash`: Bcrypt hashed password
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

### Architecture
- **Models**: SQLAlchemy ORM models for database interaction
- **Schemas**: Pydantic models for request/response validation
- **Services**: Business logic encapsulation
- **API**: FastAPI route definitions
- **Utils**: Helper functions for token and password handling
- **Auth**: Authentication and authorization logic
- **Middleware**: Cross-cutting concerns like error handling and rate limiting