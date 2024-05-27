"""empty message

Revision ID: 8d32fc83d1b9
Revises: f21ad9c753ca
Create Date: 2024-05-22 15:15:25.030898

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8d32fc83d1b9'
down_revision = 'f21ad9c753ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('prod_old_price', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('sale', sa.Boolean(), nullable=True))
        batch_op.alter_column('prod_price',
               existing_type=mysql.FLOAT(),
               type_=sa.Integer(),
               existing_nullable=True)
        batch_op.drop_column('best_prod')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('best_prod', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.alter_column('prod_price',
               existing_type=sa.Integer(),
               type_=mysql.FLOAT(),
               existing_nullable=True)
        batch_op.drop_column('sale')
        batch_op.drop_column('prod_old_price')

    # ### end Alembic commands ###
