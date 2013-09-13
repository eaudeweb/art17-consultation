import flask
from art17 import models


messages = flask.Blueprint('messages', __name__)


@messages.route('/mesaje/<comment_id>/nou', methods=['GET', 'POST'])
def new(comment_id):
    comment = models.DataSpeciesComment.query.get(comment_id)
    if comment is None:
        flask.abort(404)

    if flask.request.method == 'POST':
        message = models.CommentMessage(
            text=flask.request.form['text'],
            user_id=flask.g.identity.id,
            parent=comment.id)
        models.db.session.add(message)
        models.db.session.commit()
        return 'saved'

    return flask.render_template('messages/new.html')
