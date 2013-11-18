import uuid
import argparse
import logging
from sqlalchemy import (Column, DateTime, ForeignKey, Index, func,
                        String, Table, Text, Numeric, cast, Binary,
                        Boolean, Integer, Sequence)
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

    objectid = Column(Integer, Sequence('R679'), primary_key=True)
    code = Column(String)
    hd_name = Column(String)
    name_ro = Column('hd_name_ro', Text)
    valide_name = Column(String)
    priority = Column(Numeric)
    priority_comment = Column(String)

    @property
    def display_name(self):
        return self.name_ro


class LuGrupSpecie(Base):
    __tablename__ = u'lu_grup_specie'

    oid = Column(Integer, primary_key=True)
    code = Column(String)
    description = Column(String)


class LuHdSpecies(Base):
    __tablename__ = u'lu_hd_species'

    objectid = Column(Integer, Sequence('R680'), primary_key=True)
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

    @property
    def display_name(self):
        return self.speciesname


class LuBiogeoreg(Base):
    __tablename__ = u'lu_biogeoreg'

    objectid = Column(Integer, Sequence('R675'), primary_key=True)
    code = Column(String)
    name = Column(String)
    name_ro = Column('nume', String)
    order = Column('order_', Numeric)


class LuThreats(Base):
    __tablename__ = u'lu_threats'

    objectid = Column(Integer, Sequence('R692'), primary_key=True)
    code = Column(String)
    name = Column(String)
    note = Column(String)
    eutroph = Column(String)
    valid_entry = Column(String)


class LuRanking(Base):
    __tablename__ = u'lu_ranking'

    objectid = Column(Integer, Sequence('R690'), primary_key=True)
    code = Column(String)
    name = Column(String)
    note = Column(String)
    order_ = Column(Integer)


class LuPollution(Base):
    __tablename__ = u'lu_pollution'

    objectid = Column(Integer, Sequence('R685'), primary_key=True)
    code = Column(String)
    name = Column(String)


class LuMeasures(Base):
    __tablename__ = u'lu_measures'

    objectid = Column(Integer, Sequence('R681'), primary_key=True)
    code = Column(String)
    name = Column(String)
    valid_entry = Column(String)


class LuPresence(Base):
    __tablename__ = u'lu_presence'

    objectid = Column(Integer, Sequence('R688'), primary_key=True)
    code = Column(String)
    name = Column(String)
    order_ = Column(Integer)
    reporting = Column(String)
    habitat_reporting = Column(String)
    species_reporting = Column(String)
    bird_reporting = Column(String)


class DataHabitat(Base):
    __tablename__ = u'data_habitats'

    id = Column('objectid', Integer, Sequence('R661'), primary_key=True)
    country = Column(String)
    code = Column('habitatcode', String)
    distribution_map = Column(Integer)
    distribution_method = Column(String)
    distribution_date = Column(String)
    additional_distribution_map = Column(Integer)
    range_map = Column(Integer)
    sys_date_created = Column(DateTime)
    sys_date_modified = Column(DateTime)
    sys_date_imported = Column(DateTime)
    sys_creator_id = Column(String)
    sys_modifier_id = Column(String)
    validated = Column(Integer)
    validation_date = Column(DateTime)
    export = Column(Integer)
    import_id = Column(Integer)

    lu = relationship(u'LuHabitattypeCodes',
                      primaryjoin=(code == foreign(LuHabitattypeCodes.code)),
                      uselist=False, lazy='eager')


class DataHabitatsCheckList(Base):
    __tablename__ = u'data_habitats_check_list'

    objectid = Column(Integer, Sequence('R662'), primary_key=True)
    natura_2000_code = Column(String)
    hd_name = Column(String)
    valid_name = Column(String)
    ms = Column(String)
    bio_region = Column(String)
    presence = Column(String)
    ms_feedback_etcbd_comments = Column(Text)
    ms_added = Column(Integer)
    predefined = Column(Integer)


