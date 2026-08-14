from app.database.session import SessionLocal

from app.modules.roles.role_seeder import seed_roles
from app.modules.permissions.permission_seeder import seed_permissions
from app.modules.permissions.role_permission_seeder import (
    seed_role_permissions,
)
from app.modules.users.user_seeder import seed_test_users


def seed_database():
    db = SessionLocal()

    try:
        seed_roles(db)
        seed_permissions(db)
        seed_role_permissions(db)
        seed_test_users(db)

        print("✅ Database seeded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()