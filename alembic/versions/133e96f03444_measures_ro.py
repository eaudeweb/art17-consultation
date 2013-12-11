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
        print code, name_ro
    for code, name_ro in DATA:
        op.execute(
            lu_measures_codes.update()
                .where(lu_measures_codes.c.code == op.inline_literal(code))
                .values({'name_ro': op.inline_literal(name_ro)}))


def downgrade():
    op.drop_column('lu_measures', 'name_ro')


DATA = [
    ('1',   u"Fǎrǎ mǎsuri"),
    ('1.1', u"Nu sunt necesare mǎsuri pentru conservarea habitatelor/speciilor"),
    ('1.2', u"Mǎsuri necesare, dar neimplementate"),
    ('1.3', u"Nici o mǎsurǎ cunoscutǎ/imposibil de realizat mǎsuri specifice"),
    ('2',   u"Mǎsuri in legǎturǎ cu agricultura și habitatele deschise"),
    ('2.0', u"Alte mǎsuri legate de agriculturǎ"),
    ('2.1', u"Mentenanta pajiștilor și a altor habitate deschise"),
    ('2.2', u"Adaptare producție culturi"),
    ('3',   u"Mǎsuri legate de pǎduri și habitate forestiere"),
    ('3.0', u"Alte mǎsuri forestiere"),
    ('3.1', u"Restaurarea/imbunǎtǎțirea habitatelor forestiere"),
    ('3.2', u"Adaptare management forestier"),
    ('4',   u"Mǎsuri legate de mlaștini, apǎ dulce și habitate de coastǎ"),
    ('4.0',  u"Alte mǎsuri legate de mlaștini"),
    ('4.1', u"Restaurarea/imbunǎtǎțirea calitǎții apei"),
    ('4.2', u"Restaurarea/Imbunǎtǎțirea regimului hidrologic"),
    ('4.3', u"Abstracții ale managementului apelor"),
    ('4.4', u"Restaurarea zonelor de coastǎ"),
    ('5',   u"Mǎsuri legate de habitatele marine"),
    ('5.0', u"Alte mǎsuri legate de habitatele marine"),
    ('5.1', u"Restaurarea habitatelor marine"),
    ('6',   u"Mǎsuri legate de planificarea spațialǎ"),
    ('6.0', u"Alte mǎsuri spațiale"),
    ('6.1', u"Stabilirea ariilor/sit-urilor protejate"),
    ('6.2', u"Stabilirea zonelor sǎlbatice"),
    ('6.3', u"Protecția legalǎ a habitatelor și speciilor"),
    ('6.4', u"Managementul caracteristicilor peisagistice"),
    ('6.5', u"Adaptarea/Abolirea utilizǎrii de teren în scopuri militare"),
    ('7',   u"Mǎsuri legate de vǎnǎtoare și pescuit și managementul speciilor"),
    ('7.0', u"Alte mǎsuri ale managementului de specii"),
    ('7.1', u"Reglementarea/Managementul vǎnǎtorii și culesului"),
    ('7.2', u"Reglementarea/Managementul pescuitului în sistemele lacustre"),
    ('7.3', u"Regularea/Managementul pescuitului în sistemele marine sau cu ape sǎlcii"),
    ('7.4', u"Mǎsuri legate de specii specifice sau grupuri de specii"),
    ('8',   u"Mǎsuri legate de ariile urbane, industriale, energie și transport"),
    ('8.0', u"Alte mǎsuri"),
    ('8.1', u"Managementul deșeurilor urbane și industriale"),
    ('8.2', u"Management specific al sistemelor de trafic și transport de energie"),
    ('8.3', u"Managementul traficului marin"),
    ('9',   u"Mǎsuri legate de utilizarea unor resurse speciale"),
    ('9.0', u"Alte mǎsuri legate de resurse"),
    ('9.1', u"Reglementarea/Managementul exploatǎrilor de resurse naturale la nivel terestru"),
    ('9.2', u"Reglementarea/Managementul exploatǎrilor de resurse naturale la nivel maritim"),
]

