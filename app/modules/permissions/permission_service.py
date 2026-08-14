from sqlalchemy.orm import Session

from app.modules.permissions.permission_repository import (
    PermissionRepository,
)
from app.modules.permissions.permission_model import Permission


class PermissionService:

    @staticmethod
    def get_all(
        db: Session,
    ) -> list[Permission]:

        return PermissionRepository.get_all(db)

    @staticmethod
    def get_one(
        db: Session,
        permission_id: int,
    ) -> Permission:

        permission = PermissionRepository.get_by_id(
            db,
            permission_id,
        )

        if permission is None:
            raise ValueError(
                "Permission not found."
            )

        return permission