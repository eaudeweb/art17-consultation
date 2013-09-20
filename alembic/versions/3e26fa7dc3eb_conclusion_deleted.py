revision = '3e26fa7dc3eb'
down_revision = '32bccfe7b68a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('data_species_conclusions',
        sa.Column('deleted', sa.Boolean, nullable=False, server_default='0'))
    op.add_column('data_habitattype_conclusions',
        sa.Column('deleted', sa.Boolean, nullable=False, server_default='0'))


def downgrade():
    op.drop_column('data_habitattype_conclusions', 'deleted')
    op.drop_column('data_species_conclusions', 'deleted')
