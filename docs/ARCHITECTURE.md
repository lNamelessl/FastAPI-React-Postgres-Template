# Architecture Guide

## Project Overview

This is a full-stack web application with clear separation of concerns:

- **Backend**: FastAPI web service with PostgreSQL database
- **Frontend**: React SPA with TypeScript
- **Database**: PostgreSQL with SQLModel ORM
- **Deployment**: Docker containers on Railway

## Tech Stack

### Backend
- **FastAPI** (0.128+) - Modern async Python web framework with auto-documentation
- **SQLModel** (0.0.31+) - Combines SQLAlchemy ORM with Pydantic validation
- **PostgreSQL** - Relational database
- **Alembic** - Database schema migrations
- **PyJWT** - JWT token creation and validation
- **Passlib + Bcrypt** - Secure password hashing
- **Uvicorn** - ASGI server

**Why these choices:**
- FastAPI is the fastest modern Python web framework with built-in validation
- SQLModel bridges the gap between SQLAlchemy and Pydantic for less code duplication
- PostgreSQL is rock-solid, scalable, and feature-rich
- JWT provides stateless authentication suitable for APIs

### Frontend
- **React** (18+) - UI library with hooks
- **React Router** (6+) - Client-side routing
- **TypeScript** (5+) - Type safety and better DX
- **Vite** (4+) - Modern build tool with HMR
- **CSS Modules** - Scoped styling

**Why these choices:**
- React is industry-standard with large ecosystem
- TypeScript prevents entire classes of bugs
- Vite provides instant HMR and optimized builds
- CSS Modules avoid global namespace pollution

### DevOps
- **Docker** - Containerization for consistency
- **Docker Compose** - Local development orchestration
- **Nginx** - Reverse proxy and static file serving
- **Railway** - Platform-as-a-Service hosting

---

## Project Structure

### Backend Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── models.py            # SQLModel ORM models
│   ├── crud.py              # Database CRUD operations
│   ├── annotations.py       # Type annotations (if needed)
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependency injection (SessionDep, CurrentUser)
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── users.py     # User endpoints
│   │       ├── items.py     # Item endpoints
│   │       └── login.py     # Authentication endpoints
│   └── core/
│       ├── __init__.py
│       ├── config.py        # Settings and environment variables
│       ├── db.py            # Database engine initialization
│       └── security.py      # JWT and password utilities
├── alembic/
│   ├── env.py               # Migration environment setup
│   ├── script.py.mako       # Migration template
│   ├── README
│   └── versions/            # Migration files
├── Dockerfile               # Backend container
├── pyproject.toml          # Python dependencies
├── alembic.ini             # Alembic configuration
└── .env.example            # Environment variables template
```

**Key files explained:**

- `app/main.py` - FastAPI app with middleware setup
- `app/models.py` - SQLModel classes that are both ORM models and Pydantic schemas
- `app/crud.py` - Database operations (create, read, update, delete)
- `app/api/deps.py` - Reusable dependencies like session, current user, token parsing
- `app/core/config.py` - All settings loaded from environment variables
- `app/core/security.py` - Password hashing and JWT creation/validation

### Frontend Structure

```
frontend/
├── src/
│   ├── index.tsx            # React entry point
│   ├── App.tsx              # Main app component with routing
│   ├── index.css            # Global styles
│   ├── App.module.css       # App-specific styles
│   ├── components/
│   │   ├── Button.tsx       # Reusable button component
│   │   ├── FormInput.tsx    # Reusable form input
│   │   ├── FormError.tsx    # Error display component
│   │   └── SignupForm.tsx   # Signup form component
│   ├── pages/
│   │   ├── LoginPage.tsx    # Login page
│   │   └── SignupPage.tsx   # Signup page
│   ├── context/
│   │   └── AuthContext.tsx  # Global authentication state
│   ├── services/
│   │   └── api.ts           # API client class
│   ├── types/
│   │   ├── api.ts           # API response types
│   │   └── forms.ts         # Form data types
│   └── utils/
│       └── validation.ts    # Form validation logic
├── public/
│   ├── assets/
│   │   └── images/          # Static images
│   └── README.md
├── index.html              # HTML entry point
├── vite.config.ts          # Vite build configuration
├── tsconfig.json           # TypeScript configuration
├── package.json            # Dependencies
└── .env.local.example      # Environment variables template
```

**Key files explained:**

- `App.tsx` - Route definitions and main layout
- `context/AuthContext.tsx` - Global auth state via React Context API
- `services/api.ts` - API client with request/response handling
- `pages/` - Full-page components corresponding to routes
- `components/` - Reusable UI components

---

## Authentication Flow

### Sign Up / User Creation

```
Frontend                Backend                Database
   |                      |                        |
   |--POST /users/------->|                        |
   |  {email, password}   |                        |
   |                      |--Hash password--------|
   |                      |--INSERT user--------->|
   |                      |<---User created-------|
   |<--UserPublic---------|                        |
   |                      |                        |
   |--Redirect to login---|
