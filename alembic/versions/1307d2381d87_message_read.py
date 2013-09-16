revision = '1307d2381d87'
down_revision = '42756ed1382c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('comment_messages_read',
        sa.Column('objectid', sa.CHAR(32), nullable=False),
        sa.Column('message_id', sa.CHAR(32), nullable=False),
        sa.Column('user_id', sa.VARCHAR(256), nullable=False),
        sa.PrimaryKeyConstraint('objectid'),
    )


def downgrade():
    op.drop_table('comment_messages_read')
