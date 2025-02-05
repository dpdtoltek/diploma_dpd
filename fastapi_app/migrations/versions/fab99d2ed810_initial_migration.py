"""Initial migration

Revision ID: fab99d2ed810
Revises: f7b0e67a6f46
Create Date: 2025-01-21 12:26:02.049019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fab99d2ed810'
down_revision: Union[str, None] = 'f7b0e67a6f46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('buyers', sa.Column('balance', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('buyers', 'balance')
    # ### end Alembic commands ###
