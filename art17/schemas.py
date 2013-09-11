from werkzeug.utils import cached_property


class RecordComment(object):

    def __init__(self, row):
        self.row = row

    @cached_property
    def user_id(self):
        return self.row.user_id

    def can_edit(self):
        from art17 import auth
        if auth.admin_permission.can():
            return True

        if self.user_id:
            if auth.user_permission(self.user_id).can():
                return True

        return False


class GenericRecord(object):

    def __init__(self, row, is_comment=False):
        self.row = row
        self.is_comment = is_comment

    def _split_period(self, year_string):
        if year_string:
            return {
                'start': year_string[:4],
                'end': year_string[4:],
            }

        else:
            return None

    def _get_trend(self, name, qualifier=''):
        period = getattr(self.row, '%s_trend%s_period' % (name, qualifier))
        trend = getattr(self.row, '%s_trend%s' % (name, qualifier))
        return {
            'trend': trend,
            'period': self._split_period(period),
        }

    def _get_magnitude(self, name, qualifier=''):
        mag_min = getattr(self.row, '%s_trend%s_magnitude_min' % (name, qualifier))
        mag_max = getattr(self.row, '%s_trend%s_magnitude_max' % (name, qualifier))
        return {
            'min': mag_min,
            'max': mag_max,
        }

    def _get_conclusion(self, name):
        return {
            'value': getattr(self.row, 'conclusion_%s' % name),
        }

    def _get_reference_value(self, name, ideal):
        return {
            '_ideal': ideal,
            'number': getattr(self.row, 'complementary_favourable_%s' % name),
            'op': getattr(self.row, 'complementary_favourable_%s_op' % name),
            'x': getattr(self.row, 'complementary_favourable_%s_x' % name),
            'method': getattr(self.row, 'complementary_favourable_%s_method'
                                        % name),
        }

    @cached_property
    def comment(self):
        assert self.is_comment
        return RecordComment(self.row)


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
            'method': self.row.range_method,
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


def flatten_period(period_struct, obj, prefix):
    setattr(obj, prefix, '%s%s' % (period_struct['start'],
                                   period_struct['end']))


def flatten_trend(trend_struct, obj, prefix):
    setattr(obj, prefix, trend_struct['trend'])
    flatten_period(trend_struct['period'], obj, prefix + '_period')


def flatten_conclusion(conclusion_struct, obj, prefix):
    setattr(obj, prefix, conclusion_struct['value'])
    setattr(obj, prefix + '_trend', conclusion_struct['trend'])


def flatten_species(struct, obj):
    obj.range_surface_area = struct['range']['surface_area']
    obj.range_method = struct['range']['method']

    flatten_trend(struct['range']['trend_short'], obj, 'range_trend')
    flatten_trend(struct['range']['trend_long'], obj, 'range_trend_long')

    obj.complementary_favourable_range_op = \
        struct['range']['reference_value']['op']
    obj.complementary_favourable_range = \
        struct['range']['reference_value']['number']
    obj.complementary_favourable_range_method = \
        struct['range']['reference_method']

    flatten_conclusion(struct['range']['conclusion'], obj, 'conclusion_range')



def flatten_habitat(struct, obj):
    obj.range_surface_area = struct['range']['surface_area']
    obj.range_method = struct['range']['method']

    flatten_trend(struct['range']['trend_short'], obj, 'range_trend')
    flatten_trend(struct['range']['trend_long'], obj, 'range_trend_long')

    obj.complementary_favourable_range_op = \
        struct['range']['reference_value']['op']
    obj.complementary_favourable_range = \
        struct['range']['reference_value']['number']
    obj.complementary_favourable_range_method = \
        struct['range']['reference_method']

    flatten_conclusion(struct['range']['conclusion'], obj, 'conclusion_range')
