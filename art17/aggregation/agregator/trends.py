from flask import current_app as app

from art17.aggregation.utils import average
from art17.aggregation.agregator.rest import get_PS_trend, get_LL_trend
from art17.aggregation.agregator.subgroups import PS, LL
from art17.aggregation.agregator.conclusions import U1, U2, FV, XX


SHORT_TERM, LONG_TERM = range(2)
LOW, MEDIUM, HIGH = 'L', 'M', 'H'

INCREASE = [('+', '+'), ('+', '0'), ('0', '+'), ('x', '+'), ('+', 'x')]
DECREASE = [('-', '-'), ('-', '0'), ('0', '-'), ('x', '-'), ('-', 'x')]
STABLE = [('0', '0'), ('+', '-'), ('-', '+'), ('x', '0'), ('0', 'x')]


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


def get_species_range_trend(subgroup, term, year, current_value, prev,
                            speccode, region):
    if subgroup == LL:
        return get_bats_trend(speccode, region)
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
    if result is None:
        return 'x'

    grad, rang, env, morf = result

    if (grad == 0 and rang is None) or (grad == 1 and rang == LOW) and \
            env and 0.75 <= morf <= 1:
        return '+'
    elif grad == 3 and rang in (MEDIUM, HIGH) and not env:
        return '-'
    else:
        return '0'


def get_bats_trend(speccode, region):
    result = get_LL_trend(speccode, region)
    if result is None:
        return 'x'

    trend, cons, rang = result

    if trend in (None, XX) and cons in (None, XX):
        return 'x'
    if trend == '+' and cons in (FV, U1, XX):
        return '+'
    elif ((trend == '=' and cons in (FV, U1, XX)) or
          (trend == '+' and cons == U2)):
        return '0'
    return '-'


def get_bats_conclusion_trend(conclusion, pop_conclusion, pop_trend,
                              hab_conclusion, hab_trend):
    if conclusion not in [U1, U2]:
        return
    if pop_conclusion == FV and hab_conclusion == FV:
        return '+'
    if not all((pop_conclusion, hab_conclusion, pop_trend, hab_trend)):
        return 'x'
    stable_options = [(U1, FV, '+'), (U1, FV, '0')]
    if (pop_conclusion, hab_conclusion, hab_trend) in stable_options or \
            (hab_conclusion, pop_conclusion, pop_trend) in stable_options:
        return '0'
    return '-'


def get_species_conclusion_trend(subgroup, conclusion, trend_short, trend_long,
                                 pop_conclusion, pop_trend, hab_conclusion,
                                 hab_trend):
    if subgroup == LL:
        return get_bats_conclusion_trend(conclusion, pop_conclusion, pop_trend,
                                         hab_conclusion, hab_trend)
    return get_conclusion_trend(conclusion, trend_short, trend_long)


def get_conclusion_trend(conclusion, trend_short, trend_long):
    if conclusion not in [U1, U2]:
        return
    trend_pair = (trend_short, trend_long)
    if trend_pair in INCREASE:
        return '+'
    elif trend_pair in DECREASE:
        return '-'
    elif trend_pair in STABLE:
        return '0'
    else:
        return 'x'


def get_future_trend(conclusion_future, conclusions, grade):
    if conclusion_future not in [U1, U2]:
        return
    if len(filter(lambda x: x == U2, conclusions)) >= 1:
        return '-'
    if grade == 5:
        return '-'
    elif grade == 6:
        return '0'
    elif grade == 7:
        return '+'


def grade_trend(conclusion, trend):
    if trend == '-':
        return -1
    elif trend == '+':
        return 1
    elif not trend and conclusion == FV:
        return 1
    return 0


def get_assessment_trend(conclusion_assessment, conclusions_trends):
    if conclusion_assessment not in [U1, U2]:
        return

    X_trends = filter(lambda x: x[0] in [U1, U2] and x[1] in [None, 'x'],
                      conclusions_trends)
    if len(X_trends) >= 2:
        return 'x'

    grade = sum([grade_trend(*c) for c in conclusions_trends])
    if grade > 0:
        return '+'
    elif grade == 0:
        return '0'
    elif grade < 0:
        return '-'
