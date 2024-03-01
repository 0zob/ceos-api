"""fix Asset table, folder deafault false and nullable false

Revision ID: b5f26928c528
Revises: 498cf85507da
Create Date: 2024-03-01 11:11:01.852920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5f26928c528'
down_revision: Union[str, None] = '498cf85507da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('assets', 'folder',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('assets', 'folder',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###