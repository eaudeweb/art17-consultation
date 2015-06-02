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
        subgroup = PL
        logging.warn('Unknown subgroup for speciescode: {0} returning PL'
                     .format(speciescode))
    return subgroup