class DataHabitattypeRegion(Base):
    __tablename__ = u'data_habitattype_reg'

    id = Column('objectid', Integer, Sequence('R663'), primary_key=True)
    habitat_id = Column('hr_habitat_id', ForeignKey(DataHabitat.id))
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
    validated = Column(Integer)
    validation_date = Column(DateTime)

    cons_role = Column(String)
    cons_date = Column(DateTime)
    cons_user_id = Column(String)
    cons_status = Column(String, default='new')
    cons_deleted = Column(Boolean, default=False)
    cons_report_observation = Column(Text)

    habitat = relationship(u'DataHabitat',
        backref=db.backref('regions', lazy='dynamic'))

    lu = relationship(LuBiogeoreg,
                      primaryjoin=(region == foreign(LuBiogeoreg.code)),
                      innerjoin=True, uselist=False)

    @property
    def identifier(self):
        return 'habitat:%s' % (self.habitat.lu.code,)


class DataSpecies(Base):
    __tablename__ = u'data_species'

    id = Column('objectid', Integer, Sequence('R669'), primary_key=True)
    country = Column(String)
    code = Column('speciescode', String)
    alternative_speciesname = Column(String)
    common_speciesname = Column(String)
    distribution_map = Column(Integer)
    sensitive_species = Column(Integer)
    distribution_method = Column(String)
    distribution_date = Column(String)
    additional_distribution_map = Column(Integer)
    range_map = Column(Integer)
    validated = Column(Integer)
    validation_date = Column(DateTime)
    sys_date_created = Column(DateTime)
    sys_date_modified = Column(DateTime)
    sys_date_imported = Column(DateTime)
    sys_creator_id = Column(String)
    sys_modifier_id = Column(String)
    export = Column(Integer)
    import_id = Column(Integer)

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

    objectid = Column(Integer, Sequence('R670'), primary_key=True)
    natura_2000_code = Column(String)
    eunis_code = Column(Integer)
    hd_name = Column(String)
    species_name = Column(String)
    annex_ii = Column(String)
    annex_iv = Column(String)
    annex_v = Column(String)
    member_state = Column(String)
    bio_region = Column(String)
    presence = Column(String)
    comment = Column('comment_', Text)
    ms_added = Column(Integer)
    predefined = Column(Integer)


class DataSpeciesRegion(Base):
    __tablename__ = u'data_species_regions'

    id = Column('objectid', Integer, Sequence('R671'), primary_key=True)
    species_id = Column('sr_species_id', ForeignKey(DataSpecies.id))
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
    validated = Column(Integer)
    validation_date = Column(DateTime)

    cons_role = Column(String)
    cons_date = Column(DateTime)
    cons_user_id = Column(String)
    cons_status = Column(String, default='new')
    cons_deleted = Column(Boolean, default=False)
    cons_report_observation = Column(Text)
    cons_generalstatus = Column(String)

    species = relationship(u'DataSpecies',
        backref=db.backref('regions', lazy='dynamic'))

    lu = relationship(LuBiogeoreg,
                      primaryjoin=(region == foreign(LuBiogeoreg.code)),
                      innerjoin=True, uselist=False)

    @property
    def identifier(self):
        return 'species:%s:%s' % (
            self.species.lu.group_code,
            int(self.species.lu.code),
        )


