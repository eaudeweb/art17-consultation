# encoding: utf-8
from collections import defaultdict
from StringIO import StringIO

import flask
from flask.ext.principal import Permission, Denial, PermissionDenied
from flask.ext.script import Manager

from art17 import models, dal
from art17.aggregation.utils import (
    record_index_url,
    record_dashboard_url,
    record_edit_url,
    record_details_url,
    record_history_url,
    record_finalize_toggle_url,
    get_record,
)
from art17.common import get_roles_for_subject
from art17.auth import need


aggregation = flask.Blueprint('aggregation', __name__)
aggregation_manager = Manager()


RECORD_ROLES = {
    'missing': 'The data was missing',
    'assessment': 'Initial role',
    'final-draft': 'Assessment being edited',
    'final': 'Final record, ready for consultation',
}


def perm_edit_record(record):
    if record.is_final():
        return Denial(need.everybody)

    return Permission(
        need.admin,
        *get_roles_for_subject('reviewer', record.subject)
    )


def perm_finalize_record(record):
    if record.is_final():
        return Denial(need.everybody)

    return Permission(
        need.admin,
        *get_roles_for_subject('reviewer', record.subject)
    )


def perm_definalize_record(record):
    if not record.is_final():
        return Denial(need.everybody)

    return Permission(
        need.admin,
        *get_roles_for_subject('reviewer', record.subject)
    )


def check_aggregation_perm():
    if need.admin in flask.g.identity.provides:
        return True
    for ne in flask.g.identity.provides:
        if ne.value.startswith('reviewer'):
            return True

    raise PermissionDenied()


def check_aggregation_preview_perm():
    if need.admin in flask.g.identity.provides:
        return True
    for ne in flask.g.identity.provides:
        if ne.value.startswith('reviewer'):
            return True
    for ne in flask.g.identity.provides:
        if ne.value.startswith('expert'):
            return True

    raise PermissionDenied()


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


@aggregation.app_context_processor
def inject_funcs():
    return dict(
        home_url=flask.url_for('aggregation.home'),
        app_name='aggregation',
        get_record=get_record,
        record_index_url=record_index_url,
        record_edit_url=record_edit_url,
        record_details_url=record_details_url,
        record_finalize_toggle_url=record_finalize_toggle_url,
        record_dashboard_url=record_dashboard_url,
        record_history_url=record_history_url,
    )


def execute_on_primary(query):
    app = flask.current_app
    aggregation_engine = models.db.get_engine(app, 'primary')
    return models.db.session.execute(query, bind=aggregation_engine)


def aggregate_object(obj, dataset):
    """
    Aggregate a habitat or a species.
    Returns a new row to be inserted into database.
    """
    if isinstance(obj, models.DataHabitatsCheckList):
        region_code = obj.bio_region
        habitat_row = models.DataHabitattypeRegion(
            dataset=dataset,
            region=region_code,
        )
        return habitat_row
    elif isinstance(obj, models.DataSpeciesCheckList):
        region_code = obj.bio_region
        species_row = models.DataSpeciesRegion(
            dataset=dataset,
            region=region_code,
        )
        return species_row
    else:
        raise NotImplementedError('Unknown check list obj')


def prepare_object(obj, timestamp, user_id):
    obj.cons_date = timestamp
    obj.cons_user_id = user_id
    obj.cons_role = 'assessment'
    return obj


def get_habitat_checklist(distinct=False, dataset_id=None):
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
    return queryset


def get_species_checklist(distinct=False, dataset_id=None):
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
    return queryset


def get_reporting_id():
    current_report = models.Config.query.filter_by(id='REPORTING_ID').first()
    return current_report.value if current_report else None


def create_aggregation(timestamp, user_id):
    curr_report_id = get_reporting_id()
    dataset = models.Dataset(
        date=timestamp,
        user_id=user_id,
        checklist_id=curr_report_id,
    )
    models.db.session.add(dataset)

    habitat_id_map = dict(
        models.db.session.query(
            models.DataHabitat.code,
            models.DataHabitat.id,
        )
    )

    habitat_checklist_query = get_habitat_checklist(dataset_id=curr_report_id)

    habitat_report = defaultdict(set)
    for row in habitat_checklist_query:
        habitat_row = aggregate_object(row, dataset)
        habitat_code = row.natura_2000_code
        habitat_id = habitat_id_map.get(habitat_code)

        habitat_row = prepare_object(habitat_row, timestamp, user_id)
        habitat_row.subject_id = habitat_id
        models.db.session.add(habitat_row)

        habitat_report[habitat_code].add(habitat_row.region)

    species_id_map = dict(
        models.db.session.query(
            models.DataSpecies.code,
            models.DataSpecies.id,
        )
    )

    species_checklist_query = get_species_checklist(dataset_id=curr_report_id)

    species_report = defaultdict(set)
    for row in species_checklist_query:
        species_row = aggregate_object(row, dataset)
        species_code = row.natura_2000_code
        species_id = species_id_map.get(species_code)
        species_row = prepare_object(species_row, timestamp, user_id)
        species_row.subject_id = species_id
        models.db.session.add(species_row)

        species_report[species_code].add(species_row.region)

    report = StringIO()
    print >>report, "Habitate:"
    for habitat_code, regions in sorted(habitat_report.items()):
        print >>report, "  %s: %s" % (habitat_code, ', '.join(sorted(regions)))

    print >>report, "\n\n"
    print >>report, "Specii:"
    for species_code, regions in sorted(species_report.items()):
        print >>report, "  %s: %s" % (species_code, ', '.join(sorted(regions)))

    return report.getvalue(), dataset


def create_preview_aggregation(page, subject, comment, timestamp, user_id):
    if page == 'habitat':
        id_map = dict(
            models.db.session.query(
                models.DataHabitat.code,
                models.DataHabitat.id,
            )
        )
        rows = get_habitat_checklist().filter_by(code=subject)
    elif page == 'species':
        id_map = dict(
            models.db.session.query(
                models.DataSpecies.code,
                models.DataSpecies.id,
            )
        )
        rows = get_species_checklist().filter_by(code=subject)
    else:
        raise NotImplementedError()

    dataset = models.Dataset(
        date=timestamp,
        user_id=user_id,
        preview=True,
        comment=comment,
    )
    models.db.session.add(dataset)
    bioregions = []
    for row in rows:
        record = aggregate_object(row, dataset)
        record = prepare_object(record, timestamp, user_id)
        record.subject_id = id_map.get(row.code)
        models.db.session.add(record)
        bioregions.append(row.bio_region)
    report = ', '.join(bioregions)
    return report, dataset


# Import this after everything else
import art17.aggregation.views
import art17.aggregation.admin
