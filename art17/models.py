from sqlalchemy import (Column, DateTime, ForeignKey, Index,
                        String, Table, Text, Numeric, cast)
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Base = db.Model
metadata = db.metadata


class LuHabitattypeCodes(Base):
    __tablename__ = u'lu_habitattype_codes'

    objectid = Column(Numeric, primary_key=True)
    code = Column(String)
    hd_name = Column(String)
    valide_name = Column(String)
    priority = Column(Numeric)
    priority_comment = Column(String)


class LuGrupSpecie(Base):
    __tablename__ = u'lu_grup_specie'

    oid = Column(Numeric, primary_key=True)
    code = Column(String)
    description = Column(String)


class LuHdSpecies(Base):
    __tablename__ = u'lu_hd_species'

    objectid = Column(Numeric, primary_key=True)
    speciescode = Column(Numeric)
    hdname = Column(String)
    speciesname = Column(String)
    alternativenames = Column(String)
    reserve = Column(String)
    group_code = Column('group_', String)
    annexii = Column(String)
    annexpriority = Column(String)
    annexiv = Column(String)
    annexv = Column(String)
    annexii_comment = Column(String)
    annexiv_commet = Column(Text)
    annexv_comment = Column(Text)
    etc_comments = Column(String)


class LuCountriesRegions(Base):
    __tablename__ = u'lu_countries_regions'

    objectid = Column(Numeric, primary_key=True)
    country = Column(String)
    region_code = Column('region', String, ForeignKey('lu_biogeoreg.code'))
    order = Column('order_', Numeric)

    region = relationship('LuBiogeoreg', lazy='eager')


class LuBiogeoreg(Base):
    __tablename__ = u'lu_biogeoreg'

    objectid = Column(Numeric, primary_key=True)
    code = Column(String)
    name = Column(String)
    name_ro = Column('nume', String)
    order = Column('order_', Numeric)


class DataGmeasure(Base):
    __tablename__ = u'data_gmeasures'

    gmeasure_id = Column(Numeric, primary_key=True)
    gmeasure_greport_id = Column(ForeignKey(u'data_greport.greport_id'), index=True)
    sitecode = Column(String(18), index=True)
    sitename = Column(String(510))
    project_year = Column(Numeric)
    project_title = Column(String(510))
    impact = Column(String(510))
    commission_opinion = Column(String(510))
    project_impact = Column(Text)
    validated = Column(Numeric, nullable=False)
    validation_date = Column(DateTime)

    gmeasure_greport = relationship(u'DataGreport')


class DataGreintroductionOfSpecies(Base):
    __tablename__ = u'data_greintroduction_of_species'

    greintr_species_id = Column(Numeric, primary_key=True)
    greintr_species_greport_id = Column(ForeignKey(u'data_greport.greport_id'))
    speciescode = Column(String(510))
    speciesname = Column(String(510))
    reintro_period_since = Column(String(2))
    reintro_period = Column(String(18))
    location_number = Column(String(510))
    successful = Column(String(510))
    additional_information = Column(Text)
    validated = Column(Numeric, nullable=False)
    validation_date = Column(DateTime)

    greintr_species_greport = relationship(u'DataGreport')


class DataGreport(Base):
    __tablename__ = u'data_greport'

    greport_id = Column(Numeric, primary_key=True)
    country = Column(String(4), index=True)
    achievements = Column(Text)
    achievements_trans = Column(Text)
    general_information = Column(Text)
    information_on_network = Column(Text)
    monitoring_schemes = Column(Text)
    protection_of_species = Column(Text)
    transpose_directive = Column(Text)
    sites_total_number = Column(Numeric)
    sites_total_area = Column(Text)
    sac_total_number = Column(Numeric)
    sac_total_area = Column(Text)
    sites_terrestrial_area = Column(Text)
    sac_terrestrial_area = Column(Text)
    sites_marine_number = Column(Numeric)
    sites_marine_area = Column(Text)
    sac_marine_number = Column(Numeric)
    sac_marine_area = Column(Text)
    database_date = Column(String(510))
    sites_with_plans = Column(Numeric)
    coverage = Column(Text)
    plans_under_prep = Column(Numeric)
    coherence_measures = Column(Text)
    sys_date_created = Column(DateTime)
    sys_date_modified = Column(DateTime)
    sys_date_imported = Column(DateTime)
    sys_creator_id = Column(String(510), index=True)
    sys_modifier_id = Column(String(510), index=True)
    validated = Column(Numeric, nullable=False)
    validation_date = Column(DateTime)


