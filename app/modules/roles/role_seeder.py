from sqlalchemy.orm import Session

from app.core.enums.roles import RoleName
from app.models.role import Role


def seed_roles(db: Session) -> None:
    """Insert the default roles into the database."""
    for role_name in RoleName:
        existing_role = (
            db.query(Role)
            .filter(Role.name == role_name.value)
            .first()
        )

        if existing_role:
            continue

        db.add(
            Role(
                name=role_name.value,
            )
        )

    db.commit()
    print("✅ Roles seeded successfully.")
