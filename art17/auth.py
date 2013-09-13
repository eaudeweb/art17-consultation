import flask
from flask.ext.principal import (Principal, Permission, Identity,
                                 RoleNeed, UserNeed)

auth = flask.Blueprint('auth', __name__)

principals = Principal(use_sessions=False)

admin_permission = Permission(RoleNeed('admin'))


def user_permission(user_id):
    return Permission(UserNeed(user_id))


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
    if flask.request.method == 'POST':
        set_session_auth(flask.request.form['user_id'],
                         flask.request.form.getlist('roles'))
        return flask.redirect(flask.url_for('.debug'))

    roles = flask.session.get('auth', {}).get('roles', [])
    return flask.render_template('auth_debug.html',
                                 user_id=flask.g.identity.id,
                                 roles=roles)


def set_session_auth(user_id=None, roles=[]):
    flask.session['auth'] = {'user_id': user_id, 'roles': roles}


@auth.before_app_request
def load_sessoin_auth():
    auth_data = flask.session.get('auth')
    if auth_data and auth_data.get('user_id'):
        identity = Identity(id=auth_data['user_id'],
                            auth_type='session')
        principals.set_identity(identity)

        identity.provides.add(UserNeed(identity.id))
        for role_name in auth_data.get('roles', []):
            identity.provides.add(RoleNeed(role_name))
