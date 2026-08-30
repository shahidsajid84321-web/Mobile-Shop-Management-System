"""add database-backed login rate limiting

Revision ID: 9e4b2c7a61f0
Revises: b7c1e9d4f205
"""
from alembic import op
import sqlalchemy as sa

revision = "9e4b2c7a61f0"
down_revision = "b7c1e9d4f205"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "login_rate_limits",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("ip_address", sa.String(length=45), nullable=False),
        sa.Column("failed_attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("window_started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("locked_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_attempt_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("email", "ip_address", name="uq_login_rate_limits_email_ip"),
    )
    op.create_index("ix_login_rate_limits_email", "login_rate_limits", ["email"])
    op.create_index("ix_login_rate_limits_ip_address", "login_rate_limits", ["ip_address"])
    op.create_index("ix_login_rate_limits_locked_until", "login_rate_limits", ["locked_until"])


def downgrade() -> None:
    op.drop_index("ix_login_rate_limits_locked_until", table_name="login_rate_limits")
    op.drop_index("ix_login_rate_limits_ip_address", table_name="login_rate_limits")
    op.drop_index("ix_login_rate_limits_email", table_name="login_rate_limits")
    op.drop_table("login_rate_limits")
