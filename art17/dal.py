from datetime import datetime
from sqlalchemy import func, cast, CHAR
import flask
from art17.models import (
    db,
    LuBiogeoreg,
    LuGrupSpecie,
    LuHdSpecies,
    DataHabitat,
    DataSpecies,
    DataHabitattypeRegion,
    DataSpeciesRegion,
    CommentReply,
    CommentReplyRead,
    DataPressuresThreats,
    DataPressuresThreatsPollution,
    DataMeasures,
    History,
    DataHabitatSpecies,
)


def get_biogeo_region_list():
    return LuBiogeoreg.query.order_by(LuBiogeoreg.order).all()


def get_biogeo_region(region_code):
    return (
        LuBiogeoreg.query
        .filter_by(code=region_code)
        .first()
    )


def get_species_groups():
    return LuGrupSpecie.query.all()


def get_habitat_list():
    return (
        DataHabitat.query
        .join(DataHabitat.lu)
        .order_by(DataHabitat.code)
        .all()
    )


def get_species_list(group_code):
    return (
        DataSpecies.query
        .join(DataSpecies.lu)
        .filter(LuHdSpecies.group_code == group_code)
        .order_by(DataSpecies.code)
        .all()
    )


def get_species_group(group_code):
    return (
        LuGrupSpecie.query
        .filter_by(code=group_code)
        .first()
    )


class BaseDataset(object):

    def __init__(self, dataset_id):
        self.dataset_id = dataset_id

    def get_subject(self, subject_code):
        return (
            self.subject_model.query
            .filter_by(code=subject_code)
            .first()
        )

    def get_history(self, subject_code, region_code):
        query = (
            History.query
            .filter_by(table=cast(self.history_table_name, CHAR(128)))
            .filter_by(dataset_id=self.dataset_id)
            .join(
                self.record_model,
                History.object_id == cast(self.record_model.id, CHAR(32)),
            )
            .join(
                self.subject_model,
                self.record_model_subject_id == self.subject_model.id,
            )
            .filter(self.subject_model.code == subject_code)
            .filter(self.record_model.region == region_code)
            .order_by(History.date.desc())
        )
        return query.all()

    def get_subject_region_overview_aggregation(self):
        overview = {}
        regions_query = (
            db.session
            .query(
                self.record_model_subject_id,
                self.record_model.region,
            )
            .filter_by(cons_dataset_id=self.dataset_id)
        )
        for key in regions_query:
            overview[key] = 0
        return overview

    def get_subject_region_overview_consultation(self):
        overview = {}
        regions_query = (
            db.session
            .query(
                self.record_model_subject_id,
                self.record_model.region,
            )
            .filter_by(cons_role='assessment')
            .filter_by(cons_dataset_id=self.dataset_id)
        )
        for key in regions_query:
            overview[key] = {
                'count': 0,
            }

        comment_count_query = (
            db.session
            .query(
                self.record_model_subject_id,
                self.record_model.region,
                func.count('*'),
            )
            .filter((self.record_model.cons_role == 'comment') |
                    (self.record_model.cons_role == 'comment-draft'))
            .filter_by(cons_dataset_id=self.dataset_id)
            .filter_by(cons_deleted=False)
            .group_by(
                self.record_model_subject_id,
                self.record_model.region,
            )
        )
        for (subject_id, region_code, count) in comment_count_query:
            overview[subject_id, region_code]['count'] = count

        return overview

    def get_topic_records(self, subject, region_code):
        records_query = (
            self.record_model.query
            .filter(self.record_model_subject_id == subject.id)
            .filter_by(cons_dataset_id=self.dataset_id)
            .order_by(self.record_model.cons_date)
        )
        if region_code is not None:
            records_query = records_query.filter_by(region=region_code)

        return iter(records_query)

    def get_assessment_for_all_regions(self, subject_code):
        assessment_query = (
            db.session.query(
                self.record_model.conclusion_assessment,
                self.record_model.region,
            )
            .filter_by(cons_dataset_id=self.dataset_id)
            .join(self.subject_model)
            .filter(self.subject_model.code == subject_code)
            .filter(self.record_model.conclusion_assessment != None)
        )
        return assessment_query.all()

    def get_comment(self, comment_id):
        return self.record_model.query.get(comment_id)

    def get_reply_counts(self):
        reply_query = (
            db.session.query(
                CommentReply.parent_id,
                func.count(CommentReply.id),
            )
            .filter(CommentReply.parent_table == self.reply_parent_table)
            .group_by(CommentReply.parent_id)
        )
        return dict(reply_query)
    
    @classmethod
    def update_extra_fields(cls, struct, comment):
        for pressure in comment.get_pressures():
            db.session.delete(pressure)
        for pressure in struct['pressures']['pressures']:
            pressure_obj = DataPressuresThreats(**{
                cls.rel_id: comment.id,
                'pressure': pressure['pressure'],
                'ranking': pressure['ranking'],
                'type': 'p',
            })
            db.session.add(pressure_obj)
            db.session.flush()
            for pollution in pressure['pollutions']:
                pollution_obj = DataPressuresThreatsPollution(
                    pollution_pressure_id=pressure_obj.id,
                    pollution_qualifier=pollution,
                )
                db.session.add(pollution_obj)

        for threat in comment.get_threats():
            db.session.delete(threat)
        for threat in struct['threats']['threats']:
            threat_obj = DataPressuresThreats(**{
                cls.rel_id: comment.id,
                'pressure': threat['pressure'],
                'ranking': threat['ranking'],
                'type': 't',
            })
            db.session.add(threat_obj)
            db.session.flush()
            for pollution in threat['pollutions']:
                pollution_obj = DataPressuresThreatsPollution(
                    pollution_pressure_id=threat_obj.id,
                    pollution_qualifier=pollution,
                )
                db.session.add(pollution_obj)

        for measure in comment.measures:
            db.session.delete(measure)
        for measure in struct['measures']['measures']:
            measure_data = {cls.rel_id: comment.id}
            measure_data.update(measure)
            measure_obj = DataMeasures(**measure_data)
            db.session.add(measure_obj)
        db.session.commit()

    def create_record(self, **kwargs):
        kwargs.setdefault('cons_user_id', flask.g.identity.id)
        kwargs.setdefault('cons_date', datetime.utcnow())
        return self.record_model(**kwargs)

    def get_read_records(self, user_id, subject_id, region_code):
        read_query = (
            db.session.query(CommentReplyRead.row_id)
            .filter_by(table=self.reply_parent_table)
            .filter_by(user_id=user_id)
            .join(
                self.record_model,
                CommentReplyRead.row_id == self.record_model.id,
            )
            .filter(self.record_model_subject_id == subject_id)
            .filter_by(region=region_code)
            .filter_by(cons_dataset_id=self.dataset_id)
        )
        return set(row[0] for row in read_query)


