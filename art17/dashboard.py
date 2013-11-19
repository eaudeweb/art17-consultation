from collections import defaultdict
import flask
from sqlalchemy import func
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
    DH = models.DataHabitat
    DHR = models.DataHabitattypeRegion

    habitat_list = DH.query.join(DH.lu).all()

    habitat_regions = {}
    habitat_regions_query = (
        models.db.session
        .query(DHR.habitat_id, DHR.region)
        .filter_by(cons_role='assessment')
    )
    for key in habitat_regions_query:
        habitat_regions[key] = 0

    habitat_comment_count_query = (
        models.db.session
        .query(DHR.habitat_id, DHR.region, func.count('*'))
        .filter_by(cons_role='comment')
        .group_by(DHR.habitat_id, DHR.region)
    )
    for (habitat_id, region_code, count) in habitat_comment_count_query:
        habitat_regions[habitat_id, region_code] = count

    return flask.render_template('dashboard/habitat.html', **{
        'bioreg_list': dal.get_biogeo_regions(),
        'tabmenu_data': list(get_tabmenu_data()),
        'habitat_list': habitat_list,
        'habitat_regions': habitat_regions,
    })


@dashboard.route('/specii/<group_code>')
def species(group_code):
    DS = models.DataSpecies
    DSR = models.DataSpeciesRegion

    species_group = (
        models.LuGrupSpecie.query
        .filter_by(code=group_code)
        .first()
    )

    species_list = (
        DS.query
        .join(DS.lu)
        .filter(models.LuHdSpecies.group_code == group_code)
        .all()
    )

    species_regions = {}
    species_regions_query = (
        models.db.session
        .query(DSR.species_id, DSR.region)
        .filter_by(cons_role='assessment')
    )
    for key in species_regions_query:
        species_regions[key] = 0

    species_comment_count_query = (
        models.db.session
        .query(DSR.species_id, DSR.region, func.count('*'))
        .filter_by(cons_role='comment')
        .group_by(DSR.species_id, DSR.region)
    )
    for (species_id, region_code, count) in species_comment_count_query:
        species_regions[species_id, region_code] = count

    return flask.render_template('dashboard/species.html', **{
        'bioreg_list': dal.get_biogeo_regions(),
        'tabmenu_data': list(get_tabmenu_data()),
        'species_group': species_group,
        'species_list': species_list,
        'species_regions': species_regions,
    })


@dashboard.route('/')
def index():
    return flask.redirect(flask.url_for('.habitats'))
