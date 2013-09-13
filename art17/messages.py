# encoding: utf-8

from datetime import datetime
import flask
from art17 import models
from art17.auth import admin_permission


messages = flask.Blueprint('messages', __name__)


def _get_comment_or_404(comment_id):
    for cls in [models.DataSpeciesComment, models.DataHabitattypeComment]:
        comment = cls.query.get(comment_id)
        if comment is not None:
            return comment

    else:
        flask.abort(404)


@messages.route('/mesaje/<comment_id>/nou', methods=['GET', 'POST'])
def new(comment_id):
    comment = _get_comment_or_404(comment_id)

    if flask.request.method == 'POST':
        message = models.CommentMessage(
            text=flask.request.form['text'],
            user_id=flask.g.identity.id,
            date=datetime.utcnow(),
            parent=comment.id)
        models.db.session.add(message)
        models.db.session.commit()
        return flask.redirect(flask.url_for('.index', comment_id=comment_id))

    return flask.render_template('messages/new.html')


@messages.route('/mesaje/sterge', methods=['POST'])
@admin_permission.require(403)
def remove():
    message_id = flask.request.args['message_id']
    next_url = flask.request.args['next']
    message = models.CommentMessage.query.get_or_404(message_id)
    user_id = message.user_id
    models.db.session.delete(message)
    models.db.session.commit()
    flask.flash(u"Mesajul lui %s a fost șters." % user_id, 'success')
    return flask.redirect(next_url)


@messages.route('/mesaje/<comment_id>')
def index(comment_id):
    messages = models.CommentMessage.query.filter_by(parent=comment_id).all()
    return flask.render_template('messages/index.html', **{
        'comment_id': comment_id,
        'messages': messages,
    })
