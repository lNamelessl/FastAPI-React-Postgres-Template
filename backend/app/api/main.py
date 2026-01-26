from fastapi import APIRouter

from app.api.routes import items, users, login
from app.core.config import settings 

router = APIRouter()
router.include_router(login.router)
router.include_router(users.router)
router.include_router(items.router)