revision = '49f0e4b60d58'
down_revision = '2bfb2313fa94'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("DELETE FROM comment_replies_read")
    op.drop_column('comment_replies_read', 'reply_id')
    op.add_column('comment_replies_read',
        sa.Column('TABLE', sa.VARCHAR(255), nullable=False),
    )
    op.add_column('comment_replies_read',
        sa.Column('row_id', sa.Integer(), nullable=False),
    )


def downgrade():
    op.execute("DELETE FROM comment_replies_read")
    op.drop_column('comment_replies_read', 'row_id')
    op.drop_column('comment_replies_read', 'TABLE')
    op.add_column('comment_replies_read',
        sa.Column('reply_id', sa.CHAR(32), nullable=False),
    )
