# coding: utf-8
from sqlalchemy import Column, Date, Numeric, String, Table, Text, Unicode
from sqlalchemy.types import NullType
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


t_art17_habitats_distribution = Table(
    u'art17_habitats_distribution', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'habitat', Unicode(5), nullable=False),
    Column(u'n2k_name', Unicode(50), nullable=False),
    Column(u'n2k_qaqc', Unicode(254), nullable=False),
    Column(u'maptype', Unicode(20), nullable=False),
    Column(u'category', Unicode(20), nullable=False),
    Column(u'ste', Numeric(38, 8), nullable=False),
    Column(u'mbls', Numeric(38, 8), nullable=False),
    Column(u'bls', Numeric(38, 8), nullable=False),
    Column(u'pan', Numeric(38, 8), nullable=False),
    Column(u'alp', Numeric(38, 8), nullable=False),
    Column(u'con', Numeric(38, 8), nullable=False),
    Column(u'area', Numeric(38, 8), nullable=False),
    Column(u'bioregerr', Unicode(120), nullable=False),
    Column(u'n2k_250km', Unicode(80), nullable=False),
    Column(u'missingn2k', Unicode(254), nullable=False),
    Column(u'shape', NullType, index=True),
    Column(u'globalid', String(38), nullable=False, index=True)
)


t_art17_habitats_range = Table(
    u'art17_habitats_range', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'habitat', Unicode(5), nullable=False, index=True),
    Column(u'category', Unicode(20), nullable=False),
    Column(u'maptype', Unicode(20), nullable=False),
    Column(u'ste', Numeric(38, 8), nullable=False),
    Column(u'mbls', Numeric(38, 8), nullable=False),
    Column(u'bls', Numeric(38, 8), nullable=False),
    Column(u'pan', Numeric(38, 8), nullable=False),
    Column(u'alp', Numeric(38, 8), nullable=False),
    Column(u'con', Numeric(38, 8), nullable=False),
    Column(u'area', Numeric(38, 8), nullable=False),
    Column(u'notes', Unicode(80), nullable=False),
    Column(u'grid', Unicode(50), nullable=False),
    Column(u'gap', Numeric(38, 8), nullable=False),
    Column(u'n2k_name', Unicode(50), nullable=False),
    Column(u'shape', NullType, index=True),
    Column(u'globalid', String(38), nullable=False, index=True)
)


t_art17_species_distribution = Table(
    u'art17_species_distribution', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'specnum', Unicode(10), nullable=False),
    Column(u'n2k_name', Unicode(50), nullable=False),
    Column(u'n2k_qaqc', Unicode(254), nullable=False),
    Column(u'maptype', Unicode(20), nullable=False),
    Column(u'category', Unicode(20), nullable=False),
    Column(u'ste', Numeric(38, 8)),
    Column(u'pan', Numeric(38, 8)),
    Column(u'bls', Numeric(38, 8)),
    Column(u'mbls', Numeric(38, 8)),
    Column(u'alp', Numeric(38, 8)),
    Column(u'con', Numeric(38, 8)),
    Column(u'area', Numeric(38, 8)),
    Column(u'bioregerr', Unicode(120), nullable=False),
    Column(u'n2k_250km', Unicode(80), nullable=False),
    Column(u'missingn2k', Unicode(254), nullable=False),
    Column(u'stp', Numeric(38, 8)),
    Column(u'shape', NullType, index=True),
    Column(u'globalid', String(38), nullable=False, index=True)
)


t_art17_species_range = Table(
    u'art17_species_range', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'specnum', Unicode(10), nullable=False),
    Column(u'category', Unicode(20), nullable=False),
    Column(u'maptype', Unicode(20), nullable=False),
    Column(u'ste', Numeric(38, 8)),
    Column(u'pan', Numeric(38, 8)),
    Column(u'bls', Numeric(38, 8)),
    Column(u'mbls', Numeric(38, 8)),
    Column(u'alp', Numeric(38, 8)),
    Column(u'con', Numeric(38, 8)),
    Column(u'area', Numeric(38, 8)),
    Column(u'notes', Unicode(80), nullable=False),
    Column(u'grid', Unicode(50), nullable=False),
    Column(u'gap', Numeric(38, 8), nullable=False),
    Column(u'n2k_name', Unicode(50), nullable=False),
    Column(u'stp', Numeric(38, 8)),
    Column(u'shape', NullType, index=True),
    Column(u'globalid', String(38), nullable=False, index=True)
)


