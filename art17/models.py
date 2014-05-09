import uuid
import argparse
import logging
from sqlalchemy import (Column, DateTime, ForeignKey, Index, func,
                        String, Table, Text, Numeric, cast, Binary,
                        Boolean, Integer, Sequence)
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from art17.table_sequences import get_sequence_id

db = SQLAlchemy()
Base = db.Model
metadata = db.metadata

db_manager = Manager()


def create_uuid():
    return str(uuid.uuid4()).replace('-', '')


def create_esri_guid():
    return ('{%s}' % uuid.uuid4()).upper()


class LuHabitattypeCodes(Base):
    __tablename__ = u'lu_habitattype_codes'

    objectid = Column(
        Integer,
        Sequence(get_sequence_id('lu_habitattype_codes')),
        primary_key=True,
    )
    code = Column(String)
    hd_name = Column(String)
    name_ro = Column('hd_name_ro', Text)
    valide_name = Column(String)
    priority = Column(Numeric)
    priority_comment = Column(String)
    globalid = Column(String, default=create_esri_guid)

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

    objectid = Column(
       Integer,
       Sequence(get_sequence_id('lu_hd_species')),
       primary_key=True,
    )
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
    globalid = Column(String, default=create_esri_guid)

    @property
    def display_name(self):
        return self.speciesname


class LuBiogeoreg(Base):
    __tablename__ = u'lu_biogeoreg'

    objectid = Column(
        Integer,
        Sequence(get_sequence_id('lu_biogeoreg')),
        primary_key=True,
    )
    code = Column(String)
    name = Column(String)
    name_ro = Column('nume', String)
    order = Column('order_', Numeric)
    globalid = Column(String, default=create_esri_guid)


class LuThreats(Base):
    __tablename__ = u'lu_threats'

    objectid = Column(
        Integer,
        Sequence(get_sequence_id('lu_threats')),
        primary_key=True,
    )
    code = Column(String)
    name = Column(String)
    name_ro = Column(Text)
    note = Column(String)
    eutroph = Column(String)
    valid_entry = Column(String)
    globalid = Column(String, default=create_esri_guid)


class LuRanking(Base):
    __tablename__ = u'lu_ranking'

    objectid = Column(
        Integer,
        Sequence(get_sequence_id('lu_ranking')),
        primary_key=True,
    )
    code = Column(String)
    name = Column(String)
    name_ro = Column(String)
    note = Column(String)
    order_ = Column(Integer)
    globalid = Column(String, default=create_esri_guid)


class LuPopulation(Base):
    __tablename__ = u'lu_population_number'

    objectid = Column(
        Integer,
        Sequence(get_sequence_id('lu_population_number')),
        primary_key=True,
    )
    code = Column(String)
    name = Column(String)
    name_ro = Column(String)
    order_ = Column(Integer)
    globalid = Column(String, default=create_esri_guid)


class LuPopulationRestricted(Base):
    __tablename__ = u'lu_population_units_restricted'

    objectid = Column(
        Integer,
        Sequence(get_sequence_id('lu_population_units_restricted')),
        primary_key=True,
    )
    code = Column(String)
    name = Column(String)
    name_ro = Column(String)
    order_ = Column(Integer)
    globalid = Column(String, default=create_esri_guid)


class LuPollution(Base):
    __tablename__ = u'lu_pollution'

    objectid = Column(
        Integer,
        Sequence(get_sequence_id('lu_pollution')),
        primary_key=True,
    )
    code = Column(String)
    name = Column(String)
    name_ro = Column(String)
    globalid = Column(String, default=create_esri_guid)


class LuMeasures(Base):
    __tablename__ = u'lu_measures'

    objectid = Column(
        Integer,
        Sequence(get_sequence_id('lu_measures')),
        primary_key=True,
    )
    code = Column(String)
    name = Column(String)
    name_ro = Column(String)
    valid_entry = Column(String)
    globalid = Column(String, default=create_esri_guid)


class LuPresence(Base):
    __tablename__ = u'lu_presence'

    objectid = Column(
        Integer,
        Sequence(get_sequence_id('lu_presence')),
        primary_key=True,
    )
    code = Column(String)
    name = Column(String)
    name_ro = Column(String)
    order_ = Column(Integer)
    reporting = Column(String)
    habitat_reporting = Column(String)
    species_reporting = Column(String)
    bird_reporting = Column(String)
    globalid = Column(String, default=create_esri_guid)


class LuMethods(Base):
    __tablename__ = u'lu_methods_used'

    objectid = Column(
        Integer,
        Sequence(get_sequence_id('lu_methods_used')),
        primary_key=True,
    )
    code = Column(String)
    name = Column(String)
    order = Column('order_', Numeric)
    str_funct = Column(String)
    globalid = Column(String, default=create_esri_guid)


