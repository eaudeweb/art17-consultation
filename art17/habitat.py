import flask
from werkzeug.utils import cached_property
from art17 import models

habitat = flask.Blueprint('habitat', __name__)


class HabitatRecord(object):

    def __init__(self, row):
        self.row = row

    @cached_property
    def region(self):
        return self.row.region


@habitat.route('/habitate/')
def habitats_index():
    return flask.render_template('habitat/index.html', **{
        'records': list(models.DataHabitat.query.order_by('habitatcode')),
    })


@habitat.route('/habitate/<habitatcode>')
def habitat_view(habitatcode):
    habitat = models.DataHabitat.query.filter_by(
        habitatcode=habitatcode).first_or_404()
    checklist = models.DataHabitatsCheckList.query.filter_by(
        natura_2000_code=habitat.habitatcode,
        ms=habitat.country,
        presence="1")
    return flask.render_template('habitat/view.html', **{
        'code': habitat.habitatcode,
        'name': checklist[0].valid_name,
        'bio_regions': [c.bio_region for c in checklist],
        'records': [HabitatRecord(r) for r in habitat.regions],
    })
