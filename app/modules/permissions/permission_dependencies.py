from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.constants.permissions import PermissionCode
from app.core.enums.roles import RoleName
from app.dependencies.db import get_db
from app.models.user import User
from app.modules.auth.dependencies import get_current_user
from app.modules.permissions.permission_model import Permission
from app.modules.permissions.role_permission_model import RolePermission


def require_permission(permission_code: PermissionCode):
    """
    Require the current user to have a specific permission.
    """

    def permission_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:

        # Super Admin bypasses permission checks.
        if current_user.role.name == RoleName.SUPER_ADMIN:
            return current_user

        permission_exists = (
            db.query(RolePermission)
            .join(
                Permission,
                RolePermission.permission_id == Permission.id,
            )
            .filter(
                RolePermission.role_id == current_user.role_id,
                Permission.code == permission_code,
            )
            .first()
        )

        if not permission_exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission required: {permission_code}",
            )

        return current_user

    return permission_checker