from sqlalchemy import (Column, DateTime, ForeignKey, Index,
                        Integer, String, Table, Text)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Base = db.Model
metadata = db.metadata


class DataGmeasure(Base):
    __tablename__ = u'data_gmeasures'

    gmeasure_id = Column(Integer, primary_key=True)
    gmeasure_greport_id = Column(ForeignKey(u'data_greport.greport_id'), index=True)
    sitecode = Column(String(18), index=True)
    sitename = Column(String(510))
    project_year = Column(Integer)
    project_title = Column(String(510))
    impact = Column(String(510))
    commission_opinion = Column(String(510))
    project_impact = Column(Text)
    validated = Column(Integer, nullable=False)
    validation_date = Column(DateTime)

    gmeasure_greport = relationship(u'DataGreport')


class DataGreintroductionOfSpecies(Base):
    __tablename__ = u'data_greintroduction_of_species'

    greintr_species_id = Column(Integer, primary_key=True)
    greintr_species_greport_id = Column(ForeignKey(u'data_greport.greport_id'))
    speciescode = Column(String(510))
    speciesname = Column(String(510))
    reintro_period_since = Column(String(2))
    reintro_period = Column(String(18))
    location_number = Column(String(510))
    successful = Column(String(510))
    additional_information = Column(Text)
    validated = Column(Integer, nullable=False)
    validation_date = Column(DateTime)

    greintr_species_greport = relationship(u'DataGreport')


class DataGreport(Base):
    __tablename__ = u'data_greport'

    greport_id = Column(Integer, primary_key=True)
    country = Column(String(4), index=True)
    achievements = Column(Text)
    achievements_trans = Column(Text)
    general_information = Column(Text)
    information_on_network = Column(Text)
    monitoring_schemes = Column(Text)
    protection_of_species = Column(Text)
    transpose_directive = Column(Text)
    sites_total_number = Column(Integer)
    sites_total_area = Column(Text)
    sac_total_number = Column(Integer)
    sac_total_area = Column(Text)
    sites_terrestrial_area = Column(Text)
    sac_terrestrial_area = Column(Text)
    sites_marine_number = Column(Integer)
    sites_marine_area = Column(Text)
    sac_marine_number = Column(Integer)
    sac_marine_area = Column(Text)
    database_date = Column(String(510))
    sites_with_plans = Column(Integer)
    coverage = Column(Text)
    plans_under_prep = Column(Integer)
    coherence_measures = Column(Text)
    sys_date_created = Column(DateTime)
    sys_date_modified = Column(DateTime)
    sys_date_imported = Column(DateTime)
    sys_creator_id = Column(String(510), index=True)
    sys_modifier_id = Column(String(510), index=True)
    validated = Column(Integer, nullable=False)
    validation_date = Column(DateTime)


class DataHabitat(Base):
    __tablename__ = u'data_habitats'
    __table_args__ = (
        Index(u'data_habitats_unique_habitat_idx', u'habitatcode', u'country', u'sys_creator_id'),
    )

    habitat_id = Column(Integer, primary_key=True)
    country = Column(String(4), index=True)
    habitatcode = Column(String(510), index=True)
    distribution_map = Column(Integer, nullable=False)
    distribution_method = Column(String(510), index=True)
    distribution_date = Column(String(18))
    additional_distribution_map = Column(Integer, nullable=False)
    range_map = Column(Integer, nullable=False)
    sys_date_created = Column(DateTime)
    sys_date_modified = Column(DateTime)
    sys_date_imported = Column(DateTime)
    sys_creator_id = Column(String(510), index=True)
    sys_modifier_id = Column(String(510), index=True)
    validated = Column(Integer, nullable=False)
    validation_date = Column(DateTime)
    export = Column(Integer, nullable=False)
    import_id = Column(Integer, index=True)


class DataHabitatsCheckList(Base):
    __tablename__ = u'data_habitats_check_list'

    natura_2000_code = Column(String(510), primary_key=True, nullable=False, index=True)
    hd_name = Column(String(510))
    valid_name = Column(String(510))
    ms = Column(String(510), primary_key=True, nullable=False)
    bio_region = Column(String(510), primary_key=True, nullable=False)
    presence = Column(String(510), nullable=False)
    ms_feedback_etcbd_comments = Column(Text)
    ms_added = Column(Integer, nullable=False)
    predefined = Column(Integer, nullable=False)


