"""Add social_provider to user

Revision ID: 97439cdc84b5
Revises: 116cc3d83943
Create Date: 2025-03-19 18:25:12.513908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97439cdc84b5'
down_revision: Union[str, None] = '116cc3d83943'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('social_provider', sa.String(60), nullable=True))


def downgrade() -> None:
    op.drop_column('user', 'social_provider')