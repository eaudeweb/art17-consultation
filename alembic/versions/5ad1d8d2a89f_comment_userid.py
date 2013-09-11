revision = '5ad1d8d2a89f'
down_revision = '510dbe873d35'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('data_species_comments',
        sa.Column('user_id', sa.Numeric(38, 8), nullable=True),
        schema='reportdata_owner')
    op.add_column('data_habitattype_comments',
        sa.Column('user_id', sa.Numeric(38, 8), nullable=True),
        schema='reportdata_owner')


def downgrade():
    op.drop_column('data_habitattype_comments', 'user_id',
                   schema='reportdata_owner')
    op.drop_column('data_species_comments', 'user_id',
                   schema='reportdata_owner')