class DataHabitat(Base):
    __tablename__ = u'data_habitats'
    __table_args__ = (
        Index(u'data_habitats_unique_habitat_idx', u'habitatcode', u'country', u'sys_creator_id'),
    )

    habitat_id = Column('objectid', Numeric, primary_key=True)
    country = Column(String(4), index=True)
    habitatcode = Column(String(510), index=True)
    distribution_map = Column(Numeric, nullable=False)
    distribution_method = Column(String(510), index=True)
    distribution_date = Column(String(18))
    additional_distribution_map = Column(Numeric, nullable=False)
    range_map = Column(Numeric, nullable=False)
    sys_date_created = Column(DateTime)
    sys_date_modified = Column(DateTime)
    sys_date_imported = Column(DateTime)
    sys_creator_id = Column(String(510), index=True)
    sys_modifier_id = Column(String(510), index=True)
    validated = Column(Numeric, nullable=False)
    validation_date = Column(DateTime)
    export = Column(Numeric, nullable=False)
    import_id = Column(Numeric, index=True)

    lu = relationship(u'LuHabitattypeCodes',
                      primaryjoin=(habitatcode ==
                                   foreign(LuHabitattypeCodes.code)),
                      uselist=False, lazy='eager')


class DataHabitatsCheckList(Base):
    __tablename__ = u'data_habitats_check_list'

    natura_2000_code = Column(String(510), primary_key=True, nullable=False, index=True)
    hd_name = Column(String(510))
    valid_name = Column(String(510))
    ms = Column(String(510), primary_key=True, nullable=False)
    bio_region = Column(String(510), primary_key=True, nullable=False)
    presence = Column(String(510), nullable=False)
    ms_feedback_etcbd_comments = Column(Text)
    ms_added = Column(Numeric, nullable=False)
    predefined = Column(Numeric, nullable=False)


class DataHabitattypeRegion(Base):
    __tablename__ = u'data_habitattype_reg'
    __table_args__ = (
        Index(u'data_habitattype_regions_unique_idx', u'hr_habitat_id', u'region'),
    )

    hr_id = Column('objectid', Numeric, primary_key=True)
    hr_habitat_id = Column(ForeignKey(u'data_habitats.objectid'), index=True)
    region = Column(String(510))
    published = Column(Text)
    range_surface_area = Column(Numeric)
    range_method_used = Column(String(510))
    range_trend_period = Column(String(18))
    range_trend = Column(String(510))
    range_trend_magnitude_min = Column('range_trend_mag_min', Numeric)
    range_trend_magnitude_max = Column('range_trend_mag_max', Numeric)
    range_trend_long_period = Column(String(18))
    range_trend_long = Column(String(510))
    range_trend_long_magnitude_min = Column('range_trend_long_mag_min', Numeric)
    range_trend_long_magnitude_max = Column('range_trend_long_mag_max', Numeric)
    complementary_favourable_range = Column('compl_favourable_range', Numeric)
    complementary_favourable_range_op = Column('comp_favourable_range_op', String(10))
    complementary_favourable_range_x = Column('comp_favourable_range_x', Numeric, nullable=False)
    complementary_favourable_range_method = Column('comp_favourable_range_met', Text)
    range_reasons_for_change_a = Column('r_reasons_for_change_a', Numeric, nullable=False)
    range_reasons_for_change_b = Column('r_reasons_for_change_b', Numeric, nullable=False)
    range_reasons_for_change_c = Column('r_reasons_for_change_c', Numeric, nullable=False)
    coverage_surface_area = Column(Numeric)
    coverage_date = Column(String(18))
    coverage_method = Column(String(20))
    coverage_trend_period = Column(String(18))
    coverage_trend = Column(String(10))
    coverage_trend_magnitude_min = Column('coverage_trend_mag_min', Numeric)
    coverage_trend_magnitude_max = Column('coverage_trend_mag_max', Numeric)
    coverage_trend_magnitude_ci = Column(Numeric)
    coverage_trend_method = Column(String(20))
    coverage_trend_long_period = Column(String(18))
    coverage_trend_long = Column(String(20))
    coverage_trend_long_magnitude_min = Column('coverage_trend_long_mag_min', Numeric)
    coverage_trend_long_magnitude_max = Column('coverage_trend_long_mag_max', Numeric)
    coverage_trend_long_magnitude_ci = Column('coverage_trend_long_mag_ci', Numeric)
    coverage_trend_long_method = Column(String(510))
    complementary_favourable_area = Column('comp_favourable_area', Numeric)
    complementary_favourable_area_op = Column('comp_favourable_area_op', String(20))
    complementary_favourable_area_x = Column('comp_favourable_area_x', Numeric, nullable=False)
    complementary_favourable_area_method = Column('comp_favourable_area_method', Text)
    area_reasons_for_change_a = Column(Numeric, nullable=False)
    area_reasons_for_change_b = Column(Numeric, nullable=False)
    area_reasons_for_change_c = Column(Numeric, nullable=False)
    pressures_method = Column(String(20))
    threats_method = Column(String(20))
    typical_species_method = Column(Text)
    justification = Column(Text)
    structure_and_functions_method = Column('structure_and_func_method', String(20))
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
    natura2000_area_min = Column(Numeric)
    natura2000_area_max = Column(Numeric)
    natura2000_area_method = Column(String(20))
    natura2000_area_trend = Column(String(20))
    validated = Column(Numeric, nullable=False)
    validation_date = Column(DateTime)

    hr_habitat = relationship(u'DataHabitat',
        backref=db.backref('regions', lazy='dynamic'))


