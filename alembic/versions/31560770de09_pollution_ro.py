# encoding: utf-8

revision = '31560770de09'
down_revision = '133e96f03444'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


def upgrade():
    op.add_column('lu_pollution',
        sa.Column('name_ro', sa.UnicodeText, nullable=True))

    lu_pollution_codes = table('lu_pollution',
        column('code', sa.String),
        column('name_ro', sa.UnicodeText))

    for code, name_ro in DATA:
        op.execute(
            lu_pollution_codes.update()
                .where(lu_pollution_codes.c.code == op.inline_literal(code))
                .values({'name_ro': op.inline_literal(name_ro)}))


def downgrade():
    op.drop_column('lu_pollution', 'name_ro')


DATA = [
    ('N', u"Azot"),
    ('P', u"Fosfor/Fosfat"),
    ('O', u"Chimicale organice toxice"),
    ('X', u"Mix de poluanți"),
    ('A', u"Acid"),
    ('T', u"Chimicale anorganice toxice"),
]
