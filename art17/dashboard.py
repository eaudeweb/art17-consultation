from collections import defaultdict
import flask
from sqlalchemy import func
from art17 import models


dashboard = flask.Blueprint('dashboard', __name__)


def get_tabmenu_data():
    yield {
        'url': flask.url_for('.habitats'),
        'label': "Habitate",
        'code': 'H',
    }
    for group in models.LuGrupSpecie.query:
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
    session = models.db.session
    Topic = models.Topic
    DH = models.DataHabitat
    DHC = models.DataHabitattypeComment

    habitat_list = DH.query.join(DH.lu).all()

    habitat_regions = {}
    for acons in Topic.query.filter(Topic.habitat_id != None):
        habitat_regions[acons.habitat_id, acons.region_code] = acons.id

    habitat_comment_count = dict(
        session.query(DHC.topic_id, func.count('*'))
            .group_by(DHC.topic_id)
    )

    return flask.render_template('dashboard/habitat.html', **{
        'bioreg_list': models.LuBiogeoreg.query.all(),
        'tabmenu_data': list(get_tabmenu_data()),
        'habitat_list': habitat_list,
        'habitat_regions': habitat_regions,
        'habitat_comment_count': habitat_comment_count,
    })


@dashboard.route('/specii/<group_code>')
def species(group_code):
    session = models.db.session
    Topic = models.Topic
    DS = models.DataSpecies
    DSC = models.DataSpeciesComment

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
    for acons in Topic.query.filter(Topic.species_id != None):
        species_regions[acons.species_id, acons.region_code] = acons.id

    species_comment_count = dict(
        session.query(DSC.topic_id, func.count('*'))
            .group_by(DSC.topic_id)
    )

    return flask.render_template('dashboard/species.html', **{
        'bioreg_list': models.LuBiogeoreg.query.all(),
        'tabmenu_data': list(get_tabmenu_data()),
        'species_group': species_group,
        'species_list': species_list,
        'species_regions': species_regions,
        'species_comment_count': species_comment_count,
    })


@dashboard.route('/')
def index():
    return flask.redirect(flask.url_for('.habitats'))
