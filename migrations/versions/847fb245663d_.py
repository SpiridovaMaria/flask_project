"""empty message

Revision ID: 847fb245663d
Revises: 418559ed64b9
Create Date: 2024-05-22 17:42:14.745503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '847fb245663d'
down_revision = '418559ed64b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('baskets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('prod_id', sa.String(length=50), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['prod_id'], ['products.prod_article'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('baskets')
    # ### end Alembic commands ###