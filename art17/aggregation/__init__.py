# encoding: utf-8
from collections import defaultdict
from StringIO import StringIO

import flask
from flask.ext.principal import Permission, Denial, PermissionDenied

from art17 import models, dal
from art17.aggregation.utils import (
    record_index_url,
    record_dashboard_url,
    record_edit_url,
    record_details_url,
    record_history_url,
    record_finalize_toggle_url,
    get_record)
from art17.common import get_roles_for_subject
from art17.auth import need


aggregation = flask.Blueprint('aggregation', __name__)


def perm_edit_record(record):
    if record.cons_role == 'final':
        return Denial(need.everybody)

    return Permission(
        need.admin,
        *get_roles_for_subject('reviewer', record.subject)
    )


def perm_finalize_record(record):
    if record.cons_role == 'final':
        return Denial(need.everybody)

    return Permission(
        need.admin,
        *get_roles_for_subject('reviewer', record.subject)
    )


def perm_definalize_record(record):
    if record.cons_role != 'final':
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


def get_tabmenu_data(dataset_id):
    yield {
        'url': flask.url_for('.habitats', dataset_id=dataset_id),
        'label': "Habitate",
        'code': 'H',
    }
    for group in dal.get_species_groups():
        yield {
            'url': flask.url_for('.species',
                                 group_code=group.code,
                                 dataset_id=dataset_id),
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


def create_aggregation(timestamp, user_id):
    dataset = models.Dataset(
        date=timestamp,
        user_id=user_id,
    )
    models.db.session.add(dataset)

    habitat_id_map = dict(
        models.db.session.query(
            models.DataHabitat.code,
            models.DataHabitat.id,
        )
    )

    habitat_checklist_query = (
        models.DataHabitatsCheckList.query
        .filter(models.DataHabitatsCheckList.presence != 'EX')
        .filter(models.DataHabitatsCheckList.member_state == 'RO')
    )

    habitat_report = defaultdict(set)
    for row in habitat_checklist_query:
        region_code = row.bio_region
        habitat_code = row.natura_2000_code
        habitat_id = habitat_id_map.get(habitat_code)
        habitat_row = models.DataHabitattypeRegion(
            dataset=dataset,
            habitat_id=habitat_id,
            region=region_code,
            cons_role='assessment',
            cons_date=timestamp,
            cons_user_id=user_id,
        )
        models.db.session.add(habitat_row)
        habitat_report[habitat_code].add(region_code)

    species_id_map = dict(
        models.db.session.query(
            models.DataSpecies.code,
            models.DataSpecies.id,
        )
    )

    species_checklist_query = (
        models.DataSpeciesCheckList.query
        .filter(models.DataSpeciesCheckList.presence != 'EX')
        .filter(models.DataSpeciesCheckList.member_state == 'RO')
    )

    species_report = defaultdict(set)
    for row in species_checklist_query:
        region_code = row.bio_region
        species_code = row.natura_2000_code
        species_id = species_id_map.get(species_code)
        species_row = models.DataSpeciesRegion(
            dataset=dataset,
            species_id=species_id,
            region=region_code,
            cons_role='assessment',
            cons_date=timestamp,
            cons_user_id=user_id,
        )
        models.db.session.add(species_row)
        species_report[species_code].add(region_code)

    report = StringIO()
    print >>report, "Habitate:"
    for habitat_code, regions in sorted(habitat_report.items()):
        print >>report, "  %s: %s" % (habitat_code, ', '.join(sorted(regions)))

    print >>report, "\n\n"
    print >>report, "Specii:"
    for species_code, regions in sorted(species_report.items()):
        print >>report, "  %s: %s" % (species_code, ', '.join(sorted(regions)))

    return report.getvalue(), dataset

# Import this after everything else
import art17.aggregation.views
