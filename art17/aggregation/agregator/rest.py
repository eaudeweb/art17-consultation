from flask import current_app
from urllib import urlencode
import logging
import requests
from art17.aggregation.agregator.subgroups import PL, AR

# Colectare URLs
HABITAT_BIBLIO_URL = '/AgregareHabitate/MapServer/1'
HABITAT_SPECIES_URL = '/AgregareHabitate/MapServer/2'
HABITAT_PRESS_URL = ''  # TODO: there is no press threats url for habitats

# GIS urls
HABITAT_DISTRIBUTION_URL = "/IBB_RangeDistribution/MapServer/0"
HABITAT_RANGE_URL = "/IBB_RangeDistribution/MapServer/1"

(
    BIBLIO,
    PRES_THRE,
    POP,
    DISTRIB,
    RANGE,
) = range(5)

# TODO: map everything from here: https://www.simshab.ro/arcgis/rest/services/EDW_AGREGARE_HAB/MapServer
SPECIES_MAPPING = {
    PL: {
        BIBLIO: '/Agregare/MapServer/3',
        PRES_THRE: '/Agregare/MapServer/1',
        POP: '/Agregare/MapServer/2',
        DISTRIB: '/IBB_RangeDistribution/MapServer/2',
        RANGE: '/IBB_RangeDistribution/MapServer/3'
    },
    AR: {
        BIBLIO: '/EDW_AGREGARE_HAB/MapServer/10',
        PRES_THRE: '/EDW_AGREGARE_HAB/MapServer/9',
        POP: '/EDW_AGREGARE_HAB/MapServer/8',
        DISTRIB: '/IBB_RangeDistribution/MapServer/2',
        RANGE: '/IBB_RangeDistribution/MapServer/3'
    }
}


def _log_error(url):
    sentry = current_app.extensions.get('sentry')
    if sentry:
        sentry.captureMessage(message='Webservice down: %s' % url)
    logging.warn('Webservice down: %s' % url)


def _get_species_url(subgroup, service):
    if subgroup not in SPECIES_MAPPING:
        # raise NotImplementedError(
        #     'No mapping for species group: %s' % subgroup
        # )
        logging.debug(
            'No url found for service {0} in subgroup {1}'.format(service,
                                                                  subgroup))
        return None
    return SPECIES_MAPPING[subgroup][service]


def generic_rest_call(url, where_query, out_fields="*"):
    if not url:
        return {}
    url = current_app.config.get('GIS_API_URL') + url
    url += "/query?" + urlencode({
        'where': where_query,
        'outFields': out_fields,
        'f': "json",
        'returnGeometry': "false",
    })

    res = requests.get(url)
    data = None
    if res.status_code == 200:
        data = res.json()

    if not data or 'error' in data:
        _log_error(url)

    return data.get('features', {})


def get_species_bibliography(subgroup, specnum, region):
    # TODO: se pare ca s-a modificat apelul, nu primeste parametru REG_BIOGEO, iar in loc de SPECIE avem CODE
    # see: https://www.simshab.ro/arcgis/rest/services/EDW_AGREGARE_HAB/MapServer/10
    where_query = "SPECIE='%s' AND REG_BIOGEO='%s'" % (specnum, region)
    url = _get_species_url(subgroup, BIBLIO)
    data = generic_rest_call(url, where_query) or []

    format_string = (
        u"{AUTORI} {TITLU_LUCRARE} {AN} {PUBLICATIE} "
        u"{EDITURA} {ORAS} {VOLUM} {PAGINI}\n"
    )
    values = [format_string.format(**e["attributes"]) for e in data]
    return ''.join(values), len(data)


