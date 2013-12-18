# encoding: utf-8

revision = '1dfdfccbff9'
down_revision = '17d03b52364a'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.oracle import NVARCHAR2, NCLOB


def upgrade():
    op.execute("CREATE SEQUENCE DATASETS_SEQ")
    op.create_table('datasets',
        sa.Column('OBJECTID', sa.Integer, nullable=False),
        sa.Column('USER_ID', NVARCHAR2(255), nullable=True),
        sa.Column('DATE', sa.DateTime, nullable=True),
        sa.Column('COMMENT', NCLOB, nullable=True),
        sa.PrimaryKeyConstraint('OBJECTID'),
    )
    op.add_column(
        'data_habitattype_reg',
        sa.Column('cons_dataset_id', sa.Integer, nullable=True),
    )
    op.add_column(
        'data_species_regions',
        sa.Column('cons_dataset_id', sa.Integer, nullable=True),
    )
    op.execute(
        u"INSERT INTO DATASETS(OBJECTID, \"DATE\", \"COMMENT\") "
        u"VALUES ("
            u"DATASETS_SEQ.nextval, "
            u"TO_DATE('2013-10-01 13:30:00', 'YYYY-MM-DD HH24:MI:SS'), "
            u"'Consultare publica'"
        u") "
    )
    op.execute("UPDATE data_habitattype_reg SET cons_dataset_id = 1")
    op.execute("UPDATE data_species_regions SET cons_dataset_id = 1")


def downgrade():
    op.execute("DELETE FROM data_species_regions WHERE cons_dataset_id > 1")
    op.execute("DELETE FROM data_habitattype_reg WHERE cons_dataset_id > 1")
    op.drop_column('data_species_regions', 'cons_dataset_id')
    op.drop_column('data_habitattype_reg', 'cons_dataset_id')
    op.drop_table('datasets')
    op.execute("DROP SEQUENCE datasets_seq")
