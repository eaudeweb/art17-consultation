# encoding: utf-8

import flask
from art17 import species
from art17 import models

notifications = flask.Blueprint('notifications', __name__)

@notifications.record
def register_handlers(state):
    app = state.app

    connect(species.comment_added, app,
            table='data_species_regions', action='add')


def connect(signal, sender, **more_kwargs):
    @signal.connect_via(sender)
    def wrapper(sender, **kwargs):
        kwargs.update(more_kwargs)
        handle_signal(**kwargs)


def handle_signal(table, action, ob, **extra):
    if not ob.id:
        models.db.session.flush()
        assert ob.id

    recipients = models.NotificationUser.query.all()
    emails = {}
    for r in recipients:
        emails[r.email] = create_message(table, action, ob, r)
    # now send them all, TODO


def create_message(table, action, ob, user):
    tpl = 'unknown.html'
    if table == 'data_species_regions':
        if action == 'add':
            tpl = 'notifications/species_regions_add.html'
    return flask.render_template(tpl, **{'object': ob, 'user': user})
