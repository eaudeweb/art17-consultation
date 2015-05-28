"""
    Define a mapping between species codes and subgroups.
"""

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
    }


def get_species_subgroup(speciescode):
    mapping = get_species_mapping()

    return mapping.get(speciescode, PL)  # default: Plante
