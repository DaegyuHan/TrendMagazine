"""Add category  to article

Revision ID: ae08d558e4d2
Revises: de78e4a83601
Create Date: 2025-03-21 13:26:00.526018

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae08d558e4d2'
down_revision: Union[str, None] = 'de78e4a83601'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('article', sa.Column('category', sa.String(30), nullable=False, server_default='default_category'))

def downgrade() -> None:
    op.drop_column('article', 'category')