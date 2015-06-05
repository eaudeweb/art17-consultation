from flask import current_app as app

from art17.aggregation.refvalues import extract_key
from art17.aggregation.utils import average

FV = 'FV'
U1 = 'U1'
U2 = 'U2'
XX = 'XX'


def compare_operator(operator):
    if operator in ('=', '<'):
        return FV
    elif operator == '>':
        return U1
    elif operator == '>>':
        return U2


def compare_FV_area(current_value, fv, vals):
    u1 = fv * (1 - app.config['U1_U2_THRESHOLD'])
    u2 = 0

    if current_value >= fv:
        return FV
    elif current_value >= u1:
        return U1
    elif current_value >= u2:
        return U2
    return ''


def compare_FV_range(current_value, fv):
    u1 = fv * (1 - app.config['U1_U2_THRESHOLD'])
    u2 = 0

    if current_value >= fv:
        return FV
    elif current_value >= u1:
        return U1
    elif current_value >= u2:
        return U2
    return ''


def compare_FV_habitat(current_value, fv, quality):
    u1 = fv * (1 - app.config['U1_U2_THRESHOLD'])

    if ((current_value >= fv or current_value == 0)
            and quality in ('Good', 'Moderate')):
        return FV
    elif current_value <= u1 or quality == 'Bad':
        return U2
    return U1


def get_prev_population_size(prev, year):
    start = year - app.config['REPORTING_FREQUENCY']
    end = year
    keys = ('population_minimum_size', 'population_maximum_size')
    prev_values = [average([p[key] for key in keys if p[key]])
                   for p in prev if start <= p['year'] < end]
    return average([val for val in prev_values if val])


def compare_FV_population(current_value, fv, prev, year):
    if current_value >= fv:
        return FV

    prev_value = get_prev_population_size(prev, year)
    if (current_value < (1 - 0.25) * fv or
            (current_value < fv and current_value < (1 - 0.07) * prev_value)):
        return U2

    return U1


def get_conclusion(current_value, refvals, refval_type, **kwargs):
    if not current_value:
        return 'XX'

    vals = refvals[refval_type]
    fv_text = "adecvat" if refval_type == 'habitat' else "favorabil"
    fv = extract_key(vals, fv_text)
    fv = fv and float(fv)
    unknown = extract_key(vals, 'Necunoscut')
    operator = extract_key(vals, 'Operator')

    if fv:
        if refval_type == 'coverage_range':
            return compare_FV_area(current_value, fv, vals)
        elif refval_type == 'range':
            return compare_FV_range(current_value, fv)
        elif refval_type == 'habitat':
            return compare_FV_habitat(current_value, fv, kwargs['quality'])
        elif refval_type == 'population_range':
            return compare_FV_population(current_value, fv, kwargs['prev'],
                                         kwargs['year'])
    elif unknown:
        return 'XX'
    elif operator:
        return compare_operator(operator)
    return ''


def get_species_conclusion_range(subgroup, surface_area, refvals):
    return get_conclusion(surface_area, refvals, 'range')


def get_species_conclusion_population(subgroup, min_size, max_size, refvals, prev, year):
    size = average([s for s in (min_size, max_size) if s is not None])
    return get_conclusion(size, refvals, 'population_range', prev=prev,
                          year=year)


def get_species_conclusion_habitat(subgroup, surface_area, quality, refvals):
    return get_conclusion(surface_area, refvals, 'habitat', quality=quality)


def get_species_conclusion_future(subgroup, code, region):
    return FV


def get_habitat_conclusion_range(surface_area, refvals):
    return get_conclusion(surface_area, refvals, 'range')


def get_habitat_conclusion_area(surface_area, refvals):
    return get_conclusion(surface_area, refvals, 'coverage_range')


def get_habitat_conclusion_future(code, region):
    return FV


def get_overall_conclusion(concs):
    if concs.count(XX) > 2:
        return XX
    if FV in concs and not (U1 in concs or U2 in concs):
        return FV
    if U1 in concs and U2 not in concs:
        return U1
    if U2 in concs:
        return U2
    return ''


def get_overall_habitat_conclusion(result):
    concs = [
        result.conclusion_range or '', result.conclusion_area or '',
        result.conclusion_structure or '', result.conclusion_future or ''
    ]
    return get_overall_conclusion(concs)


def get_overall_species_conclusion(result):
    concs = [
        result.conclusion_range or '', result.conclusion_population or '',
        result.conclusion_habitat or '', result.conclusion_future or '',
    ]
    return get_overall_conclusion(concs)
