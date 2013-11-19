from collections import defaultdict
import flask
from art17 import models
from art17 import dal


dashboard = flask.Blueprint('dashboard', __name__)


def get_tabmenu_data():
    yield {
        'url': flask.url_for('.habitats'),
        'label': "Habitate",
        'code': 'H',
    }
    for group in dal.get_species_groups():
        yield {
            'url': flask.url_for('.species', group_code=group.code),
            'label': group.description,
            'code': 'S' + group.code,
        }


def consultation_url(subject, bioreg=None):
    args = {}
    if bioreg:
        args['region'] = bioreg

    if isinstance(subject, models.DataHabitat):
        args['habitat'] = subject.code
        return flask.url_for('habitat.index', **args)

    elif isinstance(subject, models.DataSpecies):
        args['species'] = subject.code
        return flask.url_for('species.index', **args)

    else:
        raise RuntimeError("Unknown object %r" % subject)


@dashboard.context_processor
def inject_funcs():
    return {
        'get_tabmenu_data': get_tabmenu_data,
        'consultation_url': consultation_url,
    }


@dashboard.route('/habitate')
def habitats():
    habitat_dataset = dal.HabitatDataset()

    return flask.render_template('dashboard/habitat.html', **{
        'bioreg_list': dal.get_biogeo_regions(),
        'tabmenu_data': list(get_tabmenu_data()),
        'habitat_list': dal.get_habitat_list(),
        'habitat_regions': habitat_dataset.get_habitat_region_overview(),
    })


@dashboard.route('/specii/<group_code>')
def species(group_code):
    species_dataset = dal.SpeciesDataset()

    return flask.render_template('dashboard/species.html', **{
        'bioreg_list': dal.get_biogeo_regions(),
        'tabmenu_data': list(get_tabmenu_data()),
        'species_group': dal.get_species_group(group_code),
        'species_list': dal.get_species_list(group_code=group_code),
        'species_regions': species_dataset.get_species_region_overview(),
    })


@dashboard.route('/')
def index():
    return flask.redirect(flask.url_for('.habitats'))
