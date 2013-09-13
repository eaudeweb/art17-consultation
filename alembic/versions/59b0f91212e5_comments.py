revision = '59b0f91212e5'
down_revision = 'dfa4cec0ca4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('comment_messages',
        sa.Column('id', sa.CHAR(32), nullable=False),
        sa.Column('parent', sa.CHAR(32), nullable=True),
        sa.Column('user_id', sa.UnicodeText, nullable=True),
        sa.Column('date', sa.DateTime, nullable=True),
        sa.Column('text', sa.UnicodeText, nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('comment_messages')
