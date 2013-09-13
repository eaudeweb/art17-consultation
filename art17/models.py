import uuid
import argparse
import logging
from sqlalchemy import (Column, DateTime, ForeignKey, Index,
                        String, Table, Text, Numeric, cast, Binary)
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager

db = SQLAlchemy()
Base = db.Model
metadata = db.metadata

db_manager = Manager()


def create_uuid():
    return str(uuid.uuid4()).replace('-', '')


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


class LuBiogeoreg(Base):
    __tablename__ = u'lu_biogeoreg'

    objectid = Column(Numeric, primary_key=True)
    code = Column(String)
    name = Column(String)
    name_ro = Column('nume', String)
    order = Column('order_', Numeric)


class LuCountriesRegions(Base):
    __tablename__ = u'lu_countries_regions'

    objectid = Column(Numeric, primary_key=True)
    country = Column(String)
    region_code = Column('region', String, ForeignKey(LuBiogeoreg.code))
    order = Column('order_', Numeric)

    region = relationship('LuBiogeoreg', lazy='eager')


class DataGreport(Base):
    __tablename__ = u'data_greport'

    greport_id = Column(Numeric, primary_key=True)
    country = Column(String, index=True)
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
    database_date = Column(String)
    sites_with_plans = Column(Numeric)
    coverage = Column(Text)
    plans_under_prep = Column(Numeric)
    coherence_measures = Column(Text)
    sys_date_created = Column(DateTime)
    sys_date_modified = Column(DateTime)
    sys_date_imported = Column(DateTime)
    sys_creator_id = Column(String, index=True)
    sys_modifier_id = Column(String, index=True)
    validated = Column(Numeric)
    validation_date = Column(DateTime)


class DataGmeasure(Base):
    __tablename__ = u'data_gmeasures'

    gmeasure_id = Column(Numeric, primary_key=True)
    gmeasure_greport_id = Column(ForeignKey(DataGreport.greport_id), index=True)
    sitecode = Column(String, index=True)
    sitename = Column(String)
    project_year = Column(Numeric)
    project_title = Column(String)
    impact = Column(String)
    commission_opinion = Column(String)
    project_impact = Column(Text)
    validated = Column(Numeric)
    validation_date = Column(DateTime)

    gmeasure_greport = relationship(u'DataGreport')


class DataGreintroductionOfSpecies(Base):
    __tablename__ = u'data_greintroduction_of_species'

    greintr_species_id = Column(Numeric, primary_key=True)
    greintr_species_greport_id = Column(ForeignKey(DataGreport.greport_id))
    speciescode = Column(String)
    speciesname = Column(String)
    reintro_period_since = Column(String)
    reintro_period = Column(String)
    location_number = Column(String)
    successful = Column(String)
    additional_information = Column(Text)
    validated = Column(Numeric)
    validation_date = Column(DateTime)

    greintr_species_greport = relationship(u'DataGreport')


class DataHabitat(Base):
    __tablename__ = u'data_habitats'

    habitat_id = Column('objectid', Numeric, primary_key=True)
    country = Column(String, index=True)
    habitatcode = Column(String, index=True)
    distribution_map = Column(Numeric)
    distribution_method = Column(String, index=True)
    distribution_date = Column(String)
    additional_distribution_map = Column(Numeric)
    range_map = Column(Numeric)
    sys_date_created = Column(DateTime)
    sys_date_modified = Column(DateTime)
    sys_date_imported = Column(DateTime)
    sys_creator_id = Column(String, index=True)
    sys_modifier_id = Column(String, index=True)
    validated = Column(Numeric)
    validation_date = Column(DateTime)
    export = Column(Numeric)
    import_id = Column(Numeric, index=True)

    lu = relationship(u'LuHabitattypeCodes',
                      primaryjoin=(habitatcode ==
                                   foreign(LuHabitattypeCodes.code)),
                      uselist=False, lazy='eager')


class DataHabitatsCheckList(Base):
    __tablename__ = u'data_habitats_check_list'

    natura_2000_code = Column(String, primary_key=True, index=True)
    hd_name = Column(String)
    valid_name = Column(String)
    ms = Column(String, primary_key=True)
    bio_region = Column(String, primary_key=True)
    presence = Column(String)
    ms_feedback_etcbd_comments = Column(Text)
    ms_added = Column(Numeric)
    predefined = Column(Numeric)


