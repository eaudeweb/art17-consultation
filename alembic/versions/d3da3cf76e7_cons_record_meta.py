revision = 'd3da3cf76e7'
down_revision = '3ca1768f0d58'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.oracle import NVARCHAR2


def upgrade():
    op.add_column(
        'data_habitattype_reg',
        sa.Column('cons_role', NVARCHAR2(255), nullable=True),
    )
    op.add_column(
        'data_habitattype_reg',
        sa.Column('cons_date', sa.DateTime, nullable=True),
    )
    op.add_column(
        'data_habitattype_reg',
        sa.Column('cons_user_id', NVARCHAR2(255), nullable=True),
    )
    op.add_column(
        'data_habitattype_reg',
        sa.Column('cons_status', NVARCHAR2(255), nullable=True),
    )
    op.add_column(
        'data_habitattype_reg',
        sa.Column('cons_deleted', sa.Boolean, nullable=True),
    )

    op.add_column(
        'data_species_regions',
        sa.Column('cons_role', NVARCHAR2(255), nullable=True),
    )
    op.add_column(
        'data_species_regions',
        sa.Column('cons_date', sa.DateTime, nullable=True),
    )
    op.add_column(
        'data_species_regions',
        sa.Column('cons_user_id', NVARCHAR2(255), nullable=True),
    )
    op.add_column(
        'data_species_regions',
        sa.Column('cons_status', NVARCHAR2(255), nullable=True),
    )
    op.add_column(
        'data_species_regions',
        sa.Column('cons_deleted', sa.Boolean, nullable=True),
    )

    op.execute("UPDATE data_habitattype_reg SET cons_role = 'assessment'")
    op.execute("UPDATE data_species_regions SET cons_role = 'assessment'")


def downgrade():
    op.drop_column('data_species_regions', 'cons_deleted')
    op.drop_column('data_species_regions', 'cons_status')
    op.drop_column('data_species_regions', 'cons_user_id')
    op.drop_column('data_species_regions', 'cons_date')
    op.drop_column('data_species_regions', 'cons_role')

    op.drop_column('data_habitattype_reg', 'cons_deleted')
    op.drop_column('data_habitattype_reg', 'cons_status')
    op.drop_column('data_habitattype_reg', 'cons_user_id')
    op.drop_column('data_habitattype_reg', 'cons_date')
    op.drop_column('data_habitattype_reg', 'cons_role')
