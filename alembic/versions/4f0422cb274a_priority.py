from sqlalchemy.sql import table, column

revision = '4f0422cb274a'
down_revision = '9aae0e83a7c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('data_species_check_list',
                  sa.Column('priority', sa.NVARCHAR(255), nullable=True))
    op.add_column('data_habitats_check_list',
                  sa.Column('priority', sa.NVARCHAR(255), nullable=True))


def downgrade():
    op.drop_column('data_species_check_list', 'priority')
    op.drop_column('data_habitats_check_list', 'priority')
