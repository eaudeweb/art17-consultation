# encoding: utf-8
from blinker import Signal

import flask
from flask.ext.principal import Permission, Denial
from flask.ext.script import Manager

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

MIMETYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

aggregation = flask.Blueprint('aggregation', __name__)
aggregation_manager = Manager()

species_record_finalize = Signal()
species_record_definalize = Signal()
habitat_record_finalize = Signal()
habitat_record_definalize = Signal()


def perm_edit_record(record):
    if record.is_agg_final():
        return Denial(need.everybody)

    return Permission(
        need.admin,
        *get_roles_for_subject('reporter', record.subject) +
        get_roles_for_subject('reviewer', record.subject)
    )


def perm_finalize_record(record):
    if record.is_agg_final():
        return Denial(need.everybody)

    return Permission(
        need.admin,
        *get_roles_for_subject('reviewer', record.subject)
    )


def perm_definalize_record(record):
    if not record.is_agg_final():
        return Denial(need.everybody)

    return Permission(
        need.admin,
        *get_roles_for_subject('reviewer', record.subject)
    )


def perm_preview_aggregation():
    return Permission(need.admin, need.expert, need.reporter, need.reviewer)


def perm_view_reports():
    return Permission(need.admin, need.expert, need.reporter, need.reviewer)


def perm_view_refvals():
    return Permission(need.admin, need.expert, need.reporter, need.reviewer)


def perm_edit_refvals():
    return Permission(need.admin, need.expert, need.reporter, need.reviewer)


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


@aggregation_manager.command
def test_species(speciescode):
    """ Generate a preview aggregation.
    Note: it is not saved to the database.
    """
    import logging
    from datetime import datetime
    from art17.aggregation.agregator import create_preview_aggregation
    logging.basicConfig(level=logging.DEBUG)

    report, agg = create_preview_aggregation(
        'species', subject=speciescode, comment='test',
        timestamp=datetime.now(), user_id='system'
    )
    print "Report: ", report


# Import this after everything else
import art17.aggregation.views
import art17.aggregation.admin
import art17.aggregation.reports
import art17.aggregation.checklist
