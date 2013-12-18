import flask
from path import path

consultation = flask.Blueprint('consultation', __name__)


@consultation.app_context_processor
def inject_home_url():
    return dict(home_url=flask.url_for('consultation.home'),
                app_name='consultation',
    )


@consultation.route('/')
def home():
    return flask.render_template('consultation/home.html')


@consultation.route('/_crashme')
def crashme():
    raise RuntimeError("Crashing, as requested.")


@consultation.route('/_ping')
def ping():
    from art17 import models
    from datetime import datetime
    count = models.History.query.count()
    now = datetime.utcnow().isoformat()
    return "art17 consultation is up; %s; %d history items" % (now, count)


@consultation.app_url_defaults
def bust_cache(endpoint, values):
    if endpoint == 'static':
        filename = values['filename']
        file_path = path(flask.current_app.static_folder) / filename
        if file_path.exists():
            mtime = file_path.stat().st_mtime
            key = ('%x' % mtime)[-6:]
            values['t'] = key
