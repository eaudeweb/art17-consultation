import flask
from art17 import models


messages = flask.Blueprint('messages', __name__)


@messages.route('/mesaje/nou', methods=['GET', 'POST'])
def new():
    if flask.request.method == 'POST':
        message = models.CommentMessage(text=flask.request.form['text'])
        models.db.session.add(message)
        models.db.session.commit()
        return 'saved'

    return flask.render_template('messages/new.html')
