revision = '42756ed1382c'
down_revision = '59b0f91212e5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('data_species_comments',
        sa.Column('status', sa.UnicodeText, nullable=True))
    op.add_column('data_habitattype_comments',
        sa.Column('status', sa.UnicodeText, nullable=True))


def downgrade():
    op.drop_column('data_habitattype_comments', 'status')
    op.drop_column('data_species_comments', 'status')
