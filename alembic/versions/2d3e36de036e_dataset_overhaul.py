revision = '2d3e36de036e'
down_revision = '20d8f799b050'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'datasets',
        sa.Column('preview', sa.Boolean(), default=False, nullable=True),
    )
    op.add_column(
        'datasets',
        sa.Column('year_start', sa.Integer(), nullable=True),
    )
    op.add_column(
        'datasets',
        sa.Column('year_end', sa.Integer(), nullable=True),
    )


def downgrade():
    op.drop_column('datasets', 'preview')
    op.drop_column('datasets', 'year_start')
    op.drop_column('datasets', 'year_end')
