from sqlalchemy import func
from art17.models import (
    db,
    LuBiogeoreg,
    LuGrupSpecie,
    LuHdSpecies,
    DataHabitat,
    DataSpecies,
    DataHabitattypeRegion,
    DataSpeciesRegion,
)


def get_biogeo_regions():
    return LuBiogeoreg.query.all()


def get_species_groups():
    return LuGrupSpecie.query.all()


def get_habitat_list():
    return (
        DataHabitat.query
        .join(DataHabitat.lu)
        .all()
    )


def get_species_list(group_code):
    return (
        DataSpecies.query
        .join(DataSpecies.lu)
        .filter(LuHdSpecies.group_code == group_code)
        .all()
    )


def get_species_group(group_code):
    return (
        LuGrupSpecie.query
        .filter_by(code=group_code)
        .first()
    )


class BaseDataset(object):

    def get_subject_region_overview(self):
        overview = {}
        regions_query = (
            db.session
            .query(
                self.record_model_subject_id,
                self.record_model.region,
            )
            .filter_by(cons_role='assessment')
        )
        for key in regions_query:
            overview[key] = 0

        comment_count_query = (
            db.session
            .query(
                self.record_model_subject_id,
                self.record_model.region,
                func.count('*'),
            )
            .filter_by(cons_role='comment')
            .group_by(
                self.record_model_subject_id,
                self.record_model.region,
            )
        )
        for (subject_id, region_code, count) in comment_count_query:
            overview[subject_id, region_code] = count

        return overview

    def get_topic_records(self, subject, region):
        records_query = (
            self.record_model.query
            .filter(self.record_model_subject_id == subject.id)
            .order_by(self.record_model.cons_date)
        )
        if region is not None:
            records_query = records_query.filter_by(region=region.code)

        return iter(records_query)

    def get_assessment_for_all_regions(self, subject_code):
        assessment_query = (
            db.session.query(
                self.record_model.conclusion_assessment,
                self.record_model.region,
            )
            .join(self.subject_model)
            .filter(self.subject_model.code == subject_code)
            .filter(self.record_model.conclusion_assessment != None)
        )
        return assessment_query.all()

    def get_comment(self, comment_id):
        return self.record_model.query.get(comment_id)


class HabitatDataset(BaseDataset):

    subject_model = DataHabitat
    record_model = DataHabitattypeRegion

    @property
    def record_model_subject_id(self):
        return DataHabitattypeRegion.habitat_id



class SpeciesDataset(BaseDataset):

    subject_model = DataSpecies
    record_model = DataSpeciesRegion

    @property
    def record_model_subject_id(self):
        return DataSpeciesRegion.species_id
