from sqlalchemy.orm import Session

from app.core.constants.permissions import PermissionCode
from app.core.enums.roles import RoleName
from app.models.role import Role
from app.modules.permissions.permission_model import Permission
from app.modules.permissions.role_permission_model import RolePermission


ROLE_PERMISSIONS = {
    RoleName.SUPER_ADMIN: "*",

    RoleName.ADMIN: [
        PermissionCode.DASHBOARD_VIEW,

        PermissionCode.USERS_VIEW,
        PermissionCode.USERS_CREATE,
        PermissionCode.USERS_UPDATE,
        PermissionCode.USERS_DELETE,

        PermissionCode.ROLES_VIEW,
        PermissionCode.ROLES_CREATE,
        PermissionCode.ROLES_UPDATE,
        PermissionCode.ROLES_DELETE,

        PermissionCode.PRODUCTS_VIEW,
        PermissionCode.PRODUCTS_CREATE,
        PermissionCode.PRODUCTS_UPDATE,
        PermissionCode.PRODUCTS_DELETE,

        PermissionCode.CATEGORIES_VIEW,
        PermissionCode.CATEGORIES_CREATE,
        PermissionCode.CATEGORIES_UPDATE,
        PermissionCode.CATEGORIES_DELETE,

        PermissionCode.SUPPLIERS_VIEW,
        PermissionCode.SUPPLIERS_CREATE,
        PermissionCode.SUPPLIERS_UPDATE,
        PermissionCode.SUPPLIERS_DELETE,

        PermissionCode.CUSTOMERS_VIEW,
        PermissionCode.CUSTOMERS_CREATE,
        PermissionCode.CUSTOMERS_UPDATE,
        PermissionCode.CUSTOMERS_DELETE,

        PermissionCode.PURCHASES_VIEW,
        PermissionCode.PURCHASES_CREATE,
        PermissionCode.PURCHASES_UPDATE,
        PermissionCode.PURCHASES_DELETE,

        PermissionCode.SALES_VIEW,
        PermissionCode.SALES_CREATE,
        PermissionCode.SALES_UPDATE,
        PermissionCode.SALES_DELETE,

        PermissionCode.INVENTORY_VIEW,
        PermissionCode.INVENTORY_ADJUST,

        PermissionCode.PAYMENTS_VIEW,
        PermissionCode.PAYMENTS_CREATE,

        PermissionCode.REPORTS_VIEW,

        PermissionCode.SETTINGS_MANAGE,
    ],

    RoleName.MANAGER: [
        PermissionCode.DASHBOARD_VIEW,

        PermissionCode.USERS_VIEW,
        PermissionCode.USERS_CREATE,
        PermissionCode.USERS_UPDATE,

        PermissionCode.ROLES_VIEW,

        PermissionCode.PRODUCTS_VIEW,
        PermissionCode.PRODUCTS_CREATE,
        PermissionCode.PRODUCTS_UPDATE,
        PermissionCode.PRODUCTS_DELETE,

        PermissionCode.CATEGORIES_VIEW,
        PermissionCode.CATEGORIES_CREATE,
        PermissionCode.CATEGORIES_UPDATE,
        PermissionCode.CATEGORIES_DELETE,

        PermissionCode.SUPPLIERS_VIEW,
        PermissionCode.SUPPLIERS_CREATE,
        PermissionCode.SUPPLIERS_UPDATE,
        PermissionCode.SUPPLIERS_DELETE,

        PermissionCode.CUSTOMERS_VIEW,
        PermissionCode.CUSTOMERS_CREATE,
        PermissionCode.CUSTOMERS_UPDATE,
        PermissionCode.CUSTOMERS_DELETE,

        PermissionCode.PURCHASES_VIEW,
        PermissionCode.PURCHASES_CREATE,
        PermissionCode.PURCHASES_UPDATE,
        PermissionCode.PURCHASES_DELETE,

        PermissionCode.SALES_VIEW,
        PermissionCode.SALES_CREATE,
        PermissionCode.SALES_UPDATE,
        PermissionCode.SALES_DELETE,

        PermissionCode.INVENTORY_VIEW,
        PermissionCode.INVENTORY_ADJUST,

        PermissionCode.PAYMENTS_VIEW,
        PermissionCode.PAYMENTS_CREATE,

        PermissionCode.REPORTS_VIEW,
    ],

    RoleName.SALESMAN: [
        PermissionCode.DASHBOARD_VIEW,

        PermissionCode.PRODUCTS_VIEW,

        PermissionCode.CUSTOMERS_VIEW,
        PermissionCode.CUSTOMERS_CREATE,
        PermissionCode.CUSTOMERS_UPDATE,

        PermissionCode.SALES_VIEW,
        PermissionCode.SALES_CREATE,

        PermissionCode.PAYMENTS_VIEW,
        PermissionCode.PAYMENTS_CREATE,
    ],

    RoleName.INVENTORY_MANAGER: [
        PermissionCode.DASHBOARD_VIEW,

        PermissionCode.PRODUCTS_VIEW,
        PermissionCode.PRODUCTS_CREATE,
        PermissionCode.PRODUCTS_UPDATE,

        PermissionCode.CATEGORIES_VIEW,
        PermissionCode.CATEGORIES_CREATE,
        PermissionCode.CATEGORIES_UPDATE,

        PermissionCode.SUPPLIERS_VIEW,
        PermissionCode.SUPPLIERS_CREATE,
        PermissionCode.SUPPLIERS_UPDATE,

        PermissionCode.PURCHASES_VIEW,
        PermissionCode.PURCHASES_CREATE,
        PermissionCode.PURCHASES_UPDATE,

        PermissionCode.INVENTORY_VIEW,
        PermissionCode.INVENTORY_ADJUST,

        PermissionCode.REPORTS_VIEW,
    ],

    RoleName.CUSTOMER: [
        PermissionCode.PRODUCTS_VIEW,
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