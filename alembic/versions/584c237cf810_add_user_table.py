"""Add User Table

Revision ID: 584c237cf810
Revises: 90ad87c7afb8
Create Date: 2022-01-31 22:03:23.830421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '584c237cf810'
down_revision = '90ad87c7afb8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
