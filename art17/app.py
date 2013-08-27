import flask
from flask.ext.script import Manager
from art17.models import db
from art17.species import species

views = flask.Blueprint('views', __name__)


@views.route('/')
def home():
    return 'hello art17'


def craete_app():
    app = flask.Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///art17_mdb'
    app.register_blueprint(views)
    app.register_blueprint(species)
    db.init_app(app)
    return app


manager = Manager(craete_app)


if __name__ == '__main__':
    manager.run()
