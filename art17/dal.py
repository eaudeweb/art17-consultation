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


class HabitatDataset():

    def get_habitat_region_overview(self):
        habitat_regions = {}
        habitat_regions_query = (
            db.session
            .query(
                DataHabitattypeRegion.habitat_id,
                DataHabitattypeRegion.region,
            )
            .filter_by(cons_role='assessment')
        )
        for key in habitat_regions_query:
            habitat_regions[key] = 0

        habitat_comment_count_query = (
            db.session
            .query(
                DataHabitattypeRegion.habitat_id,
                DataHabitattypeRegion.region,
                func.count('*'),
            )
            .filter_by(cons_role='comment')
            .group_by(
                DataHabitattypeRegion.habitat_id,
                DataHabitattypeRegion.region,
            )
        )
        for (habitat_id, region_code, count) in habitat_comment_count_query:
            habitat_regions[habitat_id, region_code] = count

        return habitat_regions

    def get_topic_records(self, habitat, region):
        records_query = (
            DataHabitattypeRegion.query
            .filter_by(habitat=habitat)
            .order_by(DataHabitattypeRegion.cons_date)
        )
        if region is not None:
            records_query = records_query.filter_by(region=region.code)

        return iter(records_query)

    def get_comment(self, comment_id):
        return DataHabitattypeRegion.query.get(comment_id)



class SpeciesDataset():

    def get_species_region_overview(self):
        species_regions = {}
        species_regions_query = (
            db.session
            .query(
                DataSpeciesRegion.species_id,
                DataSpeciesRegion.region,
            )
            .filter_by(cons_role='assessment')
        )
        for key in species_regions_query:
            species_regions[key] = 0

        species_comment_count_query = (
            db.session
            .query(
                DataSpeciesRegion.species_id,
                DataSpeciesRegion.region,
                func.count('*'),
            )
            .filter_by(cons_role='comment')
            .group_by(
                DataSpeciesRegion.species_id,
                DataSpeciesRegion.region,
            )
        )
        for (species_id, region_code, count) in species_comment_count_query:
            species_regions[species_id, region_code] = count

        return species_regions

    def get_topic_records(self, species, region):
        records_query = (
            DataSpeciesRegion.query
            .filter_by(species=species)
            .order_by(DataSpeciesRegion.cons_date)
        )
        if region is not None:
            records_query = records_query.filter_by(region=region.code)

        return iter(records_query)

    def get_comment(self, comment_id):
        return DataSpeciesRegion.query.get(comment_id)
