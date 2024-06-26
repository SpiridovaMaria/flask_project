"""empty message

Revision ID: 7562d5902fec
Revises: 852af3140a7c
Create Date: 2024-05-22 13:41:48.581915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7562d5902fec'
down_revision = '852af3140a7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('prod_color', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('prod_material', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('prod_country', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('prod_photo', sa.String(length=1000), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('prod_photo')
        batch_op.drop_column('prod_country')
        batch_op.drop_column('prod_material')
        batch_op.drop_column('prod_color')

    # ### end Alembic commands ###
