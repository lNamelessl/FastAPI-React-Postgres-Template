@echo off
REM Run local development environment (Windows)

echo 🚀 Starting FastAPI + React development environment...
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo Docs: http://localhost:8000/docs
echo.
echo To stop: Press Ctrl+C
echo.

REM Check if .env exists
if not exist backend\.env (
    echo ❌ backend\.env not found. Run: copy backend\.env.example backend\.env
    exit /b 1
)

echo Starting backend...
start "FastAPI Backend" cmd /k "cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo Starting frontend...
start "React Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Both services started in new windows. Press Ctrl+C to stop each service.
