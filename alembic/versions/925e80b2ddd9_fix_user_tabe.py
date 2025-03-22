"""Fix user tabe

Revision ID: 925e80b2ddd9
Revises: fc7f5a9afc9c
Create Date: 2025-03-22 20:53:15.565152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '925e80b2ddd9'
down_revision: Union[str, None] = 'fc7f5a9afc9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # user_role 열의 값에서 'JOURNALIST'와 'GUEST' 삭제
    op.execute("ALTER TYPE user_role DROP VALUE 'JOURNALIST'")
    op.execute("ALTER TYPE user_role DROP VALUE 'GUEST'")

    # nickname 열의 기본값 추가
    op.alter_column('user', 'nickname', server_default='default_nickname')

    # id 열에 Sequence 추가 (PostgreSQL의 경우)
    op.execute("ALTER SEQUENCE user_id_seq RESTART WITH 1")


def downgrade():
    # nickname 열의 기본값 제거
    op.alter_column('user', 'nickname', server_default=None)

    # user_role 열의 값에서 'JOURNALIST'와 'GUEST' 추가
    op.execute("ALTER TYPE user_role ADD VALUE 'JOURNALIST'")
    op.execute("ALTER TYPE user_role ADD VALUE 'GUEST'")

    # id 열에서 Sequence 제거 (PostgreSQL의 경우)