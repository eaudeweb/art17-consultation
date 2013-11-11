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


def parse_magnitude_ci_trend(obj, prefix):
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


def reasons_for_change(obj, prefix):
    return {
        'a': getattr(obj, '%s_reasons_for_change_a' % prefix),
        'b': getattr(obj, '%s_reasons_for_change_b' % prefix),
        'c': getattr(obj, '%s_reasons_for_change_c' % prefix),
    }


def additional_info(obj, prefix):
    return {
        'locality': getattr(obj, '%s_additional_locality' % prefix),
        'method': getattr(obj, '%s_additional_method' % prefix),
        'problems': getattr(obj, '%s_additional_problems' % prefix),
    }


def _get_population_size(obj):
    rv = {}
    for qualifier in ['population', 'population_alt']:
        min_size = getattr(obj, '%s_minimum_size' % qualifier)
        max_size = getattr(obj, '%s_maximum_size' % qualifier)
        unit = getattr(obj, '%s_size_unit' % qualifier)

        rv[qualifier] = {
            'min': min_size,
            'max': max_size,
            'unit': unit,
        }

    return rv


def _get_habitat_quality(obj):
    value = obj.habitat_quality
    explanation = obj.habitat_quality_explanation
    return {
        'value': value,
        'explanation': explanation,
    }


def comment_info(row):
    return {
        'user_id': row.cons_user_id,
        'comment_date': row.cons_date,
        'status': row.cons_status,
    }


def parse_species(row, is_comment=False):
    rv = {}
    rv['model'] = row
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
                                    'complementary_favourable_range'),
                                # ideal: row.range_surface_area
            'reasons_for_change': reasons_for_change(row, 'range'),
        }
    ref_value_ideal = (row.population_minimum_size or
                       row.population_alt_minimum_size)
    rv['population'] = {
            'size': _get_population_size(row),
            'method': row.population_method,
            'additional': additional_info(row, 'population'),
            'population_date': row.population_date,
            'conclusion': parse_conclusion(row, 'conclusion_population'),
            'trend_short': parse_magnitude_ci_trend(row,
                                                  'population_trend'),
            'trend_long': parse_magnitude_ci_trend(row,
                                                 'population_trend_long'),
            'reference_value': parse_reference_value(row,
                                    'complementary_favourable_population')
                                # ideal: ref_value_ideal
        }
    rv['habitat'] = {
            'surface_area': row.habitat_surface_area,
            'date': row.habitat_date,
            'method': row.habitat_method,
            'conclusion': parse_conclusion(row, 'conclusion_habitat'),
            'trend_short': parse_trend(row, 'habitat_trend'),
            'trend_long': parse_trend(row, 'habitat_trend_long'),
            'area_suitable': row.habitat_area_suitable,
            'quality': _get_habitat_quality(row),
            'reasons_for_change': reasons_for_change(row, 'habitat'),
        }

    rv['natura2000'] = {
            'population_unit': row.natura2000_population_unit,
            'population_min': row.natura2000_population_min,
            'population_max': row.natura2000_population_max,
            'population_method': row.natura2000_population_method,
            'population_trend': row.natura2000_population_trend,
    }

    rv['justification'] = row.justification
    rv['other_relevant_information'] = row.other_relevant_information
    rv['transboundary_assessment'] = row.transboundary_assessment

    rv['pressures_method'] = row.pressures_method
    rv['threats_method'] = row.threats_method

    rv['sources'] = row.published
    rv['future_prospects'] = parse_conclusion(row, 'conclusion_future')
    rv['overall_assessment'] = parse_conclusion(row, 'conclusion_assessment')
    rv['generalstatus'] = row.cons_generalstatus
    return rv


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

    rv['population'] = {
            'size': _get_population_size(row),
            'method': row.population_method,
            'trend_short': parse_trend(row, 'population_trend'),
            'trend_long': parse_trend(row, 'population_trend_long'),
            'conclusion': parse_conclusion(row, 'conclusion_population'),
            'reference_value': parse_reference_value(row,
                                    'complementary_favourable_population')
    }

    rv['habitat'] = {
            'surface_area': row.habitat_surface_area,
            'date':row.habitat_date,
            'method': row.habitat_method,
            'quality': row.habitat_quality,
            'quality_explanation': row.habitat_quality_explanation,
            'trend_short': parse_trend(row, 'habitat_trend'),
            'trend_long': parse_trend(row, 'habitat_trend_long'),
            'area_suitable': row.habitat_area_suitable,
            'conclusion': parse_conclusion(row, 'conclusion_habitat'),
    }


    rv['future_prospects'] = parse_conclusion(row, 'conclusion_future')
    rv['overall_assessment'] = parse_conclusion(row, 'conclusion_assessment')
    rv['report_observation'] = row.cons_report_observation
    rv['generalstatus'] = row.cons_generalstatus

    return rv


