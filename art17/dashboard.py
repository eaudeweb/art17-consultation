from collections import defaultdict
from itertools import groupby
import flask
from art17 import models


dashboard = flask.Blueprint('dashboard', __name__)


@dashboard.route('/')
def index():
    session = models.db.session
    DH = models.DataHabitat
    DHR = models.DataHabitattypeRegion
    DHC = models.DataHabitattypeConclusion
    DS = models.DataSpecies
    DSR = models.DataSpeciesRegion
    DSC = models.DataSpeciesConclusion

    habitat_list = DH.query.join(DH.lu).all()

    habitat_regions = {}
    for row in session.query(DHR.habitat_id, DHR.region):
        key = (int(row.habitat_id), row.region)
        habitat_regions[key] = True

    habitat_conclusion_count = defaultdict(int)
    for row in session.query(DHC.habitat_id, DHC.region):
        key = (int(row.habitat_id), row.region)
        habitat_conclusion_count[key] += 1

    species_group_list = models.LuGrupSpecie.query.all()
    species_list = (
        DS.query
        .join(DS.lu)
        .order_by(models.LuHdSpecies.group_code)
        .all()
    )
    species_by_group = {
        g: list(items)
        for g, items
        in groupby(species_list, lambda s: s.lu.group_code)
    }

    species_regions = {}
    for row in session.query(DSR.species_id, DSR.region):
        key = (int(row.species_id), row.region)
        species_regions[key] = True

    species_conclusion_count = defaultdict(int)
    for row in session.query(DSC.species_id, DSC.region):
        key = (int(row.species_id), row.region)
        species_conclusion_count[key] += 1

    return flask.render_template('dashboard/index.html', **{
        'bioreg_list': models.LuBiogeoreg.query.all(),

        'habitat_list': habitat_list,
        'habitat_regions': habitat_regions,
        'habitat_conclusion_count': dict(habitat_conclusion_count),

        'species_group_list': species_group_list,
        'species_by_group': species_by_group,
        'species_regions': species_regions,
        'species_conclusion_count': dict(species_conclusion_count),
    })