t_data_gmeasures = Table(
    u'data_gmeasures', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'gmeasure_greport_id', Numeric(scale=0, asdecimal=False)),
    Column(u'sitecode', Unicode(9)),
    Column(u'sitename', Unicode(255)),
    Column(u'project_year', Numeric(scale=0, asdecimal=False)),
    Column(u'project_title', Unicode(255)),
    Column(u'impact', Unicode(255)),
    Column(u'commission_opinion', Unicode(255)),
    Column(u'project_impact', Text),
    Column(u'validated', Numeric(5, 0, False)),
    Column(u'validation_date', Date)
)


t_data_greintrod_of_spec = Table(
    u'data_greintrod_of_spec', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'greintr_spec_gre_id', Numeric(scale=0, asdecimal=False)),
    Column(u'speciescode', Unicode(255)),
    Column(u'speciesname', Unicode(255)),
    Column(u'reintro_period_since', Unicode(1)),
    Column(u'reintro_period', Unicode(9)),
    Column(u'location_number', Unicode(255)),
    Column(u'successful_', Unicode(255)),
    Column(u'additional_information', Text),
    Column(u'validated', Numeric(5, 0, False)),
    Column(u'validation_date', Date)
)


t_data_greport = Table(
    u'data_greport', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'country', Unicode(2)),
    Column(u'achievements', Text),
    Column(u'achievements_trans', Text),
    Column(u'general_information', Text),
    Column(u'information_on_network', Text),
    Column(u'monitoring_schemes', Text),
    Column(u'protection_of_species', Text),
    Column(u'transpose_directive', Text),
    Column(u'sites_total_number', Numeric(5, 0, False)),
    Column(u'sites_total_area', Numeric(38, 8)),
    Column(u'sac_total_number', Numeric(5, 0, False)),
    Column(u'sac_total_area', Numeric(38, 8)),
    Column(u'sites_terrestrial_area', Numeric(38, 8)),
    Column(u'sac_terrestrial_area', Numeric(38, 8)),
    Column(u'sites_marine_number', Numeric(5, 0, False)),
    Column(u'sites_marine_area', Numeric(38, 8)),
    Column(u'sac_marine_number', Numeric(5, 0, False)),
    Column(u'sac_marine_area', Numeric(38, 8)),
    Column(u'database_date', Unicode(255)),
    Column(u'sites_with_plans', Numeric(5, 0, False)),
    Column(u'coverage', Numeric(38, 8)),
    Column(u'plans_under_prep', Numeric(5, 0, False)),
    Column(u'coherence_measures', Text),
    Column(u'sys_date_created', Date),
    Column(u'sys_date_modified', Date),
    Column(u'sys_date_imported', Date),
    Column(u'sys_creator_id', Unicode(255)),
    Column(u'sys_modifier_id', Unicode(255)),
    Column(u'validated', Numeric(5, 0, False)),
    Column(u'validation_date', Date)
)


t_data_habitats = Table(
    u'data_habitats', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'country', Unicode(2)),
    Column(u'habitatcode', Unicode(255)),
    Column(u'distribution_map', Numeric(5, 0, False)),
    Column(u'distribution_method', Unicode(255)),
    Column(u'distribution_date', Unicode(9)),
    Column(u'additional_distribution_map', Numeric(5, 0, False)),
    Column(u'range_map', Numeric(5, 0, False)),
    Column(u'sys_date_created', Date),
    Column(u'sys_date_modified', Date),
    Column(u'sys_date_imported', Date),
    Column(u'sys_creator_id', Unicode(255)),
    Column(u'sys_modifier_id', Unicode(255)),
    Column(u'validated', Numeric(5, 0, False)),
    Column(u'validation_date', Date),
    Column(u'export', Numeric(5, 0, False)),
    Column(u'import_id', Numeric(scale=0, asdecimal=False))
)


