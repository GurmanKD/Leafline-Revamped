from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
import jwt

from .database import get_db
from . import models
from .config import settings


def get_db_session(db: Session = Depends(get_db)) -> Session:
    """
    Wrapper dependency: use in routes for DB session.
    """
    return db


def get_current_user(
    db: Session = Depends(get_db_session),
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> models.User:
    """
    Proper auth for production-style APIs:
    Expects Authorization: Bearer <token>

    Decodes JWT, extracts user_id, loads user from DB.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing.",
        )

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Expected 'Bearer <token>'.",
        )

    token = parts[1]

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload invalid: missing 'sub'.",
        )

    stmt = select(models.User).where(models.User.id == int(user_id))
    user = db.execute(stmt).scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    return user


# TEMP: keep this around if you still want to test with X-User-Id header
def get_current_user_from_header(
    db: Session = Depends(get_db_session),
    x_user_id: int | None = Header(default=None, alias="X-User-Id"),
) -> models.User:
    """
    Previous simple auth mechanism using header `X-User-Id`.
    Kept here for debugging / fallback, but main routes will use JWT-based get_current_user.
    """
    if x_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-User-Id header missing; user not authenticated.",
        )

    stmt = select(models.User).where(models.User.id == x_user_id)
    user = db.execute(stmt).scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found for given X-User-Id.",
        )

    return user
