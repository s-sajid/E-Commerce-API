"""Add Content Column to Posts Table

Revision ID: 90ad87c7afb8
Revises: f45d6c328efd
Create Date: 2022-01-31 21:08:55.260085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90ad87c7afb8'
down_revision = 'f45d6c328efd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