t_data_habitats_check_list = Table(
    u'data_habitats_check_list', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'natura_2000_code', Unicode(255), nullable=False),
    Column(u'hd_name', Unicode(255)),
    Column(u'valid_name', Unicode(255)),
    Column(u'ms', Unicode(255)),
    Column(u'bio_region', Unicode(255), nullable=False),
    Column(u'presence', Unicode(255), nullable=False),
    Column(u'ms_feedback_etcbd_comments', Text),
    Column(u'ms_added', Numeric(5, 0, False)),
    Column(u'predefined', Numeric(5, 0, False))
)


t_data_habitattype_reg = Table(
    u'data_habitattype_reg', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'hr_habitat_id', Numeric(scale=0, asdecimal=False)),
    Column(u'region', Unicode(255)),
    Column(u'published', Text),
    Column(u'range_surface_area', Numeric(38, 8)),
    Column(u'range_method_used', Unicode(255)),
    Column(u'range_trend_period', Unicode(9)),
    Column(u'range_trend', Unicode(255)),
    Column(u'range_trend_mag_min', Numeric(38, 8)),
    Column(u'range_trend_mag_max', Numeric(38, 8)),
    Column(u'range_trend_long_period', Unicode(9)),
    Column(u'range_trend_long', Unicode(255)),
    Column(u'range_trend_long_mag_min', Numeric(38, 8)),
    Column(u'range_trend_long_mag_max', Numeric(38, 8)),
    Column(u'compl_favourable_range', Numeric(38, 8)),
    Column(u'comp_favourable_range_op', Unicode(5)),
    Column(u'comp_favourable_range_x', Numeric(5, 0, False)),
    Column(u'comp_favourable_range_met', Text),
    Column(u'r_reasons_for_change_a', Numeric(5, 0, False)),
    Column(u'r_reasons_for_change_b', Numeric(5, 0, False)),
    Column(u'r_reasons_for_change_c', Numeric(5, 0, False)),
    Column(u'coverage_surface_area', Numeric(38, 8)),
    Column(u'coverage_date', Unicode(9)),
    Column(u'coverage_method', Unicode(10)),
    Column(u'coverage_trend_period', Unicode(9)),
    Column(u'coverage_trend', Unicode(5)),
    Column(u'coverage_trend_mag_min', Numeric(38, 8)),
    Column(u'coverage_trend_mag_max', Numeric(38, 8)),
    Column(u'coverage_trend_magnitude_ci', Numeric(5, 0, False)),
    Column(u'coverage_trend_method', Unicode(10)),
    Column(u'coverage_trend_long_period', Unicode(9)),
    Column(u'coverage_trend_long', Unicode(10)),
    Column(u'coverage_trend_long_mag_min', Numeric(38, 8)),
    Column(u'coverage_trend_long_mag_max', Numeric(38, 8)),
    Column(u'coverage_trend_long_mag_ci', Numeric(5, 0, False)),
    Column(u'coverage_trend_long_method', Unicode(255)),
    Column(u'comp_favourable_area', Numeric(38, 8)),
    Column(u'comp_favourable_area_op', Unicode(10)),
    Column(u'comp_favourable_area_x', Numeric(5, 0, False)),
    Column(u'comp_favourable_area_method', Text),
    Column(u'area_reasons_for_change_a', Numeric(5, 0, False)),
    Column(u'area_reasons_for_change_b', Numeric(5, 0, False)),
    Column(u'area_reasons_for_change_c', Numeric(5, 0, False)),
    Column(u'pressures_method', Unicode(10)),
    Column(u'threats_method', Unicode(10)),
    Column(u'typical_species_method', Text),
    Column(u'justification', Text),
    Column(u'structure_and_func_method', Unicode(10)),
    Column(u'other_relevant_information', Text),
    Column(u'conclusion_range', Unicode(10)),
    Column(u'conclusion_range_trend', Unicode(10)),
    Column(u'conclusion_area', Unicode(10)),
    Column(u'conclusion_area_trend', Unicode(10)),
    Column(u'conclusion_structure', Unicode(10)),
    Column(u'conclusion_structure_trend', Unicode(10)),
    Column(u'conclusion_future', Unicode(10)),
    Column(u'conclusion_future_trend', Unicode(10)),
    Column(u'conclusion_assessment', Unicode(10)),
    Column(u'conclusion_assessment_trend', Unicode(10)),
    Column(u'natura2000_area_min', Numeric(38, 8)),
    Column(u'natura2000_area_max', Numeric(38, 8)),
    Column(u'natura2000_area_method', Unicode(10)),
    Column(u'natura2000_area_trend', Unicode(10)),
    Column(u'validated', Numeric(5, 0, False)),
    Column(u'validation_date', Date)
)


