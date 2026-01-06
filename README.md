# Todo Fullstack Application

A full-stack todo application with authentication built using FastAPI (backend) and Next.js (frontend).

## Features

- User authentication with JWT
- Todo management (create, read, update, delete, toggle completion)
- Search and filtering capabilities
- Responsive UI design
- Rate limiting for security
- Comprehensive test coverage

## Tech Stack

### Backend
- Python 3.11
- FastAPI
- SQLModel
- PostgreSQL
- JWT for authentication
- Passlib for password hashing
- Slowapi for rate limiting

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios for API calls

## Local Development Setup

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
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

5. Run the backend server:
   ```bash
   uvicorn backend.src.main:app --reload
   ```

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your backend API URL
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## Production Deployment

### Using Docker Compose

1. Make sure you have Docker and Docker Compose installed.

2. Update the environment variables in `docker-compose.yml` as needed.

3. Run the following command to start the application:
   ```bash
   docker-compose up -d
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Database: http://localhost:5432 (for direct access)

### Manual Deployment

1. Build the frontend for production:
   ```bash
   cd frontend
   npm run build
   ```

2. Deploy the backend with a WSGI server like Gunicorn:
   ```bash
   cd backend
   pip install gunicorn
   gunicorn backend.src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

3. Serve the frontend build with a web server like Nginx.

## API Documentation

API documentation is available at:
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc
- Detailed documentation: [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

## Testing

### Backend Tests

Run backend tests with pytest:
```bash
cd backend
pytest
```

### Frontend Tests

Run frontend tests with Jest:
```bash
cd frontend
npm run test
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/todoapp
JWT_SECRET_KEY=your-super-secret-jwt-signing-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Rate limiting on authentication endpoints
- Input validation
- SQL injection prevention through SQLModel/SQLAlchemy
- Secure token storage and management

## Project Structure

```
todo_fullstack_app/
├── backend/
│   ├── src/
│   │   ├── api/          # API route definitions
│   │   ├── auth/         # Authentication utilities
│   │   ├── config/       # Configuration files
│   │   ├── database/     # Database configuration
│   │   ├── middleware/   # Middleware components
│   │   ├── models/       # Data models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utility functions
│   ├── tests/            # Backend tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Next.js pages
│   │   ├── services/     # API service functions
│   │   ├── context/      # React context providers
│   │   └── styles/       # Global styles
│   ├── tests/            # Frontend tests
│   └── package.json
├── docker-compose.yml
└── API_DOCUMENTATION.md
```