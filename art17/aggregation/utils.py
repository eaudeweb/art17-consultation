import flask
from art17 import models


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
