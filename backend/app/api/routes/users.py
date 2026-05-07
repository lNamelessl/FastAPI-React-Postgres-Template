from typing import Any

from fastapi import APIRouter, HTTPException, status
from sqlmodel import col, func, select

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.models import User, UserCreate, UserPublic, UsersPublic

# works in the same way as FastAPI
router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=UsersPublic)
def read_users(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve users
    """
    if not current_user.is_super_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )

    count_stmt = select(func.count()).select_from(User)
    count = session.exec(count_stmt).one()

    stmt = select(User).order_by(col(User.created_at).desc()).offset(skip).limit(limit)
    users = session.exec(stmt).all()

    return UsersPublic(data=users, count=count)


@router.post("/", response_model=UserPublic)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new user
    """
    user = crud.create_user(session=session, user_create=user_in)

    return user
