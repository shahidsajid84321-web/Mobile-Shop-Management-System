from sqlalchemy.orm import Session

from app.modules.permissions.permission_model import Permission


class PermissionRepository:

    @staticmethod
    def get_all(
        db: Session,
    ) -> list[Permission]:

        return (
            db.query(Permission)
            .order_by(Permission.id.asc())
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        permission_id: int,
    ) -> Permission | None:

        return (
            db.query(Permission)
            .filter(
                Permission.id == permission_id,
            )
            .first()
        )

    @staticmethod
    def get_by_code(
        db: Session,
        code: str,
    ) -> Permission | None:

        return (
            db.query(Permission)
            .filter(
                Permission.code == code,
            )
            .first()
        )