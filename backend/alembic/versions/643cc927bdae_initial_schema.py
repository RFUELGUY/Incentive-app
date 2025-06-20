"""Initial schema

Revision ID: 643cc927bdae
Revises: 2a612b23eeec
Create Date: 2025-06-10 16:25:35.744385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '643cc927bdae'
down_revision: Union[str, None] = '2a612b23eeec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('claims', sa.Column('amount', sa.Float(), nullable=True))
    op.add_column('claims', sa.Column('tx_hash', sa.String(), nullable=True))
    op.add_column('salesmen', sa.Column('wallet_balance', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('salesmen', 'wallet_balance')
    op.drop_column('claims', 'tx_hash')
    op.drop_column('claims', 'amount')
    # ### end Alembic commands ###
