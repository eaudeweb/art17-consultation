import flask
from werkzeug.utils import cached_property
from art17.app import models
from art17.common import GenericRecord

habitat = flask.Blueprint('habitat', __name__)


class HabitatRecord(GenericRecord):

    @cached_property
    def region(self):
        return self.row.region

    @cached_property
    def range(self):
        surface_area = self.row.range_surface_area
        return {
            'surface_area': surface_area,
            'conclusion': self._get_conclusion('range'),
            'trend': self._get_trend('range'),
            'reference_value': self._get_reference_value('range', surface_area),
        }

    @cached_property
    def area(self):
        surface_area = self.row.coverage_surface_area
        return {
            'surface_area': surface_area,
            'trend': self._get_trend('coverage'),
            'conclusion': self._get_conclusion('area'),
            'reference_value': self._get_reference_value('area', surface_area),
        }

    @cached_property
    def structure(self):
        return self._get_conclusion('structure')

    @cached_property
    def future_prospects(self):
        return self._get_conclusion('future')

    @cached_property
    def overall_assessment(self):
        return self._get_conclusion('assessment')


@habitat.route('/habitate/')
def index():
    habitat_list = (models.DataHabitat.query
                        .join(models.DataHabitattypeRegion)
                        .order_by('habitatcode'))

    habitat_code = flask.request.args.get('habitat', type=int)

    return flask.render_template('habitat/index.html', **{
        'habitat_list': [{'id': h.habitatcode, 'text': h.lu.hd_name}
                         for h in habitat_list],
        'current_habitat_code': habitat_code,
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
