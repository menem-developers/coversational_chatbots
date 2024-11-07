"""create account table

Revision ID: 495b4a4773a6
Revises: 0e8f7aef1fc1
Create Date: 2024-11-06 17:45:28.265476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = '495b4a4773a6'
down_revision: Union[str, None] = '0e8f7aef1fc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the customer table
    op.create_table(
        'customer',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('dob', sa.DateTime, nullable=False),
        sa.Column('gender', sa.String, nullable=False),
        sa.Column('mobile', sa.String, nullable=False, unique=True),
        sa.Column('address', sa.String, nullable=False),
        sa.Column('occupation', sa.String, nullable=False),
        sa.Column('licensenumber', sa.String, nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=func.now()),
        sa.Column('deleted_at', sa.DateTime, nullable=True),
        sa.Column('is_deleted', sa.Boolean, default=False),
    )

def downgrade():
    # Drop the customer table if downgrading
    op.drop_table('customer')
