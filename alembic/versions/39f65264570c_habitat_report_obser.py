revision = '39f65264570c'
down_revision = '34e208d53dbf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('data_habitattype_reg',
        sa.Column('cons_report_observation', sa.UnicodeText,
                  nullable=True))


def downgrade():
    op.drop_column('data_habitattype_reg', 'cons_report_observation')
