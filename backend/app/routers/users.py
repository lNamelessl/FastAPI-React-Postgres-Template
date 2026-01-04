from fastapi import APIRouter

# works in the same way as FastAPI
router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}]
