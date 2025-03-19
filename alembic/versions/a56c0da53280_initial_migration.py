"""Initial migration

Revision ID: a56c0da53280
Revises: 
Create Date: 2025-03-19 17:21:28.002127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a56c0da53280'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 'user' 테이블 생성
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=16), nullable=False),
        sa.Column('hashed_password', sa.String(length=60), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # 'user' 테이블 삭제
    op.drop_table('user')