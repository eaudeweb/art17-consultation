import flask
from path import path
from sqlalchemy import or_
from art17.models import Dataset

consultation = flask.Blueprint('consultation', __name__)


def get_datasets():
    return Dataset.query.filter(
        or_(Dataset.preview==False, Dataset.preview==None)
    )


@consultation.app_context_processor
def inject_consants():
    return dict(
        home_url=flask.url_for('consultation.home'),
        app_name='consultation',
        datasets=get_datasets(),
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


@consultation.route('/export/<export_name>')
@consultation.route('/export/')
def export(export_name=None):
    from art17.scripts.xml_reports import (
        xml_habitats, xml_habitats_checklist, xml_species,
        xml_species_checklist,
    )
    KNOWN_EXPORTS = {
        'xml_habitats': xml_habitats,
        'xml_habitats_checklist': xml_habitats_checklist,
        'xml_species': xml_species,
        'xml_species_checklist': xml_species_checklist,
    }
    if export_name is None:
        return flask.Response("Known exports: %s" % KNOWN_EXPORTS.keys())
    if export_name not in KNOWN_EXPORTS:
        flask.abort(404)

    data = KNOWN_EXPORTS[export_name]()
    return flask.Response(data, mimetype='text/xml')
