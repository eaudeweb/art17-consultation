revision = '5460a9c413eb'
down_revision = '4cc431d0042'

from alembic import op

to_update = {
    'sr_species_id': 'sr_id'
}


def upgrade():
    for new_field, old_field in to_update.iteritems():
        op.execute(("update reportdata_owner.validate_fields set "
                    "primary_key_field='{0}' where "
                    "table_name='data_species_regions' and "
                    " primary_key_field='{1}'").format(new_field, old_field))


def downgrade():
    for new_field, old_field in to_update.iteritems():
        op.execute(("update reportdata_owner.validate_fields set "
                    "primary_key_field='{0}' where "
                    "table_name='data_species_regions' and "
                    " primary_key_field='{1}'").format(old_field, new_field))
