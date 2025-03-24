"""Update name tag_simularities table

Revision ID: 8413bc4186f2
Revises: d6398e85918f
Create Date: 2025-03-24 14:31:25.270625

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8413bc4186f2'
down_revision: Union[str, None] = 'd6398e85918f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# 테이블 이름 변경
def upgrade() -> None:
    op.rename_table('tag_similarity', 'tag_simularities')

def downgrade() -> None:
    op.rename_table('tag_simularities', 'tag_similarity')