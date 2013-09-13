import flask
from art17 import models


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
            parent=comment.id)
        models.db.session.add(message)
        models.db.session.commit()
        return 'saved'

    return flask.render_template('messages/new.html')
