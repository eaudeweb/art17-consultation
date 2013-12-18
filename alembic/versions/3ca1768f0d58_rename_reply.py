revision = '3ca1768f0d58'
down_revision = '44fc139f3b69'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.rename_table('comment_messages', 'comment_replies')
    op.rename_table('comment_messages_read', 'comment_replies_read')
    op.alter_column('comment_replies_read', 'message_id',
                            new_column_name='reply_id')


def downgrade():
    op.alter_column('comment_replies_read', 'reply_id',
                            new_column_name='message_id')
    op.rename_table('comment_replies_read', 'comment_messages_read')
    op.rename_table('comment_replies', 'comment_messages')
