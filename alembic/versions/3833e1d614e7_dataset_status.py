revision = '3833e1d614e7'
down_revision = '4530fbf48782'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'datasets',
        sa.Column('status', sa.Integer(), nullable=True, default=0),
    )


def downgrade():
    op.drop_column('datasets', 'status')