class DataHabitattypeRegion(Base):
    __tablename__ = u'data_habitattype_reg'

    hr_id = Column('objectid', Numeric, primary_key=True)
    hr_habitat_id = Column(ForeignKey(DataHabitat.habitat_id), index=True)
    region = Column(String)
    published = Column(Text)
    range_surface_area = Column(Numeric)
    range_method = Column('range_method_used', String)
    range_trend_period = Column(String)
    range_trend = Column(String)
    range_trend_magnitude_min = Column('range_trend_mag_min', Numeric)
    range_trend_magnitude_max = Column('range_trend_mag_max', Numeric)
    range_trend_long_period = Column(String)
    range_trend_long = Column(String)
    range_trend_long_magnitude_min = Column('range_trend_long_mag_min', Numeric)
    range_trend_long_magnitude_max = Column('range_trend_long_mag_max', Numeric)
    complementary_favourable_range = Column('compl_favourable_range', Numeric)
    complementary_favourable_range_op = Column('comp_favourable_range_op', String)
    complementary_favourable_range_x = Column('comp_favourable_range_x', Numeric)
    complementary_favourable_range_method = Column('comp_favourable_range_met', Text)
    range_reasons_for_change_a = Column('r_reasons_for_change_a', Numeric)
    range_reasons_for_change_b = Column('r_reasons_for_change_b', Numeric)
    range_reasons_for_change_c = Column('r_reasons_for_change_c', Numeric)
    coverage_surface_area = Column(Numeric)
    coverage_date = Column(String)
    coverage_method = Column(String)
    coverage_trend_period = Column(String)
    coverage_trend = Column(String)
    coverage_trend_magnitude_min = Column('coverage_trend_mag_min', Numeric)
    coverage_trend_magnitude_max = Column('coverage_trend_mag_max', Numeric)
    coverage_trend_magnitude_ci = Column(Numeric)
    coverage_trend_method = Column(String)
    coverage_trend_long_period = Column(String)
    coverage_trend_long = Column(String)
    coverage_trend_long_magnitude_min = Column('coverage_trend_long_mag_min', Numeric)
    coverage_trend_long_magnitude_max = Column('coverage_trend_long_mag_max', Numeric)
    coverage_trend_long_magnitude_ci = Column('coverage_trend_long_mag_ci', Numeric)
    coverage_trend_long_method = Column(String)
    complementary_favourable_area = Column('comp_favourable_area', Numeric)
    complementary_favourable_area_op = Column('comp_favourable_area_op', String)
    complementary_favourable_area_x = Column('comp_favourable_area_x', Numeric)
    complementary_favourable_area_method = Column('comp_favourable_area_method', Text)
    area_reasons_for_change_a = Column(Numeric)
    area_reasons_for_change_b = Column(Numeric)
    area_reasons_for_change_c = Column(Numeric)
    pressures_method = Column(String)
    threats_method = Column(String)
    typical_species_method = Column(Text)
    justification = Column(Text)
    structure_and_functions_method = Column('structure_and_func_method', String)
    other_relevant_information = Column(Text)
    conclusion_range = Column(String)
    conclusion_range_trend = Column(String)
    conclusion_area = Column(String)
    conclusion_area_trend = Column(String)
    conclusion_structure = Column(String)
    conclusion_structure_trend = Column(String)
    conclusion_future = Column(String)
    conclusion_future_trend = Column(String)
    conclusion_assessment = Column(String)
    conclusion_assessment_trend = Column(String)
    natura2000_area_min = Column(Numeric)
    natura2000_area_max = Column(Numeric)
    natura2000_area_method = Column(String)
    natura2000_area_trend = Column(String)
    validated = Column(Numeric)
    validation_date = Column(DateTime)

    hr_habitat = relationship(u'DataHabitat',
        backref=db.backref('regions', lazy='dynamic'))

    lu = relationship(LuBiogeoreg,
                      primaryjoin=(region == foreign(LuBiogeoreg.code)),
                      innerjoin=True, uselist=False)


