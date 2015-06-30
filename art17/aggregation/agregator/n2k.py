from flask import current_app
from urllib import urlencode
import requests

HABITAT_COVER_URL = '/Natura2000/MapServer/28'
SPECIES_COVER_URL = '/Natura2000/MapServer/26'


def generic_n2k_call(url, where_query, out_fields=""):
    url = current_app.config.get('GIS_API_URL') + url
    url += "/query?" + urlencode({
        'where': where_query,
        'outFields': out_fields,
        'f': "json",
        'returnGeometry': "false",
    })

    # print "Requesting:" + url
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        return data.get('features')


def get_habitat_cover_range(subgroup, habcode, region):
    if subgroup is None:
        return None, None
    where_query = "HABITAT_CODE='%s'" % habcode
    data = generic_n2k_call(HABITAT_COVER_URL, where_query,
                            out_fields="HABITAT_COVER,SITE_AREA")
    if not data:
        return None, None

    # Compute percent of site_area occupied by this habitat
    values = [(e['attributes']['HABITAT_COVER'] or 0) * 0.01 *
              (e['attributes']['SITE_AREA'] or 0) for e in data]
    # Sum up values for all sites and convert to km2
    max_val = sum(values) * 0.01
    return None, max_val


def get_species_population_range(subgroup, speccode, region):
    if subgroup is None:
        return None, None, None
    where_query = "SPECIES_CODE='%s'" % speccode
    data = generic_n2k_call(
        SPECIES_COVER_URL, where_query,
        out_fields="SPECIES_SIZE_MIN,SPECIES_SIZE_MAX,SPECIES_UNIT"
    )
    if not data:
        return None, None, None

    min_values = [
        v for v in
        (e['attributes']['SPECIES_SIZE_MIN'] for e in data)
        if v is not None
    ]

    max_values = [
        v for v in
        (e['attributes']['SPECIES_SIZE_MAX'] for e in data)
        if v is not None
    ]
    units = [
        v for v in
        (e['attributes']['SPECIES_UNIT'] for e in data)
        if v is not None
    ]
    unit = (units and units[0]) or None
    min_value, max_value = sum(min_values) or None, sum(max_values) or None

    return min_value, max_value, unit
