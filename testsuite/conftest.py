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
    app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@example.com'
    @app.before_request
    def set_identity():
        user_id = flask.current_app.config['TESTING_USER_ID']
        flask.g.identity = Mock(id=user_id)
    from art17.models import db, LuPresence
    db.init_app(app)
    with app.app_context():
        db.create_all()
        rec1 = LuPresence(objectid=1, code='1', name='Present')
        db.session.add(rec1)

        rec2 = LuPresence(objectid=2,
                                    code='SR TAX',
                                    name='Taxonomical reserve')
        db.session.add(rec2)
        db.session.commit()
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


@pytest.fixture
def notifications_app(app):
    from art17.species import species
    from art17.notifications import notifications
    app.register_blueprint(species)
    app.register_blueprint(notifications)
    return app
