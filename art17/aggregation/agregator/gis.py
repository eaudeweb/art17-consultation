import logging
from urllib import urlencode
import requests
from flask import current_app


HABITAT_DISTRIBUTION_URL = "/IBB_RangeDistribution/MapServer/0"
HABITAT_RANGE_URL = "/IBB_RangeDistribution/MapServer/1"
SPECIES_DISTRIBUTION_URL = "/IBB_RangeDistribution/MapServer/2"
SPECIES_RANGE_URL = "/IBB_RangeDistribution/MapServer/3"


def generic_surface_call(url, where_query):
    url = current_app.config.get('GIS_API_URL') + url
    url += "?" + urlencode(
        {'where': where_query, 'outFields': "SHAPE.AREA",
         'f': "json"})

    logging.debug("Requesting:" + url)
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()

        if not data['features']:
            return None

        surface = data['features']['attributes']['SHAPE.AREA']
        # return the value in square kilometers
        return surface / (1000 * 1000)
    return None


def get_habitat_dist_surface(habcode, region):
    where_query = "HABITAT=%s" % habcode

    return generic_surface_call(HABITAT_DISTRIBUTION_URL, where_query)


def get_habitat_range_surface(habcode, region):
    where_query = "HABITAT=%s" % habcode

    return generic_surface_call(HABITAT_RANGE_URL, where_query)


def get_species_dist_surface(speccode, region):
    where_query = "SPECNUM=%s" % speccode

    return generic_surface_call(SPECIES_DISTRIBUTION_URL, where_query)


def get_species_range_surface(speccode, region):
    where_query = "SPECNUM=%s" % speccode

    return generic_surface_call(SPECIES_RANGE_URL, where_query)


