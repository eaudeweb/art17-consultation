revision = '4cc431d0042'
down_revision = '1f8fced5b64'

from alembic import op


to_update = {'data_habitattype_reg': 'data_habitattype_regions'}


def upgrade():
    for new_field, old_field in to_update.iteritems():
        op.execute(("update reportdata_owner.validate_fields set "
                    "field_name='{0}' where "
                    "table_name='data_habitats' and "
                    "field_name='{1}'").format(new_field, old_field))


def downgrade():
    for new_field, old_field in to_update.iteritems():
        op.execute(("update reportdata_owner.validate_fields set "
                    "field_name='{0}' where "
                    "table_name='data_habitats' and "
                    "field_name='{1}'").format(old_field, new_field))
