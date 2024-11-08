"""create account table

Revision ID: 725934f1c3d8
Revises: 495b4a4773a6
Create Date: 2024-11-08 10:19:37.498393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = '725934f1c3d8'
down_revision: Union[str, None] = '495b4a4773a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'test_db',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('docs_string', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=func.now(), onupdate=func.now()),
        sa.Column('deleted_at', sa.DateTime, nullable=True),
        sa.Column('is_deleted', sa.Boolean, default=False),
    )

def downgrade():
    op.drop_table('test_db')
