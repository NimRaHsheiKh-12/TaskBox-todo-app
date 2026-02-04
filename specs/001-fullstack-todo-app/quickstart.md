# Quickstart Guide: Full-Stack Todo Application with Authentication

## Prerequisites

- Python 3.11+
- Node.js 18+ (with npm or yarn)
- PostgreSQL (or NeonDB account)
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd todo_fullstack_app
```

### 2. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and JWT secret
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### 3. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend  # or cd ../frontend if you're in the backend directory
   ```

2. Install dependencies:
   ```bash
   npm install
   # or yarn install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your backend API URL
   ```

4. Start the development server:
   ```bash
   npm run dev
   # or yarn dev
   ```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost/dbname
JWT_SECRET_KEY=your-super-secret-jwt-signing-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=300  # 5 minutes in seconds
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_JWT_STORAGE_KEY=todo_app_jwt
```

## Running Tests

### Backend Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_auth.py
```

### Frontend Tests
```bash
# Run all tests
npm run test

# Run tests in watch mode
npm run test:watch
```

## API Documentation

The API documentation is available at:
- Local: http://localhost:8000/docs
- Local (alternative): http://localhost:8000/redoc

## Key Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/profile` - Get current user profile
- `POST /auth/logout` - Logout user

### Todo Management
- `GET /todos` - List user's todos
- `POST /todos` - Create a new todo
- `GET /todos/{id}` - Get a specific todo
- `PUT /todos/{id}` - Update a specific todo
- `PATCH /todos/{id}/toggle` - Toggle completion status
- `DELETE /tos/{id}` - Delete a specific todo

## Development Workflow

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the project's coding standards

3. Write tests for your new functionality

4. Run tests to ensure everything works:
   ```bash
   # Backend
   pytest
   
   # Frontend
   npm run test
   ```

5. Commit your changes with a descriptive message

6. Push your branch and create a pull request

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Ensure PostgreSQL is running
   - Verify DATABASE_URL in your .env file

2. **JWT Token Issues**
   - Check that JWT_SECRET_KEY is set correctly
   - Ensure the same algorithm is used for encoding/decoding

3. **Frontend Cannot Connect to Backend**
   - Verify NEXT_PUBLIC_API_URL is set correctly
   - Check that the backend server is running

### Useful Commands

- Format backend code: `black . && isort .`
- Format frontend code: `npm run format`
- Lint backend code: `flake8 .`
- Lint frontend code: `npm run lint`