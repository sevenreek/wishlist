"""add shop url to item

Revision ID: 05d57d9d7c03
Revises: 366c238f0eeb
Create Date: 2023-01-08 12:14:11.405711

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '05d57d9d7c03'
down_revision = '366c238f0eeb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('shop_url', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item', 'shop_url')
    # ### end Alembic commands ###
