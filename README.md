# FastAPI + React + PostgreSQL Template

A full-stack web application template with a modern tech stack: FastAPI backend, React frontend, PostgreSQL database, and Docker containerization. Production-ready with authentication, API documentation, and Railway deployment support.

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL 14+ (or use Docker)
- Docker & Docker Compose (optional, for containerized setup)

### Local Development (5 minutes)

```bash
# 1. Clone and setup
git clone <repo-url>
cd FastAPI-React-Postgres-Template

# 2. Backend setup
cd backend
uv sync
cp .env.example .env
# Edit .env with your PostgreSQL credentials
uv run alembic upgrade head  # Run migrations
uv run uvicorn app.main:app --reload

# 3. Frontend setup (in new terminal)
cd frontend
npm install
cp .env.local.example .env.local
npm run dev

# Visit http://localhost:5173 (React dev server)
# API available at http://localhost:8000
# Swagger UI at http://localhost:8000/docs
```

### Using Docker Compose

```bash
cp .env.example .env
docker-compose up
```

Visit:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

## 📚 Documentation

- **[SETUP.md](docs/SETUP.md)** - Detailed local development setup instructions
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Project structure, tech stack, design patterns
- **[DATABASE.md](docs/DATABASE.md)** - Database schema, migrations, models

## 🏗️ Architecture Overview

```
FastAPI-React-Postgres-Template/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/            # API routes and dependencies
│   │   ├── core/           # Configuration, security, database
│   │   ├── models.py       # SQLModel ORM models
│   │   ├── crud.py         # Database operations
│   │   └── main.py         # FastAPI app initialization
│   ├── alembic/            # Database migrations
│   ├── Dockerfile          # Backend container
│   ├── pyproject.toml      # Python dependencies
│   └── .env.example        # Environment template
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # Reusable React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API client
│   │   ├── context/        # React Context for state
│   │   ├── types/          # TypeScript types
│   │   └── utils/          # Helper functions
│   ├── Dockerfile          # Frontend container
│   ├── package.json        # Node.js dependencies
│   ├── vite.config.ts      # Vite configuration
│   └── .env.local.example  # Environment template
├── nginx/                  # Nginx reverse proxy
│   └── nginx.conf          # Nginx configuration
├── scripts/                # Development scripts
│   ├── setup-dev.sh        # Setup automation
│   ├── run-local.sh        # Run all services
│   └── db-reset.sh         # Database reset
├── docker-compose.yml      # Local dev orchestration
└── docs/                   # Documentation
    ├── SETUP.md
    ├── ARCHITECTURE.md
    └── 
```

## 🔐 Authentication

The application uses JWT (JSON Web Tokens) for stateless authentication:

1. User signs up or logs in with email and password
2. Backend validates credentials and returns a JWT token
3. Frontend stores token in localStorage
4. Frontend includes token in Authorization header for authenticated requests
5. Backend validates token on each request using `CurrentUser` dependency

See [ARCHITECTURE.md](docs/ARCHITECTURE.md#authentication) for detailed flow.

## 🗄️ Database

- **PostgreSQL** - Relational database
- **SQLModel** - Python ORM combining SQLAlchemy and Pydantic
- **Alembic** - Database migration tool

Models:
- **User** - User accounts with email, password, roles
- **Item** - User-owned items

See [DATABASE.md](docs/DATABASE.md) for schema details.

## 📡 API Endpoints

All endpoints documented with OpenAPI (Swagger UI):
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Quick reference:
- `POST /login/access-token` - Login and get JWT token
- `POST /users/` - Create new user (public signup)
- `GET /users/` - List all users (admin only)
- `GET /items/` - List current user's items
- `POST /items/` - Create new item
- `GET /health` - Health check

See [API.md](docs/API.md) for full endpoint documentation.

## 🚢 Deployment

### Railway (Recommended)

Quick deployment to Railway:

```bash
# 1. Connect your GitHub repo to Railway
# 2. Add PostgreSQL plugin
# 3. Set environment variables (see DEPLOYMENT.md)
# 4. Deploy!
```

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed Railway instructions.

### Docker

Build and run locally:

```bash
docker-compose up --build
```

## 🛠️ Development

### Database Migrations

```bash
cd backend

# Create new migration
alembic revision --autogenerate -m "migration description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Code Formatting

```bash
# Backend
cd backend
ruff check .
ruff format .

# Frontend
cd frontend
npm run lint
```

## 📦 Key Dependencies

**Backend:**
- FastAPI 0.128+ - Web framework
- SQLModel 0.0.31+ - ORM
- Pydantic 2.x - Data validation
- PyJWT - JWT tokens
- Passlib + Bcrypt - Password hashing
- Psycopg - PostgreSQL driver
- Alembic - Database migrations

**Frontend:**
- React 18+ - UI library
- React Router 6+ - Routing
- TypeScript 5+ - Type safety
- Vite 4+ - Build tool

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.com?referralCode=uBTGZq)

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Commit changes: `git commit -am 'Add my feature'`
3. Push to branch: `git push origin feature/my-feature`
4. Open a Pull Request

## 📝 License
[LISENSE](docs/LICENSE)


## 🆘 Troubleshooting

- **Can't connect to database?** See [SETUP.md#troubleshooting](docs/SETUP.md#troubleshooting)
- **Frontend can't reach API?** Check [SETUP.md#frontend-api-configuration](docs/SETUP.md#frontend-api-configuration)
- **Alembic migration fails?** See [DATABASE.md](#database-migrations)

## 📧 Support

For issues or questions:
1. Check the [documentation](docs/)
2. Review [existing issues](../../issues)
3. Create a new issue with details

---

**Happy coding! 🎉**
