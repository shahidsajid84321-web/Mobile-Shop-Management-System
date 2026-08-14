from sqlalchemy.orm import Session

from app.models.role import Role
from app.modules.permissions.permission_model import Permission
from app.modules.permissions.role_permission_model import RolePermission


class RolePermissionRepository:

    @staticmethod
    def get_role(
        db: Session,
        role_id: int,
    ) -> Role | None:

        return (
            db.query(Role)
            .filter(Role.id == role_id)
            .first()
        )

    @staticmethod
    def get_permissions(
        db: Session,
        role_id: int,
    ) -> list[Permission]:

        return (
            db.query(Permission)
            .join(
                RolePermission,
                RolePermission.permission_id == Permission.id,
            )
            .filter(
                RolePermission.role_id == role_id,
            )
            .order_by(Permission.id.asc())
            .all()
        )

    @staticmethod
    def get_permissions_by_ids(
        db: Session,
        permission_ids: list[int],
    ) -> list[Permission]:

        if not permission_ids:
            return []

        return (
            db.query(Permission)
            .filter(
                Permission.id.in_(permission_ids),
            )
            .all()
        )

    @staticmethod
    def clear_permissions(
        db: Session,
        role_id: int,
    ) -> None:

        db.query(RolePermission).filter(
            RolePermission.role_id == role_id,
        ).delete(
            synchronize_session=False,
        )

    @staticmethod
    def add_permission(
        db: Session,
        role_id: int,
        permission_id: int,
    ) -> None:

        db.add(
            RolePermission(
                role_id=role_id,
                permission_id=permission_id,
            )
        )

    @staticmethod
    def save(
        db: Session,
    ) -> None:

        db.commit()
