"""Update name tag_simularities table

Revision ID: 63538c9e01a1
Revises: 8413bc4186f2
Create Date: 2025-03-24 14:36:17.356920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63538c9e01a1'
down_revision: Union[str, None] = '8413bc4186f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# 테이블 이름 변경
def upgrade() -> None:
    op.rename_table('tag_simularities', 'tag_similarities')

def downgrade() -> None:
    op.rename_table('tag_similarities', 'tag_simularities')