t_data_htypical_species = Table(
    u'data_htypical_species', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'species_hr_id', Numeric(scale=0, asdecimal=False)),
    Column(u'speciescode', Unicode(255)),
    Column(u'speciesname', Unicode(255)),
    Column(u'validated', Numeric(5, 0, False)),
    Column(u'validation_date', Date)
)


t_data_measures = Table(
    u'data_measures', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'measurecode', Unicode(10)),
    Column(u'measure_sr_id', Numeric(scale=0, asdecimal=False)),
    Column(u'measure_hr_id', Numeric(scale=0, asdecimal=False)),
    Column(u'type_legal', Numeric(5, 0, False)),
    Column(u'type_administrative', Numeric(5, 0, False)),
    Column(u'type_contractual', Numeric(5, 0, False)),
    Column(u'type_recurrent', Numeric(5, 0, False)),
    Column(u'type_oneoff', Numeric(5, 0, False)),
    Column(u'rankingcode', Unicode(1)),
    Column(u'location_inside', Numeric(5, 0, False)),
    Column(u'location_outside', Numeric(5, 0, False)),
    Column(u'location_both', Numeric(5, 0, False)),
    Column(u'broad_evaluation_maintain', Numeric(5, 0, False)),
    Column(u'broad_evaluation_enhance', Numeric(5, 0, False)),
    Column(u'broad_evaluation_longterm', Numeric(5, 0, False)),
    Column(u'broad_evaluation_noeffect', Numeric(5, 0, False)),
    Column(u'broad_evaluation_unknown', Numeric(5, 0, False)),
    Column(u'broad_evaluation_notevaluat_18', Numeric(5, 0, False)),
    Column(u'validated', Numeric(5, 0, False)),
    Column(u'validation_date', Date)
)


t_data_notes = Table(
    u'data_notes', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'entity_id', Numeric(scale=0, asdecimal=False), nullable=False),
    Column(u'entity_table_name', Unicode(255), nullable=False),
    Column(u'field_label', Unicode(255)),
    Column(u'note', Text, nullable=False),
    Column(u'username', Unicode(255))
)


t_data_pressures_threats = Table(
    u'data_pressures_threats', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'pressure_hr_id', Numeric(scale=0, asdecimal=False)),
    Column(u'pressure_sr_id', Numeric(scale=0, asdecimal=False)),
    Column(u'pressure', Unicode(10)),
    Column(u'ranking', Unicode(10)),
    Column(u'type', Unicode(255)),
    Column(u'validated', Numeric(5, 0, False)),
    Column(u'validation_date', Date)
)


t_data_pressures_threats_pol = Table(
    u'data_pressures_threats_pol', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'pollution_pressure_id', Numeric(scale=0, asdecimal=False)),
    Column(u'pollution_qualifier', Unicode(10)),
    Column(u'validated', Numeric(5, 0, False)),
    Column(u'validation_date', Date)
)


t_data_species = Table(
    u'data_species', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'country', Unicode(255)),
    Column(u'speciescode', Unicode(255)),
    Column(u'alternative_speciesname', Unicode(255)),
    Column(u'common_speciesname', Unicode(255)),
    Column(u'distribution_map', Numeric(5, 0, False)),
    Column(u'sensitive_species', Numeric(5, 0, False)),
    Column(u'distribution_method', Unicode(255)),
    Column(u'distribution_date', Unicode(255)),
    Column(u'additional_distribution_map', Numeric(5, 0, False)),
    Column(u'range_map', Numeric(5, 0, False)),
    Column(u'validated', Numeric(5, 0, False)),
    Column(u'validation_date', Date),
    Column(u'sys_date_created', Date),
    Column(u'sys_date_modified', Date),
    Column(u'sys_date_imported', Date),
    Column(u'sys_creator_id', Unicode(255)),
    Column(u'sys_modifier_id', Unicode(255)),
    Column(u'export', Numeric(5, 0, False)),
    Column(u'import_id', Numeric(scale=0, asdecimal=False))
)


