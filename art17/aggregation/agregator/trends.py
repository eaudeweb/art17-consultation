(SHORT_TERM, LONG_TERM) = range(2)


def term_start(term, year):
    if term == SHORT_TERM:
        return year - 12
    elif term == LONG_TERM:
        return year - 24
    else:
        raise ValueError("Invalid term")


def get_species_range_trend(term, year):
    start = term_start(term, year)

    return 'x'


def get_species_population_trend(term, year):
    start = term_start(term, year)

    return 'x'


def get_species_habitat_trend(term, year):
    start = term_start(term, year)

    return 'x'


def get_habitat_range_trend(term, year):
    start = term_start(term, year)

    return 'x'


def get_habitat_coverage_trend(term, year):
    start = term_start(term, year)

    return 'x'

