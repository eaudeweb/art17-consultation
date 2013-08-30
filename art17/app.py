import flask
from flask.ext.script import Manager
from werkzeug.local import LocalProxy
from path import path

models = LocalProxy(lambda: flask.current_app.extensions['art17_models'])

from art17.species import species
from art17.habitat import habitat

views = flask.Blueprint('views', __name__)


@views.route('/')
def home():
    return 'hello art17'


@views.app_url_defaults
def bust_cache(endpoint, values):
    if endpoint == 'static':
        filename = values['filename']
        file_path = path(flask.current_app.static_folder) / filename
        if file_path.exists():
            mtime = file_path.stat().st_mtime
            key = ('%x' % mtime)[-6:]
            values['t'] = key


def script_later(code):
    flask.g.script_later = (flask.g.get('script_later') or '') + code


@views.app_context_processor
def inject_script_tools():
    return {'script_later': script_later}


def create_app():
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('settings.py', silent=True)
    app.register_blueprint(views)
    app.register_blueprint(species)
    app.register_blueprint(habitat)

    if app.config.get('USE_MDB_MODELS'):
        from art17 import models_mdb as _models
    else:
        from art17 import models as _models
    app.extensions['art17_models'] = _models
    _models.db.init_app(app)

    return app


manager = Manager(create_app)


if __name__ == '__main__':
    manager.run()
