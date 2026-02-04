# Quickstart Guide: TaskBox Chatbot Assistant

## Overview
This guide provides instructions for getting started with the TaskBox Chatbot Assistant (Taskie) development.

## Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- PostgreSQL database
- Docker and Docker Compose (optional, for containerized setup)

## Setting Up the Development Environment

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todo_fullstack_app
```

### 2. Backend Setup
```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials and JWT secret

# Run the backend server
uvicorn backend.src.main:app --reload
```

### 3. Frontend Setup
```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your backend API URL

# Start the development server
npm run dev
```

## Key Components

### 1. Chat Service (`backend/src/services/chat_service.py`)
- Contains the core logic for processing user messages
- Implements the Taskie personality and response generation
- Handles CRUD operations on tasks based on user requests

### 2. Chat API (`backend/src/api/chat.py`)
- Defines the endpoints for chat interactions
- Handles authentication and validation
- Orchestrates communication between frontend and chat service

### 3. Chat Interface (`frontend/src/components/ChatInterface.jsx`)
- Provides the UI for interacting with Taskie
- Displays conversation history
- Sends user messages to the backend

## Making Changes to the Chatbot Logic

### 1. Understanding the Message Processing Pipeline
1. User sends a message through the frontend
2. Frontend sends the message to `/api/chat/process`
3. Backend authenticates the request and retrieves user's current tasks
4. ChatService processes the message and determines the appropriate action
5. The action is performed on the task list (create, read, update, delete, complete)
6. A response is generated with appropriate Taskie personality
7. Updated tasks and response are returned to the frontend

### 2. Modifying Taskie's Personality
- Update the response templates in `backend/src/services/chat_service.py`
- Ensure all responses follow the constitution guidelines
- Maintain the friendly, cheerful, and motivational tone
- Use appropriate emojis to keep conversations lively

### 3. Adding New Capabilities
- Extend the message parsing logic in `ChatService`
- Add new methods to handle the additional functionality
- Update API contracts if new endpoints are needed
- Add corresponding frontend components if necessary

## Running Tests

### Backend Tests
```bash
# Run all backend tests
cd backend
pytest

# Run specific chat-related tests
pytest tests/test_chat.py
```

### Frontend Tests
```bash
# Run all frontend tests
cd frontend
npm run test

# Run specific chat component tests
npm run test -- src/components/ChatInterface.test.jsx
```

## API Documentation
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Troubleshooting

### Common Issues
1. **Database Connection Errors**: Ensure PostgreSQL is running and credentials in `.env` are correct
2. **Authentication Failures**: Verify JWT tokens are properly configured
3. **CORS Issues**: Check that frontend and backend URLs are properly configured

### Debugging Tips
- Enable debug logging in the backend by setting `DEBUG=true` in your `.env`
- Use browser developer tools to inspect API requests and responses
- Check the backend logs for error messages when processing chat messages

## Contributing
1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes following the coding standards
3. Write tests for new functionality
4. Update documentation as needed
5. Submit a pull request with a clear description of your changes