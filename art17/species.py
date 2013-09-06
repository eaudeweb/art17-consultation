# encoding: utf-8

import flask
from werkzeug.utils import cached_property
from wtforms import Form, DecimalField
from wtforms.validators import Required
from art17 import models
from art17.common import GenericRecord

species = flask.Blueprint('species', __name__)


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


@species.route('/specii/regiuni/<int:species_code>')
def lookup_regions(species_code):
    species = (models.DataSpecies.query
                .filter_by(speciescode=species_code)
                .first_or_404())
    regions = [{'id': r.lu.code, 'text': r.lu.name_ro}
               for r in species.regions.join(models.DataSpeciesRegion.lu)]
    return flask.jsonify(options=regions)


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

    region_code = flask.request.args.get('region', '')
    if region_code:
        region = (models.LuBiogeoreg.query
                    .filter_by(code=region_code)
                    .first_or_404())
    else:
        region = None

    species_list = models.DataSpecies.query.join(models.DataSpeciesRegion)

    if species:
        records = (models.DataSpeciesRegion.query
                        .filter_by(sr_species=species.data))
        if region:
            records = records.filter_by(region=region.code)

    return flask.render_template('species/index.html', **{
        'species_groups': [{'id': g.code,
                            'text': g.description}
                           for g in models.LuGrupSpecie.query],
        'current_group_code': group_code,
        'species_list': [{'id': s.speciescode,
                          'group_id': s.lu.group_code,
                          'text': s.lu.speciesname}
                         for s in species_list],
        'current_species_code': species_code,
        'current_region_code': region_code,

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


class SpeciesCommentForm(Form):

    range_surface_area = DecimalField(u"Suprafață (km²)",
            [Required(u"Suprafața este obligatorie")])


@species.route('/specii/detalii/<int:record_id>/comentariu',
               methods=['GET', 'POST'])
def comment(record_id):
    record = models.DataSpeciesRegion.query.get_or_404(record_id)
    form = SpeciesCommentForm(flask.request.form)

    if flask.request.method == 'POST' and form.validate():
        comment = models.DataSpeciesComment(
            sr_species_id=record.sr_species_id,
            region=record.region)

        comment.range_surface_area = form.range_surface_area.data

        models.db.session.add(comment)
        models.db.session.commit()

        return flask.render_template('species/comment-saved.html', **{
            'species': record.sr_species,
            'record': SpeciesRecord(record),
        })

    return flask.render_template('species/comment.html', **{
        'species': record.sr_species,
        'record': SpeciesRecord(record),
        'form': form,
    })
