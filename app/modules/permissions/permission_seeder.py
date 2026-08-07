from sqlalchemy.orm import Session

from app.modules.permissions.permission_model import Permission


PERMISSIONS = [
    # Dashboard
    ("Dashboard View", "dashboard.view"),

    # Users
    ("View Users", "users.view"),
    ("Create Users", "users.create"),
    ("Update Users", "users.update"),
    ("Delete Users", "users.delete"),

    # Roles
    ("View Roles", "roles.view"),
    ("Create Roles", "roles.create"),
    ("Update Roles", "roles.update"),
    ("Delete Roles", "roles.delete"),

    # Products
    ("View Products", "products.view"),
    ("Create Products", "products.create"),
    ("Update Products", "products.update"),
    ("Delete Products", "products.delete"),

    # Categories
    ("View Categories", "categories.view"),
    ("Create Categories", "categories.create"),
    ("Update Categories", "categories.update"),
    ("Delete Categories", "categories.delete"),

    # Suppliers
    ("View Suppliers", "suppliers.view"),
    ("Create Suppliers", "suppliers.create"),
    ("Update Suppliers", "suppliers.update"),
    ("Delete Suppliers", "suppliers.delete"),

    # Customers
    ("View Customers", "customers.view"),
    ("Create Customers", "customers.create"),
    ("Update Customers", "customers.update"),
    ("Delete Customers", "customers.delete"),

    # Purchases
    ("View Purchases", "purchases.view"),
    ("Create Purchases", "purchases.create"),
    ("Update Purchases", "purchases.update"),
    ("Delete Purchases", "purchases.delete"),

    # Sales
    ("View Sales", "sales.view"),
    ("Create Sales", "sales.create"),
    ("Update Sales", "sales.update"),
    ("Delete Sales", "sales.delete"),

    # Inventory
    ("View Inventory", "inventory.view"),
    ("Adjust Inventory", "inventory.adjust"),

    # Reports
    ("View Reports", "reports.view"),

    # Payments
    ("View Payments", "payments.view"),
    ("Create Payments", "payments.create"),

    # Settings
    ("Manage Settings", "settings.manage"),
]

def seed_permissions(db: Session):

    for name, code in PERMISSIONS:

        exists = (
            db.query(Permission)
            .filter(Permission.code == code)
            .first()
        )

        if exists:
            continue

        db.add(
            Permission(
                name=name,
                code=code,
            )
        )

    db.commit()

    print("✅ Permissions Seeded")