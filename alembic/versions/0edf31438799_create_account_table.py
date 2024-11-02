"""create account table

Revision ID: 0edf31438799
Revises: 6f4143730a1d
Create Date: 2024-11-02 18:14:52.953956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = '0edf31438799'
down_revision: Union[str, None] = '6f4143730a1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'adminuser',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, index=True),
        sa.Column('email', sa.String, index=True),
        sa.Column('gender', sa.String, index=True),
        sa.Column('phonenumber', sa.String, nullable=True, index=True),
        sa.Column('address', sa.JSON, nullable=True),
        sa.Column('companyid', sa.String, nullable=True),
        sa.Column('signintype', sa.String, nullable=True),
        sa.Column('otp', sa.Integer, nullable=True),
        sa.Column('mobile_token', sa.String, nullable=True),
        sa.Column('password', sa.String, nullable=True),
        sa.Column('is_superadmin', sa.Boolean, nullable=True, default=False),
        sa.Column('superadminrole', sa.Integer, nullable=True),
        sa.Column('is_admin', sa.Boolean, nullable=True, default=False),
        sa.Column('adminrole', sa.Integer, nullable=True),
        sa.Column('is_staff', sa.Boolean, nullable=True, default=True),
        sa.Column('staffrole', sa.Integer, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=True, default=func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=True, default=func.now(), onupdate=func.now()),
        sa.Column('deleted_at', sa.DateTime, nullable=True, default=func.now()),
        sa.Column('is_deleted', sa.Boolean, nullable=True, default=False),
        sa.Column('is_active', sa.Boolean, nullable=True, default=True),
    )


def downgrade():
    op.drop_table('adminuser')
