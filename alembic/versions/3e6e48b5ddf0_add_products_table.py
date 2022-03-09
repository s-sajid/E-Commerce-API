"""Add products table

Revision ID: 3e6e48b5ddf0
Revises: 35c7b4f18271
Create Date: 2022-03-08 20:38:38.376219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e6e48b5ddf0'
down_revision = '35c7b4f18271'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('products',
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('prod_name', sa.String(), nullable=False),
                sa.Column('description', sa.String(), nullable=False),
                sa.Column('company_name', sa.String(), nullable=False),
                sa.Column('price', sa.Float(), nullable=False),
                sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),
                sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'), nullable=False),
                sa.PrimaryKeyConstraint('id'),
                sa.Column('owner_id', sa.Integer, nullable=False)
                )
        
    op.create_foreign_key('product_users_FK', source_table="products", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('product_users_FK', table_name="products")

    op.drop_table('products')
    pass