class DataHabitat(Base):
    __tablename__ = u'data_habitats'

    id = Column(
        'objectid',
        Integer,
        Sequence(get_sequence_id('data_habitats')),
        primary_key=True,
    )
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
    globalid = Column(String, default=create_esri_guid)

    lu = relationship(u'LuHabitattypeCodes',
                      primaryjoin=(code == foreign(LuHabitattypeCodes.code)),
                      uselist=False, lazy='eager')

    @property
    def identifier(self):
        return 'habitat:%s' % (self.lu.code,)

    @property
    def checklist(self):
        return (
            DataHabitatsCheckList.query
            .filter_by(dataset_id=None, code=self.code, member_state='RO')
            .first()
        )


class DataHabitatsCheckList(Base):
    __tablename__ = u'data_habitats_check_list'

    objectid = Column(
        Integer,
        Sequence(get_sequence_id('data_habitats_check_list')),
        primary_key=True,
    )
    natura_2000_code = Column(String)
    hd_name = Column(String)
    valid_name = Column(String)
    member_state = Column('ms', String)
    bio_region = Column(String)
    presence = Column(String)
    ms_feedback_etcbd_comments = Column(Text)
    ms_added = Column(Integer)
    predefined = Column(Integer)
    globalid = Column(String, default=create_esri_guid)
    dataset_id = Column(ForeignKey('datasets.objectid'), nullable=True)

    dataset = relationship('Dataset', backref='habitat_checklist')

    @hybrid_property
    def code(self):
        return self.natura_2000_code

    @code.setter
    def code(self, value):
        self.natura_2000_code = value

    @hybrid_property
    def name(self):
        return self.valid_name

    @name.setter
    def name(self, value):
        self.valid_name = value


class DataHabitattypeRegion(Base):
    __tablename__ = u'data_habitattype_reg'

    id = Column(
        'objectid',
        Integer,
        Sequence(get_sequence_id('data_habitattype_reg')),
        primary_key=True,
    )
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
    complementary_favourable_range_unknown = Column('comp_favourable_range_x', Numeric)
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
    complementary_favourable_area_unknown = Column('comp_favourable_area_x', Numeric)
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
    cons_dataset_id = Column(ForeignKey('datasets.objectid'))
    globalid = Column(String, default=create_esri_guid)

    habitat = relationship(u'DataHabitat',
        backref=db.backref('regions', lazy='dynamic'))

    lu = relationship(LuBiogeoreg,
                      primaryjoin=(region == foreign(LuBiogeoreg.code)),
                      innerjoin=True, uselist=False, passive_deletes=True)

    dataset = relationship('Dataset',
        backref=db.backref('habitat_objs', lazy='dynamic'))

    def get_pressures(self):
        return self.pressures.filter_by(type='p')

    def get_threats(self):
        return self.pressures.filter_by(type='t')

    @hybrid_property
    def subject_id(self):
        return self.habitat_id

    @subject_id.setter
    def subject_id(self, value):
        self.habitat_id = value

    @property
    def subject(self):
        return self.habitat

    @property
    def subject_identifier(self):
        return self.habitat.identifier


class DataSpecies(Base):
    __tablename__ = u'data_species'

    id = Column(
        'objectid',
        Integer,
        Sequence(get_sequence_id('data_species')),
        primary_key=True,
    )
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
    globalid = Column(String, default=create_esri_guid)

    lu = relationship(LuHdSpecies,
                      primaryjoin=(code == cast(foreign(LuHdSpecies.code),
                                                String(255))),
                      lazy='joined', innerjoin=True, uselist=False,
                      backref=db.backref('data',
                                         lazy='joined',
                                         uselist=False,
                                         innerjoin=True))

    @property
    def identifier(self):
        return 'species:%s:%s' % (self.lu.group_code, int(self.lu.code))

    @hybrid_property
    def name(self):
        return self.common_speciesname

    @property
    def checklist(self):
        return (
            DataSpeciesCheckList.query
            .filter_by(dataset_id=None, code=self.code, member_state='RO')
            .first()
        )


class DataSpeciesCheckList(Base):
    __tablename__ = u'data_species_check_list'

    objectid = Column(
        Integer,
        Sequence(get_sequence_id('data_species_check_list')),
        primary_key=True,
    )
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
    globalid = Column(String, default=create_esri_guid)
    dataset_id = Column(ForeignKey('datasets.objectid'), nullable=True)

    dataset = relationship('Dataset', backref='species_checklist')

    @hybrid_property
    def code(self):
        return self.natura_2000_code

    @code.setter
    def code(self, value):
        self.natura_2000_code = value

    @hybrid_property
    def name(self):
        return self.species_name

    @name.setter
    def name(self, value):
        self.species_name = value


