from app.database.session import SessionLocal
from app.seeders.role_seeder import seed_roles


def run_seeders():
    db = SessionLocal()

    try:
        print("Seeding database...")
        seed_roles(db)
        print("Database seeded successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    run_seeders()