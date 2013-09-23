import pytest
import flask
from flask.ext.principal import Permission


@pytest.fixture
def app():
    from art17 import auth
    app = flask.Flask('art17.app')
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'foo'
    app.config['AUTH_DEBUG'] = True
    app.register_blueprint(auth.auth)

    @app.route('/needs')
    def get_needs():
        return flask.jsonify(
            everybody=Permission(auth.need.everybody).can(),
            authenticated=Permission(auth.need.authenticated).can(),
            admin=Permission(auth.need.admin).can(),
            user_id_foo=Permission(auth.need.user_id('foo')).can(),
            user_id_bar=Permission(auth.need.user_id('bar')).can())

    return app


def get_needs_json(client):
    resp = client.get('/needs')
    assert resp.status_code == 200
    assert resp.content_type == 'application/json'
    return flask.json.loads(resp.get_data())


def test_anonymous_has_no_needs(app):
    assert get_needs_json(app.test_client()) == {
        'everybody': True,
        'authenticated': False,
        'admin': False,
        'user_id_foo': False,
        'user_id_bar': False,
    }


def test_authenticated_has_some_needs(app):
    client = app.test_client()
    client.post('/auth_debug', data={'user_id': 'foo'})
    assert get_needs_json(client) == {
        'everybody': True,
        'authenticated': True,
        'admin': False,
        'user_id_foo': True,
        'user_id_bar': False,
    }


def test_set_explicit_permissions(app):
    client = app.test_client()
    client.post('/auth_debug', data={'user_id': 'bar', 'roles': 'admin'})
    assert get_needs_json(client) == {
        'everybody': True,
        'authenticated': True,
        'admin': True,
        'user_id_foo': False,
        'user_id_bar': True,
    }
