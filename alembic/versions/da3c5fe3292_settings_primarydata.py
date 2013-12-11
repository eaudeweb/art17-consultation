revision = 'da3c5fe3292'
down_revision = '49f0e4b60d58'

from alembic import op
import sqlalchemy as sa


def upgrade():
    config = sa.sql.table(
        'config',
        sa.sql.column('objectid'),
        sa.sql.column('value'),
    )

    op.bulk_insert(config,[
        {'objectid': 'SPECIES_PRIMARY_DATA_URL', 'value': None},
        {'objectid': 'HABITAT_PRIMARY_DATA_URL', 'value': None},
    ])


def downgrade():
    pass
