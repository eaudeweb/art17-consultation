from sqlalchemy import or_

from art17.common import FINALIZED_STATUS
from art17.models import (
    DataSpeciesRegion, DataHabitattypeRegion, ROLE_FINAL, db,
)
from art17.scripts import modifier
from art17.aggregation.utils import round_2_digits


def finalize(model_cls, dataset_id):
    records = model_cls.query.filter_by(cons_dataset_id=dataset_id)
    for record in records:
        record.cons_role = ROLE_FINAL
        record.cons_status = FINALIZED_STATUS
    db.session.commit()


def finalize_species(dataset_id):
    finalize(DataSpeciesRegion, dataset_id)


def finalize_habitats(dataset_id):
    finalize(DataHabitattypeRegion, dataset_id)


@modifier.command
def finalize_all(dataset_id):
    finalize_species(dataset_id)
    finalize_habitats(dataset_id)


def round_attr(obj, attr):
    value = getattr(obj, attr)
    if value:
        setattr(obj, attr, round_2_digits(value))


@modifier.command
def round_float_values(dataset_id):
    species = DataSpeciesRegion.query.filter(
        or_(DataSpeciesRegion.natura2000_population_min != None,
            DataSpeciesRegion.natura2000_population_max != None),
        DataSpeciesRegion.cons_dataset_id == dataset_id)
    for s in species:
        round_attr(s, 'natura2000_population_min')
        round_attr(s, 'natura2000_population_max')

    habitats = DataHabitattypeRegion.query.filter(
        or_(DataHabitattypeRegion.natura2000_area_min != None,
            DataHabitattypeRegion.natura2000_area_max != None),
        DataSpeciesRegion.cons_dataset_id == dataset_id)
    for h in habitats:
        round_attr(h, 'natura2000_area_min')
        round_attr(h, 'natura2000_area_max')
    db.session.commit()
