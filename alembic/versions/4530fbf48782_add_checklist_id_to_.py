revision = '4530fbf48782'
down_revision = '45e5794291e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('datasets', sa.Column('checklist_id', sa.Integer, nullable=True))


def downgrade():
    op.drop_column('datasets', 'checklist_id')
