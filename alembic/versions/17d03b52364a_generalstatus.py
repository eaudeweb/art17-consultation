revision = '17d03b52364a'
down_revision = '39f65264570c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'data_species_regions',
        sa.Column('cons_generalstatus', NVARCHAR2(255), nullable=True),
    )


def downgrade():
    op.drop_column('data_species_regions', 'cons_generalstatus')
