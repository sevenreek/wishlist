"""Add reservations remove updated at

Revision ID: 4ab037953c0d
Revises: 5f1351f20de7
Create Date: 2023-01-07 20:15:11.838856

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4ab037953c0d'
down_revision = '5f1351f20de7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reservation',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('count', sa.Integer(), nullable=False),
        sa.Column('reserved_by_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('reserved_by_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
        sa.ForeignKeyConstraint(['reserved_by_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('item', 'updated_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_table('reservation')
    # ### end Alembic commands ###