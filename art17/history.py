# encoding: utf-8

from datetime import datetime
import flask
from art17 import models
from art17 import species
from art17 import habitat
from art17 import replies
from art17.common import json_encode_more
from art17.auth import admin_permission

history = flask.Blueprint('history', __name__)
history_consultation = flask.Blueprint('history_consultation', __name__)


TABLE_LABEL = {
    'data_species_regions': u"evaluare specie",
    'data_habitattype_regions': u"evaluare habitat",
    'comment_replies': u"replică",
}


@history.record
def register_handlers(state):
    app = state.app

    connect(species.comment_added, app,
            table='data_species_regions', action='add')
    connect(species.comment_edited, app,
            table='data_species_regions', action='edit')
    connect(species.comment_status_changed, app,
            table='data_species_regions', action='status')
    connect(species.comment_deleted, app,
            table='data_species_regions', action='delete')

    connect(habitat.comment_added, app,
            table='data_habitattype_regions', action='add')
    connect(habitat.comment_edited, app,
            table='data_habitattype_regions', action='edit')
    connect(habitat.comment_status_changed, app,
            table='data_habitattype_regions', action='status')
    connect(habitat.comment_deleted, app,
            table='data_habitattype_regions', action='delete')

    connect(replies.reply_added, app,
            table='comment_replies', action='add')
    connect(replies.reply_removed, app,
            table='comment_replies', action='remove')


def connect(signal, sender, **more_kwargs):
    @signal.connect_via(sender)
    def wrapper(sender, **kwargs):
        kwargs.update(more_kwargs)
        handle_signal(**kwargs)


def handle_signal(table, action, ob, old_data=None, new_data=None, **extra):
    if not ob.id:
        models.db.session.flush()
        assert ob.id
    item = models.History(table=table,
                          action=action,
                          object_id=ob.id,
                          date=datetime.utcnow(),
                          user_id=flask.g.identity.id)
    if old_data:
        item.old_data = flask.json.dumps(old_data, default=json_encode_more)
    if new_data:
        item.new_data = flask.json.dumps(new_data, default=json_encode_more)
    models.db.session.add(item)


@history.context_processor
def inject_lookup_tables():
    return {
        'TABLE_LABEL': TABLE_LABEL,
    }


@history_consultation.route('/activitate')
@admin_permission.require(403)
def index():
    history_items = models.History.query.order_by(models.History.date.desc())
    return flask.render_template('history/index.html', **{
        'history_items': iter(history_items),
    })


@history_consultation.route('/activitate/<item_id>')
@admin_permission.require(403)
def delta(item_id):
    return flask.render_template('history/delta.html', **{
        'item': models.History.query.get_or_404(item_id),
    })


@history.app_template_filter('pretty_json_data')
def pretty_json_data(json_data):
    data = flask.json.loads(json_data)
    return flask.json.dumps(data, indent=2, sort_keys=True)


@history_consultation.route('/activitate/specii/<subject_code>/<region_code>')
@admin_permission.require(403)
def species_comments(subject_code, region_code):
    from art17.species import get_dataset
    dataset = get_dataset()
    items = dataset.get_history(subject_code, region_code)
    return flask.render_template('history/comments.html', **{
        'history_items': items,
        'subject_category': 'specii',
        'subject_code': subject_code,
        'region_code': region_code,
    })


@history_consultation.route('/activitate/habitate/<subject_code>/<region_code>')
@admin_permission.require(403)
def habitat_comments(subject_code, region_code):
    from art17.habitat import get_dataset
    dataset = get_dataset()
    items = dataset.get_history(subject_code, region_code)
    return flask.render_template('history/comments.html', **{
        'history_items': items,
        'subject_category': 'habitate',
        'subject_code': subject_code,
        'region_code': region_code,
    })