t_data_species_check_list = Table(
    u'data_species_check_list', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'natura_2000_code', Unicode(8)),
    Column(u'eunis_code', Numeric(scale=0, asdecimal=False)),
    Column(u'hd_name', Unicode(60)),
    Column(u'species_name', Unicode(60)),
    Column(u'annex_ii', Unicode(255)),
    Column(u'annex_iv', Unicode(255)),
    Column(u'annex_v', Unicode(255)),
    Column(u'member_state', Unicode(255), nullable=False),
    Column(u'bio_region', Unicode(255), nullable=False),
    Column(u'presence', Unicode(10), nullable=False),
    Column(u'comment_', Text),
    Column(u'ms_added', Numeric(5, 0, False)),
    Column(u'predefined', Numeric(5, 0, False))
)


t_data_species_regions = Table(
    u'data_species_regions', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'sr_species_id', Numeric(scale=0, asdecimal=False)),
    Column(u'region', Unicode(255)),
    Column(u'published', Text),
    Column(u'rsurface_area', Numeric(38, 8)),
    Column(u'range_method', Unicode(255)),
    Column(u'range_trend_period', Unicode(255)),
    Column(u'range_trend', Unicode(255)),
    Column(u'range_trend_mag_min', Numeric(38, 8)),
    Column(u'range_trend_mag_max', Numeric(38, 8)),
    Column(u'range_trend_long_period', Unicode(255)),
    Column(u'range_trend_long', Unicode(255)),
    Column(u'range_trend_long_mag_min', Numeric(38, 8)),
    Column(u'range_trend_long_mag_max', Numeric(38, 8)),
    Column(u'comp_favourable_range', Numeric(38, 8)),
    Column(u'comp_favourable_range_op', Unicode(255)),
    Column(u'comp_favourable_range_x', Numeric(5, 0, False)),
    Column(u'comp_favourable_range_met', Text),
    Column(u'r_reasons_for_change_a', Numeric(5, 0, False)),
    Column(u'r_reasons_for_change_b', Numeric(5, 0, False)),
    Column(u'r_reasons_for_change_c', Numeric(5, 0, False)),
    Column(u'pop_size_unit', Unicode(255)),
    Column(u'pop_minimum_size', Numeric(38, 8)),
    Column(u'pop_maximum_size', Numeric(38, 8)),
    Column(u'pop_alt_size_unit', Unicode(255)),
    Column(u'pop_alt_minimum_size', Numeric(38, 8)),
    Column(u'pop_alt_maximum_size', Numeric(38, 8)),
    Column(u'pop_additional_locality', Text),
    Column(u'pop_additional_method', Text),
    Column(u'pop_additional_problems', Text),
    Column(u'pop_date', Unicode(255)),
    Column(u'pop_method', Unicode(255)),
    Column(u'pop_trend_period', Unicode(255)),
    Column(u'pop_trend', Unicode(255)),
    Column(u'pop_trend_mag_min', Numeric(38, 8)),
    Column(u'pop_trend_mag_max', Numeric(38, 8)),
    Column(u'pop_trend_magnitude_ci', Numeric(5, 0, False)),
    Column(u'pop_trend_method', Unicode(255)),
    Column(u'pop_trend_long_period', Unicode(255)),
    Column(u'population_trend_long', Unicode(255)),
    Column(u'pop_trend_long_mag_min', Numeric(38, 8)),
    Column(u'pop_trend_long_mag_max', Numeric(38, 8)),
    Column(u'pop_trend_long_mag_ci', Numeric(5, 0, False)),
    Column(u'pop_trend_long_method', Unicode(255)),
    Column(u'comp_favourable_pop', Numeric(38, 8)),
    Column(u'comp_favourable_pop_op', Unicode(255)),
    Column(u'comp_favourable_pop_x', Numeric(5, 0, False)),
    Column(u'comp_favourable_pop_met', Text),
    Column(u'pop_reasons_for_change_a', Numeric(5, 0, False)),
    Column(u'pop_reasons_for_change_b', Numeric(5, 0, False)),
    Column(u'pop_reasons_for_change_c', Numeric(5, 0, False)),
    Column(u'habitat_surface_area', Numeric(38, 8)),
    Column(u'habitat_date', Unicode(255)),
    Column(u'habitat_method', Unicode(255)),
    Column(u'habitat_quality', Unicode(255)),
    Column(u'habitat_quality_explanation', Text),
    Column(u'habitat_trend_period', Unicode(255)),
    Column(u'habitat_trend', Unicode(255)),
    Column(u'habitat_trend_long_period', Unicode(255)),
    Column(u'habitat_trend_long', Unicode(255)),
    Column(u'habitat_area_suitable', Numeric(38, 8)),
    Column(u'habitat_reasons_for_change__61', Numeric(5, 0, False)),
    Column(u'habitat_reasons_for_change__62', Numeric(5, 0, False)),
    Column(u'habitat_reasons_for_change__63', Numeric(5, 0, False)),
    Column(u'pressures_method', Unicode(255)),
    Column(u'threats_method', Unicode(255)),
    Column(u'justification', Text),
    Column(u'other_relevant_information', Text),
    Column(u'transboundary_assessment', Text),
    Column(u'conclusion_range', Unicode(255)),
    Column(u'conclusion_range_trend', Unicode(255)),
    Column(u'conclusion_population', Unicode(255)),
    Column(u'conclusion_population_trend', Unicode(255)),
    Column(u'conclusion_habitat', Unicode(255)),
    Column(u'conclusion_habitat_trend', Unicode(255)),
    Column(u'conclusion_future', Unicode(255)),
    Column(u'conclusion_future_trends', Unicode(255)),
    Column(u'conclusion_assessment', Unicode(255)),
    Column(u'conclusion_assessment_trend', Unicode(255)),
    Column(u'natura2000_population_unit', Unicode(255)),
    Column(u'natura2000_population_min', Numeric(38, 8)),
    Column(u'natura2000_population_max', Numeric(38, 8)),
    Column(u'natura2000_population_metho_82', Unicode(255)),
    Column(u'natura2000_population_trend', Unicode(255)),
    Column(u'validated', Numeric(5, 0, False)),
    Column(u'validation_date', Date)
)


