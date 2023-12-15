"""empty message

Revision ID: 5e5a1b27a606
Revises: 0d8e65d4cfe7
Create Date: 2023-12-15 18:27:05.604994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5e5a1b27a606'
down_revision: Union[str, None] = '0d8e65d4cfe7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role',
               existing_type=postgresql.ENUM('default', name='role'),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role',
               existing_type=postgresql.ENUM('default', name='role'),
               nullable=True)
    # ### end Alembic commands ###
