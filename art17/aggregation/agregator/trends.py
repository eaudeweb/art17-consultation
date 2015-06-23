from flask import current_app as app

from art17.aggregation.utils import average
from art17.aggregation.agregator.rest import get_PS_trend
from art17.aggregation.agregator.subgroups import PS


SHORT_TERM, LONG_TERM = range(2)
LOW, MEDIUM, HIGH = 'L', 'M', 'H'


def term_start(term, year):
    if term == SHORT_TERM:
        return year - 12
    elif term == LONG_TERM:
        return year - 24
    else:
        raise ValueError("Invalid term")


def get_trend(term, year, current, prev, key):
    if not prev:
        return 'x'

    start = term_start(term, year)

    if isinstance(key, tuple):
        prev_values = [average([p[k] for k in key if p[k]])
                       for p in prev if p['year'] > start]
    else:
        prev_values = [p[key] for p in prev if p['year'] > start]
    prev_values = [p for p in prev_values if p]

    avg = average(prev_values)
    min_value = (1 - app.config['ACCEPTED_AVG_VARIATION']) * avg
    max_value = (1 + app.config['ACCEPTED_AVG_VARIATION']) * avg

    if current > max_value:
        return '+'
    elif current < min_value:
        return '-'
    else:
        return '0'


def get_species_range_trend(subgroup, term, year, current_value, prev):
    return get_trend(term, year, current_value, prev, 'range_surface_area')


def get_species_population_trend(subgroup, term, year, current_value, prev):
    return get_trend(term, year, current_value, prev,
                     ('population_minimum_size', 'population_maximum_size'))


def get_species_habitat_trend(subgroup, term, year, current_value, prev):
    return get_trend(term, year, current_value, prev, 'habitat_surface_area')


def get_habitat_range_trend(subgroup, term, year, current_value, prev, habcode,
                            region):
    if subgroup == PS:
        return get_caves_trend(habcode, region)
    return get_trend(term, year, current_value, prev, 'range_surface_area')


def get_habitat_coverage_trend(subgroup, term, year, current_value, prev,
                               habcode, region):
    if subgroup == PS:
        return get_caves_trend(habcode, region)
    return get_trend(term, year, current_value, prev, 'coverage_surface_area')


def get_caves_trend(habcode, region):
    result = get_PS_trend(habcode, region)
    if all([elem is None for elem in result]):
        return 'x'

    grad, rang, env, morf = result

    if (grad == 0 and rang is None) or (grad == 1 and rang == LOW) and \
            env and 0.75 <= morf <= 1:
        return '+'
    elif grad == 3 and rang in (MEDIUM, HIGH) and not env:
        return '-'
    else:
        return '0'