class DataHabitattypeRegion(Base):
    __tablename__ = u'data_habitattype_regions'
    __table_args__ = (
        Index(u'data_habitattype_regions_unique_idx', u'hr_habitat_id', u'region'),
    )

    hr_id = Column(Integer, primary_key=True)
    hr_habitat_id = Column(ForeignKey(u'data_habitats.habitat_id'), index=True)
    region = Column(String(510))
    published = Column(Text)
    range_surface_area = Column(Text)
    range_method_used = Column(String(510))
    range_trend_period = Column(String(18))
    range_trend = Column(String(510))
    range_trend_magnitude_min = Column(Text)
    range_trend_magnitude_max = Column(Text)
    range_trend_long_period = Column(String(18))
    range_trend_long = Column(String(510))
    range_trend_long_magnitude_min = Column(Text)
    range_trend_long_magnitude_max = Column(Text)
    complementary_favourable_range = Column(Text)
    complementary_favourable_range_op = Column(String(10))
    complementary_favourable_range_x = Column(Integer, nullable=False)
    complementary_favourable_range_method = Column(Text)
    range_reasons_for_change_a = Column(Integer, nullable=False)
    range_reasons_for_change_b = Column(Integer, nullable=False)
    range_reasons_for_change_c = Column(Integer, nullable=False)
    coverage_surface_area = Column(Text)
    coverage_date = Column(String(18))
    coverage_method = Column(String(20))
    coverage_trend_period = Column(String(18))
    coverage_trend = Column(String(10))
    coverage_trend_magnitude_min = Column(Text)
    coverage_trend_magnitude_max = Column(Text)
    coverage_trend_magnitude_ci = Column(Integer)
    coverage_trend_method = Column(String(20))
    coverage_trend_long_period = Column(String(18))
    coverage_trend_long = Column(String(20))
    coverage_trend_long_magnitude_min = Column(Text)
    coverage_trend_long_magnitude_max = Column(Text)
    coverage_trend_long_magnitude_ci = Column(Integer)
    coverage_trend_long_method = Column(String(510))
    complementary_favourable_area = Column(Text)
    complementary_favourable_area_op = Column(String(20))
    complementary_favourable_area_x = Column(Integer, nullable=False)
    complementary_favourable_area_method = Column(Text)
    area_reasons_for_change_a = Column(Integer, nullable=False)
    area_reasons_for_change_b = Column(Integer, nullable=False)
    area_reasons_for_change_c = Column(Integer, nullable=False)
    pressures_method = Column(String(20))
    threats_method = Column(String(20))
    typical_species_method = Column(Text)
    justification = Column(Text)
    structure_and_functions_method = Column(String(20))
    other_relevant_information = Column(Text)
    conclusion_range = Column(String(20))
    conclusion_range_trend = Column(String(20))
    conclusion_area = Column(String(20))
    conclusion_area_trend = Column(String(20))
    conclusion_structure = Column(String(20))
    conclusion_structure_trend = Column(String(20))
    conclusion_future = Column(String(20))
    conclusion_future_trend = Column(String(20))
    conclusion_assessment = Column(String(20))
    conclusion_assessment_trend = Column(String(20))
    natura2000_area_min = Column(Text)
    natura2000_area_max = Column(Text)
    natura2000_area_method = Column(String(20))
    natura2000_area_trend = Column(String(20))
    validated = Column(Integer, nullable=False)
    validation_date = Column(DateTime)

    hr_habitat = relationship(u'DataHabitat')


class DataHtypicalSpecies(Base):
    __tablename__ = u'data_htypical_species'
    __table_args__ = (
        Index(u'data_htypical_species_unique_idx', u'species_hr_id', u'speciesname'),
    )

    typical_species_id = Column(Integer, primary_key=True)
    species_hr_id = Column(ForeignKey(u'data_habitattype_regions.hr_id'), index=True)
    speciescode = Column(String(510), index=True)
    speciesname = Column(String(510))
    validated = Column(Integer, nullable=False)
    validation_date = Column(DateTime)

    species_hr = relationship(u'DataHabitattypeRegion')


class DataMeasure(Base):
    __tablename__ = u'data_measures'
    __table_args__ = (
        Index(u'data_measures_unique_idx', u'measurecode', u'measure_hr_id'),
    )

    measure_id = Column(Integer, primary_key=True)
    measurecode = Column(String(20), index=True)
    measure_sr_id = Column(ForeignKey(u'data_species_regions.sr_id'), index=True)
    measure_hr_id = Column(ForeignKey(u'data_habitattype_regions.hr_id'), index=True)
    type_legal = Column(Integer, nullable=False)
    type_administrative = Column(Integer, nullable=False)
    type_contractual = Column(Integer, nullable=False)
    type_recurrent = Column(Integer, nullable=False)
    type_oneoff = Column(Integer, nullable=False)
    rankingcode = Column(String(2), index=True)
    location_inside = Column(Integer, nullable=False)
    location_outside = Column(Integer, nullable=False)
    location_both = Column(Integer, nullable=False)
    broad_evaluation_maintain = Column(Integer, nullable=False)
    broad_evaluation_enhance = Column(Integer, nullable=False)
    broad_evaluation_longterm = Column(Integer, nullable=False)
    broad_evaluation_noeffect = Column(Integer, nullable=False)
    broad_evaluation_unknown = Column(Integer, nullable=False)
    broad_evaluation_notevaluated = Column(Integer, nullable=False)
    validated = Column(Integer, nullable=False)
    validation_date = Column(DateTime)

    measure_hr = relationship(u'DataHabitattypeRegion')
    measure_sr = relationship(u'DataSpeciesRegion')


