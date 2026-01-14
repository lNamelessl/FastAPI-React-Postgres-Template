from fastapi import APIRouter
from app.models import UsersPublic, User, UserCreate
from app.api.deps import SessionDep
from typing import Any
from sqlmodel import select, func
from app import crud

# works in the same way as FastAPI
router = APIRouter()


@router.get("/", tags=["users"], response_model=UsersPublic)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users
    """

    count_stmt = select(func.count()).select_from(User)
    count = session.exec(count_stmt).one()

    stmt = select(User).offset(skip).limit(limit)
    users = session.exec(stmt).all()

    return UsersPublic(data=users, count=count)


@router.post("/", response_model=UsersPublic)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new user
    """
    user = crud.create_user(session=session, user_create=user_in)

    return user
