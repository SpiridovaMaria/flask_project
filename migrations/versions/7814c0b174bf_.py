"""empty message

Revision ID: 7814c0b174bf
Revises: 847fb245663d
Create Date: 2024-05-23 23:04:18.791047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7814c0b174bf'
down_revision = '847fb245663d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('prod_id', sa.String(length=50), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('total_price', sa.Numeric(), nullable=True),
    sa.Column('address', sa.String(length=1000), nullable=True),
    sa.ForeignKeyConstraint(['prod_id'], ['products.prod_article'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    # ### end Alembic commands ###
