"""create posts table

Revision ID: ff7552dbfe4d
Revises: 
Create Date: 2023-07-30 17:09:24.266033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff7552dbfe4d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key= True), sa.Column('title', sa.String(), nullable=True))
    pass


def downgrade():
    op.drop_table('posts')
    pass