class DataHtypicalSpecies(Base):
    __tablename__ = u'data_htypical_species'
    __table_args__ = (
        Index(u'data_htypical_species_unique_idx', u'species_hr_id', u'speciesname'),
    )

    typical_species_id = Column(Numeric, primary_key=True)
    species_hr_id = Column(ForeignKey(u'data_habitattype_reg.objectid'), index=True)
    speciescode = Column(String(510), index=True)
    speciesname = Column(String(510))
    validated = Column(Numeric, nullable=False)
    validation_date = Column(DateTime)

    species_hr = relationship(u'DataHabitattypeRegion')


class DataMeasure(Base):
    __tablename__ = u'data_measures'
    __table_args__ = (
        Index(u'data_measures_unique_idx', u'measurecode', u'measure_hr_id'),
    )

    measure_id = Column(Numeric, primary_key=True)
    measurecode = Column(String(20), index=True)
    measure_sr_id = Column(ForeignKey(u'data_species_regions.objectid'), index=True)
    measure_hr_id = Column(ForeignKey(u'data_habitattype_reg.objectid'), index=True)
    type_legal = Column(Numeric, nullable=False)
    type_administrative = Column(Numeric, nullable=False)
    type_contractual = Column(Numeric, nullable=False)
    type_recurrent = Column(Numeric, nullable=False)
    type_oneoff = Column(Numeric, nullable=False)
    rankingcode = Column(String(2), index=True)
    location_inside = Column(Numeric, nullable=False)
    location_outside = Column(Numeric, nullable=False)
    location_both = Column(Numeric, nullable=False)
    broad_evaluation_maintain = Column(Numeric, nullable=False)
    broad_evaluation_enhance = Column(Numeric, nullable=False)
    broad_evaluation_longterm = Column(Numeric, nullable=False)
    broad_evaluation_noeffect = Column(Numeric, nullable=False)
    broad_evaluation_unknown = Column(Numeric, nullable=False)
    broad_evaluation_notevaluated = Column(Numeric, nullable=False)
    validated = Column(Numeric, nullable=False)
    validation_date = Column(DateTime)

    measure_hr = relationship(u'DataHabitattypeRegion')
    measure_sr = relationship(u'DataSpeciesRegion')


class DataNote(Base):
    __tablename__ = u'data_notes'

    notes_id = Column(Numeric, primary_key=True)
    entity_id = Column(Numeric, nullable=False, index=True)
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

    pressure_id = Column(Numeric, primary_key=True)
    pressure_hr_id = Column(ForeignKey(u'data_habitattype_reg.objectid'), index=True)
    pressure_sr_id = Column(ForeignKey(u'data_species_regions.objectid'), index=True)
    pressure = Column(String(20))
    ranking = Column(String(20))
    type = Column(String(510))
    validated = Column(Numeric, nullable=False)
    validation_Date = Column(DateTime)

    pressure_hr = relationship(u'DataHabitattypeRegion')
    pressure_sr = relationship(u'DataSpeciesRegion')


