from sqlalchemy.orm import Session

from app.core.constants.permissions import PERMISSION_DEFINITIONS
from app.modules.permissions.permission_model import Permission


def seed_permissions(db: Session) -> None:
    """
    Insert default permissions into the database.
    """

    for name, code in PERMISSION_DEFINITIONS:

        existing_permission = (
            db.query(Permission)
            .filter(Permission.code == code)
            .first()
        )

        if existing_permission:
            continue

        permission = Permission(
            name=name,
            code=code,
        )

        db.add(permission)

    db.commit()

    print("✅ Permissions seeded successfully.")