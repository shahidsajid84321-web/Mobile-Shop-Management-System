from sqlalchemy.orm import Session

from app.models.role import Role


DEFAULT_ROLES = [
    "Super Admin",
    "Admin",
    "Manager",
    "Salesman",
    "Inventory Manager",
    "Customer",
]


def seed_roles(db: Session):
    """
    Insert default roles into database.
    """

    for role_name in DEFAULT_ROLES:

        existing_role = (
            db.query(Role)
            .filter(Role.name == role_name)
            .first()
        )

        if not existing_role:

            role = Role(name=role_name)

            db.add(role)

    db.commit()

    print("✅ Roles Seeded Successfully")