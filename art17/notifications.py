# encoding: utf-8

import flask
from flask.ext.mail import Mail, Message
from art17 import species
from art17 import models

notifications = flask.Blueprint('notifications', __name__)
mail = Mail()


@notifications.record
def register_handlers(state):
    app = state.app
    mail.init_app(app)

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
    for r in recipients:
        msg = Message(body=create_message(table, action, ob, r),
                subject='Notificare',
                recipients=[r.email]
        )
        mail.send(msg)

def create_message(table, action, ob, user):
    tpl = 'unknown.html'
    if table == 'data_species_regions':
        if action == 'add':
            tpl = 'notifications/species_regions_add.html'
    return flask.render_template(tpl, **{'object': ob, 'user': user})
