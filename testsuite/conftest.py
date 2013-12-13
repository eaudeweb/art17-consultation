import sys
import flask
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
    app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@example.com'
    app.config['HABITAT_MAP_URL'] = ''
    app.config['SPECIES_MAP_URL'] = ''
    @app.before_request
    def set_identity():
        user_id = flask.current_app.config['TESTING_USER_ID']
        flask.g.identity = Mock(id=user_id)
    from art17.models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


def create_mock_form_choices():
    rv = Mock()
    rv.get_lu_population_restricted.return_value = [('i', '')]
    rv.get_lu_presence.return_value = [
        ('1', 'Present'),
        ('SR TAX', 'Taxonomical reserve'),
    ]
    rv.get_lu_population.return_value = [('A', ''), ('grids10x10', '')]
    rv.get_lu_threats.return_value = [('1', '')]
    rv.get_lu_pollution.return_value = [('M', ''), ('A', '')]
    rv.get_lu_ranking.return_value = [('A', ''), ('M', '')]
    rv.get_lu_measures.return_value = []
    return rv


@pytest.fixture
def species_app(app):
    from art17.species import species
    from art17.common import common
    app.register_blueprint(species)
    app.register_blueprint(common)
    app.extensions['form_choices_loader'] = create_mock_form_choices()
    return app


@pytest.fixture
def habitat_app(app):
    from art17.habitat import habitat
    from art17.common import common
    app.register_blueprint(habitat)
    app.register_blueprint(common)
    app.extensions['form_choices_loader'] = create_mock_form_choices()
    return app


@pytest.fixture
def notifications_app(app):
    from art17.species import species
    from art17.auth import auth, set_session_auth
    from art17.common import common
    app.register_blueprint(common)
    app.register_blueprint(species)
    app.config['AUTH_DEBUG'] = True
    app.register_blueprint(auth)

    @app.route('/_fake_login/<name>')
    def fake_login(name):
        set_session_auth(name, ['admin'])
        return flask.redirect('/_ping')
    return app


@pytest.fixture
def aggregation_app(app):
    from art17.aggregation import aggregation
    from art17.common import common
    from art17.history import history, history_aggregation
    app.register_blueprint(aggregation)
    app.register_blueprint(common)
    app.register_blueprint(history)
    app.register_blueprint(history_aggregation)
    app.extensions['form_choices_loader'] = create_mock_form_choices()
    return app
