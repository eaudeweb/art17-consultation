revision = '363a0d66f02f'
down_revision = '1483f02c2bdf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('history',
        sa.Column('objectid', sa.CHAR(32), nullable=False),
        sa.Column('table', sa.CHAR(128), nullable=False),
        sa.Column('object_id', sa.CHAR(32), nullable=False),
        sa.Column('action', sa.VARCHAR(128), nullable=False),
        sa.Column('date', sa.DateTime, nullable=False),
        sa.Column('user_id', sa.VARCHAR(256), nullable=True),
        sa.Column('old_data', sa.UnicodeText, nullable=True),
        sa.Column('new_data', sa.UnicodeText, nullable=True),
        sa.PrimaryKeyConstraint('objectid'),
    )


def downgrade():
    op.drop_table('history')
