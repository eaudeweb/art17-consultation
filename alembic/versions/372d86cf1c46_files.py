revision = '372d86cf1c46'
down_revision = '12f51bf1fa69'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("CREATE SEQUENCE ATTACHMENTS_SEQ")
    op.create_table('attachments',
        sa.Column('OBJECTID', sa.Integer, nullable=False),
        sa.Column('MIME_TYPE', sa.VARCHAR(255), nullable=True),
        sa.Column('DATA', sa.BLOB, nullable=True),
        sa.PrimaryKeyConstraint('OBJECTID'),
    )

    op.add_column(
        'comment_replies',
        sa.Column('attachment_id', sa.Integer, nullable=True),
    )


def downgrade():
    op.drop_column('comment_replies', 'attachment_id')
    op.drop_table('attachments')
    op.execute("DROP SEQUENCE attachments_seq")
