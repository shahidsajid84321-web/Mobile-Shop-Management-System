"""Fix database defaults for online store timestamps.

Revision ID: 9d7e1f3a5b21
Revises: 8c4d6e2f1a90
"""
from alembic import op
import sqlalchemy as sa

revision = "9d7e1f3a5b21"
down_revision = "8c4d6e2f1a90"
branch_labels = None
depends_on = None


ONLINE_STORE_TIMESTAMP_COLUMNS = (
    ("carts", "created_at"),
    ("carts", "updated_at"),
    ("cart_items", "created_at"),
    ("cart_items", "updated_at"),
    ("orders", "created_at"),
    ("orders", "updated_at"),
    ("order_status_history", "created_at"),
    ("audit_logs", "created_at"),
    ("payment_events", "created_at"),
    ("order_returns", "created_at"),
)


def upgrade() -> None:
    for table_name, column_name in ONLINE_STORE_TIMESTAMP_COLUMNS:
        op.alter_column(
            table_name,
            column_name,
            existing_type=sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        )


def downgrade() -> None:
    for table_name, column_name in reversed(ONLINE_STORE_TIMESTAMP_COLUMNS):
        op.alter_column(
            table_name,
            column_name,
            existing_type=sa.DateTime(),
            nullable=False,
            server_default=None,
        )
