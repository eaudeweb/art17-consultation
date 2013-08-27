import flask
from flask.ext.script import Manager

views = flask.Blueprint('views', __name__)


@views.route('/')
def home():
    return 'hello art17'


def craete_app():
    app = flask.Flask(__name__)
    app.config['DEBUG'] = True
    app.register_blueprint(views)
    return app


manager = Manager(craete_app)


if __name__ == '__main__':
    manager.run()