class DataPressuresThreatsPol(Base):
    __tablename__ = u'data_pressures_threats_pol'

    pollution_id = Column(Numeric, primary_key=True)
    pollution_pressure_id = Column(ForeignKey(u'data_pressures_threats.pressure_id'), index=True)
    pollution_qualifier = Column(String(20))
    validated = Column(Numeric, nullable=False)
    validation_date = Column(DateTime)

    pollution_pressure = relationship(u'DataPressuresThreat')


class DataSpecies(Base):
    __tablename__ = u'data_species'
    __table_args__ = (
        Index(u'data_species_unique_report_idx', u'speciescode', u'country', u'sys_creator_id'),
    )

    species_id = Column('objectid', Numeric, primary_key=True, index=True)
    country = Column(String(510))
    speciescode = Column(String(510), index=True)
    alternative_speciesname = Column(String(510))
    common_speciesname = Column(String(510))
    distribution_map = Column(Numeric, nullable=False)
    sensitive_species = Column(Numeric, nullable=False)
    distribution_method = Column(String(510))
    distribution_date = Column(String(510))
    additional_distribution_map = Column(Numeric, nullable=False)
    range_map = Column(Numeric, nullable=False)
    validated = Column(Numeric, nullable=False)
    validation_date = Column(DateTime)
    sys_date_created = Column(DateTime)
    sys_date_modified = Column(DateTime)
    sys_date_imported = Column(DateTime)
    sys_creator_id = Column(String(510), index=True)
    sys_modifier_id = Column(String(510), index=True)
    export = Column(Numeric, nullable=False)
    import_id = Column(Numeric, index=True)

    lu = relationship(LuHdSpecies,
                      primaryjoin=(speciescode ==
                                   cast(foreign(LuHdSpecies.speciescode),
                                        String(255))),
                      lazy='joined', innerjoin=True, uselist=False,
                      backref=db.backref('data',
                                         lazy='joined',
                                         uselist=False,
                                         innerjoin=True))


class DataSpeciesCheckList(Base):
    __tablename__ = u'data_species_check_list'

    natura_2000_code = Column(String(16), primary_key=True, nullable=False, index=True)
    eunis_code = Column(Numeric, index=True)
    hd_name = Column(String(120))
    species_name = Column(String(120))
    annex_ii = Column(String(510))
    annex_iv = Column(String(510))
    annex_v = Column(String(510))
    member_state = Column(String(510), primary_key=True, nullable=False)
    bio_region = Column(String(510), primary_key=True, nullable=False)
    presence = Column(String(20), nullable=False)
    comment = Column('comment_', Text)
    ms_added = Column(Numeric, nullable=False)
    predefined = Column(Numeric, nullable=False)


