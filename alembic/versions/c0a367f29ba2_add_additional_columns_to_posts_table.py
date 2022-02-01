"""Add Additional Columns to Posts Table

Revision ID: c0a367f29ba2
Revises: 69179b3273dd
Create Date: 2022-01-31 22:14:54.695420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0a367f29ba2'
down_revision = '69179b3273dd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))

    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    
    op.drop_column('posts', 'created_at')
    pass
