"""Add a historical sale-cost snapshot and basic financial constraints.

Revision ID: b1c9d87e12a4
Revises: 27255c8ab738
"""

from alembic import op
import sqlalchemy as sa


revision = "b1c9d87e12a4"
down_revision = "27255c8ab738"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "sale_items",
        sa.Column("cost_price", sa.Numeric(12, 2), nullable=True),
    )
    op.execute(
        "UPDATE sale_items "
        "JOIN products ON products.id = sale_items.product_id "
        "SET sale_items.cost_price = products.purchase_price"
    )
    op.alter_column(
        "sale_items",
        "cost_price",
        existing_type=sa.Numeric(12, 2),
        nullable=False,
    )

    op.create_check_constraint("ck_products_stock_nonnegative", "products", "stock_quantity >= 0")
    op.create_check_constraint("ck_products_minimum_stock_nonnegative", "products", "minimum_stock >= 0")
    op.create_check_constraint("ck_products_purchase_price_nonnegative", "products", "purchase_price >= 0")
    op.create_check_constraint("ck_products_selling_price_nonnegative", "products", "selling_price >= 0")
    op.create_check_constraint("ck_stock_transactions_quantity_positive", "stock_transactions", "quantity > 0")
    op.create_check_constraint("ck_payments_amount_positive", "payments", "amount > 0")


def downgrade() -> None:
    op.drop_constraint("ck_payments_amount_positive", "payments", type_="check")
    op.drop_constraint("ck_stock_transactions_quantity_positive", "stock_transactions", type_="check")
    op.drop_constraint("ck_products_selling_price_nonnegative", "products", type_="check")
    op.drop_constraint("ck_products_purchase_price_nonnegative", "products", type_="check")
    op.drop_constraint("ck_products_minimum_stock_nonnegative", "products", type_="check")
    op.drop_constraint("ck_products_stock_nonnegative", "products", type_="check")
    op.drop_column("sale_items", "cost_price")
