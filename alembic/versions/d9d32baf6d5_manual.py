revision = 'd9d32baf6d5'
down_revision = '000000000000'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy.dialects.oracle import NVARCHAR2


def upgrade():
    op.create_table(
        'LU_GRUP_SPECIE',
        sa.Column('OID', sa.Integer(), nullable=False),
        sa.Column('CODE', NVARCHAR2(255), nullable=True),
        sa.Column('DESCRIPTION', NVARCHAR2(255), nullable=True),
    )

    lu_grup_specie = table(
        'lu_grup_specie',
        column('oid', sa.Integer),
        column('code', NVARCHAR2),
        column('description', NVARCHAR2),
    )

    op.bulk_insert(lu_grup_specie, [
        {'oid': 1, 'code': "A", 'description': "Amfibieni"},
        {'oid': 2, 'code': "F", 'description': "Pesti"},
        {'oid': 3, 'code': "M", 'description': "Mamifere"},
        {'oid': 4, 'code': "P", 'description': "Plante"},
        {'oid': 5, 'code': "R", 'description': "Reptile"},
        {'oid': 6, 'code': "I", 'description': "Nevertebrate"},
    ])


def downgrade():
    op.drop_table('lu_grup_specie')
