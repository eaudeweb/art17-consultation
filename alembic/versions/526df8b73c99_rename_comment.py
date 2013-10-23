revision = '526df8b73c99'
down_revision = '3e26fa7dc3eb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.rename_table('data_habitattype_conclusions',
                    'data_habitattype_comments')
    op.rename_table('data_species_conclusions', 'data_species_comments')
    op.alter_column('data_habitattype_comments', 'conclusion_date',
                                 new_column_name='comment_date')
    op.alter_column('data_species_comments', 'conclusion_date',
                             new_column_name='comment_date')


def downgrade():
    op.alter_column('data_species_comments', 'comment_date',
                             new_column_name='conclusion_date')
    op.alter_column('data_habitattype_comments', 'comment_date',
                                 new_column_name='conclusion_date')
    op.rename_table('data_species_comments', 'data_species_conclusions')
    op.rename_table('data_habitattype_comments',
                    'data_habitattype_conclusions')
