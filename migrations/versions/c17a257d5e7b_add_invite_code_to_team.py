"""Add invite_code to Team

Revision ID: c17a257d5e7b
Revises: 2484f35e0d2a
Create Date: 2025-05-25 01:13:36.678395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c17a257d5e7b'
down_revision = '2484f35e0d2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teams', schema=None) as batch_op:
        batch_op.add_column(sa.Column('invite_code', sa.String(length=20), nullable=True))
        batch_op.create_unique_constraint(None, ['invite_code'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teams', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('invite_code')

    # ### end Alembic commands ###
