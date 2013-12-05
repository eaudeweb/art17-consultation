revision = '12f51bf1fa69'
down_revision = '1dfdfccbff9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('config',
        sa.Column('objectid', sa.VARCHAR(256), nullable=False),
        sa.Column('value', sa.UnicodeText, nullable=True),
        sa.PrimaryKeyConstraint('objectid'),
    )

    config = sa.sql.table(
        'config',
        sa.sql.column('objectid'),
        sa.sql.column('value'),
    )

    op.bulk_insert(config,[
        {'objectid': 'SPECIES_MAP_URL', 'value': None},
        {'objectid': 'HABITAT_MAP_URL', 'value': None},
        {'objectid': 'CONSULTATION_DATASET', 'value': "1"},
    ])


def downgrade():
    op.drop_table('config')
