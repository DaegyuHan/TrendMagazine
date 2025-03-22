from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fc7f5a9afc9c'
down_revision: Union[str, None] = 'ae08d558e4d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # user_role enum 타입에 'USER' 추가
    op.execute("ALTER TYPE user_role ADD VALUE 'USER'")

    # 새로운 enum 타입을 만들어서 기존 칼럼을 새로운 타입으로 교체 (이 방법을 통해 JOURNALIST, GUEST 삭제)
    op.execute("""
    CREATE TYPE user_role_new AS ENUM ('admin', 'user');
    """)

    # 'user_role' 칼럼의 타입을 새로운 enum 타입으로 변경
    op.alter_column('user', 'user_role', type_=postgresql.ENUM('admin', 'user', name='user_role_new'), existing_type=postgresql.ENUM('admin', 'journalist', 'guest', name='user_role'))

    # Create magazine table
    op.create_table('magazine',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('profile_image', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=60), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=True)
    )

    op.add_column('article', sa.Column('magazine_id', sa.Integer(), sa.ForeignKey('magazine.id'), nullable=False))

def downgrade():
    # 'magazine' 테이블과 'magazine_id' 칼럼을 제거
    op.drop_column('article', 'magazine_id')
    op.drop_table('magazine')

    # 새로 만든 enum 타입을 삭제하고 원래 타입을 복원 (옵션)
    op.execute("""
    DROP TYPE user_role_new;
    """)

    # 'user_role' 칼럼을 이전 enum 타입으로 되돌림
    op.alter_column('user', 'user_role', type_=postgresql.ENUM('admin', 'journalist', 'guest', name='user_role'), existing_type=postgresql.ENUM('admin', 'user', name='user_role_new'))
