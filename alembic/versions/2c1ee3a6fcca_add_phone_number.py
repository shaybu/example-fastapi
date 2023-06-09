"""add phone number

Revision ID: 2c1ee3a6fcca
Revises: 9527944cbac1
Create Date: 2023-06-07 12:55:02.958893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c1ee3a6fcca'
down_revision = '9527944cbac1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    pass
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    pass
    # ### end Alembic commands ###
