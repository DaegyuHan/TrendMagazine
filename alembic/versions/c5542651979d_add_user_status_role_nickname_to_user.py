"""Add user_status/role, nickname to user

Revision ID: c5542651979d
Revises: 2b21f3e8b438
Create Date: 2025-03-20 11:44:57.147033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision: str = 'c5542651979d'
down_revision: Union[str, None] = '2b21f3e8b438'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


user_role_enum = ENUM('ADMIN', 'JOURNALIST', 'GUEST', name='user_role', create_type=False)
user_status_enum = ENUM('ACTIVE', 'WITHDRAWAL', name='user_status', create_type=False)


def upgrade():
    user_role_enum.create(op.get_bind(), checkfirst=True)
    user_status_enum.create(op.get_bind(), checkfirst=True)

    op.add_column('user', sa.Column('nickname', sa.String(30), nullable=False, server_default='default_nickname'))
    op.add_column('user', sa.Column('user_role', user_role_enum, nullable=False, server_default='GUEST'))
    op.add_column('user', sa.Column('user_status', user_status_enum, nullable=False, server_default='ACTIVE'))


def downgrade():
    op.drop_column('user', 'nickname')
    op.drop_column('user', 'user_role')
    op.drop_column('user', 'user_status')

    user_role_enum.drop(op.get_bind(), checkfirst=True)
    user_status_enum.drop(op.get_bind(), checkfirst=True)