class DataSpeciesRegion(Base):
    __tablename__ = u'data_species_regions'
    __table_args__ = (
        Index(u'data_species_regions_region_unique_idx', u'sr_species_id', u'region'),
    )

    sr_id = Column('objectid', Numeric, primary_key=True, index=True)
    sr_species_id = Column(ForeignKey(u'data_species.objectid'), index=True)
    region = Column(String(510))
    published = Column(Text)
    range_surface_area = Column('rsurface_area', Numeric)
    range_method = Column(String(510))
    range_trend_period = Column(String(510))
    range_trend = Column(String(510))
    range_trend_magnitude_min = Column('range_trend_mag_min', Numeric)
    range_trend_magnitude_max = Column('range_trend_mag_max', Numeric)
    range_trend_long_period = Column(String(510))
    range_trend_long = Column(String(510))
    range_trend_long_magnitude_min = Column('range_trend_long_mag_min', Numeric)
    range_trend_long_magnitude_max = Column('range_trend_long_mag_max', Numeric)
    complementary_favourable_range = Column('comp_favourable_range', Numeric)
    complementary_favourable_range_op = Column('comp_favourable_range_op', String(510))
    complementary_favourable_range_x = Column('comp_favourable_range_x', Numeric, nullable=False)
    complementary_favourable_range_method = Column('comp_favourable_range_met', Text)
    range_reasons_for_change_a = Column('r_reasons_for_change_a', Numeric, nullable=False)
    range_reasons_for_change_b = Column('r_reasons_for_change_b', Numeric, nullable=False)
    range_reasons_for_change_c = Column('r_reasons_for_change_c', Numeric, nullable=False)
    population_size_unit = Column('pop_size_unit', String(510))
    population_minimum_size = Column('pop_minimum_size', Numeric)
    population_maximum_size = Column('pop_maximum_size', Numeric)
    population_alt_size_unit = Column('pop_alt_size_unit', String(510))
    population_alt_minimum_size = Column('pop_alt_minimum_size', Numeric)
    population_alt_maximum_size = Column('pop_alt_maximum_size', Numeric)
    population_additional_locality = Column('pop_additional_locality', Text)
    population_additional_method = Column('pop_additional_method', Text)
    population_additional_problems = Column('pop_additional_problems', Text)
    population_date = Column('pop_date', String(510))
    population_method = Column('pop_method', String(510))
    population_trend_period = Column('pop_trend_period', String(510))
    population_trend = Column('pop_trend', String(510))
    population_trend_magnitude_min = Column('pop_trend_mag_min', Numeric)
    population_trend_magnitude_max = Column('pop_trend_mag_max', Numeric)
    population_trend_magnitude_ci = Column('pop_trend_magnitude_ci', Numeric)
    population_trend_method = Column('pop_trend_method', String(510))
    population_trend_long_period = Column('pop_trend_long_period', String(510))
    population_trend_long = Column(String(510))
    population_trend_long_magnitude_min = Column('pop_trend_long_mag_min', Numeric)
    population_trend_long_magnitude_max = Column('pop_trend_long_mag_max', Numeric)
    population_trend_long_magnitude_ci = Column('pop_trend_long_mag_ci', Numeric)
    population_trend_long_method = Column('pop_trend_long_method', String(510))
    complementary_favourable_population = Column('comp_favourable_pop', Numeric)
    complementary_favourable_population_op = Column('comp_favourable_pop_op', String(510))
    complementary_favourable_population_x = Column('comp_favourable_pop_x', Numeric, nullable=False)
    complementary_favourable_population_method = Column('comp_favourable_pop_met', Text)
    population_reasons_for_change_a = Column('pop_reasons_for_change_a', Numeric, nullable=False)
    population_reasons_for_change_b = Column('pop_reasons_for_change_b', Numeric, nullable=False)
    population_reasons_for_change_c = Column('pop_reasons_for_change_c', Numeric, nullable=False)
    habitat_surface_area = Column(Numeric)
    habitat_date = Column(String(510))
    habitat_method = Column(String(510))
    habitat_quality = Column(String(510))
    habitat_quality_explanation = Column(Text)
    habitat_trend_period = Column(String(510))
    habitat_trend = Column(String(510))
    habitat_trend_long_period = Column(String(510))
    habitat_trend_long = Column(String(510))
    habitat_area_suitable = Column(Numeric)
    habitat_reasons_for_change_a = Column('habitat_reasons_for_change__61', Numeric, nullable=False)
    habitat_reasons_for_change_b = Column('habitat_reasons_for_change__62', Numeric, nullable=False)
    habitat_reasons_for_change_c = Column('habitat_reasons_for_change__63', Numeric, nullable=False)
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
    conclusion_future_trend = Column('conclusion_future_trends', String(510))
    conclusion_assessment = Column(String(510))
    conclusion_assessment_trend = Column(String(510))
    natura2000_population_unit = Column(String(510))
    natura2000_population_min = Column(Numeric)
    natura2000_population_max = Column(Numeric)
    natura2000_population_method = Column('natura2000_population_metho_82', String(510))
    natura2000_population_trend = Column(String(510))
    validated = Column(Numeric, nullable=False)
    validation_date = Column(DateTime)

    sr_species = relationship(u'DataSpecies',
        backref=db.backref('regions', lazy='dynamic'))


class SysImport(Base):
    __tablename__ = u'sys_import'

    import_id = Column(Numeric, primary_key=True)
    report_type = Column(String(510))
    filename = Column(String(510))
    nof_records_imported = Column(Numeric)
    nof_records_failed = Column(Numeric)
    log = Column(Text)
    import_time = Column(DateTime)


t_sys_info_be = Table(
    u'sys_info_be', metadata,
    Column(u'version_be', String(510)),
    Column(u'multi_user_instance', Numeric, nullable=False),
    Column(u'habitats_imported', Numeric, nullable=False),
    Column(u'species_imported', Numeric, nullable=False)
)


class SysUser(Base):
    __tablename__ = u'sys_user'

    user_name = Column(String(510), primary_key=True)
    first_name = Column(String(510))
    last_name = Column(String(510))
    contactInfo = Column(String(510))
    email = Column(String(510))
    role = Column(String(510))
    general_report = Column(Numeric, nullable=False)
    species_report = Column(Numeric, nullable=False)
    habitats_report = Column(Numeric, nullable=False)
    using_fe_version = Column(Numeric)
