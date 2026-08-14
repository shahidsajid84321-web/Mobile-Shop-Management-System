from enum import StrEnum


class RoleName(StrEnum):
    SUPER_ADMIN = "Super Admin"
    ADMIN = "Admin"
    MANAGER = "Manager"
    SALESMAN = "Salesman"
    INVENTORY_MANAGER = "Inventory Manager"
    CUSTOMER = "Customer"