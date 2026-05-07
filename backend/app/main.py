from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import items, login, users
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json", docs_url="/"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def root():
    return {"message": "Hello Bigger Applications"}


app.include_router(items.router)
app.include_router(users.router)
app.include_router(login.router)