class DataHabitattypeComment(Base):
    __tablename__ = u'data_habitattype_comments'

    hr_id = Column('objectid', String, primary_key=True, index=True,
                               default=create_uuid)
    hr_habitat_id = Column(ForeignKey(DataHabitat.habitat_id), index=True)
    region = Column(String)
    published = Column(Text)
    range_surface_area = Column(Numeric)
    range_method = Column('range_method_used', String)
    range_trend_period = Column(String)
    range_trend = Column(String)
    range_trend_magnitude_min = Column('range_trend_mag_min', Numeric)
    range_trend_magnitude_max = Column('range_trend_mag_max', Numeric)
    range_trend_long_period = Column(String)
    range_trend_long = Column(String)
    range_trend_long_magnitude_min = Column('range_trend_long_mag_min', Numeric)
    range_trend_long_magnitude_max = Column('range_trend_long_mag_max', Numeric)
    complementary_favourable_range = Column('compl_favourable_range', Numeric)
    complementary_favourable_range_op = Column('comp_favourable_range_op', String)
    complementary_favourable_range_x = Column('comp_favourable_range_x', Numeric)
    complementary_favourable_range_method = Column('comp_favourable_range_met', Text)
    range_reasons_for_change_a = Column('r_reasons_for_change_a', Numeric)
    range_reasons_for_change_b = Column('r_reasons_for_change_b', Numeric)
    range_reasons_for_change_c = Column('r_reasons_for_change_c', Numeric)
    coverage_surface_area = Column(Numeric)
    coverage_date = Column(String)
    coverage_method = Column(String)
    coverage_trend_period = Column(String)
    coverage_trend = Column(String)
    coverage_trend_magnitude_min = Column('coverage_trend_mag_min', Numeric)
    coverage_trend_magnitude_max = Column('coverage_trend_mag_max', Numeric)
    coverage_trend_magnitude_ci = Column(Numeric)
    coverage_trend_method = Column(String)
    coverage_trend_long_period = Column(String)
    coverage_trend_long = Column(String)
    coverage_trend_long_magnitude_min = Column('coverage_trend_long_mag_min', Numeric)
    coverage_trend_long_magnitude_max = Column('coverage_trend_long_mag_max', Numeric)
    coverage_trend_long_magnitude_ci = Column('coverage_trend_long_mag_ci', Numeric)
    coverage_trend_long_method = Column(String)
    complementary_favourable_area = Column('comp_favourable_area', Numeric)
    complementary_favourable_area_op = Column('comp_favourable_area_op', String)
    complementary_favourable_area_x = Column('comp_favourable_area_x', Numeric)
    complementary_favourable_area_method = Column('comp_favourable_area_method', Text)
    area_reasons_for_change_a = Column(Numeric)
    area_reasons_for_change_b = Column(Numeric)
    area_reasons_for_change_c = Column(Numeric)
    pressures_method = Column(String)
    threats_method = Column(String)
    typical_species_method = Column(Text)
    justification = Column(Text)
    structure_and_functions_method = Column('structure_and_func_method', String)
    other_relevant_information = Column(Text)
    conclusion_range = Column(String)
    conclusion_range_trend = Column(String)
    conclusion_area = Column(String)
    conclusion_area_trend = Column(String)
    conclusion_structure = Column(String)
    conclusion_structure_trend = Column(String)
    conclusion_future = Column(String)
    conclusion_future_trend = Column(String)
    conclusion_assessment = Column(String)
    conclusion_assessment_trend = Column(String)
    natura2000_area_min = Column(Numeric)
    natura2000_area_max = Column(Numeric)
    natura2000_area_method = Column(String)
    natura2000_area_trend = Column(String)
    validated = Column(Numeric)
    validation_date = Column(DateTime)
    comment_date = Column(DateTime)

    user_id = Column(Text)

    hr_habitat = relationship(u'DataHabitat',
        backref=db.backref('comments', lazy='dynamic'))


