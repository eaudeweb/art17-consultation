revision = 'd9d32baf6d5'
down_revision = '000000000000'

from alembic import op
import sqlalchemy as sa
from path import path

MANUAL_SCRIPTS = (path(__file__).abspath().parent.parent /
                  'manual_oracle_scripts')



def upgrade():
    for script_name in ['1_lu_grup_specie.sql',
                        '2_data_species_comments.sql',
                        '3_data_habitattype_comments.sql']:
        script_path = MANUAL_SCRIPTS / script_name
        for statement in script_path.text(encoding='utf-8').split(';\n'):
            if statement.strip():
                op.execute(statement)


def downgrade():
    raise NotImplementedError
