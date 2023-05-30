"""add is_admin

Revision ID: 677108039a73
Revises: 9627b27a7b5a
Create Date: 2023-05-17 00:45:20.228653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '677108039a73'
down_revision = '9627b27a7b5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_admin')
    # ### end Alembic commands ###