"""create account table

Revision ID: c64e5dafc26c
Revises: 
Create Date: 2024-10-30 15:20:40.958440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = 'c64e5dafc26c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, nullable=True),
        sa.Column('companyid', sa.String, nullable=True),
        sa.Column('email', sa.String, nullable=True),
        sa.Column('phonenumber', sa.String, nullable=True),
        sa.Column('gender', sa.String, nullable=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('profilepic', sa.String, nullable=False),
        sa.Column('otp', sa.String, nullable=False),
        sa.Column('account_active', sa.Boolean, nullable=True, default=True),
        sa.Column('address', sa.JSON, nullable=True, default=True),
        sa.Column('mobile_token', sa.String, nullable=True),
        sa.Column('signintype', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=True, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=True, server_default=func.now(), onupdate=func.now()),
        sa.Column('deleted_at', sa.DateTime, nullable=True),
        sa.Column('is_deleted', sa.Boolean, nullable=True, default=False),
        sa.Column('is_active', sa.Boolean, nullable=True, default=True),
    )


def downgrade():
    op.drop_table('user')
