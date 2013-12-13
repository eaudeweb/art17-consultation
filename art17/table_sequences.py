import os

SEQUENCE_MAP = {
    'devel': [
        ('R611', 'art17_habitats_range'),
        ('R612', 'art17_habitats_distribution'),
        ('R613', 'art17_species_distribution'),
        ('R614', 'art17_species_range'),
        ('R658', 'data_gmeasures'),
        ('R659', 'data_greintrod_of_spec'),
        ('R660', 'data_greport'),
        ('R661', 'data_habitats'),
        ('R662', 'data_habitats_check_list'),
        ('R663', 'data_habitattype_reg'),
        ('R664', 'data_htypical_species'),
        ('R665', 'data_measures'),
        ('R666', 'data_notes'),
        ('R667', 'data_pressures_threats'),
        ('R668', 'data_pressures_threats_pol'),
        ('R669', 'data_species'),
        ('R670', 'data_species_check_list'),
        ('R671', 'data_species_regions'),
        ('R672', 'lu_art17_habitats_check_list'),
        ('R673', 'lu_art17_species_check_list'),
        ('R674', 'lu_assessments'),
        ('R675', 'lu_biogeoreg'),
        ('R676', 'lu_countries_regions'),
        ('R677', 'lu_country_code'),
        ('R678', 'lu_favourable_range_operator'),
        ('R679', 'lu_habitattype_codes'),
        ('R680', 'lu_hd_species'),
        ('R681', 'lu_measures'),
        ('R682', 'lu_methods_pressures'),
        ('R683', 'lu_methods_threats'),
        ('R684', 'lu_methods_used'),
        ('R685', 'lu_pollution'),
        ('R686', 'lu_population_number'),
        ('R687', 'lu_population_units_restricted'),
        ('R688', 'lu_presence'),
        ('R689', 'lu_quality'),
        ('R690', 'lu_ranking'),
        ('R691', 'lu_reintroduction'),
        ('R692', 'lu_threats'),
        ('R693', 'lu_trends'),
        ('R694', 'lu_trends_conclusion'),
        ('R695', 'merge_diff'),
        ('R696', 'sys_dummy'),
        ('R697', 'sys_import'),
        ('R698', 'sys_info_be'),
        ('R699', 'sys_info_fe'),
        ('R700', 'sys_user'),
        ('R701', 'sys_yesno'),
        ('R702', 'validate_fields'),
        ('R703', 'validation_result'),
    ],
}

art17_db_configuration = os.environ.get('ART17_DB_CONFIGURATION', 'devel')

current_sequence_map = {t: s for s, t in SEQUENCE_MAP[art17_db_configuration]}


def get_sequence_id(table_name):
    return current_sequence_map[table_name]
