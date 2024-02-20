"""add star column in drink table

Revision ID: a1503220bc93
Revises: b78e1a940fc5
Create Date: 2024-02-20 17:14:58.541792

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1503220bc93'
down_revision: Union[str, None] = 'b78e1a940fc5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('drinks', sa.Column('stars', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('drinks', 'stars')
    # ### end Alembic commands ###