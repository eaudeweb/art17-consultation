import os

SEQUENCE_MAP = {
    'devel': [
        ('R679', 'lu_habitattype_codes'),
        ('R680', 'lu_hd_species'),
        ('R675', 'lu_biogeoreg'),
        ('R692', 'lu_threats'),
        ('R690', 'lu_ranking'),
        ('R686', 'lu_population_number'),
        ('R687', 'lu_population_units_restricted'),
        ('R685', 'lu_pollution'),
        ('R681', 'lu_measures'),
        ('R688', 'lu_presence'),
        ('R661', 'data_habitats'),
        ('R662', 'data_habitats_check_list'),
        ('R663', 'data_habitattype_reg'),
        ('R669', 'data_species'),
        ('R670', 'data_species_check_list'),
        ('R671', 'data_species_regions'),
        ('R665', 'data_measures'),
        ('R667', 'data_pressures_threats'),
        ('R668', 'data_pressures_threats_pol'),
        ('R664', 'data_htypical_species'),
    ],
}

art17_db_configuration = os.environ.get('ART17_DB_CONFIGURATION', 'devel')

current_sequence_map = {t: s for s, t in SEQUENCE_MAP[art17_db_configuration]}


def get_sequence_id(table_name):
    return current_sequence_map[table_name]
