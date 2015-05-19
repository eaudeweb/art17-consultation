revision = '116a08869ff4'
down_revision = '4f0422cb274a'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.oracle import NVARCHAR2


def upgrade():
    op.add_column(
        'data_habitattype_reg',
        sa.Column('cons_generalstatus', NVARCHAR2(255), nullable=True),
    )
    op.execute("update data_habitattype_reg set cons_generalstatus = '1'")


def downgrade():
    op.drop_column('data_habitattype_reg', 'cons_generalstatus')
