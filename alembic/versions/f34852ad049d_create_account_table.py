"""create account table

Revision ID: f34852ad049d
Revises: c64e5dafc26c
Create Date: 2024-10-30 17:28:16.836756

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = 'f34852ad049d'
down_revision: Union[str, None] = 'c64e5dafc26c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'ai_logs',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('ip', sa.Text, nullable=True),
        sa.Column('module', sa.String, nullable=True),
        sa.Column('status_code', sa.Integer, nullable=True, default=200),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('api', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=func.now()),
    )


def downgrade():
    op.drop_table('ai_logs')
