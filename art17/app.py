import flask
from flask.ext.script import Manager
from path import path

views = flask.Blueprint('views', __name__)


@views.route('/')
def home():
    return flask.render_template('home.html')


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

    app = flask.Flask(__name__, instance_relative_config=True)
    app.jinja_options = dict(
        app.jinja_options,
        extensions=app.jinja_options['extensions'] + ['jinja2.ext.do'],
        finalize=none_as_blank)
    app.config.from_pyfile('settings.py', silent=True)
    app.register_blueprint(auth)
    app.register_blueprint(views)
    app.register_blueprint(common)
    app.register_blueprint(species)
    app.register_blueprint(habitat)
    models.db.init_app(app)
    admin.init_app(app)

    return app


def create_manager():
    from art17.models import db_manager
    manager = Manager(create_app)
    manager.add_command('db', db_manager)
    return manager


if __name__ == '__main__':
    manager.run()
