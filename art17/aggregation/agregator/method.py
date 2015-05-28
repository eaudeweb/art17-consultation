from art17.aggregation.agregator import (
    UNKNOWN_METHOD, EXPERT_METHOD, EXTRAPOLATION_METHOD, COMPLETE_METHOD,
)


def get_method(count):
    if count is None:
        return UNKNOWN_METHOD
    if count < 99:
        return EXPERT_METHOD
    elif count < 299:
        return EXTRAPOLATION_METHOD
    else:
        return COMPLETE_METHOD


def get_species_method(subgroup, count):
    return get_method(count)
