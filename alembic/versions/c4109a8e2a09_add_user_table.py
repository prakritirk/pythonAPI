"""add user table

Revision ID: c4109a8e2a09
Revises: 186722ea74f3
Create Date: 2023-07-30 17:27:13.213394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4109a8e2a09'
down_revision = '186722ea74f3'
branch_labels = None
depends_on = None


def upgrade() :
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False), 
                    sa.Column('email', sa.String(), nullable=False), 
                    sa.Column('password', sa.String(), nullable=False), 
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False), 
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
