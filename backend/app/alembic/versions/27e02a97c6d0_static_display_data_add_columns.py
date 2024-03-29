"""static_display_data_add_columns

Revision ID: 27e02a97c6d0
Revises: dfa01fc7000f
Create Date: 2022-11-09 02:01:38.711121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27e02a97c6d0'
down_revision = 'dfa01fc7000f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('static_display_data', sa.Column('is_active', sa.BOOLEAN(), nullable=True))
    op.execute("UPDATE static_display_data SET is_active = false")
    op.alter_column('static_display_data', 'is_active', nullable=False)

    op.add_column('static_display_data', sa.Column('placed_databinds', sa.TEXT(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('static_display_data', 'placed_databinds')
    op.drop_column('static_display_data', 'is_active')
    # ### end Alembic commands ###
