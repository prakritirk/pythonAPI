"""add foreign key to post table'

Revision ID: 70af9b4d6b3d
Revises: c4109a8e2a09
Create Date: 2023-07-30 17:34:04.314353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70af9b4d6b3d'
down_revision = 'c4109a8e2a09'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
