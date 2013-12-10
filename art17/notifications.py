# encoding: utf-8

import flask
from flask.ext.mail import Mail, Message
from art17 import species
from art17 import replies
from art17 import habitat
from art17 import models
from art17.common import calculate_identifier_steps
from art17.ldap_access import open_ldap_server

notifications = flask.Blueprint('notifications', __name__)
mail = Mail()


@notifications.record
def register_handlers(state):
    app = state.app
    mail.init_app(app)

    connect(species.comment_added, app,
            table='data_species_regions', action='add')
    connect(species.comment_edited, app,
            table='data_species_regions', action='edit')
    connect(species.comment_status_changed, app,
            table='data_species_regions', action='status')
    connect(species.comment_deleted, app,
            table='data_species_regions', action='delete')
    connect(species.comment_submitted, app,
            table='data_species_regions', action='submit')

    connect(habitat.comment_added, app,
            table='data_habitattype_regions', action='add')
    connect(habitat.comment_edited, app,
            table='data_habitattype_regions', action='edit')
    connect(habitat.comment_status_changed, app,
            table='data_habitattype_regions', action='status')
    connect(habitat.comment_deleted, app,
            table='data_habitattype_regions', action='delete')
    connect(habitat.comment_submitted, app,
            table='data_habitattype_regions', action='submit')

    connect(replies.reply_added, app,
            table='comment_replies', action='add')
    #connect(replies.reply_removed, app,
    #        table='comment_replies', action='remove')


def connect(signal, sender, **more_kwargs):
    @signal.connect_via(sender)
    def wrapper(sender, **kwargs):
        kwargs.update(more_kwargs)
        handle_signal(**kwargs)


def handle_signal(table, action, ob, **extra):
    if flask.current_app.config.get('NOTIFICATIONS_DISABLED'):
        return

    if not ob.id:
        models.db.session.flush()
        assert ob.id

    recipients = get_notification_emails(ob)
    for r in recipients:
        msg = Message(body=create_message(table, action, ob, r),
                subject='Notificare',
                recipients=[r['email']]
        )
        mail.send(msg)


def create_message(table, action, ob, user):
    tpl = 'unknown.html'
    if table == 'data_species_regions':
        tpl = 'notifications/species.html'
    elif table == 'data_habitattype_regions':
        tpl = 'notifications/habitat.html'
    elif table == 'comment_replies':
        tpl = 'notifications/comment.html'
    return flask.render_template(tpl, **{'object': ob,
                                         'user': user,
                                         'action': action})


@notifications.app_template_global('resource_url')
def resource_url(table, objectid, _external=False):
    obj = get_parent_object(table, objectid)
    if table == 'species':
        return flask.url_for('species.index',
                             species=obj.species.code,
                             _external=_external)
    if table == 'habitat':
        return flask.url_for('habitat.index',
                             habitat=obj.habitat.code,
                             _external=_external)
    return ''


def get_parent_object(table, objectid):
    if table == 'species':
        return models.DataSpeciesRegion.query.get(objectid)
    if table == 'habitat':
        return models.DataHabitattypeRegion.query.get(objectid)
    return None


def get_notification_emails(obj):
    if isinstance(obj, models.CommentReply):
        parent = get_parent_object(obj.parent_table, obj.parent_id)
        identifier = parent.subject_identifier
    else:
        identifier = obj.subject_identifier
    emails = []
    steps = calculate_identifier_steps(identifier)
    if flask.current_app.testing:
        return [a.__dict__ for a in models.NotificationUser.query.all()]
    with open_ldap_server() as ldap_server:
        for group in steps:
            emails.extend(ldap_server.get_emails_for_group(group))
    return set(emails)
