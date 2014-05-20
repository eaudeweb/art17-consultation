import flask
from sqlalchemy import or_
from art17 import models, dal


def record_index_url(subject, region, dataset_id):
    obj = get_record(subject, region, dataset_id)
    if isinstance(obj, models.DataHabitattypeRegion):
        return flask.url_for('.habitat-index', dataset_id=dataset_id,
                             record_id=obj.id)
    if isinstance(obj, models.DataSpeciesRegion):
        return flask.url_for('.species-index', dataset_id=dataset_id,
                             record_id=obj.id)
    raise RuntimeError("Expecting a speciesregion or a habitattyperegion")


def record_dashboard_url(record):
    if record.dataset.preview:
        return flask.url_for('.post_preview', dataset_id=record.dataset.id)
    if isinstance(record, models.DataHabitattypeRegion):
        return flask.url_for('.habitats', dataset_id=record.cons_dataset_id)
    elif isinstance(record, models.DataSpeciesRegion):
        return flask.url_for('.species',
                             dataset_id=record.cons_dataset_id,
                             group_code=record.subject.lu.group_code)
    raise RuntimeError("Expecting a species or a habitat object")


def record_edit_url(record):
    if isinstance(record, models.DataHabitattypeRegion):
        return flask.url_for('.habitat-edit', dataset_id=record.cons_dataset_id,
                             record_id=record.id)
    elif isinstance(record, models.DataSpeciesRegion):
        return flask.url_for('.species-edit',
                             dataset_id=record.cons_dataset_id,
                             record_id=record.id)
    raise RuntimeError("Expecting a species or a habitat object")


def record_details_url(record):
    if isinstance(record, models.DataHabitattypeRegion):
        return flask.url_for('.habitat-details', dataset_id=record.cons_dataset_id,
                             record_id=record.id)
    elif isinstance(record, models.DataSpeciesRegion):
        return flask.url_for('.species-details',
                             dataset_id=record.cons_dataset_id,
                             record_id=record.id)
    raise RuntimeError("Expecting a species or a habitat object")


def record_history_url(record):
    if isinstance(record, models.DataHabitattypeRegion):
        return flask.url_for('history_aggregation.habitat_comments',
                             dataset_id=record.cons_dataset_id,
                             subject_code=record.habitat.code,
                             region_code=record.region,
        )
    elif isinstance(record, models.DataSpeciesRegion):
        return flask.url_for('history_aggregation.habitat_comments',
                             dataset_id=record.cons_dataset_id,
                             subject_code=record.species.code,
                             region_code=record.region,
        )
    raise RuntimeError("Expecting a species or a habitat object")


def record_finalize_toggle_url(record, finalize):
    action = 'finalize' if finalize else 'definalize'
    if isinstance(record, models.DataHabitattypeRegion):
        return flask.url_for('.habitat-' + action,
                             dataset_id=record.cons_dataset_id,
                             record_id=record.id)
    elif isinstance(record, models.DataSpeciesRegion):
        return flask.url_for('.species-' + action,
                             dataset_id=record.cons_dataset_id,
                             record_id=record.id)
    raise RuntimeError("Expecting a species or a habitat object")


def get_record(subject, region, dataset_id):
    obj = None
    if isinstance(subject, models.DataHabitat):
        obj = models.DataHabitattypeRegion.query.filter_by(
            cons_dataset_id=dataset_id,
            habitat=subject,
            region=region.code,
        ).first()
    if isinstance(subject, models.DataSpecies):
        obj = models.DataSpeciesRegion.query.filter_by(
            cons_dataset_id=dataset_id,
            species=subject,
            region=region.code,
        ).first()
    if obj:
        return obj
    raise RuntimeError("Expecting a speciesregion or a habitattyperegion")


def aggregation_missing_data_report(dataset_id):
    dataset = models.Dataset.query.get_or_404(dataset_id)

    ROLE = 'missing'
    species = dataset.species_objs.filter_by(cons_role=ROLE)
    habitats = dataset.habitat_objs.filter_by(cons_role=ROLE)

    species_list = set([s.species for s in species])
    habitat_list = set([h.habitat for h in habitats])
    species_regions = {(s.subject_id, s.region): 0 for s in species}
    habitat_regions = {(h.subject_id, h.region): 0 for h in habitats}
    relevant_regions = [
        a[1] for a in species_regions.keys() + habitat_regions.keys()
    ]
    bioreg_list = dal.get_biogeo_region_list(relevant_regions)

    return {
        'missing_species': species,
        'species_regions': species_regions,
        'species_list': species_list,
        'habitat_list': habitat_list,
        'missing_habitats': habitats,
        'habitat_regions': habitat_regions,
        'bioreg_list': bioreg_list,
    }


def get_datasets():
    return (
        models.Dataset.query
        .filter(or_(models.Dataset.preview == False,
                    models.Dataset.preview == None))
        .order_by(models.Dataset.date)
        .all()
    )