class DataHtypicalSpecies(Base):
    __tablename__ = u'data_htypical_species'

    typical_species_id = Column(Numeric, primary_key=True)
    species_hr_id = Column(ForeignKey(DataHabitattypeRegion.hr_id), index=True)
    speciescode = Column(String, index=True)
    speciesname = Column(String)
    validated = Column(Numeric)
    validation_date = Column(DateTime)

    species_hr = relationship(u'DataHabitattypeRegion')


class DataNote(Base):
    __tablename__ = u'data_notes'

    notes_id = Column(Numeric, primary_key=True)
    entity_id = Column(Numeric, index=True)
    entity_table_name = Column(String)
    field_label = Column(String)
    note = Column(Text)
    username = Column(String)


class DataSpecies(Base):
    __tablename__ = u'data_species'

    species_id = Column('objectid', Numeric, primary_key=True, index=True)
    country = Column(String)
    speciescode = Column(String, index=True)
    alternative_speciesname = Column(String)
    common_speciesname = Column(String)
    distribution_map = Column(Numeric)
    sensitive_species = Column(Numeric)
    distribution_method = Column(String)
    distribution_date = Column(String)
    additional_distribution_map = Column(Numeric)
    range_map = Column(Numeric)
    validated = Column(Numeric)
    validation_date = Column(DateTime)
    sys_date_created = Column(DateTime)
    sys_date_modified = Column(DateTime)
    sys_date_imported = Column(DateTime)
    sys_creator_id = Column(String, index=True)
    sys_modifier_id = Column(String, index=True)
    export = Column(Numeric)
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

    natura_2000_code = Column(String, primary_key=True, index=True)
    eunis_code = Column(Numeric, index=True)
    hd_name = Column(String)
    species_name = Column(String)
    annex_ii = Column(String)
    annex_iv = Column(String)
    annex_v = Column(String)
    member_state = Column(String, primary_key=True)
    bio_region = Column(String, primary_key=True)
    presence = Column(String)
    comment = Column('comment_', Text)
    ms_added = Column(Numeric)
    predefined = Column(Numeric)