t_lu_art17_habitats_check_list = Table(
    u'lu_art17_habitats_check_list', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'natura_2000_code', Unicode(4)),
    Column(u'hd_name', Unicode(255)),
    Column(u'valid_name', Unicode(255)),
    Column(u'ms', Unicode(2)),
    Column(u'bio_region', Unicode(50)),
    Column(u'presence', Unicode(15)),
    Column(u'ms_feedback_etcbd_comments', Text)
)


t_lu_art17_species_check_list = Table(
    u'lu_art17_species_check_list', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'natura_2000_code', Unicode(50)),
    Column(u'hd_name', Unicode(60)),
    Column(u'species_name', Unicode(60)),
    Column(u'annex_ii', Unicode(255)),
    Column(u'annex_iv', Unicode(255)),
    Column(u'annex_v', Unicode(255)),
    Column(u'member_state', Unicode(255)),
    Column(u'bio_region', Unicode(255)),
    Column(u'presence', Unicode(10)),
    Column(u'comment_', Text)
)


t_lu_assessments = Table(
    u'lu_assessments', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(5)),
    Column(u'name', Unicode(255))
)


t_lu_biogeoreg = Table(
    u'lu_biogeoreg', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(10)),
    Column(u'name', Unicode(255)),
    Column(u'order_', Numeric(38, 8))
)


t_lu_countries_regions = Table(
    u'lu_countries_regions', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'country', Unicode(255)),
    Column(u'region', Unicode(255)),
    Column(u'order_', Numeric(scale=0, asdecimal=False))
)


t_lu_country_code = Table(
    u'lu_country_code', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'isocode', Unicode(2)),
    Column(u'code', Unicode(255)),
    Column(u'name', Unicode(255)),
    Column(u'order_', Numeric(scale=0, asdecimal=False))
)


