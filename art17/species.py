# encoding: utf-8

import flask
from werkzeug.utils import cached_property
from art17.app import models
from art17.common import GenericRecord


species = flask.Blueprint('species', __name__)


TREND_NAME = {
    "+": u"În creștere",
    "-": u"În scădere",
    "0": u"Stabil",
    "x": u"Necunoscut",
}


@species.app_context_processor
def inject_constants():
    return {'TREND_NAME': TREND_NAME}


class SpeciesRecord(GenericRecord):

    @cached_property
    def id(self):
        return self.row.sr_id

    @cached_property
    def region(self):
        return self.row.region

    @cached_property
    def range(self):
        surface_area = self.row.range_surface_area

        return {
            'method': self.row.range_method,
            'surface_area': surface_area,
            'trend_short': self._get_trend('range'),
            'trend_long': self._get_trend('range', '_long'),
            'magnitude_short': self._get_magnitude('range'),
            'magnitude_long': self._get_magnitude('range', '_long'),
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
        return {
            'value': value,
            'explanation': explanation,
        }

    @cached_property
    def population(self):
        ref_value_ideal = (self.row.population_minimum_size or
                           self.row.population_alt_minimum_size)
        return {
            'size': self._get_population_size(),
            'conclusion': self._get_conclusion('population'),
            'trend_short': self._get_population_trend(),
            'trend_long': self._get_population_trend('_long'),
            'magnitude_short': self._get_magnitude('population'),
            'magnitude_long': self._get_magnitude('population', '_long'),
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
def index():
    group_code = flask.request.args.get('group')
    species_code = flask.request.args.get('species', type=int)
    if species_code:
        species = (models.LuHdSpecies.query
                    .filter_by(speciescode=species_code)
                    .first_or_404())
    else:
        species = None

    species_list = models.LuHdSpecies.query.order_by('speciesname')

    if species:
        records = (models.DataSpeciesRegion.query
                        .filter_by(sr_species=species.data))

    return flask.render_template('species/index.html', **{
        'species_groups': [{'id': g.code,
                            'text': g.description}
                           for g in models.LuGrupSpecie.query],
        'current_group_code': group_code,
        'species_list': [{'id': str(int(s.speciescode)),
                          'group_id': s.group_code,
                          'text': s.speciesname}
                         for s in species_list],
        'current_species_code': species_code,

        'species': None if species is None else {
            'code': species.speciescode,
            'name': species.speciesname,
            'annex_II': species.annexii == 'Y',
            'annex_IV': species.annexiv == 'Y',
            'annex_V': species.annexv == 'Y',
            'records': [SpeciesRecord(r) for r in records],
        },
    })


@species.route('/specii/detalii/<int:record_id>')
def detail(record_id):
    record = models.DataSpeciesRegion.query.get_or_404(record_id)
    return flask.render_template('species/detail.html', **{
        'species': record.sr_species,
        'record': SpeciesRecord(record),
    })