class DataSpeciesRegion(Base):
    __tablename__ = u'data_species_regions'

    sr_id = Column('objectid', Numeric, primary_key=True, index=True)
    sr_species_id = Column(ForeignKey(DataSpecies.species_id), index=True)
    region = Column(String)
    published = Column(Text)
    range_surface_area = Column('rsurface_area', Numeric)
    range_method = Column(String)
    range_trend_period = Column(String)
    range_trend = Column(String)
    range_trend_magnitude_min = Column('range_trend_mag_min', Numeric)
    range_trend_magnitude_max = Column('range_trend_mag_max', Numeric)
    range_trend_long_period = Column(String)
    range_trend_long = Column(String)
    range_trend_long_magnitude_min = Column('range_trend_long_mag_min', Numeric)
    range_trend_long_magnitude_max = Column('range_trend_long_mag_max', Numeric)
    complementary_favourable_range = Column('comp_favourable_range', Numeric)
    complementary_favourable_range_op = Column('comp_favourable_range_op', String)
    complementary_favourable_range_x = Column('comp_favourable_range_x', Numeric)
    complementary_favourable_range_method = Column('comp_favourable_range_met', Text)
    range_reasons_for_change_a = Column('r_reasons_for_change_a', Numeric)
    range_reasons_for_change_b = Column('r_reasons_for_change_b', Numeric)
    range_reasons_for_change_c = Column('r_reasons_for_change_c', Numeric)
    population_size_unit = Column('pop_size_unit', String)
    population_minimum_size = Column('pop_minimum_size', Numeric)
    population_maximum_size = Column('pop_maximum_size', Numeric)
    population_alt_size_unit = Column('pop_alt_size_unit', String)
    population_alt_minimum_size = Column('pop_alt_minimum_size', Numeric)
    population_alt_maximum_size = Column('pop_alt_maximum_size', Numeric)
    population_additional_locality = Column('pop_additional_locality', Text)
    population_additional_method = Column('pop_additional_method', Text)
    population_additional_problems = Column('pop_additional_problems', Text)
    population_date = Column('pop_date', String)
    population_method = Column('pop_method', String)
    population_trend_period = Column('pop_trend_period', String)
    population_trend = Column('pop_trend', String)
    population_trend_magnitude_min = Column('pop_trend_mag_min', Numeric)
    population_trend_magnitude_max = Column('pop_trend_mag_max', Numeric)
    population_trend_magnitude_ci = Column('pop_trend_magnitude_ci', Numeric)
    population_trend_method = Column('pop_trend_method', String)
    population_trend_long_period = Column('pop_trend_long_period', String)
    population_trend_long = Column(String)
    population_trend_long_magnitude_min = Column('pop_trend_long_mag_min', Numeric)
    population_trend_long_magnitude_max = Column('pop_trend_long_mag_max', Numeric)
    population_trend_long_magnitude_ci = Column('pop_trend_long_mag_ci', Numeric)
    population_trend_long_method = Column('pop_trend_long_method', String)
    complementary_favourable_population = Column('comp_favourable_pop', Numeric)
    complementary_favourable_population_op = Column('comp_favourable_pop_op', String)
    complementary_favourable_population_x = Column('comp_favourable_pop_x', Numeric)
    complementary_favourable_population_method = Column('comp_favourable_pop_met', Text)
    population_reasons_for_change_a = Column('pop_reasons_for_change_a', Numeric)
    population_reasons_for_change_b = Column('pop_reasons_for_change_b', Numeric)
    population_reasons_for_change_c = Column('pop_reasons_for_change_c', Numeric)
    habitat_surface_area = Column(Numeric)
    habitat_date = Column(String)
    habitat_method = Column(String)
    habitat_quality = Column(String)
    habitat_quality_explanation = Column(Text)
    habitat_trend_period = Column(String)
    habitat_trend = Column(String)
    habitat_trend_long_period = Column(String)
    habitat_trend_long = Column(String)
    habitat_area_suitable = Column(Numeric)
    habitat_reasons_for_change_a = Column('habitat_reasons_for_change__61', Numeric)
    habitat_reasons_for_change_b = Column('habitat_reasons_for_change__62', Numeric)
    habitat_reasons_for_change_c = Column('habitat_reasons_for_change__63', Numeric)
    pressures_method = Column(String)
    threats_method = Column(String)
    justification = Column(Text)
    other_relevant_information = Column(Text)
    transboundary_assessment = Column(Text)
    conclusion_range = Column(String)
    conclusion_range_trend = Column(String)
    conclusion_population = Column(String)
    conclusion_population_trend = Column(String)
    conclusion_habitat = Column(String)
    conclusion_habitat_trend = Column(String)
    conclusion_future = Column(String)
    conclusion_future_trend = Column('conclusion_future_trends', String)
    conclusion_assessment = Column(String)
    conclusion_assessment_trend = Column(String)
    natura2000_population_unit = Column(String)
    natura2000_population_min = Column(Numeric)
    natura2000_population_max = Column(Numeric)
    natura2000_population_method = Column('natura2000_population_metho_82', String)
    natura2000_population_trend = Column(String)
    validated = Column(Numeric)
    validation_date = Column(DateTime)

    sr_species = relationship(u'DataSpecies',
        backref=db.backref('regions', lazy='dynamic'))

    lu = relationship(LuBiogeoreg,
                      primaryjoin=(region == foreign(LuBiogeoreg.code)),
                      innerjoin=True, uselist=False)


