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

    connect(species.comment_added, app,
            table='data_species_comments', action='add')
    connect(species.comment_edited, app,
            table='data_species_comments', action='edit')
    connect(species.comment_status_changed, app,
            table='data_species_comments', action='status')

    connect(habitat.comment_added, app,
            table='data_habitattype_comments', action='add')
    connect(habitat.comment_edited, app,
            table='data_habitattype_comments', action='edit')
    connect(habitat.comment_status_changed, app,
            table='data_habitattype_comments', action='status')

    connect(messages.message_added, app,
            table='comment_messages', action='add')
    connect(messages.message_removed, app,
            table='comment_messages', action='remove')


def connect(signal, sender, **more_kwargs):
    @signal.connect_via(sender)
    def wrapper(sender, **kwargs):
        kwargs.update(more_kwargs)
        handle_signal(**kwargs)


def handle_signal(table, action, ob, old_data=None, **extra):
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
    models.db.session.add(item)


@history.route('/activitate')
@admin_permission.require(403)
def activity():
    return flask.render_template('activity.html', **{
        'history_items': iter(models.History.query),
    })
