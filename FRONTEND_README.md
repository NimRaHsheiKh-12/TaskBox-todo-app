# Taskie Chat Frontend

This is the frontend chat interface for Taskie, a task assistant chatbot. The UI connects to the existing backend API at `/chat`.

## Setup Instructions

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. The chat interface will be available at `http://localhost:5173`

## Notes

- The frontend expects the backend API to be running at `/chat`
- The API endpoint should accept POST requests with a JSON payload containing a `message` field
- The API should return a JSON response with a `response` or `message` field containing Taskie's reply