
revision = '4eccf01743b2'
down_revision = '39f65264570c'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.oracle import NVARCHAR2


def upgrade():
    op.create_table('notification_user',
        sa.Column('objectid', sa.CHAR(32), nullable=False),
        sa.Column('email', NVARCHAR2(255), nullable=False),
        sa.Column('full_name', NVARCHAR2(255), nullable=True),
        sa.PrimaryKeyConstraint('objectid'),
    )


def downgrade():
    op.drop_table('notification_user')
