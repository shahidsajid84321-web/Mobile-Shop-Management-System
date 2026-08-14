from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import (
    ForbiddenException,
    UnauthorizedException,
)
from app.dependencies.db import get_db
from app.models.user import User


security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> User:

    if credentials is None:
        raise UnauthorizedException(
            "Authentication credentials are required."
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        subject = payload.get("sub")

        if subject is None:
            raise UnauthorizedException(
                "Invalid token."
            )

        user_id = int(subject)

    except UnauthorizedException:
        raise

    except (JWTError, ValueError, TypeError):
        raise UnauthorizedException(
            "Invalid or expired token."
        )

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise UnauthorizedException(
            "User not found."
        )

    if not user.is_active:
        raise ForbiddenException(
            "User account is inactive."
        )

    return user