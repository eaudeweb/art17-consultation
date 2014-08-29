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


def consultation_url(subject, bioreg):
    if isinstance(subject, models.DataHabitat):
        return flask.url_for(
            'habitat.index',
            region=bioreg,
            habitat=subject.code,
        )

    elif isinstance(subject, models.DataSpecies):
        return flask.url_for(
            'species.index',
            region=bioreg,
            species=subject.code,
        )

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
    from art17.habitat import get_dal
    habitat_dataset = get_dal()
    if not habitat_dataset:
        flask.flash('No active consultation', 'danger')
        return flask.redirect('/')
    user_id = flask.g.identity.id
    data_by_region = (
        habitat_dataset
        .get_subject_region_overview_consultation(user_id)
    )
    relevant_regions = set(reg for n, reg in data_by_region)
    bioreg_list = [
        r for r in dal.get_biogeo_region_list()
        if r.code in relevant_regions
    ]

    return flask.render_template(
        'consultation/habitat.html', **{
        'bioreg_list': bioreg_list,
        'tabmenu_data': list(get_tabmenu_data()),
        'habitat_list': dal.get_habitat_list(),
        'data_by_region': data_by_region,
    })


@dashboard.route('/specii/<group_code>')
def species(group_code):
    from art17.species import get_dal
    species_dataset = get_dal()
    if not species_dataset:
        flask.flash('No active consultation', 'danger')
        return flask.redirect('/')
    user_id = flask.g.identity.id
    data_by_region = (
        species_dataset
        .get_subject_region_overview_consultation(user_id)
    )
    relevant_regions = set(reg for n, reg in data_by_region)
    bioreg_list = [
        r for r in dal.get_biogeo_region_list()
        if r.code in relevant_regions
    ]

    return flask.render_template(
        'consultation/species.html', **{
        'bioreg_list': bioreg_list,
        'tabmenu_data': list(get_tabmenu_data()),
        'species_group': dal.get_species_group(group_code),
        'species_list': dal.get_species_list(group_code=group_code),
        'data_by_region': data_by_region,
    })


@dashboard.route('/')
def index():
    return flask.redirect(flask.url_for('.habitats'))
