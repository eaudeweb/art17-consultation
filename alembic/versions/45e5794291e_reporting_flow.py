revision = '45e5794291e'
down_revision = 'fa418116288'

from alembic import op
import sqlalchemy as sa


def upgrade():
    config = sa.sql.table(
        'config',
        sa.sql.column('objectid'),
        sa.sql.column('value'),
    )

    op.bulk_insert(config, [
        {'objectid': 'REPORTING_ID', 'value': None},
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
            (config.c.objectid == op.inline_literal('REPORTING_ID'))
        ))
