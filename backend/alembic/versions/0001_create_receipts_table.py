"""create receipts table

Revision ID: 0001
Revises:
Create Date: 2026-07-06

"""

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "receipts",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("receipt_date", sa.String(length=10), nullable=False, server_default=""),
        sa.Column("vendor", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("amount", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("category", sa.String(length=20), nullable=False, server_default=""),
        sa.Column("memo", sa.String(length=20), nullable=False, server_default=""),
        sa.Column("needs_review", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("source", sa.String(length=50), nullable=False, server_default="web"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index("ix_receipts_receipt_date", "receipts", ["receipt_date"])


def downgrade() -> None:
    op.drop_index("ix_receipts_receipt_date", table_name="receipts")
    op.drop_table("receipts")
