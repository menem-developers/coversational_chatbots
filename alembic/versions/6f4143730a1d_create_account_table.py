"""create account table

Revision ID: 6f4143730a1d
Revises: f34852ad049d
Create Date: 2024-11-02 17:22:59.007275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f4143730a1d'
down_revision: Union[str, None] = 'f34852ad049d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'company',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('companyid', sa.String(), nullable=True),
        sa.Column('companyname', sa.String(), nullable=True),
        sa.Column('phonenumber', sa.String(), nullable=True),
        sa.Column('mail', sa.String(), nullable=True),
        sa.Column('address', sa.JSON, nullable=True),
        sa.Column('alternativecontact', sa.String(), nullable=True),
        sa.Column('images_name', sa.String(), nullable=True),
        sa.Column('doc_name', sa.JSON, nullable=True),
        sa.Column('paymentmethod', sa.String(), index=True, nullable=True),
        sa.Column('bankname', sa.String(), index=True, nullable=True),
        sa.Column('bankaccountnumber', sa.String(), index=True, nullable=True),
        sa.Column('accountholdername', sa.String(), index=True, nullable=True),
        sa.Column('upi_id', sa.String(), index=True, nullable=True),
        sa.Column('order_payment_account_holder_name', sa.String(), index=True, nullable=True),
        sa.Column('amount', sa.String(), index=True, nullable=True),
        sa.Column('paymentgateway', sa.String(), index=True, nullable=True),
        sa.Column('paymentstatus', sa.String(), index=True, nullable=True),
        sa.Column('paymentconfirmationnumber', sa.String(), index=True, nullable=True),
        sa.Column('subscriptionvalidity', sa.DateTime(), nullable=True),
        sa.Column('status_note', sa.String(), index=True, nullable=True),
        sa.Column('plan', sa.String(), index=True, nullable=True),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=True, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(), nullable=True, default=sa.func.now()),
        sa.Column('is_subscription', sa.Boolean(), nullable=True, default=False),
        sa.Column('is_approved', sa.Boolean(), nullable=True, default=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=True, default=False)
    )

def downgrade():
    op.drop_table('company')
