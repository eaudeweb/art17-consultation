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


def parse_period(obj, prefix):
    year_string = getattr(obj, prefix)

    if year_string:
        return {
            'start': year_string[:4],
            'end': year_string[4:],
        }

    else:
        return None


def parse_trend(obj, prefix):
    return {
        'trend': getattr(obj, prefix),
        'period': parse_period(obj, prefix + '_period'),
        'magnitude': {
            'min': getattr(obj, prefix + '_magnitude_min'),
            'max': getattr(obj, prefix + '_magnitude_max'),
        }
    }


def parse_habitat_trend(obj, prefix):
    """ habitat trend has no magnitude """
    return {
        'trend': getattr(obj, prefix),
        'period': parse_period(obj, prefix + '_period'),
    }


def parse_population_trend(obj, prefix):
    rv = parse_trend(obj, prefix)
    rv['magnitude']['ci'] = getattr(obj, prefix + '_magnitude_ci')
    rv['method'] = getattr(obj, prefix + '_method')
    return rv


def parse_conclusion(obj, prefix):
    return {
        'value': getattr(obj, prefix),
        'trend': getattr(obj, prefix + '_trend'),
    }


class GenericRecord(object):

    def __init__(self, row, is_comment=False):
        self.row = row
        self.is_comment = is_comment

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
            'surface_area': surface_area,
            'method': self.row.range_method,
            'trend_short': parse_trend(self.row, 'range_trend'),
            'trend_long': parse_trend(self.row, 'range_trend_long'),
            'conclusion': parse_conclusion(self.row, 'conclusion_range'),
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
            'conclusion': parse_conclusion(self.row, 'conclusion_population'),
            'trend_short': parse_population_trend(self.row,
                                                  'population_trend'),
            'trend_long': parse_population_trend(self.row,
                                                 'population_trend_long'),
            'reference_value': self._get_reference_value('population',
                                                         ref_value_ideal),
        }

    @cached_property
    def habitat(self):
        return {
            'surface_area': self.row.habitat_surface_area,
            'method': self.row.habitat_method,
            'conclusion': parse_conclusion(self.row, 'conclusion_habitat'),
            'trend_short': parse_habitat_trend(self.row, 'habitat_trend'),
            'trend_long': parse_habitat_trend(self.row, 'habitat_trend_long'),
            'area_suitable': self.row.habitat_area_suitable,
            'quality': self._get_habitat_quality(),
        }

    @cached_property
    def future_prospects(self):
        return parse_conclusion(self.row, 'conclusion_future')

    @cached_property
    def overall_assessment(self):
        return parse_conclusion(self.row, 'conclusion_assessment')


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
            'method': self.row.range_method,
            'trend_short': parse_trend(self.row, 'range_trend'),
            'trend_long': parse_trend(self.row, 'range_trend_long'),
            'conclusion': parse_conclusion(self.row, 'conclusion_range'),
            'reference_value': self._get_reference_value('range',
                                                         surface_area),
        }

    @cached_property
    def area(self):
        surface_area = self.row.coverage_surface_area
        return {
            'surface_area': surface_area,
            'trend_short': parse_trend(self.row, 'coverage_trend'),
            'trend_long': parse_trend(self.row, 'coverage_trend_long'),
            'conclusion': parse_conclusion(self.row, 'conclusion_area'),
            'reference_value': self._get_reference_value('area', surface_area),
        }

    @cached_property
    def structure(self):
        return parse_conclusion(self.row, 'conclusion_structure')

    @cached_property
    def future_prospects(self):
        return parse_conclusion(self.row, 'conclusion_future')

    @cached_property
    def overall_assessment(self):
        return parse_conclusion(self.row, 'conclusion_assessment')


def flatten_period(period_struct, obj, prefix):
    if period_struct is None:
        value = None
    elif not (period_struct['start'] or period_struct['end']):
        value = None
    else:
        assert period_struct['start'] and period_struct['end']
        value = '%s%s' % (period_struct['start'], period_struct['end'])
    setattr(obj, prefix, value)


def flatten_trend(trend_struct, obj, prefix):
    setattr(obj, prefix, trend_struct['trend'])
    flatten_period(trend_struct['period'], obj, prefix + '_period')


def flatten_conclusion(conclusion_struct, obj, prefix):
    setattr(obj, prefix, conclusion_struct['value'])
    setattr(obj, prefix + '_trend', conclusion_struct['trend'])


def flatten_refval(refval_struct, obj, prefix):
    setattr(obj, prefix + '_op', refval_struct['op'])
    setattr(obj, prefix, refval_struct['number'])
    setattr(obj, prefix + '_method', refval_struct['method'])


def flatten_species(struct, obj):
    obj.range_surface_area = struct['range']['surface_area']
    obj.range_method = struct['range']['method']

    flatten_trend(struct['range']['trend_short'], obj, 'range_trend')
    flatten_trend(struct['range']['trend_long'], obj, 'range_trend_long')
    flatten_refval(struct['range']['reference_value'], obj,
                   'complementary_favourable_range')
    flatten_conclusion(struct['range']['conclusion'], obj, 'conclusion_range')



def flatten_habitat(struct, obj):
    obj.range_surface_area = struct['range']['surface_area']
    obj.range_method = struct['range']['method']

    flatten_trend(struct['range']['trend_short'], obj, 'range_trend')
    flatten_trend(struct['range']['trend_long'], obj, 'range_trend_long')
    flatten_refval(struct['range']['reference_value'], obj,
                   'complementary_favourable_range')
    flatten_conclusion(struct['range']['conclusion'], obj, 'conclusion_range')


def parse_species(obj):
    record = SpeciesRecord(obj)
    rv = {}
    rv['range'] = record.range
    return rv


def parse_species_comment(obj):
    rv = parse_species(obj)
    del rv['range']['reference_value']['_ideal']
    del rv['range']['trend_short']['magnitude']
    del rv['range']['trend_long']['magnitude']
    return rv


def parse_habitat(obj):
    record = HabitatRecord(obj)
    rv = {}
    rv['range'] = record.range
    return rv


def parse_habitat_comment(obj):
    rv = parse_habitat(obj)
    del rv['range']['reference_value']['_ideal']
    del rv['range']['trend_short']['magnitude']
    del rv['range']['trend_long']['magnitude']
    return rv
