#!/bin/bash

# Setup development environment
# Run this script to set up the local development environment

set -e  # Exit on error

echo "🚀 Setting up FastAPI + React + PostgreSQL Template..."
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3.12+ is required but not installed"
    exit 1
fi

python_version=$(python3 --version | awk '{print $2}')
echo "✓ Python $python_version found"

if ! command -v node &> /dev/null; then
    echo "❌ Node.js 18+ is required but not installed"
    exit 1
fi

node_version=$(node --version)
echo "✓ Node.js $node_version found"

echo ""

# Setup backend
echo "🐍 Setting up backend..."

cd backend

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "  Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Sync dependencies
echo "  Installing Python dependencies..."
uv sync

# Setup environment variables
if [ ! -f .env ]; then
    echo "  Creating .env file from template..."
    cp .env.example .env
    echo "  ⚠️  Edit backend/.env with your PostgreSQL credentials"
else
    echo "  ✓ .env already exists"
fi

cd ..

echo "✓ Backend setup complete"

echo ""

# Setup frontend
echo "⚛️  Setting up frontend..."

cd frontend

# Install dependencies
echo "  Installing Node.js dependencies..."
npm install

# Setup environment variables
if [ ! -f .env.local ]; then
    echo "  Creating .env.local file from template..."
    cp .env.local.example .env.local
else
    echo "  ✓ .env.local already exists"
fi

cd ..

echo "✓ Frontend setup complete"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit backend/.env with your PostgreSQL credentials"
echo "  2. Run database migrations: cd backend && uv run alembic upgrade head"
echo "  3. Start backend: cd backend && uv run uvicorn app.main:app --reload"
echo "  4. Start frontend: cd frontend && npm run dev"
echo ""
echo "Or use: make dev"
echo ""