class DataNote(Base):
    __tablename__ = u'data_notes'

    notes_id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, nullable=False, index=True)
    entity_table_name = Column(String(510), nullable=False)
    field_label = Column(String(510))
    note = Column(Text, nullable=False)
    username = Column(String(510))


class DataPressuresThreat(Base):
    __tablename__ = u'data_pressures_threats'
    __table_args__ = (
        Index(u'data_pressures_threats_uniqueSr_idx', u'pressure_sr_id', u'pressure', u'type'),
        Index(u'data_pressures_threats_uniqueHr_idx', u'pressure_hr_id', u'pressure', u'type')
    )

    pressure_id = Column(Integer, primary_key=True)
    pressure_hr_id = Column(ForeignKey(u'data_habitattype_regions.hr_id'), index=True)
    pressure_sr_id = Column(ForeignKey(u'data_species_regions.sr_id'), index=True)
    pressure = Column(String(20))
    ranking = Column(String(20))
    type = Column(String(510))
    validated = Column(Integer, nullable=False)
    validation_Date = Column(DateTime)

    pressure_hr = relationship(u'DataHabitattypeRegion')
    pressure_sr = relationship(u'DataSpeciesRegion')


class DataPressuresThreatsPol(Base):
    __tablename__ = u'data_pressures_threats_pol'

    pollution_id = Column(Integer, primary_key=True)
    pollution_pressure_id = Column(ForeignKey(u'data_pressures_threats.pressure_id'), index=True)
    pollution_qualifier = Column(String(20))
    validated = Column(Integer, nullable=False)
    validation_date = Column(DateTime)

    pollution_pressure = relationship(u'DataPressuresThreat')


class DataSpecies(Base):
    __tablename__ = u'data_species'
    __table_args__ = (
        Index(u'data_species_unique_report_idx', u'speciescode', u'country', u'sys_creator_id'),
    )

    species_id = Column(Integer, primary_key=True, index=True)
    country = Column(String(510))
    speciescode = Column(String(510), index=True)
    alternative_speciesname = Column(String(510))
    common_speciesname = Column(String(510))
    distribution_map = Column(Integer, nullable=False)
    sensitive_species = Column(Integer, nullable=False)
    distribution_method = Column(String(510))
    distribution_date = Column(String(510))
    additional_distribution_map = Column(Integer, nullable=False)
    range_map = Column(Integer, nullable=False)
    validated = Column(Integer, nullable=False)
    validation_date = Column(DateTime)
    sys_date_created = Column(DateTime)
    sys_date_modified = Column(DateTime)
    sys_date_imported = Column(DateTime)
    sys_creator_id = Column(String(510), index=True)
    sys_modifier_id = Column(String(510), index=True)
    export = Column(Integer, nullable=False)
    import_id = Column(Integer, index=True)


class DataSpeciesCheckList(Base):
    __tablename__ = u'data_species_check_list'

    natura_2000_code = Column(String(16), primary_key=True, nullable=False, index=True)
    eunis_code = Column(Integer, index=True)
    HD_name = Column(String(120))
    species_name = Column(String(120))
    annex_II = Column(String(510))
    annex_IV = Column(String(510))
    annex_V = Column(String(510))
    member_state = Column(String(510), primary_key=True, nullable=False)
    bio_region = Column(String(510), primary_key=True, nullable=False)
    Presence = Column(String(20), nullable=False)
    Comment = Column(Text)
    ms_added = Column(Integer, nullable=False)
    predefined = Column(Integer, nullable=False)