class HabitatDataset(BaseDataset):

    subject_model = DataHabitat
    record_model = DataHabitattypeRegion
    reply_parent_table = 'habitat'
    rel_id = 'habitat_id'
    history_table_name = 'data_habitattype_regions'

    @property
    def record_model_subject_id(self):
        return DataHabitattypeRegion.habitat_id

    @classmethod
    def update_extra_fields(cls, struct, comment):
        super(HabitatDataset, cls).update_extra_fields(struct, comment)
        for species in comment.species:
            db.session.delete(species)
        for species in struct['typicalspecies']['species']:
            if not species:
                continue
            species_obj = DataHabitatSpecies(habitat_id=comment.id,
                                             speciesname=species)
            db.session.add(species_obj)
        db.session.commit()

    def link_to_record(self, object, record):
        object.habitat_id = record.habitat_id
        object.region = record.region
        object.cons_dataset_id = self.dataset_id


class SpeciesDataset(BaseDataset):

    subject_model = DataSpecies
    record_model = DataSpeciesRegion
    reply_parent_table = 'species'
    rel_id = 'species_id'
    history_table_name = 'data_species_regions'

    @property
    def record_model_subject_id(self):
        return DataSpeciesRegion.species_id

    def link_to_record(self, object, record):
        object.species_id = record.species_id
        object.region = record.region
        object.cons_dataset_id = self.dataset_id
