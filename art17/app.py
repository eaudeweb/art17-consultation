import flask
from flask.ext.script import Manager
from path import path

views = flask.Blueprint('views', __name__)
REPO_ROOT = path(__file__).abspath().parent.parent


@views.route('/')
def home():
    return flask.render_template('home.html')


@views.route('/_crashme')
def crashme():
    raise RuntimeError("Crashing, as requested.")


@views.route('/_ping')
def ping():
    from art17 import models
    from datetime import datetime
    count = models.History.query.count()
    now = datetime.utcnow().isoformat()
    return "art17 consultation is up; %s; %d history items" % (now, count)


@views.route('/guide')
def guide():
    return flask.render_template('guide.html')


@views.app_url_defaults
def bust_cache(endpoint, values):
    if endpoint == 'static':
        filename = values['filename']
        file_path = path(flask.current_app.static_folder) / filename
        if file_path.exists():
            mtime = file_path.stat().st_mtime
            key = ('%x' % mtime)[-6:]
            values['t'] = key


def none_as_blank(value):
    if value is None:
        value = ''
    return value


def create_app():
    from art17.auth import auth
    from art17.common import common
    from art17.species import species
    from art17.habitat import habitat
    from art17 import models
    from art17.admin import admin
    from art17.replies import replies
    from art17.history import history
    from art17.dashboard import dashboard
    from art17.notifications import notifications

    app = flask.Flask(__name__, instance_relative_config=True)
    app.jinja_options = dict(
        app.jinja_options,
        extensions=app.jinja_options['extensions'] + ['jinja2.ext.do'],
        finalize=none_as_blank)
    app.config.from_pyfile('settings.py', silent=True)
    app.config.from_pyfile(REPO_ROOT / 'settings.py', silent=True)
    app.register_blueprint(auth)
    app.register_blueprint(views)
    app.register_blueprint(common)
    app.register_blueprint(species)
    app.register_blueprint(habitat)
    app.register_blueprint(replies)
    app.register_blueprint(history)
    app.register_blueprint(dashboard, url_prefix='/dashboard')
    app.register_blueprint(notifications)
    models.db.init_app(app)
    admin.init_app(app)

    if app.config.get('SENTRY_DSN'):
        from raven.contrib.flask import Sentry
        Sentry(app)

    return app


def create_manager(app):
    from art17.models import db_manager
    from art17.common import cons_manager
    manager = Manager(app)
    manager.add_command('db', db_manager)
    manager.add_command('cons', cons_manager)

    @manager.command
    def waitress():
        from waitress import serve
        app = flask.current_app
        host = app.config.get('ART17_LISTEN_HOST', '127.0.0.1')
        port = app.config.get('ART17_LISTEN_PORT', 5000)
        serve(app.wsgi_app, host=host, port=port)

    return manager


if __name__ == '__main__':
    manager.run()
