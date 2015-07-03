from art17.aggregation.utils import get_values, get_year, most_common

POPULATION_CLASSES = [
    (1, 10),
    (10, 50),
    (50, 100),
    (100, 500),
    (500, 1000),
    (1000, 5000),
    (5000, 10000),
    (10000, 50000),
    (50000, 100000),
    (100000, 500000),
    (500000, 1000000),
    (1000000, 5000000),
    (5000000, 10000000),
    (10000000, 50000000),
    (50000000, 100000000),
]


def get_class(population):
    for i, (min_pop, max_pop) in enumerate(POPULATION_CLASSES):
        if min_pop <= population < max_pop:
            return i
    return 0


def get_population_class(values_int, values_ext):
    bats_in_colonies = sum(get_values(values_int, 'NR_INDIVIZI'))
    isolated_bats = sum(get_values(values_int, 'NR_INDIVIZI_IZOLATI'))
    obs_spots = len(get_values(values_ext, 'NR_INDIVIZI'))
    obs_dates = get_values(values_int, 'DATA') + get_values(values_ext, 'DATA')
    years = len(set([get_year(d) for d in obs_dates]))

    return (bats_in_colonies + 30 * isolated_bats + 100 * obs_spots) / years


def get_min_population(values_int):
    return len(get_values(values_int, 'NR_INDIVIZI')) * 100


def get_max_population(values_int, values_ext):
    bats_in_colonies = sum(get_values(values_int, 'NR_INDIVIZI'))
    isolated_bats = sum(get_values(values_int, 'NR_INDIVIZI_IZOLATI'))
    obs_spots = len(get_values(values_ext, 'NR_INDIVIZI'))
    return bats_in_colonies + 30 * isolated_bats + 100 * obs_spots


def get_ref_population(values_int, values_ext):
    bats_in_colonies = sum(get_values(values_int, 'NR_INDIVIZI'))
    isolated_bats = sum(get_values(values_ext, 'NR_INDIVIZI'))
    return bats_in_colonies + 100 * isolated_bats


def get_population_trend(values_int, values_ext):
    trend = most_common(get_values(values_ext, 'TREND_EVAL_POP_AR'))
    if not trend:
        return 'x'

    years_dict = get_years_dict(values_int, values_ext)
    years = sorted(years_dict.keys())
    diff = 0
    if len(years) > 1:
        for year in years[:-1]:
            pop_class = get_class(years_dict[year])
            next_year = years[years.index(year) + 1]
            next_pop_class = get_class(years_dict[next_year])
            diff += next_pop_class - pop_class
    if trend in ('X', '+') and diff > 0:
        return '+'
    elif trend in ('X', '-') and diff < 0:
        return '-'
    return '0'


def get_years_dict(values_int, values_ext):
    years_dict = {}
    for val in values_int:
        year = get_year(val['DATA'])
        if year not in years_dict:
            years_dict[year] = 0
        years_dict[year] += val['NR_INDIVIZI'] or 0
        years_dict[year] += 30 * (val['NR_INDIVIZI_IZOLATI'] or 0)
    for val in values_ext:
        year = get_year(val['DATA'])
        if year not in years_dict:
            years_dict[year] = 0
        if val['NR_INDIVIZI']:
            years_dict[year] += 100
    return years_dict


def get_population_magnitude(values_int, values_ext):
    years_dict = get_years_dict(values_int, values_ext)
    population_min = min(years_dict.values())
    population_max = max(years_dict.values())
    max_diff = population_max - population_min
    magnitude_max = max_diff / (population_min or 1) * 100
    min_diff = max_diff
    pop_min_diff = population_min
    for k1, v1 in years_dict.iteritems():
        for k2, v2 in years_dict.iteritems():
            if 0 <= v1 - v2 < max_diff:
                min_diff = v1 - v2
                pop_min_diff = v2
    magnitude_min = min_diff / (pop_min_diff or 1) * 100
    return magnitude_min, magnitude_max
