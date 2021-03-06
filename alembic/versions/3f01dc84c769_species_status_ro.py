# encoding: utf-8

revision = '3f01dc84c769'
down_revision = '31560770de09'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


def upgrade():
    op.add_column('lu_presence',
        sa.Column('name_ro', sa.UnicodeText, nullable=True))

    lu_presence_codes = table('lu_presence',
        column('code', sa.String),
        column('name_ro', sa.UnicodeText))

    for code, name_ro in DATA:
        op.execute(
            lu_presence_codes.update()
                .where(lu_presence_codes.c.code == op.inline_literal(code))
                .values({'name_ro': op.inline_literal(name_ro)}))


def downgrade():
    op.drop_column('lu_presence', 'name_ro')


DATA = [
    ('EXB', u"Extinct"),
    ('PEXB', u"Extinct inainte de 1980"),
    ('EXBA', u"Extinct dupa 1980"),
    ('EX', u"Extinct inainte ca HD sa intre in vigoare"),
    ('PEX', u"Extinct dupa ce HD a intrat in vigoare"),
    ('ARR', u"Introdus"),
    ('1', u"Prezent"),
    ('LR', u"Prezent - LR"),
    ('MAR', u"Prezent marginala"),
    ('OCC', u"Ocazional"),
    ('SR TAX', u"Rezerva taxonomica"),
    ('N/SR TAX', u"Rezerva taxonomica - fara raport"),
    ('OP', u"Raportul nu este obligatoriu"),
    ('SR', u"Rezerva stiintifica"),
    ('N', u"Nu este prezenta - stearsa din checklist"),
    ('N/R', u"Nu este prezenta - rezerva"),
]
