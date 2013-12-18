# encoding: utf-8

revision = '236f754feafc'
down_revision = '41f95734ef9'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


def upgrade():
    op.add_column('lu_population_number',
        sa.Column('name_ro', sa.UnicodeText, nullable=True))

    op.add_column('lu_population_units_restricted',
        sa.Column('name_ro', sa.UnicodeText, nullable=True))

    lu_pop_codes = table('lu_population_number',
        column('code', sa.String),
        column('name_ro', sa.UnicodeText))

    lu_pop_restrict_codes = table('lu_population_units_restricted',
        column('code', sa.String),
        column('name_ro', sa.UnicodeText))

    for code, name_ro in DATA:

        op.execute(
            lu_pop_codes.update()
                .where(lu_pop_codes.c.code == op.inline_literal(code))
                .values({'name_ro': op.inline_literal(name_ro)}))

        op.execute(
            lu_pop_restrict_codes.update()
                .where(lu_pop_restrict_codes.c.code == op.inline_literal(code))
                .values({'name_ro': op.inline_literal(name_ro)}))



def downgrade():
    op.drop_column('lu_population_number', 'name_ro')
    op.drop_column('lu_population_units_restricted', 'name_ro')


DATA = [
    ('i', u"Numarul de indivizi"),
    ('adults', u"Numarul de adulti"),
    ('subadults', u"Numarul de subadulti"),
    ('bfemales', u"Numarul de femele de reproductie"),
    ('cmales', u"Numarul de masculi de asteptare"),
    ('males', u"Numarul de masculi"),
    ('p', u"Numarul de perechi"),
    ('shoots', u"Numarul de lastari"),
    ('tufts', u"Numarul de tufe"),
    ('fstems', u"Numarul de tulpini cu flori"),
    ('localities', u"Numarul de zone"),
    ('colonies', u"Numarul de colonii"),
    ('logs', u"Numarul de busteni locuiti"),
    ('trees', u"Numarul de arbori locuiti"),
    ('stones', u"Numarul de pietre locuite / bolovani"),
    ('area', u"Suprafata acoperita de populatie"),
    ('length', u"Durata de facilitate locuit km"),
    ('grids1x1', u"Numarul de grile 1x1"),
    ('grids5x5', u"Numarul de grile 5x5"),
    ('grids10x10', u"Numarul de grile 10x10"),
]
