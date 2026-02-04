# API Documentation: Todo Fullstack Application

## Base URL
All API endpoints are relative to: `http://localhost:8000` (or your deployed domain)

## Authentication
Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### Authentication

#### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### POST /auth/login
Authenticate user and return JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "jwt-token-string",
  "token_type": "bearer"
}
```

#### GET /auth/profile
Get current user's profile information.

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### POST /auth/logout
Logout user by adding token to blacklist.

**Response (200 OK):**
```json
{
  "message": "Successfully logged out"
}
```

#### POST /auth/validate-token
Validate JWT token.

**Response (200 OK):**
```json
{
  "valid": true,
  "user_id": "uuid-string"
}
```

### Todo Management

#### GET /todos
List todos for the authenticated user.

**Query Parameters:**
- `search` (optional): Search term for title
- `status` (optional): "true" for completed, "false" for pending
- `priority` (optional): "Low", "Medium", "High"
- `category` (optional): Category name
- `due_date` (optional): "today", "upcoming", "overdue", or specific date in YYYY-MM-DD format
- `limit` (optional): Number of results (default: 100, max: 100)
- `offset` (optional): Offset for pagination (default: 0)

**Response (200 OK):**
```json
[
  {
    "id": "uuid-string",
    "user_id": "uuid-string",
    "title": "Todo title",
    "description": "Todo description",
    "is_completed": false,
    "priority": "Medium",
    "category": "Work",
    "due_date": "2023-12-31",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
]
```

#### POST /todos
Create a new todo for the authenticated user.

**Request Body:**
```json
{
  "title": "New todo title",
  "description": "Todo description",
  "priority": "Medium",
  "category": "Work",
  "due_date": "2023-12-31"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-string",
  "user_id": "uuid-string",
  "title": "New todo title",
  "description": "Todo description",
  "is_completed": false,
  "priority": "Medium",
  "category": "Work",
  "due_date": "2023-12-31",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### GET /todos/{id}
Get a specific todo for the authenticated user.

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "user_id": "uuid-string",
  "title": "Todo title",
  "description": "Todo description",
  "is_completed": false,
  "priority": "Medium",
  "category": "Work",
  "due_date": "2023-12-31",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### PUT /todos/{id}
Update a specific todo for the authenticated user.

**Request Body:**
```json
{
  "title": "Updated todo title",
  "description": "Updated description",
  "is_completed": true,
  "priority": "High",
  "category": "Personal",
  "due_date": "2023-12-31"
}
```

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "user_id": "uuid-string",
  "title": "Updated todo title",
  "description": "Updated description",
  "is_completed": true,
  "priority": "High",
  "category": "Personal",
  "due_date": "2023-12-31",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### PATCH /todos/{id}/toggle
Toggle completion status of a specific todo.

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "user_id": "uuid-string",
  "title": "Todo title",
  "description": "Todo description",
  "is_completed": true,
  "priority": "Medium",
  "category": "Work",
  "due_date": "2023-12-31",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### DELETE /todos/{id}
Delete a specific todo for the authenticated user.

**Response (204 No Content)**

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message explaining the issue"
}
```

## Rate Limiting

Authentication endpoints are rate limited:
- Registration: 5 requests per hour
- Login: 10 requests per 15 minutes
- Logout: 20 requests per minute
- Token validation: 30 requests per minute
- Profile access: 100 requests per minute