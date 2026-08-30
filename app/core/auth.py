from datetime import UTC, datetime, timedelta
import hashlib
import secrets
from uuid import uuid4

from jose import jwt

from app.core.config import settings


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> tuple[str, str, datetime]:
    """Create a short-lived JWT access token and return its JTI and expiry."""
    now = datetime.now(UTC)
    expire = now + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    jti = uuid4().hex
    to_encode = data.copy()
    to_encode.update({
        "jti": jti,
        "type": "access",
        "iat": now,
        "exp": expire,
    })
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt, jti, expire


def create_refresh_token() -> tuple[str, str, datetime]:
    """Create an opaque refresh token and its hash for server-side storage."""
    token = secrets.token_urlsafe(64)
    token_hash = hash_token(token)
    expires_at = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return token, token_hash, expires_at


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
