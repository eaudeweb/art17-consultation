
(SHORT_TERM, LONG_TERM) = range(2)

def get_species_range_trend(term, year):
    if term == SHORT_TERM:
        start = year - 12
    elif term == LONG_TERM:
        start = year - 24
    else:
        raise ValueError("Invalid term")


    return 'x'
