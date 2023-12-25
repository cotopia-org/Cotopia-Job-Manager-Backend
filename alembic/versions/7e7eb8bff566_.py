"""empty message

Revision ID: 7e7eb8bff566
Revises: 18f4ab1b2363
Create Date: 2023-12-25 10:06:48.030510

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e7eb8bff566'
down_revision: Union[str, None] = '18f4ab1b2363'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users_jobs', sa.Column('acceptor_status', sa.Enum('todo', 'doing', 'done', name='jobstatus'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users_jobs', 'acceptor_status')
    # ### end Alembic commands ###
