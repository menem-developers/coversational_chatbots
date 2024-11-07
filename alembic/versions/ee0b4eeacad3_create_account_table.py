"""create account table

Revision ID: ee0b4eeacad3
Revises: 0edf31438799
Create Date: 2024-11-04 11:27:33.597431

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee0b4eeacad3'
down_revision: Union[str, None] = '0edf31438799'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the createuser table
    op.create_table(
        'chatbot',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, nullable=False),
        sa.Column('chatbotid', sa.String(), nullable=True, index=True),
        sa.Column('userid', sa.Integer(), nullable=True, index=True),
        sa.Column('admin_userid', sa.Integer(), nullable=True, index=True),
        sa.Column('aidomain', sa.String(), nullable=False),
        sa.Column('template', sa.String(), nullable=False),
        sa.Column('chatbotname', sa.String(), nullable=False),
        sa.Column('ainame', sa.String(), nullable=False),
        sa.Column('aimodel', sa.String(), nullable=False),
        sa.Column('doc_name', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.false())
    )

def downgrade():
    # Drop the createuser table
    op.drop_table('chatbot')

