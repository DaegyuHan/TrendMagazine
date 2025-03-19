"""Add social_id to user

Revision ID: 116cc3d83943
Revises: a56c0da53280
Create Date: 2025-03-19 17:52:07.224512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '116cc3d83943'
down_revision: Union[str, None] = 'a56c0da53280'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('user', sa.Column('social_id', sa.String(60), nullable=True))

def downgrade():
    op.drop_column('user', 'social_id')