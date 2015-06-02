"""
    Define a mapping between species codes and subgroups.
"""
import logging

(
    AR,  # Amfibieni si reptile
    LL,  # Lilieci
    MM,  # Mamifere
    NV,  # Nevertebrate
    PE,  # Pesti
    PL,  # Plante
    MR,  # Mamifere marine
    PM,  # Pesti marini
) = range(8)

SPECIES_SUBGROUPS = [
    AR, LL, MM, NV, PE, PL, MR, PM,
]


def get_species_mapping():
    # TODO: maybe load it from somewhere
    return {
        '1758': PL,
        '1188': AR,
    }


def get_species_subgroup(speciescode):
    mapping = get_species_mapping()

    subgroup = mapping.get(speciescode)
    if subgroup is None:
        logging.warn('Unknown subgroup for speciescode: {0} '
                     .format(speciescode))
    return subgroup


(
    PADURI,
) = range(1)


def get_habitat_mapping():
    return {
        '9110': PADURI,
        '9130': PADURI,
        '9150': PADURI,
        '9170': PADURI,
        '9180': PADURI,
        '91AA': PADURI,
        '91D0': PADURI,
        '91E0': PADURI,
        '91F0': PADURI,
        '91H0': PADURI,
        '91I0': PADURI,
        '91K0': PADURI,
        '91L0': PADURI,
        '91M0': PADURI,
        '91Q0': PADURI,
        '91V0': PADURI,
        '91X0': PADURI,
        '91Y0': PADURI,
        '9260': PADURI,
        '92A0': PADURI,
        '92D0': PADURI,
        '9410': PADURI,
        '9420': PADURI,
        '9530': PADURI,
    }


def get_habitat_subgroup(habcode):
    mapping = get_habitat_mapping()

    subgroup = mapping.get(habcode)
    if subgroup is None:
        logging.warn('Unknown subgroup for habcode: {0}'
                     .format(habcode))
    return subgroup
