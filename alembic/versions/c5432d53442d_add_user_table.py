"""add user table

Revision ID: c5432d53442d
Revises: a21bc704ea45
Create Date: 2023-06-07 10:34:51.309168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5432d53442d'
down_revision = 'a21bc704ea45'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
