from sqlalchemy.orm import Session

from app.modules.permissions.role_permission_repository import (
    RolePermissionRepository,
)
from app.modules.permissions.role_permission_schema import (
    RolePermissionUpdate,
)
from app.core.enums.roles import RoleName
from app.models.user import User

class RolePermissionService:

    @staticmethod
    def get_permissions(
        db: Session,
        role_id: int,
    ):

        role = RolePermissionRepository.get_role(
            db,
            role_id,
        )

        if role is None:
            raise ValueError("Role not found.")

        permissions = (
            RolePermissionRepository.get_permissions(
                db,
                role_id,
            )
        )

        return {
            "role_id": role.id,
            "role_name": role.name,
            "permissions": [
                permission.code
                for permission in permissions
            ],
        }

    @staticmethod
    def update_permissions(
        db: Session,
        role_id: int,
        data: RolePermissionUpdate,
        actor: User,
    ):

        role = RolePermissionRepository.get_role(
            db,
            role_id,
        )

        if role is None:
            raise ValueError("Role not found.")

        if role.name == RoleName.SUPER_ADMIN and actor.role.name != RoleName.SUPER_ADMIN:
            raise ValueError("Only a Super Admin can modify Super Admin permissions.")

        # Never allow removing all permissions
        # from Super Admin.
        if role.name == RoleName.SUPER_ADMIN:
            raise ValueError(
                "Super Admin permissions cannot be modified."
            )

        # Remove duplicate IDs.
        permission_ids = list(
            dict.fromkeys(data.permission_ids)
        )

        permissions = (
            RolePermissionRepository.get_permissions_by_ids(
                db,
                permission_ids,
            )
        )

        if len(permissions) != len(permission_ids):
            raise ValueError(
                "One or more permissions were not found."
            )

        RolePermissionRepository.clear_permissions(
            db,
            role_id,
        )

        for permission_id in permission_ids:
            RolePermissionRepository.add_permission(
                db,
                role_id,
                permission_id,
            )

        RolePermissionRepository.save(db)

        return {
            "role_id": role.id,
            "role_name": role.name,
            "permissions": [
                permission.code
                for permission in permissions
            ],
        }
