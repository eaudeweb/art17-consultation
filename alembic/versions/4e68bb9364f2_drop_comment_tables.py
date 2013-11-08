revision = '4e68bb9364f2'
down_revision = '38218110d368'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('data_habitattype_comments')
    op.drop_table('data_species_comments')
    op.drop_table('consultation_topic')


def downgrade():
    raise NotImplementedError
