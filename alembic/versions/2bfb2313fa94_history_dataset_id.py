revision = '2bfb2313fa94'
down_revision = '372d86cf1c46'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('history',
                  sa.Column('dataset_id', sa.Integer, nullable=True))

    op.execute("update history "
               "set dataset_id = 1")


def downgrade():
    op.drop_column('history', 'dataset_id')
