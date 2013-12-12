# encoding: utf-8

revision = '41f95734ef9'
down_revision = '3f01dc84c769'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


def upgrade():
    op.add_column('lu_ranking',
        sa.Column('name_ro', sa.UnicodeText, nullable=True))

    lu_ranking_codes = table('lu_ranking',
        column('code', sa.String),
        column('name_ro', sa.UnicodeText))

    for code, name_ro in DATA:
        op.execute(
            lu_ranking_codes.update()
                .where(lu_ranking_codes.c.code == op.inline_literal(code))
                .values({'name_ro': op.inline_literal(name_ro)}))


def downgrade():
    op.drop_column('lu_ranking', 'name_ro')


DATA = [
    ('H', u"importanțǎ mare"),
    ('M', u"importanțǎ medie"),
    ('L', u"importanțǎ micǎ"),
]
