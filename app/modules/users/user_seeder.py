from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user import User
from app.core.security import hash_password


def seed_test_users(db: Session) -> None:
    """Create default test users for development."""

    salesman_role = (
        db.query(Role)
        .filter(Role.name == "Salesman")
        .first()
    )

    if salesman_role is None:
        raise ValueError("Salesman role not found.")

    existing_user = (
        db.query(User)
        .filter(User.email == "salesman@test.com")
        .first()
    )

    if existing_user:
        print("ℹ️ Salesman test user already exists.")
        return

    salesman = User(
        full_name="Test Salesman",
        email="salesman@test.com",
        phone="03000000000",
        password=hash_password("Salesman@123"),
        is_active=True,
        email_verified_at=datetime.now(UTC),
        role_id=salesman_role.id,
    )

    db.add(salesman)
    db.commit()

    print("✅ Salesman test user created.")