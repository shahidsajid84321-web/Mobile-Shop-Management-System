from sqlalchemy.orm import Session

from app.models.role import Role
from app.modules.permissions.permission_model import Permission
from app.modules.permissions.role_permission_model import RolePermission


ROLE_PERMISSIONS = {"Admin": "*",

"Manager": [
    "dashboard.view",

    "users.view",
    "users.create",
    "users.update",

    "roles.view",

    "products.view",
    "products.create",
    "products.update",
    "products.delete",

    "categories.view",
    "categories.create",
    "categories.update",
    "categories.delete",

    "suppliers.view",
    "suppliers.create",
    "suppliers.update",
    "suppliers.delete",

    "customers.view",
    "customers.create",
    "customers.update",
    "customers.delete",

    "purchases.view",
    "purchases.create",
    "purchases.update",
    "purchases.delete",

    "sales.view",
    "sales.create",
    "sales.update",
    "sales.delete",

    "inventory.view",
    "inventory.adjust",

    "reports.view",

    "payments.view",
    "payments.create",
],

"Cashier": [
    "dashboard.view",

    "products.view",

    "customers.view",
    "customers.create",
    "customers.update",

    "sales.view",
    "sales.create",

    "payments.view",
    "payments.create",
],

"Inventory Manager": [
    "dashboard.view",

    "products.view",
    "products.create",
    "products.update",

    "categories.view",
    "categories.create",
    "categories.update",

    "suppliers.view",
    "suppliers.create",
    "suppliers.update",

    "purchases.view",
    "purchases.create",
    "purchases.update",

    "inventory.view",
    "inventory.adjust",

    "reports.view",
],

}

def seed_role_permissions(db: Session) -> None:

    roles = db.query(Role).all()

    permissions = db.query(Permission).all()

    permission_map = {
        permission.code: permission
        for permission in permissions
    }

    for role in roles:

        assigned_permissions = ROLE_PERMISSIONS.get(role.name)

        if assigned_permissions is None:
            continue

        # Admin gets every permission
        if assigned_permissions == "*":
            selected_permissions = permissions

        else:
            selected_permissions = [
                permission_map[code]
                for code in assigned_permissions
                if code in permission_map
            ]

        for permission in selected_permissions:

            existing = (
                db.query(RolePermission)
                .filter(
                    RolePermission.role_id == role.id,
                    RolePermission.permission_id == permission.id,
                )
                .first()
            )

            if existing:
                continue

            db.add(
                RolePermission(
                    role_id=role.id,
                    permission_id=permission.id,
                )
            )

    db.commit()

    print("✅ Role permissions seeded successfully.")