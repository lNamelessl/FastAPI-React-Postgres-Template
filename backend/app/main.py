from fastapi import Depends, FastAPI

from .api.deps import get_query_token, get_token_header
from .routers import items, users

app = FastAPI()


#  will create the path operations on startup and won't affect performance
@app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications"}
