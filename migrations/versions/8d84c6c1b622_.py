"""empty message

Revision ID: 8d84c6c1b622
Revises: e39d109048eb
Create Date: 2024-05-26 17:22:55.707826

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8d84c6c1b622'
down_revision = 'e39d109048eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('size',
               existing_type=mysql.DECIMAL(precision=10, scale=0),
               type_=sa.Integer(),
               existing_nullable=True)
        batch_op.create_foreign_key(None, 'sizes_in_stock', ['size'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('size',
               existing_type=sa.Integer(),
               type_=mysql.DECIMAL(precision=10, scale=0),
               existing_nullable=True)

    # ### end Alembic commands ###