t_lu_favourable_range_operator = Table(
    u'lu_favourable_range_operator', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(5)),
    Column(u'name', Unicode(255)),
    Column(u'order_', Numeric(scale=0, asdecimal=False)),
    Column(u'str_funct', Unicode(1))
)


t_lu_habitattype_codes = Table(
    u'lu_habitattype_codes', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(255)),
    Column(u'hd_name', Unicode(255)),
    Column(u'valide_name', Unicode(255)),
    Column(u'priority', Numeric(38, 8)),
    Column(u'priority_comment', Unicode(255))
)


t_lu_hd_species = Table(
    u'lu_hd_species', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'speciescode', Numeric(38, 8)),
    Column(u'hdname', Unicode(255)),
    Column(u'speciesname', Unicode(255)),
    Column(u'alternativenames', Unicode(255)),
    Column(u'reserve', Unicode(255)),
    Column(u'group_', Unicode(255)),
    Column(u'annexii', Unicode(255)),
    Column(u'annexpriority', Unicode(255)),
    Column(u'annexiv', Unicode(255)),
    Column(u'annexv', Unicode(255)),
    Column(u'annexii_comment', Unicode(255)),
    Column(u'annexiv_commet', Text),
    Column(u'annexv_comment', Text),
    Column(u'etc_comments', Unicode(255))
)


t_lu_measures = Table(
    u'lu_measures', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(255)),
    Column(u'name', Unicode(255)),
    Column(u'valid_entry', Unicode(255))
)


t_lu_methods_pressures = Table(
    u'lu_methods_pressures', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(255)),
    Column(u'name', Unicode(255)),
    Column(u'order_', Numeric(scale=0, asdecimal=False))
)


t_lu_methods_threats = Table(
    u'lu_methods_threats', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(255)),
    Column(u'name', Unicode(255)),
    Column(u'order_', Numeric(38, 8))
)


t_lu_methods_used = Table(
    u'lu_methods_used', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(255)),
    Column(u'name', Unicode(255)),
    Column(u'order_', Numeric(scale=0, asdecimal=False)),
    Column(u'str_funct', Unicode(1))
)


t_lu_pollution = Table(
    u'lu_pollution', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(255)),
    Column(u'name', Unicode(255))
)


t_lu_population_number = Table(
    u'lu_population_number', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(100)),
    Column(u'name', Unicode(255)),
    Column(u'order_', Numeric(38, 8))
)


t_lu_population_units_restricted = Table(
    u'lu_population_units_restricted', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(255)),
    Column(u'name', Unicode(255)),
    Column(u'order_', Numeric(scale=0, asdecimal=False))
)


t_lu_presence = Table(
    u'lu_presence', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(255)),
    Column(u'name', Unicode(255)),
    Column(u'order_', Numeric(38, 8)),
    Column(u'reporting', Unicode(255)),
    Column(u'habitat_reporting', Unicode(255)),
    Column(u'species_reporting', Unicode(255)),
    Column(u'bird_reporting', Unicode(255))
)


t_lu_quality = Table(
    u'lu_quality', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(10)),
    Column(u'name', Unicode(255)),
    Column(u'order_', Numeric(scale=0, asdecimal=False))
)


t_lu_ranking = Table(
    u'lu_ranking', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(255)),
    Column(u'name', Unicode(255)),
    Column(u'note', Unicode(255)),
    Column(u'order_', Numeric(38, 8))
)


t_lu_reintroduction = Table(
    u'lu_reintroduction', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(20)),
    Column(u'name', Unicode(255)),
    Column(u'order_', Numeric(scale=0, asdecimal=False))
)


t_lu_threats = Table(
    u'lu_threats', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(255)),
    Column(u'name', Unicode(255)),
    Column(u'note', Unicode(255)),
    Column(u'eutroph', Unicode(255)),
    Column(u'valid_entry', Unicode(255))
)


t_lu_trends = Table(
    u'lu_trends', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(1)),
    Column(u'name', Unicode(255))
)


t_lu_trends_conclusion = Table(
    u'lu_trends_conclusion', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(1)),
    Column(u'name', Unicode(255)),
    Column(u'order_', Numeric(scale=0, asdecimal=False))
)


