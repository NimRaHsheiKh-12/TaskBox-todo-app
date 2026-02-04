# API Contract: User Authentication

## Overview
This document defines the API contracts for the user authentication module. All endpoints require HTTPS in production.

## Base URL
```
https://api.todoapp.com/auth
```

## Authentication
- Registration and login endpoints do not require authentication
- All other endpoints require a valid JWT token in the Authorization header
- Format: `Authorization: Bearer <token>`

## Common Headers
- `Content-Type: application/json`
- `Accept: application/json`

## Error Response Format
```json
{
  "detail": "Error message"
}
```

## Endpoints

### 1. User Registration
- **Endpoint**: `POST /register`
- **Description**: Register a new user with email and password
- **Authentication**: None required

#### Request
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

#### Request Validation
- Email must be a valid email format
- Password must be at least 8 characters long
- Email must be unique

#### Success Response (201 Created)
```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "email": "user@example.com",
  "created_at": "2023-01-01T10:00:00Z"
}
```

#### Error Responses
- `400 Bad Request`: Invalid request format or validation errors
- `409 Conflict`: Email already registered

### 2. User Login
- **Endpoint**: `POST /login`
- **Description**: Authenticate user and return JWT token
- **Authentication**: None required

#### Request
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

#### Success Response (200 OK)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Error Responses
- `400 Bad Request`: Invalid request format
- `401 Unauthorized`: Invalid credentials

### 3. User Profile (Protected)
- **Endpoint**: `GET /profile`
- **Description**: Get authenticated user's profile information
- **Authentication**: JWT token required

#### Success Response (200 OK)
```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "email": "user@example.com",
  "created_at": "2023-01-01T10:00:00Z"
}
```

#### Error Responses
- `401 Unauthorized`: Invalid or missing token

### 4. Token Validation (Protected)
- **Endpoint**: `POST /validate-token`
- **Description**: Validate JWT token without returning user data
- **Authentication**: JWT token required

#### Success Response (200 OK)
```json
{
  "valid": true,
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
}
```

#### Error Responses
- `401 Unauthorized`: Invalid or missing token

## Security Considerations
- Passwords must never be returned in any response
- Use HTTPS for all requests in production
- JWT tokens should be stored securely on the client
- Implement rate limiting on authentication endpoints
- Use secure, HttpOnly cookies for token storage if applicable

## Rate Limits
- Registration: 5 requests per hour per IP
- Login: 10 attempts per 15 minutes per IP
- All other endpoints: 1000 requests per hour per user

## Future Extensions
- `/refresh` endpoint for token refresh (to be implemented)
- `/logout` endpoint for token invalidation (to be implemented)
- `/forgot-password` and `/reset-password` endpoints (to be implemented)