@echo off
REM Setup development environment (Windows)

echo 🚀 Setting up FastAPI + React + PostgreSQL Template...
echo.

REM Check prerequisites
echo 📋 Checking prerequisites...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3.12+ is required but not installed
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% found

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js 18+ is required but not installed
    exit /b 1
)

for /f %%i in ('node --version') do set NODE_VERSION=%%i
echo ✓ Node.js %NODE_VERSION% found

echo.

REM Setup backend
echo 🐍 Setting up backend...

cd backend

REM Install uv if not present
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo   Installing uv...
    powershell -Command "Invoke-WebRequest -Uri https://astral.sh/uv/install.ps1 -OutFile uv-installer.ps1; & .\uv-installer.ps1; del uv-installer.ps1"
)

REM Sync dependencies
echo   Installing Python dependencies...
uv sync

REM Setup environment variables
if not exist .env (
    echo   Creating .env file from template...
    copy .env.example .env
    echo   ⚠️  Edit backend\.env with your PostgreSQL credentials
) else (
    echo   ✓ .env already exists
)

cd ..

echo ✓ Backend setup complete

echo.

REM Setup frontend
echo ⚛️  Setting up frontend...

cd frontend

REM Install dependencies
echo   Installing Node.js dependencies...
call npm install

REM Setup environment variables
if not exist .env.local (
    echo   Creating .env.local file from template...
    copy .env.local.example .env.local
) else (
    echo   ✓ .env.local already exists
)

cd ..

echo ✓ Frontend setup complete

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo   1. Edit backend\.env with your PostgreSQL credentials
echo   2. Run database migrations: cd backend ^&^& uv run alembic upgrade head
echo   3. Start backend: cd backend ^&^& uv run uvicorn app.main:app --reload
echo   4. Start frontend: cd frontend ^&^& npm run dev
echo.
echo Or use: make dev
echo.

pause
