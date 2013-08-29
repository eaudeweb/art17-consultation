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
        surface_area = self.row.range_surface_area
        return {
            'method': self.row.range_method,
            'surface_area': surface_area,
            'trend': self._get_trend('range'),
            'conclusion': self._get_conclusion('range'),
            'reference_value': self._get_reference_value('range',
                                                         surface_area),
        }

    def _get_population_size(self):
        rv = []
        for qualifier in ['', '_alt']:
            min_size = getattr(self.row, 'population%s_minimum_size'
                                         % qualifier)
            max_size = getattr(self.row, 'population%s_maximum_size'
                                         % qualifier)
            unit = getattr(self.row, 'population%s_size_unit' % qualifier)

            if unit:
                rv.append({
                    'min': min_size,
                    'max': max_size,
                    'unit': unit,
                })

        return rv

    def _get_population_trend(self, qualifier=''):
        base_info = self._get_trend('population', qualifier)
        magnitude_min = getattr(self.row,
                'population_trend%s_magnitude_min' % qualifier)
        magnitude_max = getattr(self.row,
                'population_trend%s_magnitude_max' % qualifier)
        magnitude_ci = getattr(self.row,
                'population_trend%s_magnitude_ci' % qualifier)
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
        ref_value_ideal = (self.row.population_minimum_size or
                           self.row.population_alt_minimum_size)
        return {
            'size': self._get_population_size(),
            'conclusion': self._get_conclusion('population'),
            'trend_short': self._get_population_trend(),
            'trend_long': self._get_population_trend('_long'),
            'reference_value': self._get_reference_value('population',
                                                         ref_value_ideal),
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
    group_code = flask.request.args.get('group')
    if group_code:
        group = (models.LuGrupSpecie.query
                    .filter_by(code=group_code)
                    .first_or_404())
    else:
        group = None

    species_code = flask.request.args.get('species')
    if species_code:
        species = (models.LuHdSpecies.query
                    .filter_by(speciescode=species_code)
                    .first_or_404())
    else:
        species = None

    species_list = models.LuHdSpecies.query.order_by('speciesname')
    if group:
        species_list = species_list.filter_by(group_code=group.code)

    if species:
        records = (models.DataSpeciesRegion.query
                        .filter_by(sr_species=species.data))

    return flask.render_template('species/index.html', **{
        'species_groups': models.LuGrupSpecie.query.all(),
        'current_group': group,
        'species_list': species_list.all(),
        'current_species': species,

        'species': None if species is None else {
            'code': species.speciescode,
            'name': species.speciesname,
            'annex_II': species.annexii == 'Y',
            'annex_IV': species.annexiv == 'Y',
            'annex_V': species.annexv == 'Y',
            'records': [SpeciesRecord(r) for r in records],
        },
    })
