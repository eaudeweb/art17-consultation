"""
    Define a mapping between species codes and subgroups.
"""
import logging

from art17.aggregation.refvalues import load_refval

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


def get_mapping(filename):
    mapping = load_refval(filename)
    return {code: eval(subgroup) for code, subgroup in mapping.iteritems()}


def get_species_mapping():
    return get_mapping('species_subgroups.json')


def get_species_subgroup(speciescode):
    mapping = get_species_mapping()

    subgroup = mapping.get(speciescode)
    if subgroup is None:
        logging.warn('Unknown subgroup for speciescode: {0} '
                     .format(speciescode))
    return subgroup


(
    AD,  # Apa dulce
    DN,  # Dune
    HM,  # Habitate marine
    PS,  # Pesteri
    ML,  # Mlastini, Stancarii
    PD,  # Paduri,
    PJ,  # Pajisti
    SR,  # Saraturi
) = range(8)


TYPICAL_SPECIES_METHOD = {
    PS: 'Aggregation of all species of bats found in caves',
}


def get_habitat_mapping():
    return get_mapping('habitats_subgroups.json')


def get_habitat_subgroup(habcode):
    mapping = get_habitat_mapping()

    subgroup = mapping.get(habcode)
    if subgroup is None:
        logging.warn('Unknown subgroup for habcode: {0}'
                     .format(habcode))
    return subgroup
