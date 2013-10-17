from collections import defaultdict
import flask
from art17 import models


dashboard = flask.Blueprint('dashboard', __name__)


@dashboard.route('/')
def index():
    session = models.db.session
    DH = models.DataHabitat
    DHR = models.DataHabitattypeRegion
    DHC = models.DataHabitattypeConclusion

    habitat_regions = {}
    for row in session.query(DHR.habitat_id, DHR.region):
        key = (int(row.habitat_id), row.region)
        habitat_regions[key] = True

    habitat_conclusion_count = defaultdict(int)
    for row in session.query(DHC.habitat_id, DHC.region):
        key = (int(row.habitat_id), row.region)
        habitat_conclusion_count[key] += 1

    return flask.render_template('dashboard/index.html', **{
        'bioreg_list': models.LuBiogeoreg.query.all(),
        'habitat_list': DH.query.join(DH.lu).all(),
        'habitat_regions': habitat_regions,
        'habitat_conclusion_count': dict(habitat_conclusion_count),
    })
