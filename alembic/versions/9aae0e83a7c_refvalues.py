revision = '9aae0e83a7c'
down_revision = '3833e1d614e7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('refvalues',
        sa.Column('objectid', sa.VARCHAR(256), nullable=False),
        sa.Column('object_type', sa.UnicodeText, nullable=False),
        sa.Column('object_code', sa.UnicodeText, nullable=False),
        sa.Column('group', sa.UnicodeText, nullable=False),
        sa.Column('name', sa.UnicodeText, nullable=False),
        sa.Column('value', sa.UnicodeText, nullable=False),
        sa.Column('value_type', sa.UnicodeText, nullable=True),
        sa.PrimaryKeyConstraint('objectid'),
    )


def downgrade():
    op.drop_table('refvalues')