```

**Code paths:**
- Frontend: `SignupForm.tsx` → `api.signup()` → `POST /users/`
- Backend: `api/routes/users.py` → `create_user()` → `crud.py` → Database

### Login / Token Generation

```
Frontend                Backend                Database
   |                      |                        |
   |--POST /login-------->|                        |
   | {email, password}    |                        |
   |                      |--SELECT user--------->|
   |                      |<---User data----------|
   |                      |--Verify password------|
   |                      |--Create JWT token-----|
   |<--Token-------------|                        |
   |--Store in          |
   |  localStorage      |
```

**Code paths:**
- Frontend: `LoginPage.tsx` → `api.login()` → `POST /login/access-token`
- Backend: `api/routes/login.py` → `crud.authenticate()` → `security.create_access_token()`

### Authenticated Request

```
Frontend                Backend                Database
   |                      |                        |
   |--GET /items/-------->|                        |
   |Authorization: Bearer |                        |
   |<token>              |                        |
   |                      |--Decode JWT----------|
   |                      |--Validate token--------|
   |                      |--SELECT items-------->|
   |                      |<---Items data---------|
   |<--Items array--------|                        |
```

**Code paths:**
- Frontend: Adds token to headers in `api.ts` request method
- Backend: `api/deps.py` → `get_current_user()` → validates token, returns User object
- Route handler uses `CurrentUser` dependency to get authenticated user

### Key Security Features

1. **Password Hashing**: Passwords hashed with bcrypt (never stored in plain text)
2. **JWT Tokens**: Stateless authentication, tokens expire after configured duration
3. **Token Validation**: Every protected endpoint validates token signature and expiration
4. **CORS**: Configurable allowed origins to prevent cross-site requests

---

## Database Schema

### User Model

```python
class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    hashed_password: str
    full_name: str | None = Field(default=None, max_length=255)
    is_active: bool = True
    is_super_user: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
```

**Fields:**
- `id` - Primary key (UUID)
- `email` - Unique, indexed for fast lookups
- `hashed_password` - Bcrypt hash of password
- `full_name` - Optional user display name
- `is_active` - Can be disabled without deletion
- `is_super_user` - Admin flag for authorization
- `created_at` - Account creation timestamp
- `items` - Relationship to Item model (one-to-many)

### Item Model

```python
class Item(ItemBase, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    owner_id: UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    owner: User | None = Relationship(back_populates="items")
```

**Fields:**
- `id` - Primary key (UUID)
- `title` - Item name/title
- `description` - Optional item description
- `owner_id` - Foreign key to User (cascade delete if user deleted)
- `owner` - Relationship back to User

### Database Relationships

```
User (1) ──── (many) Item
  |                    |
  | primary_key        | foreign_key (owner_id)
  | id                 |
  +----────────────────+
       one-to-many
    (user has many items,
     each item has one owner)
```

See [DATABASE.md](DATABASE.md) for migration details.

---

## API Design Patterns

### Request/Response Models

**Separation of concerns:**

```python
# Database model (has both ORM and validation)
class User(UserBase, table=True):
    id: UUID = ...
    hashed_password: str = ...  # Sensitive!

# Public response model (excludes sensitive fields)
class UserPublic(UserBase):
    id: UUID  # Only public fields

# Creation model (requires password, but API users don't set ID)
class UserCreate(UserBase):
    password: str

# Update model (all fields optional)
class UserUpdate(SQLModel):
    fullname: str | None = None
    email: EmailStr | None = None
```

**Why:**
- Prevents leaking sensitive data (passwords, internal fields)
- Enforces validation on input (min length, format)
- Clear contract with API consumers

### Pagination

```python
# Response always includes count and data
class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

# Query uses skip/limit
@router.get("/", response_model=UsersPublic)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100):
    stmt = select(User).offset(skip).limit(limit)
    users = session.exec(stmt).all()
    count = session.exec(select(func.count()).select_from(User)).one()
    return UsersPublic(data=users, count=count)