class DataSpeciesComment(Base):
    __tablename__ = u'data_species_comments'

    sr_id = Column('objectid', String, primary_key=True, index=True,
                               default=create_uuid)
    sr_species_id = Column(ForeignKey(DataSpecies.species_id), index=True)
    region = Column(String)
    published = Column(Text)
    range_surface_area = Column('rsurface_area', Numeric)
    range_method = Column(String)
    range_trend_period = Column(String)
    range_trend = Column(String)
    range_trend_magnitude_min = Column('range_trend_mag_min', Numeric)
    range_trend_magnitude_max = Column('range_trend_mag_max', Numeric)
    range_trend_long_period = Column(String)
    range_trend_long = Column(String)
    range_trend_long_magnitude_min = Column('range_trend_long_mag_min', Numeric)
    range_trend_long_magnitude_max = Column('range_trend_long_mag_max', Numeric)
    complementary_favourable_range = Column('comp_favourable_range', Numeric)
    complementary_favourable_range_op = Column('comp_favourable_range_op', String)
    complementary_favourable_range_x = Column('comp_favourable_range_x', Numeric)
    complementary_favourable_range_method = Column('comp_favourable_range_met', Text)
    range_reasons_for_change_a = Column('r_reasons_for_change_a', Numeric)
    range_reasons_for_change_b = Column('r_reasons_for_change_b', Numeric)
    range_reasons_for_change_c = Column('r_reasons_for_change_c', Numeric)
    population_size_unit = Column('pop_size_unit', String)
    population_minimum_size = Column('pop_minimum_size', Numeric)
    population_maximum_size = Column('pop_maximum_size', Numeric)
    population_alt_size_unit = Column('pop_alt_size_unit', String)
    population_alt_minimum_size = Column('pop_alt_minimum_size', Numeric)
    population_alt_maximum_size = Column('pop_alt_maximum_size', Numeric)
    population_additional_locality = Column('pop_additional_locality', Text)
    population_additional_method = Column('pop_additional_method', Text)
    population_additional_problems = Column('pop_additional_problems', Text)
    population_date = Column('pop_date', String)
    population_method = Column('pop_method', String)
    population_trend_period = Column('pop_trend_period', String)
    population_trend = Column('pop_trend', String)
    population_trend_magnitude_min = Column('pop_trend_mag_min', Numeric)
    population_trend_magnitude_max = Column('pop_trend_mag_max', Numeric)
    population_trend_magnitude_ci = Column('pop_trend_magnitude_ci', Numeric)
    population_trend_method = Column('pop_trend_method', String)
    population_trend_long_period = Column('pop_trend_long_period', String)
    population_trend_long = Column(String)
    population_trend_long_magnitude_min = Column('pop_trend_long_mag_min', Numeric)
    population_trend_long_magnitude_max = Column('pop_trend_long_mag_max', Numeric)
    population_trend_long_magnitude_ci = Column('pop_trend_long_mag_ci', Numeric)
    population_trend_long_method = Column('pop_trend_long_method', String)
    complementary_favourable_population = Column('comp_favourable_pop', Numeric)
    complementary_favourable_population_op = Column('comp_favourable_pop_op', String)
    complementary_favourable_population_x = Column('comp_favourable_pop_x', Numeric)
    complementary_favourable_population_method = Column('comp_favourable_pop_met', Text)
    population_reasons_for_change_a = Column('pop_reasons_for_change_a', Numeric)
    population_reasons_for_change_b = Column('pop_reasons_for_change_b', Numeric)
    population_reasons_for_change_c = Column('pop_reasons_for_change_c', Numeric)
    habitat_surface_area = Column(Numeric)
    habitat_date = Column(String)
    habitat_method = Column(String)
    habitat_quality = Column(String)
    habitat_quality_explanation = Column(Text)
    habitat_trend_period = Column(String)
    habitat_trend = Column(String)
    habitat_trend_long_period = Column(String)
    habitat_trend_long = Column(String)
    habitat_area_suitable = Column(Numeric)
    habitat_reasons_for_change_a = Column('habitat_reasons_for_change__61', Numeric)
    habitat_reasons_for_change_b = Column('habitat_reasons_for_change__62', Numeric)
    habitat_reasons_for_change_c = Column('habitat_reasons_for_change__63', Numeric)
    pressures_method = Column(String)
    threats_method = Column(String)
    justification = Column(Text)
    other_relevant_information = Column(Text)
    transboundary_assessment = Column(Text)
    conclusion_range = Column(String)
    conclusion_range_trend = Column(String)
    conclusion_population = Column(String)
    conclusion_population_trend = Column(String)
    conclusion_habitat = Column(String)
    conclusion_habitat_trend = Column(String)
    conclusion_future = Column(String)
    conclusion_future_trend = Column('conclusion_future_trends', String)
    conclusion_assessment = Column(String)
    conclusion_assessment_trend = Column(String)
    natura2000_population_unit = Column(String)
    natura2000_population_min = Column(Numeric)
    natura2000_population_max = Column(Numeric)
    natura2000_population_method = Column('natura2000_population_metho_82', String)
    natura2000_population_trend = Column(String)
    validated = Column(Numeric)
    validation_date = Column(DateTime)
    comment_date = Column(DateTime)

    user_id = Column(Text)

    sr_species = relationship(u'DataSpecies',
        backref=db.backref('comments', lazy='dynamic'))


