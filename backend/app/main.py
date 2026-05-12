from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import items, login, users
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Full-stack web application with FastAPI, React, and PostgreSQL",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/",
    redoc_url="/redoc",
)

# Configure CORS
allowed_origins = settings.ALLOWED_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {"message": "Hello Bigger Applications", "status": "healthy"}


# Include routers
app.include_router(items.router)
app.include_router(users.router)
app.include_router(login.router)


app.include_router(items.router)
app.include_router(users.router)
app.include_router(login.router)
