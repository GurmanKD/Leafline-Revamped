import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Any, Dict

from .config import settings


# ==== PASSWORD HASHING ====


def hash_password(plain_password: str) -> str:
    """
    Hashes a plain-text password using bcrypt.
    Returns the hashed password as a UTF-8 string.
    """
    password_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    """
    Verifies a plain-text password against a stored bcrypt hash.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        password_hash.encode("utf-8"),
    )


# ==== JWT TOKENS ====


def create_access_token(
    data: Dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a JWT access token encoding the given data.
    `data` should already be safe to put in the token (no secrets).
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
