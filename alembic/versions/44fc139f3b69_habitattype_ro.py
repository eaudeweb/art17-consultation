revision = '44fc139f3b69'
down_revision = '5413be0df64'

from alembic import op
import sqlalchemy as sa
from path import path

MANUAL_SCRIPTS = (path(__file__).abspath().parent.parent /
                  'manual_oracle_scripts')


def upgrade():
    script_path = MANUAL_SCRIPTS / '4_lu_biogeoreg_nume.sql'
    for statement in script_path.text(encoding='utf-8').split(';\n'):
        if statement.strip():
            op.execute(statement)


def downgrade():
    op.drop_column('lu_biogeoreg', 'nume')
