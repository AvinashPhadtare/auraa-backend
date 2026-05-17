"""initial tables

Revision ID: c20a48f0e609
Revises: 339f824a5c87
Create Date: 2026-05-14 17:00:23.939129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c20a48f0e609'
down_revision: Union[str, Sequence[str], None] = '339f824a5c87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    dishcategory = sa.Enum('starters', 'main_course', 'desserts', 'drinks', 'specials', name='dishcategory')
    dishcategory.create(op.get_bind())
    op.add_column('dish', sa.Column('category', dishcategory, nullable=True, server_default='main_course'))


def downgrade() -> None:
    op.drop_column('dish', 'category')
    sa.Enum(name='dishcategory').drop(op.get_bind())
