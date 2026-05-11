@echo off
REM Reset database (Windows)

echo ⚠️  WARNING: This will delete all database data!
set /p confirm="Are you sure? Type 'yes' to confirm: "

if not "%confirm%"=="yes" (
    echo Cancelled.
    exit /b 0
)

echo Resetting database...

cd backend

echo   Removing all migrations...
uv run alembic downgrade base

echo   Recreating schema...
uv run alembic upgrade head

cd ..

echo ✅ Database reset complete!
pause
