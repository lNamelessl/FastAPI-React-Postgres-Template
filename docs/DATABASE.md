# Database Guide

## Overview

The application uses PostgreSQL with SQLModel as the ORM layer. Database changes are managed with Alembic migrations.

## Models

### User Model

**Location:** `backend/app/models.py`

```python
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
```

**Inherited from UserBase:**
```python
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_super_user: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="The date of creation",
    )
```

**Database Table:**
```sql
CREATE TABLE "user" (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_super_user BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    INDEX idx_email ON email
);
```

**Fields Explained:**
- `id` - UUID primary key, auto-generated
- `email` - Unique, indexed for fast login queries
- `hashed_password` - Bcrypt hash (never plain text)
- `full_name` - Optional display name
- `is_active` - Soft delete flag (user can be disabled)
- `is_super_user` - Admin access flag
- `created_at` - Account creation timestamp in UTC
- `items` - One-to-many relationship (user has many items)

### Item Model

**Location:** `backend/app/models.py`

```python
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")
```

**Inherited from ItemBase:**
```python
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
```

**Database Table:**
```sql
CREATE TABLE "item" (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    owner_id UUID NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES "user"(id) ON DELETE CASCADE
);
```

**Fields Explained:**
- `id` - UUID primary key, auto-generated
- `title` - Item name (required, 1-255 chars)
- `description` - Optional item description
- `owner_id` - Foreign key to User
- `owner` - Relationship back to User (cascade delete)

### Relationships

```
User (1) ──────────── (Many) Item
  ↑                         ↑
  └─ id (PK)         owner_id (FK)
     └─ One user has many items
     └─ Delete user automatically deletes items
```

---

## Migrations

Migrations are managed by Alembic and stored in `backend/alembic/versions/`.

### Creating Migrations

**Automatic migration (recommended):**

After modifying `app/models.py`, run:

```bash
cd backend
uv run alembic revision --autogenerate -m "describe your change"
```

This generates a new migration file like `5d5197a2ed57_describe_your_change.py` in `alembic/versions/`.

**Manual migration:**

```bash
cd backend
uv run alembic revision -m "describe your change"
```

Then edit the generated file to add upgrade/downgrade logic.

### Applying Migrations

**Apply all pending migrations:**

```bash
cd backend
uv run alembic upgrade head
```

**Apply specific migration:**

```bash
cd backend
uv run alembic upgrade 5d5197a2ed57
```

**Check current version:**

```bash
cd backend
uv run alembic current
```

### Rollback Migrations

**Rollback one migration:**

```bash
cd backend
uv run alembic downgrade -1
```

**Rollback to specific migration:**

```bash
cd backend
uv run alembic downgrade 5d5197a2ed57
```

### Viewing Migration History

```bash
cd backend
uv run alembic history
```

Output:
```
<base> -> 5d5197a2ed57 (head), initial_migration
```

---

## Initial Migration

The project includes `backend/alembic/versions/5d5197a2ed57_initial_migration.py` which creates the initial schema:

1. User table with all fields
2. Item table with foreign key to User
3. Indexes on frequently queried fields

To apply:

```bash
cd backend
uv run alembic upgrade head
```

---

## Common Database Operations

### Create a User Programmatically

```python
from app import crud
from app.models import UserCreate
from app.core.db import engine
from sqlmodel import Session

with Session(engine) as session:
    user_in = UserCreate(
        email="user@example.com",
        password="securepassword123",
        full_name="John Doe"
    )
    user = crud.create_user(session=session, user_create=user_in)
    print(f"Created user: {user.id}")
```

### Query Users

```python
from app.models import User
from app.core.db import engine
from sqlmodel import Session, select

with Session(engine) as session:
    # Get by email
    stmt = select(User).where(User.email == "user@example.com")
    user = session.exec(stmt).first()
    
    # Get all
    stmt = select(User)
    users = session.exec(stmt).all()
    
    # Get with pagination
    stmt = select(User).offset(0).limit(10)
    users = session.exec(stmt).all()
```

### Update User

```python
from app.models import UserUpdate
from app.core.db import engine
from sqlmodel import Session

with Session(engine) as session:
    user = session.get(User, user_id)
    
    user_update = UserUpdate(full_name="New Name")
    user_data = user_update.model_dump(exclude_unset=True)
    user.sqlmodel_update(user_data)
    
    session.add(user)
    session.commit()
    session.refresh(user)
```

### Delete User (Cascade)

```python
from app.core.db import engine
from sqlmodel import Session

with Session(engine) as session:
    user = session.get(User, user_id)
    session.delete(user)  # Deletes user AND all their items
    session.commit()
```

