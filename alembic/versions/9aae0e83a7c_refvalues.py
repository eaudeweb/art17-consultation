revision = '9aae0e83a7c'
down_revision = '3833e1d614e7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('refvalues',
        sa.Column('objectid', sa.VARCHAR(256), nullable=False),
        sa.Column('object_type', sa.String(10), nullable=False),
        sa.Column('object_code', sa.String(10), nullable=False),
        sa.Column('object_region', sa.String(10), nullable=False),
        sa.Column('group', sa.String(100), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('value', sa.UnicodeText, nullable=False),
        sa.Column('value_type', sa.String(10), nullable=True),
        sa.PrimaryKeyConstraint('objectid'),
    )


def downgrade():
    op.drop_table('refvalues')
