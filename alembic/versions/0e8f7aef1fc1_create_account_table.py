"""create account table

Revision ID: 0e8f7aef1fc1
Revises: ee0b4eeacad3
Create Date: 2024-11-06 16:26:24.064922

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e8f7aef1fc1'
down_revision: Union[str, None] = 'ee0b4eeacad3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the Createmotorinsurance table
    op.create_table(
        'motorinsurance',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('chassisno', sa.String, nullable=False, index=True),
        sa.Column('make', sa.String, nullable=False),
        sa.Column('model', sa.String, nullable=False),
        sa.Column('seatingcapacity', sa.String, nullable=False),
        sa.Column('bodytype', sa.String, nullable=False),
        sa.Column('vehicleusage', sa.String, nullable=False),
        sa.Column('year', sa.String, nullable=False),
        sa.Column('customerid', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime, nullable=True),
        sa.Column('is_deleted', sa.Boolean, default=False),
    )

def downgrade():
    # Drop the Createmotorinsurance table if downgrading
    op.drop_table('motorinsurance')

