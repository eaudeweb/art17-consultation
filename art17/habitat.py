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
    habitat_code = flask.request.args.get('habitat', type=int)
    if habitat_code:
        habitat = (models.DataHabitat.query
                    .filter_by(habitatcode=habitat_code)
                    .first_or_404())
    else:
        habitat = None

    region_code = flask.request.args.get('region', '')
    if region_code:
        region = (models.LuBiogeoreg.query
                    .filter_by(code=region_code)
                    .first_or_404())
    else:
        region = None

    habitat_list = (models.DataHabitat.query
                        .join(models.DataHabitattypeRegion)
                        .order_by('habitatcode'))

    region_list = models.LuBiogeoreg.query.order_by('order_')

    if habitat:
        records = habitat.regions
        if region:
            records = records.filter_by(region=region.code)

    return flask.render_template('habitat/index.html', **{
        'habitat_list': [{'id': h.habitatcode, 'text': h.lu.hd_name}
                         for h in habitat_list],
        'current_habitat_code': habitat_code,
        'region_list': [{'id': r.code,
                         'text': r.name_ro}
                        for r in region_list],
        'current_region_code': region_code,

        'habitat': None if habitat is None else {
            'name': habitat.lu.hd_name,
            'code': habitat.habitatcode,
            'records': [HabitatRecord(r) for r in records],
        },
    })


@habitat.route('/habitate/detalii/<int:record_id>')
def detail(record_id):
    record = models.DataHabitattypeRegion.query.get_or_404(record_id)
    return flask.render_template('habitat/detail.html', **{
        'habitat': record.hr_habitat,
        'record': HabitatRecord(record),
    })


@habitat.route('/habitate/detalii/<int:record_id>/comment',
               methods=['GET', 'POST'])
def comment(record_id):
    record = models.DataHabitattypeRegion.query.get_or_404(record_id)

    if flask.request.method == 'POST':
        data = flask.request.json
        if data:
            if data.get('range-surface-area'):
                return flask.jsonify(saved=True)

    html = flask.render_template('habitat/comment.html', **{
        'habitat': record.hr_habitat,
        'record': HabitatRecord(record),
    })
    return flask.jsonify(html=html)
