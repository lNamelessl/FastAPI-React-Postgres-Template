# Development Makefile for FastAPI + React + PostgreSQL Template

.PHONY: help install dev backend frontend docker docker-up docker-down db-migrate db-reset clean lint format test

help:
	@echo "Available commands:"
	@echo "  make install         Install dependencies (backend + frontend)"
	@echo "  make dev             Run both backend and frontend locally"
	@echo "  make backend         Run backend only"
	@echo "  make frontend        Run frontend only"
	@echo "  make docker          Build Docker images"
	@echo "  make docker-up       Start Docker containers"
	@echo "  make docker-down     Stop Docker containers"
	@echo "  make docker-reset    Remove containers and volumes"
	@echo "  make db-migrate      Run database migrations"
	@echo "  make db-reset        Reset database (WARNING: deletes data)"
	@echo "  make lint            Lint code (backend + frontend)"
	@echo "  make format          Format code (backend + frontend)"
	@echo "  make test            Run tests (backend + frontend)"
	@echo "  make clean           Clean build artifacts"

# Installation
install:
	@echo "Installing backend dependencies..."
	cd backend && uv sync
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

# Local Development
dev:
	@echo "Starting backend and frontend..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@echo "Docs: http://localhost:8000/docs"
	@echo ""
	@echo "Run in separate terminals or use 'make dev' multiple times"
	@echo "Backend starting..."
	cd backend && uv run uvicorn app.main:app --reload

backend:
	@echo "Starting backend on http://localhost:8000"
	cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	@echo "Starting frontend on http://localhost:5173"
	cd frontend && npm run dev

# Docker
docker:
	@echo "Building Docker images..."
	docker-compose build

docker-up:
	@echo "Starting Docker containers..."
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"
	@echo "Docs: http://localhost:8000/docs"
	docker-compose up

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

docker-reset:
	@echo "WARNING: This will remove all containers and data!"
	@echo "Removing Docker containers and volumes..."
	docker-compose down -v
	@echo "Containers and volumes removed."

# Database
db-migrate:
	@echo "Running database migrations..."
	cd backend && uv run alembic upgrade head

db-reset:
	@echo "WARNING: This will delete all data!"
	@echo "Resetting database..."
	cd backend && uv run alembic downgrade base
	cd backend && uv run alembic upgrade head
	@echo "Database reset complete."

# Code Quality
lint:
	@echo "Linting backend..."
	cd backend && ruff check .
	@echo "Linting frontend..."
	cd frontend && npm run lint

format:
	@echo "Formatting backend..."
	cd backend && ruff format .
	@echo "Formatting frontend..."
	cd frontend && npm run format 2>/dev/null || echo "Frontend format not configured"

# Cleanup
clean:
	@echo "Cleaning build artifacts..."
	rm -rf backend/.venv backend/dist backend/build backend/*.egg-info
	rm -rf frontend/dist frontend/node_modules
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete."

# Environment setup
env-setup:
	@echo "Setting up environment files..."
	@if [ ! -f backend/.env ]; then \
		cp backend/.env.example backend/.env; \
		echo "Created backend/.env"; \
	else \
		echo "backend/.env already exists"; \
	fi
	@if [ ! -f frontend/.env.local ]; then \
		cp frontend/.env.local.example frontend/.env.local; \
		echo "Created frontend/.env.local"; \
	else \
		echo "frontend/.env.local already exists"; \
	fi

# Quick start
quickstart: env-setup install db-migrate
	@echo "Setup complete! Run 'make dev' to start."

.DEFAULT_GOAL := help
