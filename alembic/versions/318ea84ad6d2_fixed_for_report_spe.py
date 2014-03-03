revision = '318ea84ad6d2'
down_revision = '5460a9c413eb'

from alembic import op

to_update = {
    'pressure_sr_id': 'pressure_id',
}


def upgrade():
    for new_field, old_field in to_update.iteritems():
        op.execute(("update reportdata_owner.validate_fields set "
                    "primary_key_field='{0}' where "
                    "table_name='data_pressures_threats' and "
                    " primary_key_field='{1}'").format(new_field, old_field))


def downgrade():
    for new_field, old_field in to_update.iteritems():
        op.execute(("update reportdata_owner.validate_fields set "
                    "primary_key_field='{0}' where "
                    "table_name='data_pressures_threats' and "
                    " primary_key_field='{1}'").format(new_field, old_field))