class DataSpeciesRegion(Base):
    __tablename__ = u'data_species_regions'

    id = Column(
        'objectid',
        Integer,
        Sequence(get_sequence_id('data_species_regions')),
        primary_key=True,
    )
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
    complementary_favourable_range_unknown = Column('comp_favourable_range_x', Numeric)
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
    complementary_favourable_population_unknown = Column('comp_favourable_pop_x', Numeric)
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
    globalid = Column(String, default=create_esri_guid)

    cons_role = Column(String)
    cons_date = Column(DateTime)
    cons_user_id = Column(String)
    cons_status = Column(String, default='new')
    cons_deleted = Column(Boolean, default=False)
    cons_report_observation = Column(Text)
    cons_generalstatus = Column(String)
    cons_dataset_id = Column(ForeignKey('datasets.objectid'))

    species = relationship(u'DataSpecies',
        backref=db.backref('regions', lazy='dynamic'))

    lu = relationship(LuBiogeoreg,
                      primaryjoin=(region == foreign(LuBiogeoreg.code)),
                      innerjoin=True, uselist=False, passive_deletes=True)

    dataset = relationship('Dataset',
        backref=db.backref('species_objs', lazy='dynamic'))

    def get_pressures(self):
        return self.pressures.filter_by(type='p')

    def get_threats(self):
        return self.pressures.filter_by(type='t')

    @hybrid_property
    def subject_id(self):
        return self.species_id

    @subject_id.setter
    def subject_id(self, value):
        self.species_id = value

    @property
    def subject(self):
        return self.species

    @property
    def subject_identifier(self):
        return self.species.identifier

    @hybrid_property
    def conclusion_future_trends(self):
        return self.conclusion_future_trend

    @conclusion_future_trends.setter
    def conclusion_future_trends(self, value):
        self.conclusion_future_trend = value


class DataMeasures(Base):
    __tablename__ = u'data_measures'

    id = Column(
        'objectid',
        Integer,
        Sequence(get_sequence_id('data_measures')),
        primary_key=True,
    )
    measurecode = Column(String)
    species_id = Column('measure_sr_id', Numeric, ForeignKey(DataSpeciesRegion.id))
    habitat_id = Column('measure_hr_id', Numeric, ForeignKey(DataHabitattypeRegion.id))
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
    broad_evaluation_notevaluated = Column('broad_evaluation_notevaluat_18', Numeric)
    validated = Column(Integer)
    validation_date = Column(DateTime)
    globalid = Column(String, default=create_esri_guid)

    species = relationship(u'DataSpeciesRegion',
        backref=db.backref('measures', lazy='dynamic'))

    habitat = relationship(u'DataHabitattypeRegion',
        backref=db.backref('measures', lazy='dynamic'))

    lu = relationship(LuMeasures,
                      primaryjoin=(measurecode == foreign(LuMeasures.code)),
                      innerjoin=True, uselist=False, passive_deletes=True)

    lu_ranking = relationship(LuRanking,
                      primaryjoin=(rankingcode == foreign(LuRanking.code)),
                      innerjoin=True, uselist=False, passive_deletes=True)

    @hybrid_property
    def ranking(self):
        return self.rankingcode

    @ranking.setter
    def ranking(self, value):
        self.rankingcode = value

    @hybrid_property
    def code(self):
        return self.measurecode

    @code.setter
    def code(self, value):
        self.measurecode = value


class DataPressuresThreats(Base):
    __tablename__ = u'data_pressures_threats'

    id = Column(
        'objectid',
        Integer,
        Sequence(get_sequence_id('data_pressures_threats')),
        primary_key=True,
    )
    habitat_id = Column('pressure_hr_id', Integer,
                        ForeignKey(DataHabitattypeRegion.id))
    species_id = Column('pressure_sr_id', Integer,
                        ForeignKey(DataSpeciesRegion.id))
    pressure = Column(String)
    ranking = Column(String)
    type = Column(String)
    validated = Column(Integer)
    validation_date = Column(DateTime)
    globalid = Column(String, default=create_esri_guid)

    species = relationship(u'DataSpeciesRegion',
        backref=db.backref('pressures', lazy='dynamic'))

    habitat = relationship(u'DataHabitattypeRegion',
        backref=db.backref('pressures', lazy='dynamic'))

    lu = relationship(LuThreats,
                      primaryjoin=(pressure == foreign(LuThreats.code)),
                      innerjoin=True, uselist=False, passive_deletes=True)

    lu_ranking = relationship(LuRanking,
                      primaryjoin=(ranking == foreign(LuRanking.code)),
                      innerjoin=True, uselist=False, passive_deletes=True)