class DataSpeciesRegion(Base):
    __tablename__ = u'data_species_regions'
    __table_args__ = (
        Index(u'data_species_regions_region_unique_idx', u'sr_species_id', u'region'),
    )

    sr_id = Column(Integer, primary_key=True, index=True)
    sr_species_id = Column(ForeignKey(u'data_species.species_id'), index=True)
    region = Column(String(510))
    published = Column(Text)
    range_surface_area = Column(Text)
    range_method = Column(String(510))
    range_trend_period = Column(String(510))
    range_trend = Column(String(510))
    range_trend_magnitude_min = Column(Text)
    range_trend_magnitude_max = Column(Text)
    range_trend_long_period = Column(String(510))
    range_trend_long = Column(String(510))
    range_trend_long_magnitude_min = Column(Text)
    range_trend_long_magnitude_max = Column(Text)
    complementary_favourable_range = Column(Text)
    complementary_favourable_range_op = Column(String(510))
    complementary_favourable_range_x = Column(Integer, nullable=False)
    complementary_favourable_range_method = Column(Text)
    range_reasons_for_change_a = Column(Integer, nullable=False)
    range_reasons_for_change_b = Column(Integer, nullable=False)
    range_reasons_for_change_c = Column(Integer, nullable=False)
    population_size_unit = Column(String(510))
    population_minimum_size = Column(Text)
    population_maximum_size = Column(Text)
    population_alt_size_unit = Column(String(510))
    population_alt_minimum_size = Column(Text)
    population_alt_maximum_size = Column(Text)
    population_additional_locality = Column(Text)
    population_additional_method = Column(Text)
    population_additional_problems = Column(Text)
    population_date = Column(String(510))
    population_method = Column(String(510))
    population_trend_period = Column(String(510))
    population_trend = Column(String(510))
    population_trend_magnitude_min = Column(Text)
    population_trend_magnitude_max = Column(Text)
    population_trend_magnitude_ci = Column(Integer)
    population_trend_method = Column(String(510))
    population_trend_long_period = Column(String(510))
    population_trend_long = Column(String(510))
    population_trend_long_magnitude_min = Column(Text)
    population_trend_long_magnitude_max = Column(Text)
    population_trend_long_magnitude_ci = Column(Integer)
    population_trend_long_method = Column(String(510))
    complementary_favourable_population = Column(Text)
    complementary_favourable_population_op = Column(String(510))
    complementary_favourable_population_x = Column(Integer, nullable=False)
    complementary_favourable_population_method = Column(Text)
    population_reasons_for_change_a = Column(Integer, nullable=False)
    population_reasons_for_change_b = Column(Integer, nullable=False)
    population_reasons_for_change_c = Column(Integer, nullable=False)
    habitat_surface_area = Column(Text)
    habitat_date = Column(String(510))
    habitat_method = Column(String(510))
    habitat_quality = Column(String(510))
    habitat_quality_explanation = Column(Text)
    habitat_trend_period = Column(String(510))
    habitat_trend = Column(String(510))
    habitat_trend_long_period = Column(String(510))
    habitat_trend_long = Column(String(510))
    habitat_area_suitable = Column(Text)
    habitat_reasons_for_change_a = Column(Integer, nullable=False)
    habitat_reasons_for_change_b = Column(Integer, nullable=False)
    habitat_reasons_for_change_c = Column(Integer, nullable=False)
    pressures_method = Column(String(510))
    threats_method = Column(String(510))
    justification = Column(Text)
    other_relevant_information = Column(Text)
    transboundary_assessment = Column(Text)
    conclusion_range = Column(String(510))
    conclusion_range_trend = Column(String(510))
    conclusion_population = Column(String(510))
    conclusion_population_trend = Column(String(510))
    conclusion_habitat = Column(String(510))
    conclusion_habitat_trend = Column(String(510))
    conclusion_future = Column(String(510))
    conclusion_future_trends = Column(String(510))
    conclusion_assessment = Column(String(510))
    conclusion_assessment_trend = Column(String(510))
    natura2000_population_unit = Column(String(510))
    natura2000_population_min = Column(Text)
    natura2000_population_max = Column(Text)
    natura2000_population_method = Column(String(510))
    natura2000_population_trend = Column(String(510))
    validated = Column(Integer, nullable=False)
    validation_date = Column(DateTime)

    sr_species = relationship(u'DataSpecies',
        backref=db.backref('regions', lazy='dynamic'))


class SysImport(Base):
    __tablename__ = u'sys_import'

    import_id = Column(Integer, primary_key=True)
    report_type = Column(String(510))
    filename = Column(String(510))
    nof_records_imported = Column(Integer)
    nof_records_failed = Column(Integer)
    log = Column(Text)
    import_time = Column(DateTime)


t_sys_info_be = Table(
    u'sys_info_be', metadata,
    Column(u'version_be', String(510)),
    Column(u'multi_user_instance', Integer, nullable=False),
    Column(u'habitats_imported', Integer, nullable=False),
    Column(u'species_imported', Integer, nullable=False)
)


class SysUser(Base):
    __tablename__ = u'sys_user'

    user_name = Column(String(510), primary_key=True)
    first_name = Column(String(510))
    last_name = Column(String(510))
    contactInfo = Column(String(510))
    email = Column(String(510))
    role = Column(String(510))
    general_report = Column(Integer, nullable=False)
    species_report = Column(Integer, nullable=False)
    habitats_report = Column(Integer, nullable=False)
    using_fe_version = Column(Integer)
