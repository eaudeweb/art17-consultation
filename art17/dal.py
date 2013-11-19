from art17.models import (
    LuBiogeoreg,
)


def get_biogeo_regions():
    return LuBiogeoreg.query.all()
