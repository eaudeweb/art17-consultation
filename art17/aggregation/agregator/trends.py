from flask import current_app as app

from art17.aggregation.utils import average


(SHORT_TERM, LONG_TERM) = range(2)


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
        return '='


def get_species_range_trend(term, year, current_value, prev):
    return get_trend(term, year, current_value, prev, 'range_surface_area')


def get_species_population_trend(term, year, current_value, prev):
    return get_trend(term, year, current_value, prev,
                     ('population_minimum_size', 'population_maximum_size'))


def get_species_habitat_trend(term, year, current_value, prev):
    return get_trend(term, year, current_value, prev, 'habitat_surface_area')


def get_habitat_range_trend(term, year, current_value, prev):
    return get_trend(term, year, current_value, prev, 'range_surface_area')


def get_habitat_coverage_trend(term, year, current_value, prev):
    return get_trend(term, year, current_value, prev, 'coverage_surface_area')
