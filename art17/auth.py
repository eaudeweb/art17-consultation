from contextlib import contextmanager
import flask
from flask.ext.principal import (Principal, Permission, Identity,
                                 RoleNeed, UserNeed, PermissionDenied)
import ldap, ldap.filter

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
def inject_permissions():
    return {
        'admin_permission': admin_permission,
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


@auth.before_app_request
def load_debug_auth():
    if not flask.current_app.config.get('AUTH_DEBUG'):
        return

    auth_data = flask.session.get('auth')
    if auth_data and auth_data.get('user_id'):
        identity = Identity(id=auth_data['user_id'],
                            auth_type='session')
        principals.set_identity(identity)

        identity.provides.add(need.user_id(identity.id))
        identity.provides.add(need.authenticated)
        for role_name in auth_data.get('roles', []):
            identity.provides.add(RoleNeed(role_name))

    if 'identity' in flask.g:
        flask.g.identity.provides.add(need.everybody)


@auth.app_errorhandler(PermissionDenied)
def handle_permission_denied(error):
    return flask.render_template('auth/denied.html')


@contextmanager
def open_ldap_server():
    app = flask.current_app
    ldap_server = LdapServer(
        app.config.get('LDAP_SERVER', 'ldap://localhost'),
        app.config.get('LDAP_BASE_DN', ''),
        app.config.get('LDAP_LOGIN'),
    )
    try:
        yield ldap_server
    finally:
        ldap_server.close()


def get_value(attrs, name, default=None):
    values = attrs.get(name)
    return values[0].decode('utf-8') if values else default


def get_member_groups(attrs):
    for group_dn in attrs.get('memberOf', []):
        (attr, group_name) = group_dn.split(',', 1)[0].split('=')
        assert attr.lower() == 'cn'
        yield group_name


class LdapServer(object):

    def __init__(self, uri, base_dn, login=None):
        self.conn = ldap.initialize(uri)
        self.base_dn = base_dn
        if login is not None:
            (username, password) = login
            result = self.conn.bind_s(username, password)
            if result != (97, []):
                raise RuntimeError("LDAP login failed")

    def close(self):
        self.conn.unbind_s()

    def get_user_info(self, user_id):
        filters = ldap.filter.filter_format(
            '(&(objectClass=user)(cn=%s))',
            [user_id],
        )
        results = self.conn.search_s(
            self.base_dn,
            ldap.SCOPE_SUBTREE,
            filters,
            ['memberOf', 'givenName', 'mail', 'company'],
        )
        if len(results) < 1:
            raise RuntimeError("User %r not found" % user_id)
        dn, attrs = results[0]
        return {
            'name': get_value(attrs, 'givenName', ''),
            'email': get_value(attrs, 'mail', None),
            'company': get_value(attrs, 'company', None),
            'groups': list(get_member_groups(attrs)),
        }

    def get_emails_for_group(self, group_name):
        results = self.conn.search_s(
            self.base_dn,
            ldap.SCOPE_SUBTREE,
            '(objectClass=user)',
            ['memberOf', 'mail'],
        )
        rv = []
        for dn, attrs in results:
            if group_name in get_member_groups(attrs):
                email = get_value(attrs, 'mail', None)
                if email:
                    rv.append(email)
        return rv
