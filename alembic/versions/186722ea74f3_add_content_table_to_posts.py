"""add content table to posts

Revision ID: 186722ea74f3
Revises: ff7552dbfe4d
Create Date: 2023-07-30 17:20:41.967643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '186722ea74f3'
down_revision = 'ff7552dbfe4d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() :
    op.drop_column('posts', 'content')
    pass
