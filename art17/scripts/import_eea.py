from sqlalchemy import create_engine
from bs4 import BeautifulSoup
from art17.scripts import importer
from art17.models import DataSpeciesRegion, DataSpecies, DataHabitat, db, \
    DataMeasures, DataPressuresThreats, DataPressuresThreatsPollution, \
    LuHdSpecies


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

SCHEMA_XML = {
    'etc_data_species': [
        'alternative_speciesname',
        'common_speciesname',
        'distribution_map',
        'sensitive_species',
        'distribution_method',
        'distribution_date',
        'additional_distribution_map',
        'range_map',
    ],
    'lu_hd_species': [
        'speciescode',
        'speciesname',
    ],
    'etc_data_species_regions': [
        'range_surface_area',
        'published',
        'range_method',
        'range_trend_period',
        'range_trend',
        'range_trend_magnitude_min',
        'range_trend_magnitude_max',
        'range_trend_long_period',
        'range_trend_long',
        'range_trend_long_magnitude_min',
        'range_trend_long_magnitude_max',
        'complementary_favourable_range',
        'complementary_favourable_range_op',
        'complementary_favourable_range_unknown',
        'complementary_favourable_range_method',
        'range_reasons_for_change_a',
        'range_reasons_for_change_b',
        'range_reasons_for_change_c',
        'population_size_unit',
        'population_minimum_size',
        'population_maximum_size',
        'population_alt_size_unit',
        'population_alt_minimum_size',
        'population_alt_maximum_size',
        'population_additional_locality',
        'population_additional_method',
        'population_additional_problems',
        'population_date',
        'population_method',
        'population_trend_period',
        'population_trend',
        'population_trend_magnitude_min',
        'population_trend_magnitude_max',
        'population_trend_magnitude_ci',
        'population_trend_method',
        'population_trend_long_period',
        'population_trend_long',
        'population_trend_long_magnitude_min',
        'population_trend_long_magnitude_max',
        'population_trend_long_magnitude_ci',
        'population_trend_long_method',
        'complementary_favourable_population',
        'complementary_favourable_population_op',
        'complementary_favourable_population_unknown',
        'complementary_favourable_population_method',
        'population_reasons_for_change_a',
        'population_reasons_for_change_b',
        'population_reasons_for_change_c',
        'habitat_surface_area',
        'habitat_date',
        'habitat_method',
        'habitat_quality',
        'habitat_quality_explanation',
        'habitat_trend_period',
        'habitat_trend',
        'habitat_trend_long_period',
        'habitat_trend_long',
        'habitat_area_suitable',
        'habitat_reasons_for_change_a',
        'habitat_reasons_for_change_b',
        'habitat_reasons_for_change_c',
        'pressures_method',
        'threats_method',
        'justification',
        'other_relevant_information',
        'transboundary_assessment',
        'conclusion_range',
        'conclusion_range_trend',
        'conclusion_population',
        'conclusion_population_trend',
        'conclusion_habitat',
        'conclusion_habitat_trend',
        'conclusion_future',
        'conclusion_future_trends',
        'conclusion_assessment',
        'conclusion_assessment_trend',
        'natura2000_population_unit',
        'natura2000_population_min',
        'natura2000_population_max',
        'natura2000_population_method',
        'natura2000_population_trend',
    ],
    'data_measures': [
        'code',
        'type_legal',
        'type_administrative',
        'type_contractual',
        'type_recurrent',
        'type_oneoff',
        'ranking',
        'location_inside',
        'location_outside',
        'location_both',
        'broad_evaluation_maintain',
        'broad_evaluation_enhance',
        'broad_evaluation_longterm',
        'broad_evaluation_noeffect',
        'broad_evaluation_unknown',
        'broad_evaluation_notevaluated',
    ],
    'data_pressures_threats': [
        'code',
        'ranking',
    ],
    'data_pressures_threats_pol': [
        'code',
    ],
}


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


