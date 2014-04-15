revision = 'fa418116288'
down_revision = '576f3f7c63ce'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'datasets',
        sa.Column('checklist', sa.Boolean(), default=False, nullable=True),
    )
    op.add_column(
        'data_habitats_check_list',
        sa.Column('dataset_id', sa.Integer, nullable=True),
    )
    op.add_column(
        'data_species_check_list',
        sa.Column('dataset_id', sa.Integer, nullable=True),
    )


def downgrade():
    op.execute("DELETE FROM DATASETS WHERE CHECKLIST=1")
    op.drop_column('datasets', 'checklist')
    op.drop_column('data_species_check_list', 'dataset_id')
    op.drop_column('data_habitats_check_list', 'dataset_id')