t_merge_diff = Table(
    u'merge_diff', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'parent', Unicode(255)),
    Column(u'field_name', Unicode(255)),
    Column(u'field_value', Text),
    Column(u'subheader', Unicode(255))
)


class S109Idx$(Base):
    __tablename__ = u's109_idx$'

    gx = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    gy = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    minx = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    miny = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    maxx = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    maxy = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    sp_id = Column(NullType, primary_key=True, nullable=False)


class S110Idx$(Base):
    __tablename__ = u's110_idx$'

    gx = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    gy = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    minx = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    miny = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    maxx = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    maxy = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    sp_id = Column(NullType, primary_key=True, nullable=False)


class S111Idx$(Base):
    __tablename__ = u's111_idx$'

    gx = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    gy = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    minx = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    miny = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    maxx = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    maxy = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    sp_id = Column(NullType, primary_key=True, nullable=False)


class S112Idx$(Base):
    __tablename__ = u's112_idx$'

    gx = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    gy = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    minx = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    miny = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    maxx = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    maxy = Column(Numeric(scale=0, asdecimal=False), primary_key=True, nullable=False)
    sp_id = Column(NullType, primary_key=True, nullable=False)


t_sys_dummy = Table(
    u'sys_dummy', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(255)),
    Column(u'name', Unicode(255))
)


t_sys_import = Table(
    u'sys_import', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'report_type', Unicode(255)),
    Column(u'filename', Unicode(255)),
    Column(u'nof_records_imported', Numeric(scale=0, asdecimal=False)),
    Column(u'nof_records_failed', Numeric(scale=0, asdecimal=False)),
    Column(u'log', Text),
    Column(u'import_time', Date)
)


t_sys_info_be = Table(
    u'sys_info_be', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'version_be', Unicode(255)),
    Column(u'multi_user_instance', Numeric(5, 0, False)),
    Column(u'habitats_imported', Numeric(5, 0, False)),
    Column(u'species_imported', Numeric(5, 0, False))
)


t_sys_info_fe = Table(
    u'sys_info_fe', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'versionfe', Unicode(255)),
    Column(u'country_code', Unicode(2)),
    Column(u'role', Numeric(scale=0, asdecimal=False)),
    Column(u'reporter', Unicode(255))
)


t_sys_user = Table(
    u'sys_user', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'user_name', Unicode(255)),
    Column(u'first_name', Unicode(255)),
    Column(u'last_name', Unicode(255)),
    Column(u'contactinfo', Unicode(255)),
    Column(u'email', Unicode(255)),
    Column(u'role', Unicode(255)),
    Column(u'general_report', Numeric(5, 0, False)),
    Column(u'species_report', Numeric(5, 0, False)),
    Column(u'habitats_report', Numeric(5, 0, False)),
    Column(u'using_fe_version', Numeric(scale=0, asdecimal=False))
)


t_sys_yesno = Table(
    u'sys_yesno', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'code', Unicode(255)),
    Column(u'label', Unicode(255)),
    Column(u'order_', Numeric(scale=0, asdecimal=False))
)


t_validate_fields = Table(
    u'validate_fields', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'table_name', Unicode(255)),
    Column(u'field_name', Unicode(255)),
    Column(u'table_filter', Unicode(255)),
    Column(u'label', Unicode(255)),
    Column(u'field_type', Unicode(255)),
    Column(u'mask', Unicode(255)),
    Column(u'optional', Numeric(5, 0, False)),
    Column(u'rule', Unicode(255)),
    Column(u'xml_tag', Unicode(255)),
    Column(u'xml_tag_section', Unicode(255)),
    Column(u'xml_desc_relation', Unicode(255)),
    Column(u'import', Numeric(5, 0, False)),
    Column(u'xml_order', Numeric(5, 0, False)),
    Column(u'is_related_table', Numeric(5, 0, False)),
    Column(u'foreign_key_field', Unicode(255)),
    Column(u'primary_key_field', Unicode(255))
)


t_validation_result = Table(
    u'validation_result', metadata,
    Column(u'objectid', Numeric(scale=0, asdecimal=False), nullable=False, index=True),
    Column(u'validation', Text),
    Column(u'validation_time', Date),
    Column(u'style', Unicode(255)),
    Column(u'record_id', Unicode(255))
)
