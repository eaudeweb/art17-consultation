import flask
from werkzeug.utils import cached_property
from art17.app import models
from art17.common import GenericRecord


species = flask.Blueprint('species', __name__)


class SpeciesRecord(GenericRecord):

    @cached_property
    def region(self):
        return self.row.region

    @cached_property
    def range(self):
        return {
            'method': self.row.range_method,
            'surface_area': self.row.range_surface_area,
            'trend': self._get_trend('range'),
            'conclusion': self._get_conclusion('range'),
            'reference_value': self._get_reference_value('range'),
        }

    def _get_population_size_and_unit(self):
        if self.row.population_size_unit:
            min_size = self.row.population_minimum_size
            max_size = self.row.population_minimum_size
            unit = self.row.population_size_unit

        else:
            min_size = self.row.population_alt_minimum_size
            max_size = self.row.population_alt_minimum_size
            unit = self.row.population_alt_size_unit

        if min_size == max_size:
            return "%s %s" % (min_size, unit)

        else:
            return "%s-%s %s" % (min_size, max_size, unit)

    def _get_population_trend(self, qualifier=''):
        base_info = self._get_trend('population', qualifier)
        magnitude_min = getattr(self.row, 'population_trend%s_magnitude_min' % qualifier)
        magnitude_max = getattr(self.row, 'population_trend%s_magnitude_max' % qualifier)
        magnitude_ci = getattr(self.row, 'population_trend%s_magnitude_ci' % qualifier)
        method = getattr(self.row, 'population_trend%s_method' % qualifier)
        return "%s method=%s magnitude=(min=%s max=%s ci=%s)" % (
            base_info, method, magnitude_min, magnitude_max, magnitude_ci)

    def _get_habitat_quality(self):
        value = self.row.habitat_quality
        explanation = self.row.habitat_quality_explanation
        if explanation:
            return "%s (%s)" % (value, explanation)
        else:
            return "%s" % value

    @cached_property
    def population(self):
        return {
            'size_and_unit': self._get_population_size_and_unit(),
            'conclusion': self._get_conclusion('population'),
            'trend_short': self._get_population_trend(),
            'trend_long': self._get_population_trend('_long'),
            'reference_value': self._get_reference_value('population'),
        }

    @cached_property
    def habitat(self):
        return {
            'surface_area': self.row.habitat_surface_area,
            'method': self.row.habitat_method,
            'conclusion': self._get_conclusion('habitat'),
            'trend_short': self._get_trend('habitat'),
            'trend_long': self._get_trend('habitat', '_long'),
            'area_suitable': self.row.habitat_area_suitable,
            'quality': self._get_habitat_quality(),
        }

    @cached_property
    def future_prospects(self):
        return self._get_conclusion('future')

    @cached_property
    def overall_assessment(self):
        return self._get_conclusion('assessment')


@species.route('/specii/')
def species_index():
    return flask.render_template('species/index.html', **{
        'records': list(models.DataSpecies.query.order_by('speciescode')),
    })


@species.route('/specii/<speciescode>')
def species_view(speciescode):
    species = models.DataSpecies.query.filter_by(
        speciescode=speciescode).first_or_404()
    checklist = models.DataSpeciesCheckList.query.filter_by(
        natura_2000_code=species.speciescode,
        member_state=species.country)
    return flask.render_template('species/view.html', **{
        'code': species.speciescode,
        'name': checklist[0].species_name,
        'bio_regions': [c.bio_region for c in checklist],
        'annex_II': checklist[0].annex_ii == 'Y',
        'annex_IV': checklist[0].annex_iv == 'Y',
        'annex_V': checklist[0].annex_v == 'Y',
        'records': [SpeciesRecord(r) for r in species.regions],
    })
