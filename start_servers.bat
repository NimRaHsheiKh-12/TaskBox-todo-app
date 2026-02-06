@echo off
echo Starting Todo Fullstack App...

REM Start the backend server in a new window
start cmd /k "cd backend && python -c \"from src.main import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')\""

REM Wait a moment for the backend to start
timeout /t 3 /nobreak >nul

REM Start the frontend server in a new window
start cmd /k "cd frontend && npm run dev"

echo Servers starting... The backend should be available at http://localhost:8000 and the frontend at http://localhost:3000
pause