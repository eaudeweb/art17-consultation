revision = '576f3f7c63ce'
down_revision = '2d3e36de036e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    config = sa.sql.table(
        'config',
        sa.sql.column('objectid'),
        sa.sql.column('value'),
    )

    op.bulk_insert(config, [
        {'objectid': 'REPORTING_BEGIN', 'value': None},
        {'objectid': 'REPORTING_END', 'value': None},
    ])


def downgrade():
    config = sa.sql.table(
        'config',
        sa.sql.column('objectid'),
        sa.sql.column('value'),
    )

    op.execute(
        config.delete().
        where(
            (config.c.objectid == op.inline_literal('REPORTING_BEGIN')) |
            (config.c.objectid == op.inline_literal('REPORTING_END'))
        ))
