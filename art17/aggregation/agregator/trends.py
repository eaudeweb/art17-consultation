from flask import current_app as app


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
    hist_values = [p[key] for p in prev if p[key] and p['year'] > start]
    average = float(sum(hist_values)) / len(hist_values)
    min_value = (1 - app.config['ACCEPTED_AVG_VARIATION']) * average
    max_value = (1 + app.config['ACCEPTED_AVG_VARIATION']) * average

    if current > max_value:
        return '+'
    elif current < min_value:
        return '-'
    else:
        return '='


def get_species_range_trend(term, year, current_value, prev):
    return get_trend(term, year, current_value, prev, 'range_surface_area')


def get_species_population_trend(term, year):
    start = term_start(term, year)

    return 'x'


def get_species_habitat_trend(term, year, current_value, prev):
    return get_trend(term, year, current_value, prev, 'habitat_surface_area')


def get_habitat_range_trend(term, year, current_value, prev):
    return get_trend(term, year, current_value, prev, 'range_surface_area')


def get_habitat_coverage_trend(term, year, current_value, prev):
    return get_trend(term, year, current_value, prev, 'coverage_surface_area')