def get_species_pressures_threats(subgroup, specnum, region):
    type_map = {
        None: None,  # ???
        1: 't',  # threat
        2: 'p',  # pressure
    }
    where_query = "SPECIE='%s' AND REG_BIOGEO='%s'" % (specnum, region)
    url = _get_species_url(subgroup, PRES_THRE)
    data = generic_rest_call(url, where_query)
    if not data:
        return ''

    data = [e["attributes"] for e in data]
    return [
        {
            'pressure': d["AMENINTARI"],
            'ranking': d["RANG"],
            'type': type_map[d["TIP"]],
            'pollution': d["POLUARE"],
        }
        for d in data
    ]


def get_species_population_size(subgroup, specnum, region):
    where_query = "SPECIE='%s' AND REG_BIOGEO='%s'" % (specnum, region)
    url = _get_species_url(subgroup, POP)
    data = generic_rest_call(url, where_query) or []
    return sum(r['attributes']['NR_INDIVIZI'] for r in data)


def get_species_habitat_quality(subgroup, specnum, region):
    OK_VALUE_LIST = [1, 2, 3]
    VALUE_MAP = {
        1: 'Bad',
        2: 'Moderate',
        3: 'Good',
    }
    where_query = "SPECIE='%s' AND REG_BIOGEO='%s'" % (specnum, region)
    url = _get_species_url(subgroup, POP)
    data = generic_rest_call(url, where_query) or []
    values = [r['attributes']['CALITATE_HAB'] for r in data]
    ok_values = [v for v in values if v in OK_VALUE_LIST]

    if ok_values:
        avg = sum(ok_values) * 1. / len(ok_values)
        return VALUE_MAP[int(round(avg))]

    else:
        return 'Unknown'


def get_habitat_published(habcode, region):
    FIELDS = [
        'AUTORI',
        'TITLU_LUCRARE',
        'AN',
        'PUBLICATIE',
        'EDITURA',
        'ORAS',
        'VOLUM',
        'PAGINI',
    ]
    where_query = "COD_HABITAT='%s' AND REG_BIOGEG='%s'" % (habcode, region)
    data = generic_rest_call(HABITAT_BIBLIO_URL, where_query) or []

    rv = []
    for row in data:
        rv.append(', '.join(row['attributes'][k] for k in FIELDS) + '\n')
    return ''.join(rv), len(data)


def get_habitat_typical_species(habcode, region):
    where_query = "HABITAT='%s' AND REG_BIOGEG='%s'" % (habcode, region)
    data = generic_rest_call(HABITAT_SPECIES_URL, where_query) or []
    return [r['attributes']['NAME'] for r in data]


def get_habitat_pressures_threats(habcode, region):
    type_map = {
        None: None,  # ???
        1: 't',  # threat
        2: 'p',  # pressure
    }
    data = []  # TODO connect to a web service
    return [
        {
            'pressure': d["AMENINTARI"],
            'ranking': d["RANG"],
            'type': type_map[d["TIP"]],
            'pollution': d["POLUARE"],
        }
        for d in data
    ]


def generic_surface_call(url, where_query, out_fields=""):
    features = generic_rest_call(url, where_query, out_fields=out_fields)
    result = (features and features[0]['attributes']) or {}
    if ',' in out_fields:
        surface = {c: result.get(c) for c in out_fields.split(',')}
    else:
        surface = result.get(out_fields)
    return surface


def get_habitat_dist_surface(habcode, region):
    where_query = "HABITAT='%s'" % habcode

    return generic_surface_call(HABITAT_DISTRIBUTION_URL, where_query, region)


def get_habitat_range_surface(habcode, region):
    where_query = "HABITAT='%s'" % habcode

    return generic_surface_call(HABITAT_RANGE_URL, where_query, region)


def get_species_dist_surface(subgroup, speccode, region):
    where_query = "SPECNUM='%s'" % speccode
    url = _get_species_url(subgroup, DISTRIB)
    return generic_surface_call(url, where_query, region)


def get_species_range_surface(subgroup, speccode, region):
    where_query = "SPECNUM='%s'" % speccode
    url = _get_species_url(subgroup, RANGE)
    return generic_surface_call(url, where_query, region)
