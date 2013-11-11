revision = '34e208d53dbf'
down_revision = '4e68bb9364f2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('data_species_regions',
        sa.Column('cons_report_observation', sa.UnicodeText,
                  nullable=True))


def downgrade():
    op.drop_column('data_species_regions', 'cons_report_observation')
