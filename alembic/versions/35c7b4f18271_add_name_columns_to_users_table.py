"""add_name_columns_to_users_table

Revision ID: 35c7b4f18271
Revises: 8c4134bd5512
Create Date: 2022-03-06 12:58:30.335539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35c7b4f18271'
down_revision = '8c4134bd5512'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('username', sa.String(), nullable=False, unique=True))

    op.add_column('users', sa.Column('first_name', sa.String(), nullable=True))

    op.add_column('users', sa.Column('last_name', sa.String(), nullable=True))

    op.add_column('users', sa.Column('company_name', sa.String(), nullable=True))

    op.add_column('users', sa.Column('location', sa.String(), nullable=True))

    pass


def downgrade():
    op.drop_column('users', 'username')

    op.drop_column('users', 'first_name')

    op.drop_column('users', 'last_name')

    op.drop_column('users', 'company_name')

    op.drop_column('users', 'location')
    
    pass
