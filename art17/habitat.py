import flask
from werkzeug.utils import cached_property
from art17.app import models
from art17.common import GenericRecord

habitat = flask.Blueprint('habitat', __name__)


class HabitatRecord(GenericRecord):

    @cached_property
    def id(self):
        return self.row.hr_id

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
    if habitat_code:
        habitat = (models.DataHabitat.query
                    .filter_by(habitatcode=habitat_code)
                    .first_or_404())
    else:
        habitat = None

    return flask.render_template('habitat/index.html', **{
        'habitat_list': [{'id': h.habitatcode, 'text': h.lu.hd_name}
                         for h in habitat_list],
        'current_habitat_code': habitat_code,
        'habitat': None if habitat is None else {
            'name': habitat.lu.hd_name,
            'code': habitat.habitatcode,
            'records': [HabitatRecord(r) for r in habitat.regions],
        },
    })


@habitat.route('/habitate/detalii/<int:record_id>')
def detail(record_id):
    record = models.DataHabitattypeRegion.query.get_or_404(record_id)
    return flask.render_template('habitat/detail.html', **{
        'habitat': record.hr_habitat,
        'record': HabitatRecord(record),
    })
