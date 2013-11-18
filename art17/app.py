import flask
from flask.ext.script import Manager, Server, Option
from path import path

REPO_ROOT = path(__file__).abspath().parent.parent


def none_as_blank(value):
    if value is None:
        value = ''
    return value


def create_app():
    from art17.auth import auth
    from art17 import models

    app = flask.Flask(__name__, instance_relative_config=True)
    app.jinja_options = dict(
        app.jinja_options,
        extensions=app.jinja_options['extensions'] + ['jinja2.ext.do'],
        finalize=none_as_blank)
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 240  # 4 minutes
    app.config.from_pyfile('settings.py', silent=True)
    app.config.from_pyfile(REPO_ROOT / 'settings.py', silent=True)
    app.register_blueprint(auth)
    models.db.init_app(app)

    if app.config.get('SENTRY_DSN'):
        from raven.contrib.flask import Sentry
        Sentry(app)

    return app


def create_consultation_app():
    from art17.consultation import consultation
    from art17.common import common
    from art17.species import species
    from art17.habitat import habitat
    from art17.admin import admin
    from art17.replies import replies
    from art17.history import history
    from art17.dashboard import dashboard
    from art17.notifications import notifications

    app = create_app()
    app.register_blueprint(consultation)
    app.register_blueprint(common)
    app.register_blueprint(species)
    app.register_blueprint(habitat)
    app.register_blueprint(replies)
    app.register_blueprint(history)
    app.register_blueprint(dashboard, url_prefix='/dashboard')
    app.register_blueprint(notifications)
    admin.init_app(app)

    return app


def create_aggregation_app():
    app = create_app()

    @app.route('/')
    def home():
        return 'aggregation home'

    return app


def create_app_by_name(app_name):
    if app_name == 'consultation':
        return create_consultation_app()

    elif app_name == 'aggregation':
        return create_aggregation_app()

    else:
        raise RuntimeError("Unknown application %r" % app_name)


class Art17Server(Server):

    def get_options(self):
        options = super(Art17Server, self).get_options()
        options += (
            Option('app_name', default='consultation'),
        )
        return options

    def handle(self, app, app_name, *args, **kwargs):
        http_app = create_app_by_name(app_name)
        return super(Art17Server, self).handle(http_app, *args, **kwargs)


def create_manager(app):
    from art17.models import db_manager
    from art17.common import cons_manager

    manager = Manager(app)
    manager.add_command('db', db_manager)
    manager.add_command('cons', cons_manager)
    manager.add_command('runserver', Art17Server())

    @manager.command
    def waitress(app_name):
        from waitress import serve
        http_app = create_app_by_name(app_name)
        host = http_app.config.get('ART17_LISTEN_HOST', '127.0.0.1')
        port = http_app.config.get('ART17_LISTEN_PORT', 5000)
        serve(http_app.wsgi_app, host=host, port=port)

    return manager


def main():
    import os
    import logging
    os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.UTF8'  # encoding for cx_oracle
    logging.basicConfig()
    logging.getLogger('werkzeug').setLevel(logging.INFO)
    app = create_app()
    if app.config.get('SQL_DEBUG'):
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    create_manager(app).run()
