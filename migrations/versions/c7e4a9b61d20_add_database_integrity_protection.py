"""Add database-level integrity protection.

Revision ID: c7e4a9b61d20
Revises: 9d7e1f3a5b21
"""

from alembic import op
import sqlalchemy as sa


revision = "c7e4a9b61d20"
down_revision = "9d7e1f3a5b21"
branch_labels = None
depends_on = None


CHECKS = {
    # Inventory
    "ck_stock_transactions_unit_price_nonnegative": (
        "stock_transactions",
        "unit_price >= 0",
    ),

    # Core master data: reject empty/whitespace-only required text.
    "ck_roles_name_not_blank": ("roles", "TRIM(name) <> ''"),
    "ck_users_full_name_not_blank": ("users", "TRIM(full_name) <> ''"),
    "ck_users_email_not_blank": ("users", "TRIM(email) <> ''"),
    "ck_users_password_not_blank": ("users", "TRIM(password) <> ''"),
    "ck_categories_name_not_blank": ("categories", "TRIM(name) <> ''"),
    "ck_products_name_not_blank": ("products", "TRIM(name) <> ''"),
    "ck_products_brand_not_blank": ("products", "TRIM(brand) <> ''"),
    "ck_products_sku_not_blank": ("products", "TRIM(sku) <> ''"),
    "ck_suppliers_company_name_not_blank": (
        "suppliers",
        "TRIM(company_name) <> ''",
    ),
    "ck_suppliers_contact_person_not_blank": (
        "suppliers",
        "TRIM(contact_person) <> ''",
    ),
    "ck_suppliers_phone_not_blank": ("suppliers", "TRIM(phone) <> ''"),
    "ck_customers_full_name_not_blank": (
        "customers",
        "TRIM(full_name) <> ''",
    ),
    "ck_customers_phone_not_blank": ("customers", "TRIM(phone) <> ''"),
    "ck_purchases_invoice_not_blank": (
        "purchases",
        "TRIM(invoice_number) <> ''",
    ),
    "ck_sales_invoice_not_blank": (
        "sales",
        "TRIM(invoice_number) <> ''",
    ),

    # Online store / operational records.
    "ck_orders_order_number_not_blank": (
        "orders",
        "TRIM(order_number) <> ''",
    ),
    "ck_orders_delivery_name_not_blank": (
        "orders",
        "TRIM(delivery_name) <> ''",
    ),
    "ck_orders_delivery_phone_not_blank": (
        "orders",
        "TRIM(delivery_phone) <> ''",
    ),
    "ck_orders_delivery_address_not_blank": (
        "orders",
        "TRIM(delivery_address) <> ''",
    ),
    "ck_orders_delivery_city_not_blank": (
        "orders",
        "TRIM(delivery_city) <> ''",
    ),
    "ck_order_items_product_name_not_blank": (
        "order_items",
        "TRIM(product_name) <> ''",
    ),
    "ck_order_items_sku_not_blank": (
        "order_items",
        "TRIM(sku) <> ''",
    ),
    "ck_payments_method_not_blank": (
        "payments",
        "TRIM(payment_method) <> ''",
    ),
    "ck_order_returns_status_not_blank": (
        "order_returns",
        "TRIM(status) <> ''",
    ),
    "ck_order_returns_reason_not_blank": (
        "order_returns",
        "TRIM(reason) <> ''",
    ),
    "ck_payment_events_provider_not_blank": (
        "payment_events",
        "TRIM(provider) <> ''",
    ),
    "ck_payment_events_event_id_not_blank": (
        "payment_events",
        "TRIM(event_id) <> ''",
    ),
    "ck_payment_events_event_type_not_blank": (
        "payment_events",
        "TRIM(event_type) <> ''",
    ),
    "ck_audit_logs_action_not_blank": (
        "audit_logs",
        "TRIM(action) <> ''",
    ),
    "ck_audit_logs_entity_not_blank": (
        "audit_logs",
        "TRIM(entity) <> ''",
    ),
}


def _assert_clean_data(bind: sa.Connection) -> None:
    invalid = []

    for name, (table, expression) in CHECKS.items():
        count = bind.execute(
            sa.text(f"SELECT COUNT(*) FROM `{table}` WHERE NOT ({expression})")
        ).scalar_one()
        if count:
            invalid.append(f"{table}: {name} -> {count}")

    if invalid:
        raise RuntimeError(
            "Cannot apply database integrity protection because existing data "
            "violates the new constraints: " + ", ".join(invalid)
        )


def upgrade() -> None:
    bind = op.get_bind()
    _assert_clean_data(bind)

    for name, (table, expression) in CHECKS.items():
        op.create_check_constraint(name, table, expression)


def downgrade() -> None:
    for name, (table, _expression) in reversed(list(CHECKS.items())):
        op.drop_constraint(name, table, type_="check")
