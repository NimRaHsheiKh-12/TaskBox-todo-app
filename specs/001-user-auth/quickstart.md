# Quickstart Guide: User Authentication Module

## Prerequisites

- Python 3.11+
- PostgreSQL database
- pip package manager
- virtual environment tool (optional but recommended)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todo_fullstack_app
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-dotenv pytest
```

### 4. Environment Configuration
Create a `.env` file in the project root with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/todoapp
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Important**: Use a strong, randomly generated secret key in production.

### 5. Database Setup
1. Ensure PostgreSQL is running
2. Update the DATABASE_URL in your .env file with your database credentials
3. Run database migrations (or create tables manually for initial setup)

## Running the Application

### Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Or using a production ASGI server like Gunicorn:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## API Endpoints

### Register a New User
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }'
```

### Access Protected Endpoint
```bash
curl -X GET "http://localhost:8000/auth/profile" \
  -H "Authorization: Bearer <your-jwt-token>"
```

## Testing

### Run Unit Tests
```bash
pytest
```

### Run Tests with Coverage
```bash
pytest --cov=.
```

## Project Structure
```
todo_fullstack_app/
├── main.py                 # Application entry point
├── models/                 # Database models
│   └── user.py
├── schemas/                # Pydantic schemas
│   └── user.py
├── database/               # Database configuration
│   └── database.py
├── auth/                   # Authentication logic
│   └── auth_handler.py
├── api/                    # API routes
│   └── auth.py
├── utils/                  # Utility functions
│   ├── password.py
│   └── token.py
├── requirements.txt        # Dependencies
├── tests/                  # Test files
│   ├── test_auth.py
│   └── conftest.py
└── .env                    # Environment variables
```

## Configuration Options

### JWT Settings
- `JWT_SECRET_KEY`: Secret key for signing JWT tokens
- `JWT_ALGORITHM`: Algorithm used for signing (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes

### Database Settings
- `DATABASE_URL`: Connection string for the PostgreSQL database

## Security Best Practices

1. Always use HTTPS in production
2. Store JWT secrets securely (environment variables or secret management system)
3. Implement rate limiting on authentication endpoints
4. Use strong password requirements
5. Regularly rotate JWT secrets
6. Implement proper logging and monitoring

## Troubleshooting

### Common Issues

1. **Database Connection Error**: Verify that PostgreSQL is running and credentials in DATABASE_URL are correct
2. **JWT Token Issues**: Check that JWT_SECRET_KEY is properly set and matches between token generation and validation
3. **Password Hashing Error**: Ensure passlib[bcrypt] is installed correctly

### Getting Help
- Check the API documentation at `/docs` when running the development server
- Review the logs for error details
- Consult the project's issue tracker