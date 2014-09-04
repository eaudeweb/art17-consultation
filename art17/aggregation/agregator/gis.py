import logging
from urllib import urlencode
import requests
from flask import current_app


HABITAT_DISTRIBUTION_URL = "/IBB_RangeDistribution/MapServer/0"
HABITAT_RANGE_URL = "/IBB_RangeDistribution/MapServer/1"
SPECIES_DISTRIBUTION_URL = "/IBB_RangeDistribution/MapServer/2"
SPECIES_RANGE_URL = "/IBB_RangeDistribution/MapServer/3"


def generic_surface_call(url, where_query, out_fields=""):
    url = current_app.config.get('GIS_API_URL') + url
    url += "/query?" + urlencode({
        'where': where_query,
        'outFields': out_fields,
        'f': "json",
        'returnGeometry': "false",
    })

    #print "Requesting:" + url
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()

        if not data['features']:
            return None


        result = data['features'][0]['attributes']
        if ',' in out_fields:
            surface = {c: result[c] for c in out_fields.split(',')}
        else:
            surface = result[out_fields]
        return surface
    return None


def get_habitat_dist_surface(habcode, region):
    where_query = "HABITAT='%s'" % habcode

    return generic_surface_call(HABITAT_DISTRIBUTION_URL, where_query, region)


def get_habitat_range_surface(habcode, region):
    where_query = "HABITAT='%s'" % habcode

    return generic_surface_call(HABITAT_RANGE_URL, where_query, region)


def get_species_dist_surface(speccode, region):
    where_query = "SPECNUM='%s'" % speccode

    return generic_surface_call(SPECIES_DISTRIBUTION_URL, where_query, region)


def get_species_range_surface(speccode, region):
    where_query = "SPECNUM='%s'" % speccode

    return generic_surface_call(SPECIES_RANGE_URL, where_query, region)


