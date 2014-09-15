from flask import current_app
from urllib import urlencode
import requests

SPECIES_BIBLIO_URL = '/Agregare/MapServer/3'


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