class DataMeasures(Base):
    __tablename__ = u'data_measures'

    id = Column('objectid', Integer, Sequence('R665'), primary_key=True)
    measurecode = Column(String)
    measure_sr_id = Column(Numeric, ForeignKey(DataSpeciesRegion.id))
    measure_hr_id = Column(Numeric, ForeignKey(DataHabitattypeRegion.id))
    type_legal = Column(Numeric)
    type_administrative = Column(Numeric)
    type_contractual = Column(Numeric)
    type_recurrent = Column(Numeric)
    type_oneoff = Column(Numeric)
    rankingcode = Column(String)
    location_inside = Column(Numeric)
    location_outside = Column(Numeric)
    location_both = Column(Numeric)
    broad_evaluation_maintain = Column(Numeric)
    broad_evaluation_enhance = Column(Numeric)
    broad_evaluation_longterm = Column(Numeric)
    broad_evaluation_noeffect = Column(Numeric)
    broad_evaluation_unknown = Column(Numeric)
    broad_evaluation_notevaluat_18 = Column(Numeric)
    validated = Column(Integer)
    validation_date = Column(DateTime)

    species = relationship(u'DataSpeciesRegion',
        backref=db.backref('measures', lazy='dynamic'))

    habitat = relationship(u'DataHabitattypeRegion',
        backref=db.backref('measures', lazy='dynamic'))

    lu = relationship(LuMeasures,
                      primaryjoin=(measurecode == foreign(LuMeasures.code)),
                      innerjoin=True, uselist=False)

    lu_ranking = relationship(LuRanking,
                      primaryjoin=(rankingcode == foreign(LuRanking.code)),
                      innerjoin=True, uselist=False)


class DataPressuresThreats(Base):
    __tablename__ = u'data_pressures_threats'

    id = Column('objectid', Integer, Sequence('R667'), primary_key=True)
    habitat_id = Column('pressure_hr_id', Integer,
                        ForeignKey(DataHabitattypeRegion.id))
    species_id = Column('pressure_sr_id', Integer,
                        ForeignKey(DataSpeciesRegion.id))
    pressure = Column(String)
    ranking = Column(String)
    type = Column(String)
    validated = Column(Integer)
    validation_date = Column(DateTime)

    species = relationship(u'DataSpeciesRegion',
        backref=db.backref('pressures', lazy='dynamic'))

    habitat = relationship(u'DataHabitattypeRegion',
        backref=db.backref('pressures', lazy='dynamic'))

    lu = relationship(LuThreats,
                      primaryjoin=(pressure == foreign(LuThreats.code)),
                      innerjoin=True, uselist=False)

    lu_ranking = relationship(LuRanking,
                      primaryjoin=(ranking == foreign(LuRanking.code)),
                      innerjoin=True, uselist=False)


class DataPressuresThreatsPollution(Base):
    __tablename__ = u'data_pressures_threats_pol'

    id = Column('objectid', Integer, Sequence('R668'), primary_key=True)
    pollution_pressure_id = Column(Integer, ForeignKey(DataPressuresThreats.id))
    pollution_qualifier = Column(String)
    validated = Column(Integer)
    validation_date = Column(DateTime)

    lu = relationship(LuPollution,
            primaryjoin=(pollution_qualifier == foreign(LuPollution.code)),
            innerjoin=True, uselist=False)

    pressure = relationship(u'DataPressuresThreats',
        backref=db.backref('pollutions', lazy='dynamic', cascade='all'))


class DataHabitatSpecies(Base):
    __tablename__ = u'data_htypical_species'

    id = Column('objectid', Integer, Sequence('R664'), primary_key=True)
    habitat_id = Column('species_hr_id', Integer,
                        ForeignKey(DataHabitattypeRegion.id))
    species_id = Column('speciescode', Integer,
                        ForeignKey(DataSpecies.id))
    speciesname = Column(String)
    validated = Column(Integer)
    validation_date = Column(DateTime)

    habitats = relationship(u'DataHabitattypeRegion',
        backref=db.backref('species', lazy='dynamic'))


class CommentReply(Base):
    __tablename__ = u'comment_replies'

    id = Column('objectid', String, primary_key=True, default=create_uuid)
    parent_table = Column(String)
    parent_id = Column(String)
    user_id = Column(String)
    date = Column(DateTime)
    text = Column(Text)


class CommentReplyRead(Base):
    __tablename__ = u'comment_replies_read'

    id = Column('objectid', String, primary_key=True, default=create_uuid)
    reply_id = Column('reply_id', String, ForeignKey(CommentReply.id))
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


class NotificationUser(Base):
    __tablename__ = u'notification_user'

    id = Column('objectid', String, primary_key=True, default=create_uuid)
    email = Column(String)
    full_name = Column(String)


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
