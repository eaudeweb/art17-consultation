import flask
from flask.ext.principal import Principal, Permission, RoleNeed, Identity

auth = flask.Blueprint('auth', __name__)

principals = Principal(use_sessions=False)

admin_permission = Permission(RoleNeed('admin'))


@auth.record
def register_principals(state):
    app = state.app
    principals.init_app(app)


@auth.route('/auth_debug', methods=['GET', 'POST'])
def debug():
    if flask.request.method == 'POST':
        flask.session['user_id'] = flask.request.form['user_id']
        return flask.redirect(flask.url_for('.debug'))

    return flask.render_template('auth_debug.html',
                                 user_id=flask.g.identity.id)


@auth.before_app_request
def debug_load_user():
    user_id = flask.session.get('user_id')
    if user_id:
        identity = Identity(id=user_id, auth_type='session')
        principals.set_identity(identity)