### Query User's Items

```python
from app.models import User, Item
from app.core.db import engine
from sqlmodel import Session, select

with Session(engine) as session:
    user = session.get(User, user_id)
    
    # Via relationship
    items = user.items
    
    # Or query directly
    stmt = select(Item).where(Item.owner_id == user_id)
    items = session.exec(stmt).all()
```

---

## Database Connection

### Connection String

Configured in `backend/app/core/config.py`:

```python
@computed_field
@property
def POSTGRES_DATABASE_URI(self) -> PostgresDsn:
    return PostgresDsn.build(
        scheme="postgresql+psycopg",
        username=self.POSTGRES_USER,
        password=self.POSTGRES_PASSWORD,
        host=self.POSTGRES_SERVER,
        port=self.POSTGRES_PORT,
        path=self.POSTGRES_DB,
    )
```

**Environment Variables:**
- `POSTGRES_SERVER` - Host (e.g., localhost, db, postgres.railway.app)
- `POSTGRES_PORT` - Port (default: 5432)
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_DB` - Database name

### Engine Configuration

**Location:** `backend/app/core/db.py`

```python
from sqlmodel import create_engine
from app.core.config import settings

engine = create_engine(str(settings.POSTGRES_DATABASE_URI))
```

**Note:** For production, add connection pooling:

```python
engine = create_engine(
    str(settings.POSTGRES_DATABASE_URI),
    echo=False,  # Don't log SQL statements
    pool_size=20,  # Connection pool size
    max_overflow=0,  # Max overflow connections
)
```

### Session Management

The application uses FastAPI dependency injection for session management:

```python
def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]

# Usage in routes
@router.get("/items/")
def read_items(session: SessionDep, current_user: CurrentUser):
    # session is automatically provided
    stmt = select(Item).where(Item.owner_id == current_user.id)
    items = session.exec(stmt).all()
    return items
```

---

## Indexes

Indexes are defined in models to speed up common queries:

```python
class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, ...)  # Indexed
    # ...

class Item(ItemBase, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: UUID = Field(
        foreign_key="user.id", 
        nullable=False, 
        ondelete="CASCADE"
    )  # Foreign key is indexed automatically
    # ...
```

**Indexes created:**
- `User.email` - Fast email lookups (login)
- `Item.owner_id` - Fast owner queries (list user's items)

---

## Performance Tips

1. **Always paginate** - Use `offset` and `limit`
2. **Use indexes** - Add index=True to frequently queried fields
3. **Lazy load relationships** - Avoid N+1 queries
4. **Use select() with where()** - Let database filter
5. **Connection pooling** - Configure in production

---

## Troubleshooting

### Database Connection Failed

```
ERROR: could not translate host name "postgres" to address
```

**Solutions:**
1. Verify PostgreSQL is running: `pg_isready -h localhost`
2. Check `.env` credentials match your setup
3. If Docker: ensure db service is running: `docker-compose up db`

### Migration Conflicts

If migrations conflict, resolve manually:

```bash
cd backend
uv run alembic merge  # Merge conflicting heads
```

### Reset Database

**Warning: This deletes all data**

```bash
cd backend

# Drop all tables
uv run alembic downgrade base

# Recreate from scratch
uv run alembic upgrade head
```

Or with Docker:

```bash
docker-compose down -v  # Remove volumes (database)
docker-compose up       # Recreates fresh database
```

### Query Debugging

Enable SQL logging in `backend/app/core/db.py`:

```python
engine = create_engine(
    str(settings.POSTGRES_DATABASE_URI),
    echo=True  # Log all SQL queries
)
```

---

## Backing Up Data

### PostgreSQL Dump

```bash
pg_dump -h localhost -U postgres -d fastapi_db > backup.sql
```

### Restore from Dump

```bash
psql -h localhost -U postgres -d fastapi_db < backup.sql
```

### Docker Backup

```bash
docker-compose exec db pg_dump -U postgres -d fastapi_db > backup.sql
```

---

## Production Considerations

1. **Enable SSL connections** - Set `sslmode=require` in connection string
2. **Use managed PostgreSQL** - Railway, AWS RDS, or similar
3. **Set up automated backups** - Daily backups with point-in-time recovery
4. **Monitor query performance** - Enable slow query logs
5. **Use read replicas** - For read-heavy workloads

---

See [SETUP.md](SETUP.md) for database initialization and [ARCHITECTURE.md](ARCHITECTURE.md) for schema design details.