class DataPressuresThreatsPollution(Base):
    __tablename__ = u'data_pressures_threats_pol'

    id = Column(
        'objectid',
        Integer,
        Sequence(get_sequence_id('data_pressures_threats_pol')),
        primary_key=True,
    )
    pollution_pressure_id = Column(Integer, ForeignKey(DataPressuresThreats.id))
    pollution_qualifier = Column(String)
    validated = Column(Integer)
    validation_date = Column(DateTime)
    globalid = Column(String, default=create_esri_guid)

    lu = relationship(LuPollution,
            primaryjoin=(pollution_qualifier == foreign(LuPollution.code)),
            innerjoin=True, uselist=False, passive_deletes=True)

    pressure = relationship(u'DataPressuresThreats',
        backref=db.backref('pollutions', lazy='dynamic', cascade='all'))


class DataHabitatSpecies(Base):
    __tablename__ = u'data_htypical_species'

    id = Column(
        'objectid',
        Integer,
        Sequence(get_sequence_id('data_htypical_species')),
        primary_key=True,
    )
    habitat_id = Column('species_hr_id', Integer,
                        ForeignKey(DataHabitattypeRegion.id))
    species_id = Column('speciescode', Integer,
                        ForeignKey(DataSpecies.id))
    speciesname = Column(String)
    validated = Column(Integer)
    validation_date = Column(DateTime)
    globalid = Column(String, default=create_esri_guid)

    habitats = relationship(u'DataHabitattypeRegion',
        backref=db.backref('species', lazy='dynamic'))


class Attachment(Base):
    __tablename__ = u'attachments'

    id = Column('objectid', Integer, Sequence('attachments_seq'),
                primary_key=True)
    mime_type = Column(String)
    data = Column(Binary)


class CommentReply(Base):
    __tablename__ = u'comment_replies'

    id = Column('objectid', String, primary_key=True, default=create_uuid)
    parent_table = Column(String)
    parent_id = Column(String)
    user_id = Column(String)
    date = Column(DateTime)
    text = Column(Text)
    attachment_id = Column(ForeignKey(Attachment.id))

    attachment = relationship(u'Attachment')

    @property
    def thread_users(self):
        return {r for r, in db.session.query(CommentReply.user_id)\
            .filter_by(parent_table=self.parent_table)\
            .filter_by(parent_id=self.parent_id)}



class CommentReplyRead(Base):
    __tablename__ = u'comment_replies_read'

    id = Column('objectid', String, primary_key=True, default=create_uuid)
    user_id = Column(String)
    table = Column('TABLE', String)
    row_id = Column(Integer)


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
    dataset_id = Column(ForeignKey('datasets.objectid'))


class Dataset(Base):
    __tablename__ = u'datasets'

    id = Column('objectid', Integer, Sequence('datasets_seq'),
                primary_key=True)
    user_id = Column(String)
    date = Column('DATE', DateTime)
    comment = Column('COMMENT', Text)
    preview = Column(Boolean, default=False, nullable=True)
    checklist = Column(Boolean, default=False, nullable=True)
    year_start = Column(Integer, nullable=True)
    year_end = Column(Integer, nullable=True)

    @property
    def details(self):
        new = (
            self.habitat_objs.filter_by(cons_role='assessment').count() +
            self.species_objs.filter_by(cons_role='assessment').count()
        )
        draft = (
            self.habitat_objs.filter_by(cons_role='final-draft').count() +
            self.species_objs.filter_by(cons_role='final-draft').count()
        )
        final = (
            self.habitat_objs.filter_by(cons_role='final').count() +
            self.species_objs.filter_by(cons_role='final').count()
        )
        return {
            'new': new, 'draft': draft, 'final': final,
        }


class NotificationUser(Base):
    __tablename__ = u'notification_user'

    id = Column('objectid', String, primary_key=True, default=create_uuid)
    email = Column(String)
    full_name = Column(String)


class Config(Base):
    __tablename__ = u'config'

    id = Column('objectid', String, primary_key=True)
    value = Column(Text)


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


@db_manager.command
def sequences():
    pairs = list(db.session.execute(
        "select 'R'||registration_id sequence_name, table_name "
        "from sde.table_registry where owner = 'REPORTDATA_OWNER'"
    ))

    print "["
    for a, b in pairs:
        print "    %r," % ((str(a), str(b.lower())),)
    print "]"
