"""Add article table

Revision ID: de78e4a83601
Revises: c5542651979d
Create Date: 2025-03-21 00:15:47.136993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de78e4a83601'
down_revision: Union[str, None] = 'c5542651979d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    from sqlalchemy import TIMESTAMP
    op.create_table(
        "article",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("content", sa.Text, nullable=True),
        sa.Column("created_at", TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id", ondelete="CASCADE"), nullable=True),
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("article")