"""Add Foreign Key to Posts Table

Revision ID: 69179b3273dd
Revises: 584c237cf810
Create Date: 2022-01-31 22:09:33.782437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69179b3273dd'
down_revision = '584c237cf810'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))

    op.create_foreign_key('posts_users_FK', source_table="posts", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_FK', table_name="posts")

    op.drop_column('posts', 'owner_id')
    pass
