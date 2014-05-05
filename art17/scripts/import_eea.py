from sqlalchemy import create_engine
from art17.scripts import importer
from art17.models import DataSpeciesRegion, DataSpecies, DataHabitat


SCHEMA = dict([
    ('etc_data_species_regions', [
        'country', 'eu_country_code', 'delivery', 'envelope', 'filename',
        'region', 'region_ms', 'region_was_changed', 'group', 'tax_group',
        'tax_order', 'upper_group', 'mid_group', 'family', 'annex',
        'annex_II', 'annex_II_exception', 'priority', 'annex_IV',
        'annex_IV_exception', 'annex_V', 'annex_V_addition', 'code',
        'speciescode', 'speciesname', 'species_name_different',
        'eunis_species_code', 'valid_speciesname', 'n2000_species_code',
        'assesment_speciesname', 'assesment_speciesname_changed',
        'grouped_assesment', 'species_type', 'species_type_asses',
        'range_surface_area', 'percentage_range_surface_area',
        'range_trend', 'range_yearly_magnitude',
        'complementary_favourable_range_q',
        'complementary_favourable_range', 'population_minimum_size',
        'percentage_population_minimum_size', 'population_maximum_size',
        'percentage_population_maximum_size', 'filled_population',
        'population_size_unit', 'number_of_different_population_units',
        'different_population_percentage',
        'percentage_population_mean_size', 'population_trend',
        'population_yearly_magnitude',
        'complementary_favourable_population_q',
        'complementary_favourable_population',
        'filled_complementary_favourable_population',
        'habitat_surface_area', 'percentage_habitat_surface_area',
        'habitat_trend', 'complementary_suitable_habitat',
        'future_prospects', 'conclusion_range', 'conclusion_population',
        'conclusion_habitat', 'conclusion_future', 'conclusion_assessment',
        'range_quality', 'population_quality', 'habitat_quality',
        'complementary_other_information',
        'complementary_other_information_english', 'range_grid_area',
        'percentage_range_grid_area', 'distribution_grid_area',
        'percentage_distribution_grid_area',
        'range_change_reason', 'population_change_reason',
        'habitat_change_reason',
        'population_units_agreed', 'population_units_other',
        'conclusion_assessment_trend', 'conclusion_assessment_prev',
        'conclusion_assessment_change',
    ]),
    ('etc_data_habitattype_regions', [
        'country', 'eu_country_code', 'delivery', 'envelope', 'filename',
        'region', 'region_ms', 'region_changed', 'group', 'annex',
        'annex_I', 'priority', 'code', 'habitatcode', 'habitattype_type',
        'habitattype_type_asses', 'range_surface_area',
        'percentage_range_surface_area', 'range_trend',
        'range_yearly_magnitude', 'complementary_favourable_range_q',
        'complementary_favourable_range', 'coverage_surface_area',
        'percentage_coverage_surface_area', 'coverage_trend',
        'coverage_yearly_magnitude', 'complementary_favourable_area_q',
        'complementary_favourable_area', 'conclusion_range',
        'conclusion_area', 'conclusion_structure', 'conclusion_future',
        'conclusion_assessment', 'range_quality', 'coverage_quality',
        'complementary_other_information',
        'complementary_other_information_english', 'range_grid_area',
        'percentage_range_grid_area', 'distribution_grid_area',
        'percentage_distribution_grid_area',
        'range_change_reason', 'coverage_change_reason',
        'conclusion_assessment_trend', 'conclusion_assessment_prev',
        'conclusion_assessment_change',
    ]),
])


def _get_table_data(input_conn, table_name, dataset_id):
    columns = SCHEMA[table_name]
    fields = ','.join(['`%s`' % c for c in columns])
    query = (
        "SELECT %s FROM `%s` " +
        "WHERE `country`='RO' AND `ext_dataset_id`='%s'"
    ) % (fields, table_name, dataset_id)

    rows = input_conn.execute(query)
    return [dict(zip(columns, row)) for row in rows]


@importer.command
def diff(input_db, dataset_id=1):
    input_conn = create_engine(input_db + '?charset=utf8').connect()

    # species
    current_species = {
        r.code: r for r in DataSpecies.query.all()
    }
    species_rows = _get_table_data(input_conn, 'etc_data_species_regions',
                                   dataset_id)
    for row in species_rows:
        code = row['code']
        if code not in current_species:
            print "Missing species: ", code, row['speciesname']
        else:
            print code, row['speciesname'], row['region']
            species = DataSpeciesRegion.query.filter_by(
                species=current_species[code],
                region=row['region']).first()
            if not species:
                print "* no current species found:", code, row['region']
                continue
            for k, v in DSR_MAP.iteritems():
                current = getattr(species, k)
                eea = row.get(v, '')
                if current != eea:
                    print "  - different: ", k,  "c:", current, "e:", eea
                else:
                    print "  - ok: ", k

    # habitat
    current_habitats = [
        r[0] for r in DataHabitat.query.with_entities(DataHabitat.code).all()
    ]
    habitat_rows = _get_table_data(input_conn, 'etc_data_habitattype_regions',
                                   dataset_id)
    for row in habitat_rows:
        code = row['code']
        if code not in current_habitats:
            print "Missing: ", code
        else:
            print code

    print len(species_rows), 'species', len(habitat_rows), 'habitats'

DSR_MAP = {
    'region': 'region',
    'range_surface_area': 'range_surface_area',
    'range_trend': 'range_trend',
    'complementary_favourable_range': 'complementary_favourable_range',
    'population_size_unit': 'population_size_unit',
    'population_minimum_size': 'population_minimum_size',
    'population_maximum_size': 'population_maximum_size',
    'complementary_favourable_population':
    'complementary_favourable_population',
    'habitat_surface_area': 'habitat_surface_area',
    'habitat_area_suitable': 'complementary_suitable_habitat',
    'conclusion_range': 'conclusion_range',
    'conclusion_population': 'conclusion_population',
    'conclusion_habitat': 'conclusion_habitat',
    'conclusion_future': 'conclusion_future',
    'conclusion_assessment': 'conclusion_assessment',
    'conclusion_assessment_trend': 'conclusion_assessment_trend',
}
