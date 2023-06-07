"""add content colum to posts table

Revision ID: a21bc704ea45
Revises: ccedd1eec8cc
Create Date: 2023-06-06 18:46:54.403090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a21bc704ea45'
down_revision = 'ccedd1eec8cc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
