import flask
from art17 import models
from art17 import species
from art17 import habitat

history = flask.Blueprint('history', __name__)


@history.record
def register_handlers(state):
    app = state.app
    @species.comment_added.connect_via(app)
    def handle_comment_added(sender, **extra):
        handle_signal(table='data_species_comments', **extra)
    @habitat.comment_added.connect_via(app)
    def handle_comment_added(sender, **extra):
        handle_signal(table='data_habitattype_comments', **extra)


def handle_signal(table, ob, **extra):
    models.db.session.flush()
    item = models.History(table=table,
                          action='add',
                          object_id=ob.id,
                          user_id=flask.g.identity.id)
    models.db.session.add(item)
