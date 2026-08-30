from datetime import UTC, datetime

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.dependencies.db import get_db
from app.models.auth_session import AuthSession
from app.models.user import User

security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise UnauthorizedException("Authentication credentials are required.")

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        subject = payload.get("sub")
        jti = payload.get("jti")
        token_type = payload.get("type")
        if subject is None or jti is None or token_type != "access":
            raise UnauthorizedException("Invalid token.")
        user_id = int(subject)
    except UnauthorizedException:
        raise
    except (JWTError, ValueError, TypeError):
        raise UnauthorizedException("Invalid or expired token.")

    session = (
        db.query(AuthSession)
        .filter(
            AuthSession.user_id == user_id,
            AuthSession.access_jti == jti,
            AuthSession.revoked_at.is_(None),
        )
        .first()
    )
    if session is None:
        raise UnauthorizedException("Invalid, expired, or revoked token.")

    access_expires_at = session.access_expires_at
    if access_expires_at.tzinfo is None:
        access_expires_at = access_expires_at.replace(tzinfo=UTC)
    if access_expires_at <= datetime.now(UTC):
        raise UnauthorizedException("Invalid, expired, or revoked token.")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise UnauthorizedException("User not found.")
    if not user.is_active:
        raise ForbiddenException("User account is inactive.")
    return user
