import flask
from werkzeug.utils import cached_property
from art17 import models
from art17.common import GenericRecord
from art17 import forms

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
            'trend_short': self._get_trend('range'),
            'trend_long': self._get_trend('range', '_long'),
            'magnitude_short': self._get_magnitude('range'),
            'magnitude_long': self._get_magnitude('range', '_long'),
            'reference_value': self._get_reference_value('range', surface_area),
        }

    @cached_property
    def area(self):
        surface_area = self.row.coverage_surface_area
        return {
            'surface_area': surface_area,
            'trend_short': self._get_trend('coverage'),
            'trend_long': self._get_trend('coverage', '_long'),
            'magnitude_short': self._get_magnitude('coverage'),
            'magnitude_long': self._get_magnitude('coverage', '_long'),
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


@habitat.route('/habitate/regiuni/<int:habitat_code>')
def lookup_regions(habitat_code):
    habitat = (models.DataHabitat.query
                .filter_by(habitatcode=habitat_code)
                .first_or_404())
    regions = [{'id': r.lu.code, 'text': r.lu.name_ro}
               for r in habitat.regions.join(models.DataHabitattypeRegion.lu)]
    return flask.jsonify(options=regions)


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

    if habitat:
        records = habitat.regions
        if region:
            records = records.filter_by(region=region.code)

    return flask.render_template('habitat/index.html', **{
        'habitat_list': [{'id': h.habitatcode, 'text': h.lu.hd_name}
                         for h in habitat_list],
        'current_habitat_code': habitat_code,
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


@habitat.route('/habitate/detalii/<int:record_id>/comentariu',
               methods=['GET', 'POST'])
def comment(record_id):
    record = models.DataHabitattypeRegion.query.get_or_404(record_id)
    form = forms.SpeciesComment(flask.request.form)
    next_url = flask.request.args.get('next')

    if flask.request.method == 'POST' and form.validate():
        comment = models.DataHabitattypeComment(
            hr_habitat_id=record.hr_habitat_id,
            region=record.region)

        form.populate_obj(comment)

        models.db.session.add(comment)
        models.db.session.commit()

        return flask.render_template('habitat/comment-saved.html', **{
            'habitat': record.hr_habitat,
            'record': HabitatRecord(record),
            'next_url': next_url,
        })

    return flask.render_template('habitat/comment.html', **{
        'habitat': record.hr_habitat,
        'record': HabitatRecord(record),
        'form': form,
        'next_url': next_url,
    })
