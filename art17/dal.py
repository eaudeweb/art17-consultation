from art17.models import (
    LuBiogeoreg,
    LuGrupSpecie,
)


def get_biogeo_regions():
    return LuBiogeoreg.query.all()


def get_species_groups():
    return LuGrupSpecie.query.all()
