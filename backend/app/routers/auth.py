from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from .. import models, schemas
from ..deps import get_db_session
from ..security import hash_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/signup", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def signup(user_in: schemas.UserCreate, db: Session = Depends(get_db_session)) -> schemas.UserOut:
    """
    Register a new user (plantation owner, industry, or admin).

    - Validates email uniqueness
    - Hashes the password
    - Persists the user in the database
    """
    # Check if email already exists
    stmt = select(models.User).where(models.User.email == user_in.email)
    existing_user = db.execute(stmt).scalar_one_or_none()
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    # Hash the password
    password_hash = hash_password(user_in.password)

    # Create user instance
    new_user = models.User(
        email=user_in.email,
        full_name=user_in.full_name,
        role=user_in.role,
        password_hash=password_hash,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Pydantic will convert SQLAlchemy object -> UserOut via from_attributes
    return schemas.UserOut.model_validate(new_user)
