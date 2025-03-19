"""Update email to user

Revision ID: 2b21f3e8b438
Revises: 97439cdc84b5
Create Date: 2025-03-20 00:18:42.119526

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b21f3e8b438'
down_revision: Union[str, None] = '97439cdc84b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('user', 'username', new_column_name='email')
    op.alter_column('user', 'email', type_=sa.String(60), existing_nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('user', 'email', new_column_name='username')
