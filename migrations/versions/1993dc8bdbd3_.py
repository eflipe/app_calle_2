"""empty message

Revision ID: 1993dc8bdbd3
Revises: 9838908f4a41
Create Date: 2021-01-11 19:19:39.862940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1993dc8bdbd3'
down_revision = '9838908f4a41'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('app_data', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_app_data_timestamp'), 'app_data', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_app_data_timestamp'), table_name='app_data')
    op.drop_column('app_data', 'timestamp')
    # ### end Alembic commands ###
