import flask
from werkzeug.utils import cached_property
from art17 import models


species = flask.Blueprint('species', __name__)


class BioRegionRender(object):

    def __init__(self, row):
        self.row = row

    @cached_property
    def region(self):
        return self.row.region

    def _get_range_reference_value(self):
        if self.row.complementary_favourable_range:
          return self.row.complementary_favourable_range

        elif self.row.complementary_favourable_range_op:
          return (self.row.complementary_favourable_range_op
                  + self.row.range_surface_area)

        elif self.row.complementary_favourable_range_x:
          return "Unknown"

        else:
          return "N/A"

    def _split_period(self, year_string):
        if year_string:
            return "(%s-%s)" % (year_string[:4], year_string[4:])
        else:
            return ""

    def _get_conclusion(self, name):
        assessment = getattr(self.row, 'conclusion_%s' % name)
        trend = getattr(self.row, 'conclusion_%s_trend' % name)
        if trend:
            return "%s (%s)" % (assessment, trend)
        else:
            return assessment

    @cached_property
    def range(self):
        return {
            'method': self.row.range_method,
            'surface_area': self.row.range_surface_area,
            'trend': {
                'trend': self.row.range_trend,
                'period': self._split_period(self.row.range_trend_period),
            },
            'conclusion': self._get_conclusion('range'),
            'reference_value': self._get_range_reference_value(),
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


    @cached_property
    def population(self):
        return {
            'size_and_unit': self._get_population_size_and_unit(),
            'conclusion': self._get_conclusion('population'),
        }


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
        'annex_II': checklist[0].annex_II == 'Y',
        'annex_IV': checklist[0].annex_IV == 'Y',
        'annex_V': checklist[0].annex_V == 'Y',
        'records': [BioRegionRender(r) for r in species.regions],
    })
