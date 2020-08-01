"""Create ClothesIndex

Revision ID: 89f21945899b
Revises: 83bf2cac084d
Create Date: 2020-07-10 11:32:10.328602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89f21945899b'
down_revision = '83bf2cac084d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clothes_index',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clothes_index')
    # ### end Alembic commands ###