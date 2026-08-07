from fastapi import Depends, HTTPException, status

from app.models.user import User
from app.modules.auth.dependencies import get_current_user


def require_roles(*allowed_roles: str):
    """
    Allow only users with the specified roles.
    """

    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        if current_user.role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to perform this action.",
            )

        return current_user

    return role_checker
