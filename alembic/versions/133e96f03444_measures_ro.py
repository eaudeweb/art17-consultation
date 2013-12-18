# encoding: utf-8

revision = '133e96f03444'
down_revision = 'da3c5fe3292'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


def upgrade():
    op.add_column('lu_measures',
        sa.Column('name_ro', sa.UnicodeText, nullable=True))

    lu_measures_codes = table('lu_measures',
        column('code', sa.String),
        column('name_ro', sa.UnicodeText))

    for code, name_ro in DATA:
        op.execute(
            lu_measures_codes.update()
                .where(lu_measures_codes.c.code == op.inline_literal(code))
                .values({'name_ro': op.inline_literal(name_ro)}))


def downgrade():
    op.drop_column('lu_measures', 'name_ro')


DATA = [
    ('1',   u"Fara masuri"),
    ('1.1', u"Nu sunt necesare masuri pentru conservarea habitatelor/speciilor"),
    ('1.2', u"Masuri necesare, dar neimplementate"),
    ('1.3', u"Nici o masura cunoscuta/imposibil de realizat masuri specifice"),
    ('2',   u"Masuri in legatura cu agricultura si habitatele deschise"),
    ('2.0', u"Alte masuri legate de agricultura"),
    ('2.1', u"Mentenanta pajistilor si a altor habitate deschise"),
    ('2.2', u"Adaptare productie culturi"),
    ('3',   u"Masuri legate de paduri si habitate forestiere"),
    ('3.0', u"Alte masuri forestiere"),
    ('3.1', u"Restaurarea/imbunatatirea habitatelor forestiere"),
    ('3.2', u"Adaptare management forestier"),
    ('4',   u"Masuri legate de mlastini, apa dulce si habitate de coasta"),
    ('4.0',  u"Alte masuri legate de mlastini"),
    ('4.1', u"Restaurarea/imbunatatirea calitatii apei"),
    ('4.2', u"Restaurarea/Imbunatatirea regimului hidrologic"),
    ('4.3', u"Abstractii ale managementului apelor"),
    ('4.4', u"Restaurarea zonelor de coasta"),
    ('5',   u"Masuri legate de habitatele marine"),
    ('5.0', u"Alte masuri legate de habitatele marine"),
    ('5.1', u"Restaurarea habitatelor marine"),
    ('6',   u"Masuri legate de planificarea spatiala"),
    ('6.0', u"Alte masuri spatiale"),
    ('6.1', u"Stabilirea ariilor/sit-urilor protejate"),
    ('6.2', u"Stabilirea zonelor salbatice"),
    ('6.3', u"Protectia legala a habitatelor si speciilor"),
    ('6.4', u"Managementul caracteristicilor peisagistice"),
    ('6.5', u"Adaptarea/Abolirea utilizarii de teren in scopuri militare"),
    ('7',   u"Masuri legate de vanatoare si pescuit si managementul speciilor"),
    ('7.0', u"Alte masuri ale managementului de specii"),
    ('7.1', u"Reglementarea/Managementul vanatorii si culesului"),
    ('7.2', u"Reglementarea/Managementul pescuitului in sistemele lacustre"),
    ('7.3', u"Regularea/Managementul pescuitului in sistemele marine sau cu ape salcii"),
    ('7.4', u"Masuri legate de specii specifice sau grupuri de specii"),
    ('8',   u"Masuri legate de ariile urbane, industriale, energie si transport"),
    ('8.0', u"Alte masuri"),
    ('8.1', u"Managementul deseurilor urbane si industriale"),
    ('8.2', u"Management specific al sistemelor de trafic si transport de energie"),
    ('8.3', u"Managementul traficului marin"),
    ('9',   u"Masuri legate de utilizarea unor resurse speciale"),
    ('9.0', u"Alte masuri legate de resurse"),
    ('9.1', u"Reglementarea/Managementul exploatarilor de resurse naturale la nivel terestru"),
    ('9.2', u"Reglementarea/Managementul exploatarilor de resurse naturale la nivel maritim"),
]

