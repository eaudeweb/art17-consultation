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
    ('i', u"Numǎrul de indivizi"),
    ('adults', u"Numǎrul de adulți"),
    ('subadults', u"Numǎrul de subadulți"),
    ('bfemales', u"Numǎrul de femele de reproducție"),
    ('cmales', u"Numǎrul de masculi de așteptare"),
    ('males', u"Numǎrul de masculi"),
    ('p', u"Numǎrul de perechi"),
    ('shoots', u"Numǎrul de lăstari"),
    ('tufts', u"Numǎrul de tufe"),
    ('fstems', u"Numǎrul de tulpini cu flori"),
    ('localities', u"Numǎrul de zone"),
    ('colonies', u"Numǎrul de colonii"),
    ('logs', u"Numǎrul de bușteni locuiți"),
    ('trees', u"Numǎrul de arbori locuiți"),
    ('stones', u"Numǎrul de pietre locuite / bolovani"),
    ('area', u"Suprafața acoperitǎ de populație"),
    ('length', u"Durata de facilitate locuit km"),
    ('grids1x1', u"Numǎrul de grile 1x1"),
    ('grids5x5', u"Numǎrul de grile 5x5"),
    ('grids10x10', u"Numǎrul de grile 10x10"),
]
