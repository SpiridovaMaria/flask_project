"""empty message

Revision ID: e39d109048eb
Revises: 5cc0d4410c8d
Create Date: 2024-05-26 16:25:47.872155

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e39d109048eb'
down_revision = '5cc0d4410c8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('address',
               existing_type=mysql.VARCHAR(length=1000),
               type_=sa.Integer(),
               existing_nullable=True)
        batch_op.create_foreign_key(None, 'departments', ['address'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('address',
               existing_type=sa.Integer(),
               type_=mysql.VARCHAR(length=1000),
               existing_nullable=True)

    # ### end Alembic commands ###
