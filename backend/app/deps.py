from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from .database import get_db
from . import models


def get_db_session(db: Session = Depends(get_db)) -> Session:
    """
    Wrapper dependency: use in routes for DB session.
    """
    return db


def get_current_user_from_header(
    db: Session = Depends(get_db_session),
    x_user_id: int | None = Header(default=None, alias="X-User-Id"),
) -> models.User:
    """
    Temporary 'auth' mechanism for development/demo:

    We read a header `X-User-Id` and treat that as the authenticated user.
    In a production setup this would be replaced by proper JWT-based auth.

    Usage in routes:
        current_user: models.User = Depends(get_current_user_from_header)
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
