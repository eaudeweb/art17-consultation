revision = '44fc139f3b69'
down_revision = '5413be0df64'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.oracle import NVARCHAR2
from sqlalchemy.sql import table, column


def upgrade():
    op.add_column(
        'LU_BIOGEOREG',
        sa.Column('NUME', NVARCHAR2(50), nullable=True),
    )

    lu_biogeoreg = table(
        'lu_biogeoreg',
        column('objectid', sa.Integer),
        column('nume', NVARCHAR2),
    )

    for objectid, nume in DATA:
        op.execute(
            lu_biogeoreg.update()
            .where(lu_biogeoreg.c.objectid == op.inline_literal(objectid))
            .values({'nume': op.inline_literal(nume)})
        )


def downgrade():
    op.drop_column('LU_BIOGEOREG', 'NUME')

DATA = [
    (1,  "Alpin"),
    (3,  "Marea Neagra"),
    (5,  "Continental"),
    (9,  "Regiunea marina a Marii Negre"),
    (13, "Panonic"),
    (14, "Stepic"),
]