class DataPressuresThreat(Base):
    __tablename__ = u'data_pressures_threats'

    pressure_id = Column(Numeric, primary_key=True)
    pressure_hr_id = Column(ForeignKey(DataHabitattypeRegion.hr_id), index=True)
    pressure_sr_id = Column(ForeignKey(DataSpeciesRegion.sr_id), index=True)
    pressure = Column(String)
    ranking = Column(String)
    type = Column(String)
    validated = Column(Numeric)
    validation_Date = Column(DateTime)

    pressure_hr = relationship(u'DataHabitattypeRegion')
    pressure_sr = relationship(u'DataSpeciesRegion')


class DataPressuresThreatsPol(Base):
    __tablename__ = u'data_pressures_threats_pol'

    pollution_id = Column(Numeric, primary_key=True)
    pollution_pressure_id = Column(ForeignKey(DataPressuresThreat.pressure_id), index=True)
    pollution_qualifier = Column(String)
    validated = Column(Numeric)
    validation_date = Column(DateTime)

    pollution_pressure = relationship(u'DataPressuresThreat')


class DataMeasure(Base):
    __tablename__ = u'data_measures'

    measure_id = Column(Numeric, primary_key=True)
    measurecode = Column(String, index=True)
    measure_sr_id = Column(ForeignKey(DataSpeciesRegion.sr_id), index=True)
    measure_hr_id = Column(ForeignKey(DataHabitattypeRegion.hr_id), index=True)
    type_legal = Column(Numeric)
    type_administrative = Column(Numeric)
    type_contractual = Column(Numeric)
    type_recurrent = Column(Numeric)
    type_oneoff = Column(Numeric)
    rankingcode = Column(String, index=True)
    location_inside = Column(Numeric)
    location_outside = Column(Numeric)
    location_both = Column(Numeric)
    broad_evaluation_maintain = Column(Numeric)
    broad_evaluation_enhance = Column(Numeric)
    broad_evaluation_longterm = Column(Numeric)
    broad_evaluation_noeffect = Column(Numeric)
    broad_evaluation_unknown = Column(Numeric)
    broad_evaluation_notevaluated = Column(Numeric)
    validated = Column(Numeric)
    validation_date = Column(DateTime)

    measure_hr = relationship(u'DataHabitattypeRegion')
    measure_sr = relationship(u'DataSpeciesRegion')


class SysImport(Base):
    __tablename__ = u'sys_import'

    import_id = Column(Numeric, primary_key=True)
    report_type = Column(String)
    filename = Column(String)
    nof_records_imported = Column(Numeric)
    nof_records_failed = Column(Numeric)
    log = Column(Text)
    import_time = Column(DateTime)


t_sys_info_be = Table(
    u'sys_info_be', metadata,
    Column(u'version_be', String),
    Column(u'multi_user_instance', Numeric),
    Column(u'habitats_imported', Numeric),
    Column(u'species_imported', Numeric)
)


class SysUser(Base):
    __tablename__ = u'sys_user'

    user_name = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    contactInfo = Column(String)
    email = Column(String)
    role = Column(String)
    general_report = Column(Numeric)
    species_report = Column(Numeric)
    habitats_report = Column(Numeric)
    using_fe_version = Column(Numeric)


@db_manager.option('alembic_args', nargs=argparse.REMAINDER)
def alembic(alembic_args):
    from alembic.config import CommandLine
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logging.getLogger('alembic').setLevel(logging.INFO)
    CommandLine().main(argv=alembic_args)


@db_manager.command
def revision(message=None):
    if message is None:
        message = raw_input('revision name: ')
    return alembic(['revision', '-m', message])


@db_manager.command
def upgrade(revision='head'):
    return alembic(['upgrade', revision])


@db_manager.command
def downgrade(revision):
    return alembic(['downgrade', revision])