def parse_habitat(row, is_comment=False):
    rv = {}
    rv['model'] = row
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
                                    'complementary_favourable_range'),
            'reasons_for_change': reasons_for_change(row, 'range')
        }
    rv['coverage'] = {
            'surface_area': row.coverage_surface_area,
            'coverage_date': row.coverage_date,
            'method': row.coverage_method,
            'trend_short': parse_magnitude_ci_trend(row, 'coverage_trend'),
            'trend_long': parse_magnitude_ci_trend(row, 'coverage_trend_long'),
            'conclusion': parse_conclusion(row, 'conclusion_area'),
            'reference_value': parse_reference_value(row,
                                    'complementary_favourable_area'),
            'reasons_for_change': reasons_for_change(row, 'area')
        }

    rv['natura2000'] = {
            'area_min': row.natura2000_area_min,
            'area_max': row.natura2000_area_max,
            'area_method': row.natura2000_area_method,
            'area_trend': row.natura2000_area_trend,
    }

    rv['typical_species_method'] = row.typical_species_method
    rv['justification'] = row.justification
    rv['structure_and_functions_method'] = row.structure_and_functions_method
    rv['other_relevant_information'] = row.other_relevant_information

    rv['pressures_method'] = row.pressures_method
    rv['threats_method'] = row.threats_method

    rv['sources'] = row.published

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

    rv['coverage'] = {
            'surface_area': row.coverage_surface_area,
            'date':row.coverage_date,
            'method': row.coverage_method,
            'trend_short': parse_trend(row, 'coverage_trend'),
            'trend_long': parse_trend(row, 'coverage_trend_long'),
            'reference_value': parse_reference_value(row,
                                    'complementary_favourable_area'),
            'conclusion': parse_conclusion(row, 'conclusion_area')
        }

    rv['structure'] = parse_conclusion(row, 'conclusion_structure')
    rv['future_prospects'] = parse_conclusion(row, 'conclusion_future')
    rv['overall_assessment'] = parse_conclusion(row, 'conclusion_assessment')
    rv['report_observation'] = row.cons_report_observation

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


def _set_population_size(pop_size_struct, obj):
    for qualifier in ['population', 'population_alt']:
        setattr(obj, '%s_minimum_size' % qualifier,
                    pop_size_struct[qualifier]['min'])
        setattr(obj, '%s_maximum_size' % qualifier,
                    pop_size_struct[qualifier]['max'])
        setattr(obj, '%s_size_unit' % qualifier,
                    pop_size_struct[qualifier]['unit'])


def flatten_species_commentform(struct, obj):
    obj.range_surface_area = struct['range']['surface_area']
    obj.range_method = struct['range']['method']
    flatten_trend(struct['range']['trend_short'], obj, 'range_trend')
    flatten_trend(struct['range']['trend_long'], obj, 'range_trend_long')
    flatten_refval(struct['range']['reference_value'], obj,
                   'complementary_favourable_range')
    flatten_conclusion(struct['range']['conclusion'], obj, 'conclusion_range')

    _set_population_size(struct['population']['size'], obj)
    obj.population_method = struct['population']['method']
    flatten_trend(struct['population']['trend_short'], obj,
                    'population_trend')
    flatten_trend(struct['population']['trend_long'], obj,
                    'population_trend_long')
    flatten_refval(struct['population']['reference_value'], obj,
                    'complementary_favourable_population')
    flatten_conclusion(struct['population']['conclusion'], obj,
                    'conclusion_population')

    obj.habitat_surface_area = struct['habitat']['surface_area']
    obj.habitat_date = struct['habitat']['date']
    obj.habitat_method = struct['habitat']['method']
    obj.habitat_quality = struct['habitat']['quality']
    obj.habitat_quality_explanation = struct['habitat']['quality_explanation']
    flatten_trend(struct['habitat']['trend_short'], obj,
                    'habitat_trend')
    flatten_trend(struct['habitat']['trend_long'], obj,
                    'habitat_trend_long')
    obj.habitat_area_suitable = struct['habitat']['area_suitable']
    flatten_conclusion(struct['habitat']['conclusion'], obj,
                    'conclusion_habitat')

    flatten_conclusion(struct['future_prospects'], obj,
                    'conclusion_future')
    flatten_conclusion(struct['overall_assessment'], obj,
                    'conclusion_assessment')
    obj.cons_report_observation = struct['report_observation']
    obj.cons_generalstatus = struct['generalstatus']

def flatten_habitat_commentform(struct, obj):
    obj.range_surface_area = struct['range']['surface_area']
    obj.range_method = struct['range']['method']

    flatten_trend(struct['range']['trend_short'], obj, 'range_trend')
    flatten_trend(struct['range']['trend_long'], obj, 'range_trend_long')
    flatten_refval(struct['range']['reference_value'], obj,
                   'complementary_favourable_range')
    flatten_conclusion(struct['range']['conclusion'], obj, 'conclusion_range')


    obj.coverage_surface_area = struct['coverage']['surface_area']
    obj.coverage_date = struct['coverage']['date']
    obj.coverage_method = struct['coverage']['method']
    flatten_trend(struct['coverage']['trend_short'], obj,
                    'coverage_trend')
    flatten_trend(struct['coverage']['trend_long'], obj,
                    'coverage_trend_long')
    flatten_refval(struct['coverage']['reference_value'], obj,
                    'complementary_favourable_area')
    flatten_conclusion(struct['coverage']['conclusion'], obj,
                    'conclusion_area')

    flatten_conclusion(struct['structure'], obj,
                    'conclusion_structure')
    flatten_conclusion(struct['future_prospects'], obj,
                    'conclusion_future')
    flatten_conclusion(struct['overall_assessment'], obj,
                    'conclusion_assessment')
    obj.cons_report_observation = struct['report_observation']
