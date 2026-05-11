#!/bin/bash

# Run local development environment
# Starts both backend and frontend servers

set -e

echo "🚀 Starting FastAPI + React development environment..."
echo ""
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "Docs: http://localhost:8000/docs"
echo ""
echo "To stop: Press Ctrl+C"
echo ""

# Check if .env exists
if [ ! -f backend/.env ]; then
    echo "❌ backend/.env not found. Run: cp backend/.env.example backend/.env"
    exit 1
fi

# Start backend in background
echo "Starting backend..."
(cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000) &
backend_pid=$!

# Start frontend in background
echo "Starting frontend..."
(cd frontend && npm run dev) &
frontend_pid=$!

# Handle Ctrl+C
trap "kill $backend_pid $frontend_pid 2>/dev/null" EXIT

# Wait for processes
wait $backend_pid $frontend_pid
