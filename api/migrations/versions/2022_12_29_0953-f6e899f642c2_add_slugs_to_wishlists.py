"""add slugs to wishlists

Revision ID: f6e899f642c2
Revises: cec0a39f45b5
Create Date: 2022-12-29 09:53:46.112233

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'f6e899f642c2'
down_revision = 'cec0a39f45b5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('wishlist', sa.Column('slug', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.create_unique_constraint(None, 'wishlist', ['slug'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'wishlist', type_='unique')
    op.drop_column('wishlist', 'slug')
    # ### end Alembic commands ###
