revision = '17d03b52364a'
down_revision = '4eccf01743b2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.oracle import NVARCHAR2


def upgrade():
    op.add_column(
        'data_species_regions',
        sa.Column('cons_generalstatus', NVARCHAR2(255), nullable=True),
    )
    op.execute("update data_species_regions set cons_generalstatus = '1'")


def downgrade():
    op.drop_column('data_species_regions', 'cons_generalstatus')
