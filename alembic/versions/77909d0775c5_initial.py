"""initial

Revision ID: 77909d0775c5
Revises: 
Create Date: 2026-05-18 20:06:44.035311
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '77909d0775c5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'dish',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=True),
        sa.Column('dish_name', sa.String(), nullable=False, index=True),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(), nullable=False, server_default='Main Course'),
        sa.Column('image_url', sa.String(), nullable=True),
    )

    op.create_table(
        'order',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=True),
        sa.Column('total_amount', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('qr_code_path', sa.String(), nullable=True),
        sa.Column('table_number', sa.String(), nullable=True),
    )

    op.create_table(
        'orderitem',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=True),
        sa.Column('order_id', sa.Integer(), sa.ForeignKey('order.id'), nullable=False),
        sa.Column('dish_id', sa.Integer(), sa.ForeignKey('dish.id'), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('price_at_time', sa.Integer(), nullable=False),
        sa.Column('dish_name_at_time', sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('orderitem')
    op.drop_table('order')
    op.drop_table('dish')