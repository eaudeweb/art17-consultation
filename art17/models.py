import uuid
import argparse
import logging
from sqlalchemy import (Column, DateTime, ForeignKey, Index, func,
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
    name_ro = Column('hd_name_ro', Text)
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
    code = Column('speciescode', Numeric)
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


class DataHabitat(Base):
    __tablename__ = u'data_habitats'

    id = Column('objectid', Numeric, primary_key=True)
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

    id = Column('objectid', Numeric, primary_key=True)
    habitat_id = Column('hr_habitat_id', ForeignKey(DataHabitat.id), index=True)
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

    id = Column('objectid', String, primary_key=True, default=create_uuid)
    habitat_id = Column('hr_habitat_id', ForeignKey(DataHabitat.id), index=True)
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
    user_id = Column(String)
    status = Column(Text, default='new')

    hr_habitat = relationship(u'DataHabitat',
        backref=db.backref('comments', lazy='dynamic'))


class DataSpecies(Base):
    __tablename__ = u'data_species'

    id = Column('objectid', Numeric, primary_key=True, index=True)
    country = Column(String)
    code = Column('speciescode', String, index=True)
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
                      primaryjoin=(code == cast(foreign(LuHdSpecies.code),
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

    id = Column('objectid', Numeric, primary_key=True, index=True)
    species_id = Column('sr_species_id', ForeignKey(DataSpecies.id), index=True)
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

    species = relationship(u'DataSpecies',
        backref=db.backref('regions', lazy='dynamic'))

    lu = relationship(LuBiogeoreg,
                      primaryjoin=(region == foreign(LuBiogeoreg.code)),
                      innerjoin=True, uselist=False)


class DataSpeciesComment(Base):
    __tablename__ = u'data_species_comments'

    id = Column('objectid', String, primary_key=True, default=create_uuid)
    species_id = Column('sr_species_id', ForeignKey(DataSpecies.id), index=True)
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
    user_id = Column(String)
    status = Column(Text, default='new')

    species = relationship(u'DataSpecies',
        backref=db.backref('comments', lazy='dynamic'))


class CommentMessage(Base):
    __tablename__ = u'comment_messages'

    id = Column('objectid', String, primary_key=True, default=create_uuid)
    parent = Column(String)
    user_id = Column(String)
    date = Column(DateTime)
    text = Column(Text)


class CommentMessageRead(Base):
    __tablename__ = u'comment_messages_read'

    id = Column('objectid', String, primary_key=True, default=create_uuid)
    message_id = Column(String, ForeignKey(CommentMessage.id))
    user_id = Column(String)


class History(Base):
    __tablename__ = u'history'

    id = Column('objectid', String, primary_key=True, default=create_uuid)
    table = Column(String)
    object_id = Column(String)
    action = Column(String)
    date = Column(DateTime)
    user_id = Column(String)
    old_data = Column(Text)
    new_data = Column(Text)


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
