import sys
from path import path
import pytest
from mock import Mock

sys.path.append(path(__file__).abspath().parent.parent)


@pytest.fixture
def app():
    import flask
    app = flask.Flask('art17.app')
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'foo'
    app.config['TESTING_USER_ID'] = None
    @app.before_request
    def set_identity():
        user_id = flask.current_app.config['TESTING_USER_ID']
        flask.g.identity = Mock(id=user_id)
    from art17.models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


@pytest.fixture
def species_app(app):
    from art17.species import species
    app.register_blueprint(species)
    return app


@pytest.fixture
def habitat_app(app):
    from art17.habitat import habitat
    app.register_blueprint(habitat)
    return app
