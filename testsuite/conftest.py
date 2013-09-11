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
    @app.before_request
    def set_identity():
        flask.g.identity = Mock(id='somewho')
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


def flatten_dict(data):
    rv = {}
    for k, v in data.items():
        if isinstance(v, dict):
            for kx, vx in flatten_dict(v).items():
                rv[k + '.' + kx] = vx
        else:
            rv[k] = unicode(v)
    return rv


class Obj(object):
    """ A blank class. Useful sometimes. """
