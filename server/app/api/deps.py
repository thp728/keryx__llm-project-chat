from typing import (
    Generator,
)
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.core import security
from app.core.config import settings
from app.db.session import get_db

from app.services.llm_service import LLMService

# OAuth2PasswordBearer is used for extracting the token from the Authorization header
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_VER_STR}/login/access-token"  # This will be your login endpoint
)


def get_llm_service() -> LLMService:
    """
    Provides an instance of LLMService.
    """
    return LLMService()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    """
    Get the current authenticated user from the JWT token.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        # The 'sub' claim in NextAuth.js JWT typically holds the user ID or email.
        # Assuming 'sub' holds the user's email for lookup.
        token_data = schemas.TokenPayload(sub=payload.get("sub"))
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    Get the current active user.
    """
    if not crud.user.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user
