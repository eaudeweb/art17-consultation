# encoding: utf-8

from datetime import datetime
import flask
from flask.ext.principal import Permission
from blinker import Signal
from art17 import models
from art17.auth import require, need

messages = flask.Blueprint('messages', __name__)

message_added = Signal()
message_removed = Signal()


def _get_conclusion_or_404(conclusion_id):
    for cls in [models.DataSpeciesConclusion,
                models.DataHabitattypeConclusion]:
        conclusion = cls.query.get(conclusion_id)
        if conclusion is not None:
            return conclusion

    else:
        flask.abort(404)


def _dump_message_data(message):
    return {k: getattr(message, k)
            for k in ['text', 'user_id', 'parent', 'date']}


@messages.route('/mesaje/<conclusion_id>/nou', methods=['POST'])
@require(Permission(need.authenticated))
def new(conclusion_id):
    conclusion = _get_conclusion_or_404(conclusion_id)

    if flask.request.method == 'POST':
        message = models.ConclusionMessage(
            text=flask.request.form['text'],
            user_id=flask.g.identity.id,
            date=datetime.utcnow(),
            parent=conclusion.id)
        models.db.session.add(message)
        app = flask.current_app._get_current_object()
        message_added.send(app, ob=message,
                           new_data=_dump_message_data(message))
        models.db.session.commit()
        url = flask.url_for('.index', conclusion_id=conclusion_id)
        return flask.redirect(url)

    return flask.render_template('messages/new.html')


@messages.route('/mesaje/sterge', methods=['POST'])
@require(Permission(need.admin))
def remove():
    message_id = flask.request.args['message_id']
    next_url = flask.request.args['next']
    message = models.ConclusionMessage.query.get_or_404(message_id)
    user_id = message.user_id
    models.db.session.delete(message)
    app = flask.current_app._get_current_object()
    message_removed.send(app, ob=message, old_data=_dump_message_data(message))
    models.db.session.commit()
    flask.flash(u"Mesajul lui %s a fost șters." % user_id, 'success')
    return flask.redirect(next_url)


@messages.route('/mesaje/citit', methods=['POST'])
@require(Permission(need.authenticated))
def set_read_status():
    message_id = flask.request.form['message_id']
    read = (flask.request.form.get('read') == 'on')
    message = models.ConclusionMessage.query.get_or_404(message_id)

    user_id = flask.g.identity.id
    if user_id is None:
        flask.abort(403)

    existing = (models.ConclusionMessageRead
                    .query.filter_by(message_id=message.id, user_id=user_id))

    if read:
        if not existing.count():
            row = models.ConclusionMessageRead(message_id=message.id,
                                               user_id=user_id)
            models.db.session.add(row)
            models.db.session.commit()

    else:
        existing.delete()
        models.db.session.commit()

    return flask.jsonify(read=read)


@messages.route('/mesaje/<conclusion_id>')
def index(conclusion_id):
    messages = (models.ConclusionMessage
                    .query.filter_by(parent=conclusion_id).all())
    user_id = flask.g.identity.id

    if user_id:
        read_by_user = (models.ConclusionMessageRead
                            .query.filter_by(user_id=user_id))
        read_msgs = set(r.message_id for r in read_by_user)

    else:
        read_msgs = []

    return flask.render_template('messages/index.html', **{
        'conclusion_id': conclusion_id,
        'messages': messages,
        'read_msgs': read_msgs,
        'new_message_permission': Permission(need.authenticated).can(),
    })
