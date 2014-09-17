from flask import current_app
from urllib import urlencode
import requests

SPECIES_BIBLIO_URL = '/Agregare/MapServer/3'
SPECIES_PT_URL = '/Agregare/MapServer/1'
SPECIES_POP_URL = '/Agregare/MapServer/2'
HABITAT_SPECIES_URL = '/AgregareHabitate/MapServer/2'


def generic_rest_call(url, where_query, out_fields="*"):
    url = current_app.config.get('GIS_API_URL') + url
    url += "/query?" + urlencode({
        'where': where_query,
        'outFields': out_fields,
        'f': "json",
        'returnGeometry': "false",
    })

    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        return data.get('features')


def get_species_bibliography(specnum, region):
    where_query = "SPECIE='%s' AND REG_BIOGEO='%s'" % (specnum, region)
    data = generic_rest_call(SPECIES_BIBLIO_URL, where_query)
    if not data:
        return ''

    format_string = (
        u"{AUTORI} {TITLU_LUCRARE} {AN} {PUBLICATIE} "
        u"{EDITURA} {ORAS} {VOLUM} {PAGINI}\n"
    )
    values = [format_string.format(**e["attributes"]) for e in data]
    return ''.join(values)


def get_species_pressures_threats(specnum, region):
    type_map = {
        None: None,  # ???
        1: 't',  # threat
        2: 'p',  # pressure
    }
    where_query = "SPECIE='%s' AND REG_BIOGEO='%s'" % (specnum, region)
    data = generic_rest_call(SPECIES_PT_URL, where_query)
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


def get_species_population_size(specnum, region):
    where_query = "SPECIE='%s' AND REG_BIOGEO='%s'" % (specnum, region)
    data = generic_rest_call(SPECIES_POP_URL, where_query) or []
    return sum(r['attributes']['NR_INDIVIZI'] for r in data)


def get_species_habitat_quality(specnum, region):
    OK_VALUE_LIST = [1, 2, 3]
    VALUE_MAP = {
        1: 'Bad',
        2: 'Moderate',
        3: 'Good',
    }
    where_query = "SPECIE='%s' AND REG_BIOGEO='%s'" % (specnum, region)
    data = generic_rest_call(SPECIES_POP_URL, where_query) or []
    values = [r['attributes']['CALITATE_HAB'] for r in data]
    ok_values = [v for v in values if v in OK_VALUE_LIST]

    if ok_values:
        avg = sum(ok_values) * 1. / len(ok_values)
        return VALUE_MAP[int(round(avg))]

    else:
        return 'Unknown'


def get_habitat_typical_species(habcode, region):
    where_query = "HABITAT='%s' AND REG_BIOGEG='%s'" % (habcode, region)
    data = generic_rest_call(HABITAT_SPECIES_URL, where_query) or []
    return [r['attributes']['NAME'] for r in data]
