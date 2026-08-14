"""harden security orders and auditing

Revision ID: 8c4d6e2f1a90
Revises: 7b2f1e4c8d90
"""
from alembic import op
import sqlalchemy as sa

revision = "8c4d6e2f1a90"
down_revision = "7b2f1e4c8d90"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("sales", sa.Column("is_voided", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.create_index("ix_sales_is_voided", "sales", ["is_voided"])

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("entity", sa.String(length=50), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=True),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"])
    op.create_index("ix_audit_logs_entity", "audit_logs", ["entity"])
    op.create_index("ix_audit_logs_entity_id", "audit_logs", ["entity_id"])
    op.create_index("ix_audit_logs_created_at", "audit_logs", ["created_at"])

    op.create_table(
        "payment_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("event_id", sa.String(length=150), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("payload", sa.Text(), nullable=True),
        sa.Column("processed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_payment_events_event_id", "payment_events", ["event_id"], unique=True)

    op.create_table(
        "order_returns",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("reason", sa.String(length=500), nullable=False),
        sa.Column("refund_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"]),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"]),
        sa.CheckConstraint("refund_amount >= 0", name="ck_order_returns_refund_nonnegative"),
    )
    op.create_index("ix_order_returns_order_id", "order_returns", ["order_id"])
    op.create_index("ix_order_returns_customer_id", "order_returns", ["customer_id"])
    op.create_index("ix_order_returns_status", "order_returns", ["status"])


def downgrade() -> None:
    op.drop_index("ix_order_returns_status", table_name="order_returns")
    op.drop_index("ix_order_returns_customer_id", table_name="order_returns")
    op.drop_index("ix_order_returns_order_id", table_name="order_returns")
    op.drop_table("order_returns")
    op.drop_index("ix_payment_events_event_id", table_name="payment_events")
    op.drop_table("payment_events")
    op.drop_index("ix_audit_logs_created_at", table_name="audit_logs")
    op.drop_index("ix_audit_logs_entity_id", table_name="audit_logs")
    op.drop_index("ix_audit_logs_entity", table_name="audit_logs")
    op.drop_index("ix_audit_logs_action", table_name="audit_logs")
    op.drop_index("ix_audit_logs_user_id", table_name="audit_logs")
    op.drop_table("audit_logs")
    op.drop_index("ix_sales_is_voided", table_name="sales")
    op.drop_column("sales", "is_voided")
