from enum import StrEnum


class PermissionCode(StrEnum):
    DASHBOARD_VIEW = "dashboard.view"

    USERS_VIEW = "users.view"
    USERS_CREATE = "users.create"
    USERS_UPDATE = "users.update"
    USERS_DELETE = "users.delete"

    ROLES_VIEW = "roles.view"
    ROLES_CREATE = "roles.create"
    ROLES_UPDATE = "roles.update"
    ROLES_DELETE = "roles.delete"

    PRODUCTS_VIEW = "products.view"
    PRODUCTS_CREATE = "products.create"
    PRODUCTS_UPDATE = "products.update"
    PRODUCTS_DELETE = "products.delete"

    CATEGORIES_VIEW = "categories.view"
    CATEGORIES_CREATE = "categories.create"
    CATEGORIES_UPDATE = "categories.update"
    CATEGORIES_DELETE = "categories.delete"

    SUPPLIERS_VIEW = "suppliers.view"
    SUPPLIERS_CREATE = "suppliers.create"
    SUPPLIERS_UPDATE = "suppliers.update"
    SUPPLIERS_DELETE = "suppliers.delete"

    CUSTOMERS_VIEW = "customers.view"
    CUSTOMERS_CREATE = "customers.create"
    CUSTOMERS_UPDATE = "customers.update"
    CUSTOMERS_DELETE = "customers.delete"

    PURCHASES_VIEW = "purchases.view"
    PURCHASES_CREATE = "purchases.create"
    PURCHASES_UPDATE = "purchases.update"
    PURCHASES_DELETE = "purchases.delete"

    SALES_VIEW = "sales.view"
    SALES_CREATE = "sales.create"
    SALES_UPDATE = "sales.update"
    SALES_DELETE = "sales.delete"

    INVENTORY_VIEW = "inventory.view"
    INVENTORY_ADJUST = "inventory.adjust"

    PAYMENTS_VIEW = "payments.view"
    PAYMENTS_CREATE = "payments.create"

    REPORTS_VIEW = "reports.view"

    SETTINGS_MANAGE = "settings.manage"


PERMISSION_DEFINITIONS = [
    ("Dashboard View", PermissionCode.DASHBOARD_VIEW),

    ("Users View", PermissionCode.USERS_VIEW),
    ("Users Create", PermissionCode.USERS_CREATE),
    ("Users Update", PermissionCode.USERS_UPDATE),
    ("Users Delete", PermissionCode.USERS_DELETE),

    ("Roles View", PermissionCode.ROLES_VIEW),
    ("Roles Create", PermissionCode.ROLES_CREATE),
    ("Roles Update", PermissionCode.ROLES_UPDATE),
    ("Roles Delete", PermissionCode.ROLES_DELETE),

    ("Products View", PermissionCode.PRODUCTS_VIEW),
    ("Products Create", PermissionCode.PRODUCTS_CREATE),
    ("Products Update", PermissionCode.PRODUCTS_UPDATE),
    ("Products Delete", PermissionCode.PRODUCTS_DELETE),

    ("Categories View", PermissionCode.CATEGORIES_VIEW),
    ("Categories Create", PermissionCode.CATEGORIES_CREATE),
    ("Categories Update", PermissionCode.CATEGORIES_UPDATE),
    ("Categories Delete", PermissionCode.CATEGORIES_DELETE),

    ("Suppliers View", PermissionCode.SUPPLIERS_VIEW),
    ("Suppliers Create", PermissionCode.SUPPLIERS_CREATE),
    ("Suppliers Update", PermissionCode.SUPPLIERS_UPDATE),
    ("Suppliers Delete", PermissionCode.SUPPLIERS_DELETE),

    ("Customers View", PermissionCode.CUSTOMERS_VIEW),
    ("Customers Create", PermissionCode.CUSTOMERS_CREATE),
    ("Customers Update", PermissionCode.CUSTOMERS_UPDATE),
    ("Customers Delete", PermissionCode.CUSTOMERS_DELETE),

    ("Purchases View", PermissionCode.PURCHASES_VIEW),
    ("Purchases Create", PermissionCode.PURCHASES_CREATE),
    ("Purchases Update", PermissionCode.PURCHASES_UPDATE),
    ("Purchases Delete", PermissionCode.PURCHASES_DELETE),

    ("Sales View", PermissionCode.SALES_VIEW),
    ("Sales Create", PermissionCode.SALES_CREATE),
    ("Sales Update", PermissionCode.SALES_UPDATE),
    ("Sales Delete", PermissionCode.SALES_DELETE),

    ("Inventory View", PermissionCode.INVENTORY_VIEW),
    ("Inventory Adjust", PermissionCode.INVENTORY_ADJUST),

    ("Payments View", PermissionCode.PAYMENTS_VIEW),
    ("Payments Create", PermissionCode.PAYMENTS_CREATE),

    ("Reports View", PermissionCode.REPORTS_VIEW),

    ("Settings Manage", PermissionCode.SETTINGS_MANAGE),
]