from datetime import datetime
import flask
from art17 import models
from art17 import species
from art17 import habitat
from art17 import messages
from art17.common import json_encode_more
from art17.auth import admin_permission

history = flask.Blueprint('history', __name__)


@history.record
def register_handlers(state):
    app = state.app

    connect(species.conclusion_added, app,
            table='data_species_conclusions', action='add')
    connect(species.conclusion_edited, app,
            table='data_species_conclusions', action='edit')
    connect(species.conclusion_status_changed, app,
            table='data_species_conclusions', action='status')
    connect(species.conclusion_deleted, app,
            table='data_species_conclusions', action='delete')

    connect(habitat.conclusion_added, app,
            table='data_habitattype_conclusions', action='add')
    connect(habitat.conclusion_edited, app,
            table='data_habitattype_conclusions', action='edit')
    connect(habitat.conclusion_status_changed, app,
            table='data_habitattype_conclusions', action='status')
    connect(habitat.conclusion_deleted, app,
            table='data_habitattype_conclusions', action='delete')

    connect(messages.message_added, app,
            table='conclusion_messages', action='add')
    connect(messages.message_removed, app,
            table='conclusion_messages', action='remove')


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


@history.route('/activitate')
@admin_permission.require(403)
def index():
    history_items = models.History.query.order_by(models.History.date.desc())
    return flask.render_template('history/index.html', **{
        'history_items': iter(history_items),
    })


@history.route('/activitate/<item_id>')
@admin_permission.require(403)
def detail(item_id):
    return flask.render_template('history/detail.html', **{
        'item': models.History.query.get_or_404(item_id),
    })


@history.app_template_filter('pretty_json_data')
def pretty_json_data(json_data):
    data = flask.json.loads(json_data)
    return flask.json.dumps(data, indent=2, sort_keys=True)