```

### Error Handling

```python
# Raises HTTPException with proper status codes
if not user:
    raise HTTPException(status_code=404, detail="User not found")

if not user.is_active:
    raise HTTPException(status_code=400, detail="Inactive user")

if not verify_password(password, user.hashed_password):
    raise HTTPException(status_code=401, detail="Incorrect password")
```

---

## Dependency Injection Pattern

The backend uses FastAPI's dependency injection extensively:

```python
# In api/deps.py
SessionDep = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

# In routes
@router.get("/items/")
def read_items(session: SessionDep, current_user: CurrentUser):
    # FastAPI automatically:
    # 1. Gets database session via get_db()
    # 2. Gets current user via get_current_user()
    # 3. Validates user token
    # 4. Returns 403 if not authenticated
    ...
```

**Benefits:**
- Automatic dependency resolution
- Reusable across all routes
- Clear in function signatures
- Testable (easy to mock dependencies)

---

## Frontend State Management

### AuthContext

Uses React Context API for global authentication state:

```typescript
interface AuthContextType {
  user: UserPublic | null;
  token: string | null;
  loading: boolean;
  isAuthenticated: boolean;
  logout: () => void;
}
```

**Flows:**
1. App initializes, loads stored user/token from localStorage
2. User logs in → token stored in localStorage
3. All API requests include token in Authorization header
4. Protected routes check `isAuthenticated` flag

### Component Pattern

```typescript
// Custom hook for auth context
const auth = useAuth();

// Protected route
if (!auth.isAuthenticated) {
  return <Navigate to="/login" />;
}

// API call with auth
const response = await apiService.logout();
auth.logout();
```

---

## Deployment Architecture

### Local Development

```
Frontend (Vite)          Backend (Uvicorn)      Database (PostgreSQL)
:5173                    :8000                  :5432
├── HMR                  ├── API Routes         ├── Tables
├── Dev Tools            ├── Auto-docs          └── Data
└── Hot Reload           └── Debug Mode
```

### Production (Railway)

```
                      Railway
                         |
    ┌─────────────────────┼─────────────────────┐
    |                     |                     |
  Frontend              Backend              PostgreSQL
  (Node.js)           (Python)             (Managed DB)
   :3000                :8000
    |                     |
    └─────────────────────┼─────────────────────┘
           Nginx Reverse Proxy
```

**Architecture:**
- Static frontend files served by Nginx
- API requests proxied to backend
- Backend connects to managed PostgreSQL
- All services containerized and auto-scaling

---

## Development Workflow

### Adding a New Endpoint

1. **Define model** in `app/models.py`:
   ```python
   class MyModel(SQLModel, table=True):
       id: UUID = ...
       # fields
   ```

2. **Add CRUD function** in `app/crud.py`:
   ```python
   def create_my_model(session: Session, obj_in: MyModelCreate) -> MyModel:
       # create and return
   ```

3. **Create route** in `app/api/routes/my_route.py`:
   ```python
   @router.post("/", response_model=MyModelPublic)
   def create(session: SessionDep, obj_in: MyModelCreate):
       return crud.create_my_model(session, obj_in)
   ```

4. **Include router** in `app/main.py`:
   ```python
   app.include_router(my_route.router)
   ```

5. **Create migration** if schema changed:
   ```bash
   alembic revision --autogenerate -m "add my_model"
   alembic upgrade head
   ```

### Adding a New Component

1. Create component file: `frontend/src/components/MyComponent.tsx`
2. Export from `components/` if reusable
3. Use in page: `import MyComponent from '../components/MyComponent'`

---

## Monitoring & Logging

### Backend Logging (Can be added)

```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"User {user.email} logged in")
logger.warning(f"Failed login attempt for {email}")
logger.error(f"Database error: {str(e)}")
```

### Frontend Console Logging

```typescript
console.log("API Response:", data);
console.error("API Error:", error);
```

### Railway Monitoring

- View logs: `railway logs`
- Metrics: CPU, memory, network usage in Railway dashboard
- Errors: Automatic error tracking and alerts

---

## Performance Considerations

### Backend
- Database indexes on frequently queried fields (email, owner_id)
- Connection pooling configured in database engine
- JWT validation cached (checked on each request)
- Pagination prevents loading entire dataset

### Frontend
- Code splitting via React Router
- CSS Modules prevent style bloat
- Vite optimizes bundle size
- Lazy loading for routes (can be added)

---

See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment details and [DATABASE.md](DATABASE.md) for database schema information.
