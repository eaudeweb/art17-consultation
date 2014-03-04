revision = '20d8f799b050'
down_revision = '318ea84ad6d2'

from alembic import op


to_update = {
    'rsurface_area': 'range_surface_area',
    'range_trend_mag_min': 'range_trend_long_magnitude_min',
    'range_trend_mag_max': 'range_trend_long_magnitude_max',
    'range_trend_mag_max': 'range_trend_long_magnitude_max',
    'range_trend_mag_min': 'range_trend_long_magnitude_min',
    'comp_favourable_range': 'complementary_favourable_range',
    'comp_favourable_range_op': 'complementary_favourable_range_op',
    'comp_favourable_range_x': 'complementary_favourable_range_x',
    'comp_favourable_range_met': 'complementary_favourable_range_method',
    'pop_minimum_size': 'population_minimum_size',
    'pop_maximum_size': 'population_maximum_size',
    'pop_size_unit': 'population_size_unit',
    'pop_alt_size_unit': 'population_alt_size_unit',
    'pop_alt_minimum_size': 'population_alt_minimum_size',
    'pop_alt_maximum_size': 'population_alt_maximum_size',
    'pop_additional_locality': 'population_additional_locality',
    'pop_additional_method': 'population_additional_method',
    'pop_additional_problems': 'population_additional_problems',
    'pop_date':  'population_date',
    'pop_method': 'population_method',
    'pop_trend_period': 'population_trend_period',
    'pop_trend': 'population_trend',
    'pop_trend_mag_min': 'population_trend_magnitude_min',
    'pop_trend_mag_max':  'population_trend_magnitude_max',
    'pop_trend_magnitude_ci': 'population_trend_magnitude_ci',
    'pop_trend_method': 'population_trend_method',
    'pop_trend_long_period':  'population_trend_long_period',
    'pop_trend_long_mag_max':  'population_trend_long_magnitude_max',
    'pop_trend_long_mag_min':  'population_trend_long_magnitude_min',
    'pop_trend_long_mag_ci': 'population_trend_long_magnitude_ci',
    'pop_trend_long_method':  'population_trend_long_method',
    'comp_favourable_pop':  'complementary_favourable_population',
    'comp_favourable_pop_op': 'complementary_favourable_population_op',
    'comp_favourable_pop_x': 'complementary_favourable_population_x',
    'comp_favourable_pop':  'complementary_favourable_population',
    'comp_favourable_pop_met':  'complementary_favourable_population_method',
    'pop_reasons_for_change_a': 'population_reasons_for_change_a',
    'pop_reasons_for_change_b': 'population_reasons_for_change_b',
    'pop_reasons_for_change_c': 'population_reasons_for_change_c',
    'habitat_reasons_for_change__61': 'habitat_reasons_for_change_a',
    'habitat_reasons_for_change__62': 'habitat_reasons_for_change_b',
    'habitat_reasons_for_change__63': 'habitat_reasons_for_change_c',
    'r_reasons_for_change_a': 'range_reasons_for_change_a',
    'r_reasons_for_change_b': 'range_reasons_for_change_b',
    'r_reasons_for_change_c': 'range_reasons_for_change_c',
}


def upgrade():
    op.execute("update reportdata_owner.validate_fields set "
               "table_name='data_habitattype_reg' where "
               "table_name='data_habitattype_regions'")

    for new_field, old_field in to_update.iteritems():
        op.execute(("update reportdata_owner.validate_fields set "
                    "field_name='{0}' where "
                    "table_name='data_habitattype_reg' and "
                    " field_name='{1}'").format(new_field, old_field))

    op.execute(("update reportdata_owner.validate_fields set "
                "primary_key_field='hr_habitat_id' where "
                "table_name='data_habitattype_reg' and "
                " primary_key_field='hr_id'").format(new_field, old_field))


def downgrade():
    op.execute("update reportdata_owner.validate_fields set "
               "table_name='data_habitattype_regions' where "
               "table_name='data_habitattype_reg'")

    for new_field, old_field in to_update.iteritems():
        op.execute(("update reportdata_owner.validate_fields set "
                    "field_name='{0}' where "
                    "table_name='data_habitattype_reg' and "
                    " field_name='{1}'").format(old_field, new_field))

    op.execute(("update reportdata_owner.validate_fields set "
                "primary_key_field='hr_id' where "
                "table_name='data_habitattype_reg' and "
                " primary_key_field='hr_habitat_id'"
                "").format(new_field, old_field))
