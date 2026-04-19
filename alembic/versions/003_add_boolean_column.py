"""add is_safe_to_go_outside column

Revision ID: 003
Revises: 002
Create Date: 19.04.2026
"""
from alembic import op
import sqlalchemy as sa

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column(
        "air_quality",
        sa.Column("is_safe_to_go_outside", sa.Boolean, nullable=True)
    )

def downgrade():
    op.drop_column("air_quality", "is_safe_to_go_outside")