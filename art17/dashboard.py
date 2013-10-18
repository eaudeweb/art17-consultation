from collections import defaultdict
import flask
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


@dashboard.route('/habitate')
def habitats():
    session = models.db.session
    DH = models.DataHabitat
    DHR = models.DataHabitattypeRegion
    DHC = models.DataHabitattypeConclusion

    habitat_list = DH.query.join(DH.lu).all()

    habitat_regions = {}
    for row in session.query(DHR.habitat_id, DHR.region):
        key = (int(row.habitat_id), row.region)
        habitat_regions[key] = True

    habitat_conclusion_count = defaultdict(int)
    for row in session.query(DHC.habitat_id, DHC.region):
        key = (int(row.habitat_id), row.region)
        habitat_conclusion_count[key] += 1

    return flask.render_template('dashboard/habitat.html', **{
        'bioreg_list': models.LuBiogeoreg.query.all(),
        'tabmenu_data': list(get_tabmenu_data()),
        'habitat_list': habitat_list,
        'habitat_regions': habitat_regions,
        'habitat_conclusion_count': dict(habitat_conclusion_count),
    })


@dashboard.route('/specii/<group_code>')
def species(group_code):
    session = models.db.session
    DS = models.DataSpecies
    DSR = models.DataSpeciesRegion
    DSC = models.DataSpeciesConclusion

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
    for row in session.query(DSR.species_id, DSR.region):
        key = (int(row.species_id), row.region)
        species_regions[key] = True

    species_conclusion_count = defaultdict(int)
    for row in session.query(DSC.species_id, DSC.region):
        key = (int(row.species_id), row.region)
        species_conclusion_count[key] += 1

    return flask.render_template('dashboard/species.html', **{
        'bioreg_list': models.LuBiogeoreg.query.all(),
        'tabmenu_data': list(get_tabmenu_data()),
        'species_group': species_group,
        'species_list': species_list,
        'species_regions': species_regions,
        'species_conclusion_count': dict(species_conclusion_count),
    })


@dashboard.route('/')
def index():
    return flask.redirect(flask.url_for('.habitats'))
