revision = '163d2c1249b2'
down_revision = '3ca1768f0d58'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.oracle import NVARCHAR2


def upgrade():
    op.create_table('cons_assessments',
        sa.Column('objectid', sa.CHAR(32), nullable=False),
        sa.Column('type', NVARCHAR2(255), nullable=True),
        sa.Column('region_code', NVARCHAR2(255), nullable=True),
        sa.Column('species_id', sa.Integer, nullable=True),
        sa.Column('habitat_id', sa.Integer, nullable=True),
        sa.Column('species_assessment_id', sa.CHAR(32), nullable=True),
        sa.Column('habitat_assessment_id', sa.CHAR(32), nullable=True),
        sa.Column('finalized', sa.Boolean, nullable=False),
        sa.Column('finalized_date', sa.DateTime, nullable=True),
        sa.Column('finalized_user_id', sa.VARCHAR(256), nullable=True),
        sa.PrimaryKeyConstraint('objectid'),
    )

    op.add_column('data_habitattype_comments',
        sa.Column('cons_assessment_id', sa.CHAR(32), nullable=True))

    op.add_column('data_species_comments',
        sa.Column('cons_assessment_id', sa.CHAR(32), nullable=True))


def downgrade():
    op.drop_column('data_species_comments', 'cons_assessment_id')
    op.drop_column('data_habitattype_comments', 'cons_assessment_id')
    op.drop_table('cons_assessments')
