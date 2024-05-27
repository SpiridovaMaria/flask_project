"""empty message

Revision ID: 5cc0d4410c8d
Revises: 20445b180d7b
Create Date: 2024-05-24 11:48:00.580967

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5cc0d4410c8d'
down_revision = '20445b180d7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('baskets', schema=None) as batch_op:
        batch_op.alter_column('size',
               existing_type=mysql.DECIMAL(precision=10, scale=0),
               type_=sa.Integer(),
               existing_nullable=True)
        batch_op.create_foreign_key(None, 'sizes_in_stock', ['size'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('baskets', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('size',
               existing_type=sa.Integer(),
               type_=mysql.DECIMAL(precision=10, scale=0),
               existing_nullable=True)

    # ### end Alembic commands ###