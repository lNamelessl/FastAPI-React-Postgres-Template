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
    Retrieve all users (admin only).
    
    Requires admin privileges to list all users in the system.
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
    Create a new user account (public endpoint).
    
    This endpoint allows anyone to create a new user account with an email and password.
    Email must be unique and password must be 8-72 characters.
    """
    if crud.get_user_by_email(email=user_in.email, session=session):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = crud.create_user(session=session, user_create=user_in)

    return user
