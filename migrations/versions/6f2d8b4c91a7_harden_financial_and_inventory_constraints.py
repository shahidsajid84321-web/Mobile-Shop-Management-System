"""Harden financial and inventory constraints and add FK indexes.

Revision ID: 6f2d8b4c91a7
Revises: b1c9d87e12a4
"""

from alembic import op
import sqlalchemy as sa


revision = "6f2d8b4c91a7"
down_revision = "b1c9d87e12a4"
branch_labels = None
depends_on = None

CHECKS = {
    "ck_purchase_items_quantity_positive": ("purchase_items", "quantity > 0"),
    "ck_purchase_items_unit_price_nonnegative": ("purchase_items", "unit_price >= 0"),
    "ck_purchase_items_subtotal_nonnegative": ("purchase_items", "subtotal >= 0"),
    "ck_purchases_total_nonnegative": ("purchases", "total_amount >= 0"),
    "ck_sale_items_quantity_positive": ("sale_items", "quantity > 0"),
    "ck_sale_items_unit_price_nonnegative": ("sale_items", "unit_price >= 0"),
    "ck_sale_items_cost_price_nonnegative": ("sale_items", "cost_price >= 0"),
    "ck_sale_items_subtotal_nonnegative": ("sale_items", "subtotal >= 0"),
    "ck_sales_total_nonnegative": ("sales", "total_amount >= 0"),
    "ck_sales_discount_nonnegative": ("sales", "discount >= 0"),
    "ck_sales_tax_nonnegative": ("sales", "tax >= 0"),
    "ck_sales_grand_total_nonnegative": ("sales", "grand_total >= 0"),
    "ck_payments_sale_amount_positive": ("payments", "amount > 0"),
}

INDEXES = (
    ("ix_products_category_id", "products", ["category_id"], False),
    ("ix_purchases_supplier_id", "purchases", ["supplier_id"], False),
    ("ix_purchase_items_purchase_id", "purchase_items", ["purchase_id"], False),
    ("ix_purchase_items_product_id", "purchase_items", ["product_id"], False),
    ("ix_sales_customer_id", "sales", ["customer_id"], False),
    ("ix_sale_items_sale_id", "sale_items", ["sale_id"], False),
    ("ix_sale_items_product_id", "sale_items", ["product_id"], False),
    ("ix_payments_sale_id", "payments", ["sale_id"], False),
    ("ix_stock_transactions_product_id", "stock_transactions", ["product_id"], False),
    ("ix_users_role_id", "users", ["role_id"], False),
)


def _assert_clean_data(bind: sa.Connection) -> None:
    checks = {
        "purchase_items.quantity": "SELECT COUNT(*) FROM purchase_items WHERE quantity <= 0",
        "purchase_items.unit_price": "SELECT COUNT(*) FROM purchase_items WHERE unit_price < 0",
        "purchase_items.subtotal": "SELECT COUNT(*) FROM purchase_items WHERE subtotal < 0",
        "purchases.total_amount": "SELECT COUNT(*) FROM purchases WHERE total_amount < 0",
        "sale_items.quantity": "SELECT COUNT(*) FROM sale_items WHERE quantity <= 0",
        "sale_items.unit_price": "SELECT COUNT(*) FROM sale_items WHERE unit_price < 0",
        "sale_items.cost_price": "SELECT COUNT(*) FROM sale_items WHERE cost_price < 0",
        "sale_items.subtotal": "SELECT COUNT(*) FROM sale_items WHERE subtotal < 0",
        "sales.total_amount": "SELECT COUNT(*) FROM sales WHERE total_amount < 0",
        "sales.discount": "SELECT COUNT(*) FROM sales WHERE discount < 0",
        "sales.tax": "SELECT COUNT(*) FROM sales WHERE tax < 0",
        "sales.grand_total": "SELECT COUNT(*) FROM sales WHERE grand_total < 0",
        "payments.amount": "SELECT COUNT(*) FROM payments WHERE amount <= 0",
    }
    invalid = []
    for name, sql in checks.items():
        count = bind.execute(sa.text(sql)).scalar_one()
        if count:
            invalid.append(f"{name}: {count}")
    if invalid:
        raise RuntimeError(
            "Cannot apply migration 6f2d8b4c91a7 because existing data violates "
            "the new integrity constraints: " + ", ".join(invalid)
        )


def upgrade() -> None:
    bind = op.get_bind()
    _assert_clean_data(bind)
    for name, (table, expression) in CHECKS.items():
        op.create_check_constraint(name, table, expression)
    for name, table, columns, unique in INDEXES:
        op.create_index(name, table, columns, unique=unique)


def downgrade() -> None:
    for name, table, columns, unique in reversed(INDEXES):
        op.drop_index(name, table_name=table)
    for name, (table, _expression) in reversed(list(CHECKS.items())):
        op.drop_constraint(name, table, type_="check")
