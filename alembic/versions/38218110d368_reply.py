revision = '38218110d368'
down_revision = 'd3da3cf76e7'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.oracle import NVARCHAR2


def upgrade():
    op.execute('DELETE FROM comment_replies')

    op.drop_column('comment_replies', 'parent')

    op.add_column(
        'comment_replies',
        sa.Column('parent_table', NVARCHAR2(255), nullable=True),
    )

    op.add_column(
        'comment_replies',
        sa.Column('parent_id', NVARCHAR2(255), nullable=True),
    )


def downgrade():
    op.execute('DELETE FROM comment_replies')

    op.drop_column('comment_replies', 'parent_id')

    op.drop_column('comment_replies', 'parent_table')

    op.add_column(
        'comment_replies',
        sa.Column('parent', sa.CHAR(32), nullable=True),
    )
