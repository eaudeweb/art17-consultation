# encoding: utf-8

from datetime import datetime
import flask
from flask.ext.principal import Permission
from blinker import Signal
from art17 import models
from art17.auth import require, need

replies = flask.Blueprint('replies', __name__)

reply_added = Signal()
reply_removed = Signal()


def get_comment_from_reply(parent_table, parent_id):
    if parent_table == 'habitat':
        return models.DataHabitattypeRegion.query.get(parent_id)
    elif parent_table == 'species':
        return models.DataSpeciesRegion.query.get(parent_id)
    return None


def _get_comment_or_404(parent_table, parent_id):
    return get_comment_from_reply(parent_table, parent_id) or flask.abort(404)


def _dump_reply_data(reply):
    attributes = ['text', 'user_id', 'parent_table', 'parent_id', 'date']
    return {k: getattr(reply, k) for k in attributes}


@replies.route(
    '/replici/habitate/<parent_id>/nou',
    defaults={'parent_table': 'habitat'},
    methods=['POST'],
)
@replies.route(
    '/replici/specii/<parent_id>/nou',
    defaults={'parent_table': 'species'},
    methods=['POST'],
)
@require(Permission(need.authenticated))
def new(parent_table, parent_id):
    comment = _get_comment_or_404(parent_table, parent_id)

    reply = models.CommentReply(
        text=flask.request.form['text'],
        user_id=flask.g.identity.id,
        date=datetime.utcnow(),
        parent_table=parent_table,
        parent_id=comment.id,
    )

    attachment_file = flask.request.files.get('attachment')
    if attachment_file:
        reply.attachment = models.Attachment(
            mime_type=attachment_file.mimetype,
            data=attachment_file.read(),
        )

    models.db.session.add(reply)
    app = flask.current_app._get_current_object()

    old_read_marks = (
        models.CommentReplyRead.query
        .filter_by(table=parent_table)
        .filter_by(row_id=parent_id)
    )
    old_read_marks.delete()

    reply_added.send(
        app,
        ob=reply,
        new_data=_dump_reply_data(reply),
    )

    models.db.session.commit()
    url = flask.url_for(
        '.index',
        parent_table=parent_table,
        parent_id=parent_id,
    )
    return flask.redirect(url)


@replies.route('/replici/sterge', methods=['POST'])
@require(Permission(need.admin))
def remove():
    reply_id = flask.request.args['reply_id']
    next_url = flask.request.args['next']
    reply = models.CommentReply.query.get_or_404(reply_id)
    user_id = reply.user_id
    if reply.attachment is not None:
        models.db.session.delete(reply.attachment)
    models.db.session.delete(reply)
    app = flask.current_app._get_current_object()
    reply_removed.send(app, ob=reply, old_data=_dump_reply_data(reply))
    models.db.session.commit()
    flask.flash(u"Replica lui %s a fost ștearsă." % user_id, 'success')
    return flask.redirect(next_url)


@replies.route(
    '/replici/habitate/<parent_id>',
    defaults={'parent_table': 'habitat'},
)
@replies.route(
    '/replici/specii/<parent_id>',
    defaults={'parent_table': 'species'},
)
def index(parent_table, parent_id):
    replies = (
        models.CommentReply.query
        .filter_by(parent_table=parent_table)
        .filter_by(parent_id=parent_id)
        .all()
    )
    user_id = flask.g.identity.id
    if user_id is not None:
        fields = {
            'user_id': user_id,
            'table': parent_table,
            'row_id': parent_id,
        }
        if models.CommentReplyRead.query.filter_by(**fields).count() < 1:
            models.db.session.add(models.CommentReplyRead(**fields))
            models.db.session.commit()

    return flask.render_template('replies/index.html', **{
        'parent_id': parent_id,
        'parent_table': parent_table,
        'replies': replies,
        'can_post_new_reply': Permission(need.authenticated).can(),
        'can_delete_reply': Permission(need.admin).can()
    })


@replies.route('/atasament/<int:attachment_id>')
def attachment(attachment_id):
    attachment_row = models.Attachment.query.get_or_404(attachment_id)
    return flask.Response(
        attachment_row.data,
        mimetype=attachment_row.mime_type,
    )
