revision = '59b0f91212e5'
down_revision = 'd9d32baf6d5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('comment_messages',
        sa.Column('objectid', sa.CHAR(32), nullable=False),
        sa.Column('parent', sa.CHAR(32), nullable=True),
        sa.Column('user_id', sa.VARCHAR(256), nullable=False),
        sa.Column('date', sa.DateTime, nullable=True),
        sa.Column('text', sa.UnicodeText, nullable=True),
        sa.PrimaryKeyConstraint('objectid'),
    )


def downgrade():
    op.drop_table('comment_messages')
