import flask
from flask.ext.script import Manager
from art17.models import db

views = flask.Blueprint('views', __name__)


@views.route('/')
def home():
    return 'hello art17'


def craete_app():
    app = flask.Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///art17_mdb'
    app.register_blueprint(views)
    db.init_app(app)
    return app


manager = Manager(craete_app)


if __name__ == '__main__':
    manager.run()
