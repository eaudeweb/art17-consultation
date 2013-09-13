revision = 'dfa4cec0ca4'
down_revision = '5ad1d8d2a89f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('data_species_comments',
        sa.Column('comment_date', sa.DateTime, nullable=True),
        schema='reportdata_owner')
    op.add_column('data_habitattype_comments',
        sa.Column('comment_date', sa.DateTime, nullable=True),
        schema='reportdata_owner')


def downgrade():
    op.drop_column('data_habitattype_comments', 'comment_date',
                   schema='reportdata_owner')
    op.drop_column('data_species_comments', 'comment_date',
                   schema='reportdata_owner')
