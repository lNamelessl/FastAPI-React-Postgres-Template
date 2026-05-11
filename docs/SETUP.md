# Setup Guide

Complete step-by-step instructions for setting up the application locally.

## Prerequisites

### System Requirements
- **Python 3.12** or higher
- **Node.js 18** or higher  
- **PostgreSQL 14** or higher (optional if using Docker)
- **Git**

### Installation

#### Python 3.12

**macOS:**
```bash
brew install python@3.12
```

**Windows:**
- Download from https://www.python.org/downloads/
- Or use `choco install python --version=3.12`

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3.12 python3.12-venv
```

#### Node.js 18+

**macOS:**
```bash
brew install node
```

**Windows:**
- Download from https://nodejs.org/
- Or use `choco install nodejs`

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install nodejs
```

#### PostgreSQL (Optional - use Docker if unsure)

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Windows:**
- Download from https://www.postgresql.org/download/
- Or use `choco install postgresql`

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

---

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Install Dependencies with uv

The project uses `uv` for fast Python dependency management:

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

### 3. Configure Environment Variables

```bash
# Copy template
cp .env.example .env

# Edit with your values
nano .env  # or use your editor
```

**Minimum required variables:**

```env
# Database
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=fastapi_db

# Security
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# API
API_V1_STR=/api/v1
PROJECT_NAME=FastAPI + React App
```

See [ENVIRONMENT.md](ENVIRONMENT.md) for all available variables.

### 4. Initialize Database

```bash
# Run migrations
uv run alembic upgrade head

# Verify connection
uv run python -c "from app.core.db import engine; print('DB connected!')"
```

### 5. Run Development Server

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access at: http://localhost:8000
- API: http://localhost:8000/api/v1
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Frontend Setup

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

```bash
# Copy template
cp .env.local.example .env.local

# Edit with your values
nano .env.local  # or use your editor
```

**Minimum required variables:**

```env
VITE_API_URL=http://localhost:8000
```

### 4. Run Development Server

```bash
npm run dev
```

Access at: http://localhost:5173

The dev server supports hot module replacement (HMR) - changes update instantly.

### 5. Build for Production

```bash
npm run build
npm run preview
```

---

## Docker Setup (Alternative)

If you prefer containerized development:

### 1. Ensure Docker is Running

```bash
docker --version
docker-compose --version
```

### 2. Create Root Environment File

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL credentials.

### 3. Start Services

```bash
docker-compose up
```

This starts:
- **PostgreSQL** on port 5432
- **Backend API** on port 8000
- **Frontend** on port 3000
- **Nginx** reverse proxy on port 80

Access:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

### 4. View Logs

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### 5. Stop Services

```bash
docker-compose down
```

To remove volumes (clears database):
```bash
docker-compose down -v
```

---

## Database Migrations

### Create New Migration

After modifying models in `app/models.py`:

```bash
cd backend
uv run alembic revision --autogenerate -m "describe your changes"
```

This generates a migration file in `alembic/versions/`.

### Apply Migrations

```bash
cd backend
uv run alembic upgrade head
```

### Rollback Last Migration

```bash
cd backend
uv run alembic downgrade -1
```

### View Migration History

```bash
cd backend
uv run alembic current
uv run alembic history
```

---

## Troubleshooting

### Backend Issues

#### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uv run uvicorn app.main:app --reload --port 8001
```

#### Database Connection Failed

```
ERROR: could not translate host name "postgres" to address
```

**Solution:**
- Check PostgreSQL is running: `pg_isready -h localhost`
- Verify `.env` credentials match your PostgreSQL setup
- If using Docker, ensure PostgreSQL service is running: `docker-compose logs db`

#### Permission Denied on .env File

```bash
chmod 600 .env
```

#### ImportError: No module named 'app'

```bash
# Ensure you're in backend directory
cd backend

# Reinstall dependencies
uv sync
```

### Frontend Issues

#### npm Command Not Found

```bash
# Install Node.js again or verify PATH
node --version
npm --version
```

#### Cannot GET http://localhost:5173

- Frontend dev server may not be running
- Check terminal for errors
- Try: `npm run dev` again
- Clear cache: `rm -rf node_modules/.vite`

#### API Calls Failing (CORS Error)

```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
- Verify backend is running at `http://localhost:8000`
- Check `.env.local` has correct `VITE_API_URL`
- Verify backend CORS settings in `app/main.py`

#### Blank Page or 404

- Check browser console for errors (F12)
- Verify build: `npm run build`
- Check that index.html exists and is readable

---

## Frontend API Configuration

The frontend uses `VITE_API_URL` environment variable:

**Development (http://localhost:5173):**
```env
VITE_API_URL=http://localhost:8000
```

**Docker (via Nginx reverse proxy):**
```env
VITE_API_URL=/api
```

**Production (Railway):**
```env
VITE_API_URL=https://your-app.railway.app
```

---

## Development Workflow

### Running Both Services

**Option 1: Two Terminals**

Terminal 1 - Backend:
```bash
cd backend
uv run uvicorn app.main:app --reload
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

**Option 2: Docker Compose**

```bash
docker-compose up
```

**Option 3: Using Make**

```bash
make dev
```

---

## Next Steps

1. Create your first User via `/docs` Swagger UI
2. Create Items for that User
3. Modify components in `frontend/src/components/`
4. Add new API routes in `backend/app/api/routes/`
5. See [ARCHITECTURE.md](ARCHITECTURE.md) for code structure overview

---

## Getting Help

- Check [ARCHITECTURE.md](ARCHITECTURE.md) for code structure overview
- See [DATABASE.md](DATABASE.md) for database-related questions
