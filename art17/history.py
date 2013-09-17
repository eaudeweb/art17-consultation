import flask
from art17 import models
from art17 import species
from art17 import habitat

history = flask.Blueprint('history', __name__)


@history.record
def register_handlers(state):
    app = state.app

    connect(species.comment_added, app,
            table='data_species_comments', action='add')
    connect(species.comment_edited, app,
            table='data_species_comments', action='edit')

    connect(habitat.comment_added, app,
            table='data_habitattype_comments', action='add')
    connect(habitat.comment_edited, app,
            table='data_habitattype_comments', action='edit')


def connect(signal, sender, **more_kwargs):
    @signal.connect_via(sender)
    def wrapper(sender, **kwargs):
        kwargs.update(more_kwargs)
        handle_signal(**kwargs)


def handle_signal(table, action, ob, **extra):
    models.db.session.flush()
    item = models.History(table=table,
                          action=action,
                          object_id=ob.id,
                          user_id=flask.g.identity.id)
    models.db.session.add(item)