@importer.command
def xml_species(xml_path, dataset_id=1):

    def extract_record(table_name, element):
        data = {}
        for field in SCHEMA_XML[table_name]:
            value = getattr(element, field).text or None
            if value in ('true', 'false'):
                value = True if value == 'true' else False
            data[field] = value
        return data

    def update_object(obj, data):
        for k, v in data.iteritems():
            setattr(obj, k, v)

    with open(xml_path, 'r') as fin:
        parser = BeautifulSoup(fin)

        ok_species = []
        for species in parser.find_all('species_report'):
            speciescode = species.speciescode.text
            ok_species.append(speciescode)
            data = extract_record('etc_data_species', species)
            species_obj = DataSpecies.query.filter_by(code=speciescode).first()
            if not species_obj:
                print "Missing species: ", speciescode
                speciescode_numeric = int(speciescode)
                species_lu_obj = LuHdSpecies.query.filter_by(code=speciescode_numeric).first()
                if not species_lu_obj:
                    lu_data = extract_record('lu_hd_species', species)
                    lu_data['group_code'] = 'X'  # unknown
                    species_lu_obj = LuHdSpecies(**lu_data)
                    db.session.add(species_lu_obj)
                    print "Added species hd."
                species_obj = DataSpecies(country='RO', code=speciescode,
                                          **data)
                db.session.add(species_obj)
                print "Added new species."
            print "Species: ", species_obj.id, species_obj.code, species_obj.alternative_speciesname
            ok_regions = []
            for region in species.regional.find_all('region'):
                regioncode = region.code.text
                ok_regions.append(regioncode)
                data = extract_record('etc_data_species_regions', region)

                # Get existing region and update
                species_region = (
                    species_obj.regions.filter_by(region=regioncode,
                                                  cons_role='assessment',
                                                  cons_dataset_id=dataset_id)
                ).first()
                if not species_region:
                    print " Missing species region: ", regioncode
                    species_region = (
                        DataSpeciesRegion(species=species_obj,
                                          region=regioncode,
                                          cons_dataset_id=dataset_id,
                                          cons_role='assessment',
                                          cons_status=None,
                                          cons_generalstatus='1',
                        )
                    )
                    db.session.add(species_region)
                print " Region:", regioncode, species_region.id
                update_object(species_region, data)
                # Get all measures
                for existing_measure in species_region.measures:
                    db.session.delete(existing_measure)
                for measure in region.measures.find_all('measure'):
                    data = extract_record('data_measures', measure)
                    measure_obj = DataMeasures(species=species_region, **data)
                    db.session.add(measure_obj)
                    print "  added measure: ", measure_obj.code
                # Get all pressures
                for existing_pressure in species_region.get_pressures():
                    print "  deleting", existing_pressure.id
                    db.session.delete(existing_pressure)
                for pressure in region.pressures.find_all('pressure'):
                    data = extract_record('data_pressures_threats', pressure)
                    data['type'] = 'p'
                    pressure_obj = (
                        DataPressuresThreats(species=species_region, **data)
                    )
                    db.session.add(pressure_obj)
                    print "  added pressure: ", pressure_obj.code
                    for p in pressure.pollution_qualifiers.find_all('pollution_qualifier'):
                        data = extract_record('data_pressures_threats_pol', p)
                        pol_obj = DataPressuresThreatsPollution(pressure=pressure_obj, **data)
                        db.session.add(pol_obj)
                        print "   added pollution: ", pol_obj.code
                # Get all threats
                for existing_threat in species_region.get_threats():
                    print "  deleting", existing_threat.id
                    db.session.delete(existing_threat)
                for threat in region.threats.find_all('threat'):
                    data = extract_record('data_pressures_threats', threat)
                    data['type'] = 't'
                    threat_obj = (
                        DataPressuresThreats(species=species_region, **data)
                    )
                    db.session.add(pressure_obj)
                    print "  added threat: ", threat_obj.code
                    for p in threat.pollution_qualifiers.find_all('pollution_qualifier'):
                        data = extract_record('data_pressures_threats_pol', p)
                        pol_obj = DataPressuresThreatsPollution(pressure=threat_obj, **data)
                        db.session.add(pol_obj)
                        print "   added pollution: ", pol_obj.code
            for existing_region in species_obj.regions.filter_by(cons_dataset_id=dataset_id):
                if existing_region.region not in ok_regions:
                    print " Deleting existing region: ", existing_region.region
                    db.session.delete(existing_region)
        for existing_species in DataSpecies.query.all():
            if existing_species.code not in ok_species:
                print "Deleting regions for non existent species: ", existing_species.code
                for existing_region in existing_species.regions.filter_by(cons_dataset_id=dataset_id):
                    print " - ", existing_region.region
                    db.session.delete(existing_region)
    db.session.commit()
