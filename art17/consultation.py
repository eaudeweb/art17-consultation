import flask
from path import path

from art17.common import get_datasets
from art17.models import Dataset
from art17.habitat import get_dataset as get_habitat_dataset
from art17.species import get_dataset as get_species_dataset


consultation = flask.Blueprint('consultation', __name__)


def get_current_dataset():
    from art17 import config
    dataset_id = config.get_config_value('CONSULTATION_DATASET')
    return Dataset.query.get(dataset_id) or None


def get_reports_data(overview):
    sections = ['reports', 'comments', 'replies']
    reports_data = {
        'final': {section: 0 for section in sections},
        'notfinal': {section: 0 for section in sections},
    }
    record_ids = set([])
    for record, data in overview.iteritems():
        target = 'final' if 'final_record' in data else 'notfinal'
        reports_data[target]['reports'] += 1
        reports_data[target]['comments'] += data['count']
        reports_data[target]['replies'] += data['with_reply']
        record_ids.add(record[0])
    reports_data['all'] = {
        section:
        reports_data['final'][section] + reports_data['notfinal'][section]
        for section in sections
    }
    return reports_data, len(record_ids)


@consultation.app_context_processor
def inject_consants():
    return dict(
        home_url=flask.url_for('consultation.home'),
        app_name='consultation',
        datasets=get_datasets(),
        current_dataset=get_current_dataset(),
    )


@consultation.route('/')
def home():
    habitat_dataset = get_habitat_dataset()
    habitat_overview = (
        habitat_dataset
        .get_subject_region_overview_consultation(flask.g.identity.id)
    )
    habitat_details, habitat_count = get_reports_data(habitat_overview)

    species_dataset = get_species_dataset()
    species_overview = (
        species_dataset
        .get_subject_region_overview_consultation(flask.g.identity.id)
    )
    species_details, species_count = get_reports_data(species_overview)

    return flask.render_template(
        'consultation/home.html', **{
            'habitat_details': habitat_details,
            'habitat_count': habitat_count,
            'species_details': species_details,
            'species_count': species_count,
        })


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
