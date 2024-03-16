"""third migrate

Revision ID: 3337c5253310
Revises: 67587a62356e
Create Date: 2024-03-16 22:06:31.321294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3337c5253310'
down_revision = '67587a62356e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('prod_article', sa.Integer(), nullable=False),
    sa.Column('prod_name', sa.String(length=100), nullable=True),
    sa.Column('prod_category', sa.String(length=100), nullable=True),
    sa.Column('prod_description', sa.String(length=200), nullable=True),
    sa.Column('in_stock', sa.Boolean(), nullable=True),
    sa.Column('prod_price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('prod_article')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    # ### end Alembic commands ###
