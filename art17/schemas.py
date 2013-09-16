def parse_period(obj, prefix):
    year_string = getattr(obj, prefix)

    if year_string:
        return {
            'start': year_string[:4],
            'end': year_string[4:],
        }

    else:
        return None


def parse_trend(obj, prefix, magnitude=False):
    rv = {
        'trend': getattr(obj, prefix),
        'period': parse_period(obj, prefix + '_period'),
    }
    if magnitude:
        rv['magnitude'] = {
            'min': getattr(obj, prefix + '_magnitude_min'),
            'max': getattr(obj, prefix + '_magnitude_max'),
        }
    return rv


def parse_population_trend(obj, prefix):
    rv = parse_trend(obj, prefix, magnitude=True)
    rv['magnitude']['ci'] = getattr(obj, prefix + '_magnitude_ci')
    rv['method'] = getattr(obj, prefix + '_method')
    return rv


def parse_conclusion(obj, prefix):
    return {
        'value': getattr(obj, prefix),
        'trend': getattr(obj, prefix + '_trend'),
    }


def parse_reference_value(obj, prefix):
    return {
        'number': getattr(obj, prefix),
        'op': getattr(obj, prefix + '_op'),
        'x': getattr(obj, prefix + '_x'),
        'method': getattr(obj, prefix + '_method'),
    }


def _get_population_size(obj):
    rv = []
    for qualifier in ['', '_alt']:
        min_size = getattr(obj, 'population%s_minimum_size' % qualifier)
        max_size = getattr(obj, 'population%s_maximum_size' % qualifier)
        unit = getattr(obj, 'population%s_size_unit' % qualifier)

        if unit:
            rv.append({
                'min': min_size,
                'max': max_size,
                'unit': unit,
            })

    return rv


def _get_habitat_quality(obj):
    value = obj.habitat_quality
    explanation = obj.habitat_quality_explanation
    return {
        'value': value,
        'explanation': explanation,
    }


def can_edit_comment(row):
    from art17 import auth
    if auth.admin_permission.can():
        return True

    if row.user_id:
        if auth.user_permission(row.user_id).can():
            return True

    return False


def comment_info(row):
    return {
        'user_id': row.user_id,
        'can_edit': can_edit_comment(row),
        'comment_date': row.comment_date,
        'status': row.status,
    }


def parse_species(row, is_comment=False):
    rv = {}
    if is_comment:
        rv.update(comment_info(row))
    rv['id'] = row.id
    rv['region'] = row.region
    rv['range'] = {
            'surface_area': row.range_surface_area,
            'method': row.range_method,
            'trend_short': parse_trend(row, 'range_trend', magnitude=True),
            'trend_long': parse_trend(row, 'range_trend_long', magnitude=True),
            'conclusion': parse_conclusion(row, 'conclusion_range'),
            'reference_value': parse_reference_value(row,
                                    'complementary_favourable_range')
                                # ideal: row.range_surface_area
        }
    ref_value_ideal = (row.population_minimum_size or
                       row.population_alt_minimum_size)
    rv['population'] = {
            'size': _get_population_size(row),
            'conclusion': parse_conclusion(row, 'conclusion_population'),
            'trend_short': parse_population_trend(row,
                                                  'population_trend'),
            'trend_long': parse_population_trend(row,
                                                 'population_trend_long'),
            'reference_value': parse_reference_value(row,
                                    'complementary_favourable_population')
                                # ideal: ref_value_ideal
        }
    rv['habitat'] = {
            'surface_area': row.habitat_surface_area,
            'method': row.habitat_method,
            'conclusion': parse_conclusion(row, 'conclusion_habitat'),
            'trend_short': parse_trend(row, 'habitat_trend'),
            'trend_long': parse_trend(row, 'habitat_trend_long'),
            'area_suitable': row.habitat_area_suitable,
            'quality': _get_habitat_quality(row),
        }
    rv['future_prospects'] = parse_conclusion(row, 'conclusion_future')
    rv['overall_assessment'] = parse_conclusion(row, 'conclusion_assessment')
    return rv


def parse_species_commentform(row):
    rv = {}
    rv['range'] = {
            'surface_area': row.range_surface_area,
            'method': row.range_method,
            'trend_short': parse_trend(row, 'range_trend'),
            'trend_long': parse_trend(row, 'range_trend_long'),
            'conclusion': parse_conclusion(row, 'conclusion_range'),
            'reference_value': parse_reference_value(row,
                                    'complementary_favourable_range')
        }
    return rv


def parse_habitat(row, is_comment=False):
    rv = {}
    if is_comment:
        rv.update(comment_info(row))
    rv['id'] = row.id
    rv['region'] = row.region
    rv['range'] = {
            'surface_area': row.range_surface_area,
            'method': row.range_method,
            'trend_short': parse_trend(row, 'range_trend', magnitude=True),
            'trend_long': parse_trend(row, 'range_trend_long', magnitude=True),
            'conclusion': parse_conclusion(row, 'conclusion_range'),
            'reference_value': parse_reference_value(row,
                                    'complementary_favourable_range')
                                # ideal: row.range_surface_area
        }
    rv['coverage'] = {
            'surface_area': row.coverage_surface_area,
            'trend_short': parse_trend(row, 'coverage_trend', magnitude=True),
            'trend_long': parse_trend(row, 'coverage_trend_long', magnitude=True),
            'conclusion': parse_conclusion(row, 'conclusion_area'),
            'reference_value': parse_reference_value(row,
                                    'complementary_favourable_area')
                                # ideal: row.coverage_surface_area
        }
    rv['structure'] = parse_conclusion(row, 'conclusion_structure')
    rv['future_prospects'] = parse_conclusion(row, 'conclusion_future')
    rv['overall_assessment'] = parse_conclusion(row, 'conclusion_assessment')
    return rv


def parse_habitat_commentform(row):
    rv = {}
    rv['range'] = {
            'surface_area': row.range_surface_area,
            'method': row.range_method,
            'trend_short': parse_trend(row, 'range_trend'),
            'trend_long': parse_trend(row, 'range_trend_long'),
            'conclusion': parse_conclusion(row, 'conclusion_range'),
            'reference_value': parse_reference_value(row,
                                    'complementary_favourable_range')
        }
    return rv


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


def flatten_species_commentform(struct, obj):
    obj.range_surface_area = struct['range']['surface_area']
    obj.range_method = struct['range']['method']

    flatten_trend(struct['range']['trend_short'], obj, 'range_trend')
    flatten_trend(struct['range']['trend_long'], obj, 'range_trend_long')
    flatten_refval(struct['range']['reference_value'], obj,
                   'complementary_favourable_range')
    flatten_conclusion(struct['range']['conclusion'], obj, 'conclusion_range')



def flatten_habitat_commentform(struct, obj):
    obj.range_surface_area = struct['range']['surface_area']
    obj.range_method = struct['range']['method']

    flatten_trend(struct['range']['trend_short'], obj, 'range_trend')
    flatten_trend(struct['range']['trend_long'], obj, 'range_trend_long')
    flatten_refval(struct['range']['reference_value'], obj,
                   'complementary_favourable_range')
    flatten_conclusion(struct['range']['conclusion'], obj, 'conclusion_range')
