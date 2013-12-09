import flask
from flask.ext.principal import (Principal, Permission, Identity,
                                 RoleNeed, UserNeed, PermissionDenied)
from werkzeug.urls import url_encode
from art17.ldap_access import open_ldap_server

auth = flask.Blueprint('auth', __name__)

principals = Principal(use_sessions=False)


class need(object):
    """ A list of needs defined by our application. """

    everybody = RoleNeed('everybody')
    admin = RoleNeed('admin')
    authenticated = RoleNeed('authenticated')
    impossible = RoleNeed('impossible')

    @staticmethod
    def user_id(user_id):
        return UserNeed(user_id)

    @staticmethod
    def role(role):
        return RoleNeed(role)


admin_permission = Permission(need.admin)
impossible_permission = Permission(need.impossible)


def user_permission(user_id):
    return Permission(UserNeed(user_id))


def require(permission):
    def decorator(func):
        return permission.require()(func)
    return decorator


@auth.record
def register_principals(state):
    app = state.app
    principals.init_app(app)


@auth.app_context_processor
def inject_context():
    return {
        'admin_permission': admin_permission,
        'get_profile_login_url': get_profile_login_url,
    }


@auth.route('/auth_debug', methods=['GET', 'POST'])
def debug():
    auth_debug_allowed = bool(flask.current_app.config.get('AUTH_DEBUG'))
    if flask.request.method == 'POST':
        if not auth_debug_allowed:
            flask.abort(403)
        user_id = flask.request.form['user_id']
        roles = flask.request.form['roles'].strip().split()
        set_session_auth(user_id, roles)
        return flask.redirect(flask.url_for('.debug'))

    roles = flask.session.get('auth', {}).get('roles', [])
    return flask.render_template('auth/debug.html', **{
        'user_id': flask.g.identity.id,
        'roles_txt': ''.join('%s\n' % r for r in roles),
        'roles_example': (
            'admin\n'
            'expert:species:M\n'
            'expert:species:M:1353\n'
            'reviewer:habitat:8230\n'
        ),
        'auth_debug_allowed': auth_debug_allowed,
    })


def set_session_auth(user_id=None, roles=[]):
    flask.session['auth'] = {'user_id': user_id, 'roles': roles}


def load_debug_auth():
    auth_data = flask.session.get('auth')
    if auth_data and auth_data.get('user_id'):
        identity = Identity(id=auth_data['user_id'], auth_type='debug')
        principals.set_identity(identity)

        identity.provides.add(need.user_id(identity.id))
        identity.provides.add(need.authenticated)
        for role_name in auth_data.get('roles', []):
            identity.provides.add(RoleNeed(role_name))


def load_reverse_proxy_auth():
    user_id = flask.request.headers.get('X-RP-AuthUser')
    if user_id:
        with open_ldap_server() as ldap_server:
            user_info = ldap_server.get_user_info(user_id)

        identity = Identity(id=user_id, auth_type='reverse-proxy')
        principals.set_identity(identity)

        identity.provides.add(need.user_id(identity.id))
        identity.provides.add(need.authenticated)
        for group_name in user_info['groups']:
            identity.provides.add(RoleNeed(group_name))


@auth.record
def setup_auth_handlers(state):
    app = state.app
    if app.config.get('AUTH_DEBUG'):
        app.before_request(load_debug_auth)

    if app.config.get('AUTH_REVERSE_PROXY'):
        app.before_request(load_reverse_proxy_auth)

    @app.before_request
    def set_everybody_need():
        if 'identity' in flask.g:
            flask.g.identity.provides.add(need.everybody)


@auth.app_errorhandler(PermissionDenied)
def handle_permission_denied(error):
    return flask.render_template('auth/denied.html')


def get_profile_login_url():
    default_url = flask.url_for('auth.debug', next=flask.request.url)
    if flask.current_app.config.get('AUTH_DEBUG'):
        return default_url

    login_url = flask.current_app.config.get('AUTH_LOGIN_URL')
    if login_url:
        next_arg = flask.current_app.config.get('AUTH_LOGIN_NEXT_PARAM', 'next')
        return login_url + u'?' + url_encode({next_arg: flask.request.url})
    return default_url
