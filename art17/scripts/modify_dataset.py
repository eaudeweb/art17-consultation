from art17.common import FINALIZED_STATUS
from art17.models import (
    DataSpeciesRegion, DataHabitattypeRegion, ROLE_FINAL, db,
)
from art17.scripts import modifier


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
