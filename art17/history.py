import flask
from art17 import models
from art17 import species
from art17 import habitat

history = flask.Blueprint('history', __name__)


@history.record
def register_handlers(state):
    app = state.app
    connect(species.comment_added, app,
            table='data_species_comments')
    connect(habitat.comment_added, app,
            table='data_habitattype_comments')


def connect(signal, sender, **more_kwargs):
    @signal.connect_via(sender)
    def wrapper(sender, **kwargs):
        kwargs.update(more_kwargs)
        handle_signal(**kwargs)


def handle_signal(table, ob, **extra):
    models.db.session.flush()
    item = models.History(table=table,
                          action='add',
                          object_id=ob.id,
                          user_id=flask.g.identity.id)
    models.db.session.add(item)
