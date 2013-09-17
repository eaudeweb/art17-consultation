revision = '1483f02c2bdf'
down_revision = '1307d2381d87'

from alembic import op
import sqlalchemy as sa


def upgrade():
    for table_name in ['data_species_comments',
                       'data_habitattype_comments',
                       'comment_messages']:
        op.drop_column(table_name, 'user_id')
        op.add_column(table_name,
            sa.Column('user_id', sa.VARCHAR(256),
                      nullable=False, server_default='_'))


def downgrade():
    for table_name in ['comment_messages',
                       'data_habitattype_comments',
                       'data_species_comments']:
        op.drop_column(table_name, 'user_id')
        op.add_column(table_name,
            sa.Column('user_id', sa.UnicodeText, nullable=True))
