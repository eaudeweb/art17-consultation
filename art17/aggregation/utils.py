# coding=utf-8
import flask
from flask import current_app
from sqlalchemy import or_
from art17 import models, dal, ROLE_MISSING


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
        return flask.url_for('aggregation.habitat-details',
                             dataset_id=record.cons_dataset_id,
                             record_id=record.id)
    elif isinstance(record, models.DataSpeciesRegion):
        return flask.url_for('aggregation.species-details',
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


def get_history_aggregation_record_url(history_item):
    object_table = history_item.table.strip()
    object_id = history_item.object_id
    if object_table == 'data_species_regions':
        obj = models.DataSpeciesRegion.query.get(object_id)
        title = obj and obj.species.lu.display_name
    elif object_table == 'data_habitattype_regions':
        obj = models.DataHabitattypeRegion.query.get(object_id)
        title = obj and obj.habitat.lu.display_name
    else:
        return '', '', ''
    if obj:
        return record_details_url(obj), title, obj.region
    return ''


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

    species = dataset.species_objs.filter_by(cons_role=ROLE_MISSING)
    habitats = dataset.habitat_objs.filter_by(cons_role=ROLE_MISSING)

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


def get_checklist(checklist_id):
    class DefaultCL(object):
        id = None
        name = u"Lista de verificare inițială"
        year_start = current_app.config.get('DEFAULT_YEAR_START')
        year_end = current_app.config.get('DEFAULT_YEAR_END')
        def __unicode__(self):
            return self.name

    if checklist_id is None or checklist_id == '':
        return DefaultCL()
    return (
        models.Dataset.query.filter_by(id=checklist_id).first() or DefaultCL()
    )


def get_reporting_id():
    current_report = models.Config.query.filter_by(id='REPORTING_ID').first()
    if current_report:
        return current_report.value or None
    return None


def get_species_checklist(distinct=False, dataset_id=None, groupped=False):
    queryset = (
        models.DataSpeciesCheckList.query
        #.filter(models.DataSpeciesCheckList.presence != 'EX')
        .filter_by(dataset_id=dataset_id)
        .filter(models.DataSpeciesCheckList.member_state == 'RO')
        .order_by(models.DataSpeciesCheckList.name)
    )
    if distinct:
        queryset = (
            queryset
            .with_entities(
                models.DataSpeciesCheckList.code,
                models.DataSpeciesCheckList.code.concat(
                    ' ' +
                    models.DataSpeciesCheckList.name
                ),
            )
            .group_by(models.DataSpeciesCheckList.name,
                      models.DataSpeciesCheckList.code)
            .order_by(models.DataSpeciesCheckList.name)
        )
    elif groupped:
        queryset = (
            queryset
            .join(models.DataSpeciesCheckList.lu)
            .with_entities(
                models.DataSpeciesCheckList.code,
                models.DataSpeciesCheckList.code.concat(
                    ' ' +
                    models.DataSpeciesCheckList.name
                ),
                models.LuHdSpecies.group_code,
            )
            .group_by(models.DataSpeciesCheckList.name,
                      models.DataSpeciesCheckList.code,
                      models.LuHdSpecies.group_code)
            .order_by(models.DataSpeciesCheckList.name)
        )
        queryset = sorted(queryset, key=lambda d: d[2])

    return queryset


def get_habitat_checklist(distinct=False, dataset_id=None, groupped=False):
    queryset = (
        models.DataHabitatsCheckList.query
        #.filter(models.DataHabitatsCheckList.presence != 'EX')
        .filter_by(dataset_id=dataset_id)
        .filter(models.DataHabitatsCheckList.member_state == 'RO')
        .order_by(models.DataHabitatsCheckList.name)
    )
    if distinct:
        queryset = (
            queryset
            .with_entities(
                models.DataHabitatsCheckList.code,
                models.DataHabitatsCheckList.code.concat(
                    ' ' +
                    models.DataHabitatsCheckList.name
                ),
            )
            .group_by(models.DataHabitatsCheckList.name,
                      models.DataHabitatsCheckList.code)
            .order_by(models.DataHabitatsCheckList.name)
        )
    if groupped:
        queryset = [a + ('',) for a in queryset]

    return queryset


def get_tabmenu_data(dataset):
    yield {
        'url': flask.url_for('.habitats', dataset_id=dataset.id),
        'label': "Habitate",
        'code': 'H',
    }
    for group in dal.get_species_groups():
        yield {
            'url': flask.url_for('.species',
                                 group_code=group.code,
                                 dataset_id=dataset.id),
            'label': group.description,
            'code': 'S' + group.code,
        }


def get_tabmenu_preview(dataset):
    if dataset.habitat_objs.count():
        yield {
            'url': flask.url_for('.habitats', dataset_id=dataset.id),
            'label': "Habitate",
            'code': 'H',
        }
    species = list(dataset.species_objs)
    for group in dal.get_species_groups():
        qs = [s for s in species if s.species.lu.group_code == group.code]
        if qs:
            yield {
                'url': flask.url_for('.species',
                                     group_code=group.code,
                                     dataset_id=dataset.id),
                'label': group.description,
                'code': 'S' + group.code,
            }


def valid_checklist():
    current = get_reporting_id()
    current = get_checklist(current)

    ok = all((current.year_start, current.year_end))
    if not ok:
        flask.flash(u"Anii de început și sfârșit nu sunt setați pentru raportarea curentă.", 'danger')
    return current
