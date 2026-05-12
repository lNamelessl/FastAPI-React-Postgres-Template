from datetime import timedelta
from typing import Annotated

from app import crud
from app.api.deps import SessionDep
from app.core import security
from app.core.config import settings
from app.models import Token
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["login"])


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    Login and receive JWT access token.
    
    Authenticate with email and password to receive a JWT access token.
    Use the token in the Authorization header for subsequent requests.
    
    The token expires after the configured ACCESS_TOKEN_EXPIRE_MINUTES.
    """
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
