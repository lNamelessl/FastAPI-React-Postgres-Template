from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import main
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


app.add_middleware(
    CORSMiddleware,
    allow_orgins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.include_router(main.router)
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications"}
