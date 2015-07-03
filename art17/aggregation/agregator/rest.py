import hashlib
import json
import os
from flask import current_app
from urllib import urlencode
import logging
import requests
from art17.aggregation.agregator.subgroups import (
    AR, LL, MM, NV, PE, PL, MR, PM, AD, DN, HM, PS, ML, PD, PJ, SR,
)
from art17.aggregation.utils import (
    most_common, get_values, average, get_season, root_mean_square,
)

# GIS urls
SPECIES_DISTRIBUTION_URL = '/IBB_RangeDistribution/MapServer/2'
SPECIES_RANGE_URL = '/IBB_RangeDistribution/MapServer/3'
HABITAT_DISTRIBUTION_URL = "/IBB_RangeDistribution/MapServer/0"
HABITAT_RANGE_URL = "/IBB_RangeDistribution/MapServer/1"

(
    BIBLIO,
    PRES_THRE,
    POP,
    HAB_Q,
    DISTRIB,
    RANGE,
    TYPICAL,
    TREND,
    LAST_10,
    POP_INT,
    POP_EXT,
    TREND_HAB,
) = range(12)

SPECIES_MAPPING = {
    AR: {
        BIBLIO: '/EDW_AGREGARE_HAB/MapServer/55',
        PRES_THRE: '/EDW_AGREGARE_HAB/MapServer/54',
        POP: '/EDW_AGREGARE_HAB/MapServer/53',
        HAB_Q: '/EDW_AGREGARE_HAB/MapServer/52',
        DISTRIB: SPECIES_DISTRIBUTION_URL,
        RANGE: SPECIES_RANGE_URL,
    },
    LL: {
        BIBLIO: '/EDW_AGREGARE_HAB/MapServer/16',
        PRES_THRE: '/EDW_AGREGARE_HAB/MapServer/15',
        HAB_Q: '/EDW_AGREGARE_HAB/MapServer/14',
        TREND: '/EDW_AGREGARE_HAB/MapServer/56',
        POP_INT: '/EDW_AGREGARE_HAB/MapServer/59',
        POP_EXT: '/EDW_AGREGARE_HAB/MapServer/58',
        TREND_HAB: '/EDW_AGREGARE_HAB/MapServer/57',
        DISTRIB: SPECIES_DISTRIBUTION_URL,
        RANGE: SPECIES_RANGE_URL,
    },
    MM: {
        BIBLIO: '/EDW_AGREGARE_HAB/MapServer/23',
        PRES_THRE: '/EDW_AGREGARE_HAB/MapServer/42',
        POP: '/EDW_AGREGARE_HAB/MapServer/43',
        HAB_Q: '/EDW_AGREGARE_HAB/MapServer/43',
        DISTRIB: SPECIES_DISTRIBUTION_URL,
        RANGE: SPECIES_RANGE_URL,
    },
    NV: {
        BIBLIO: '/EDW_AGREGARE_HAB/MapServer/26',
        PRES_THRE: '/EDW_AGREGARE_HAB/MapServer/25',
        POP: '/EDW_AGREGARE_HAB/MapServer/24',
        HAB_Q: '/EDW_AGREGARE_HAB/MapServer/24',
        DISTRIB: SPECIES_DISTRIBUTION_URL,
        RANGE: SPECIES_RANGE_URL,
    },
    PE: {
        BIBLIO: '/EDW_AGREGARE_HAB/MapServer/39',
        PRES_THRE: '/EDW_AGREGARE_HAB/MapServer/40',
        POP: '/EDW_AGREGARE_HAB/MapServer/41',
        DISTRIB: SPECIES_DISTRIBUTION_URL,
        RANGE: SPECIES_RANGE_URL,
    },
    PL: {
        BIBLIO: '/EDW_AGREGARE_HAB/MapServer/35',
        PRES_THRE: '/EDW_AGREGARE_HAB/MapServer/6',
        POP: '/EDW_AGREGARE_HAB/MapServer/34',
        HAB_Q: '/EDW_AGREGARE_HAB/MapServer/36',
        DISTRIB: SPECIES_DISTRIBUTION_URL,
        RANGE: SPECIES_RANGE_URL,
    },
    MR: {
        BIBLIO: '/EDW_AGREGARE_HAB/MapServer/21',
        PRES_THRE: '/EDW_AGREGARE_HAB/MapServer/22',
        POP: '/EDW_AGREGARE_HAB/MapServer/60',
        HAB_Q: '/EDW_AGREGARE_HAB/MapServer/60',
        DISTRIB: SPECIES_DISTRIBUTION_URL,
        RANGE: SPECIES_RANGE_URL,
    },
    PM: {
        BIBLIO: '/EDW_AGREGARE_HAB/MapServer/28',
        PRES_THRE: '/EDW_AGREGARE_HAB/MapServer/29',
        POP: '/EDW_AGREGARE_HAB/MapServer/27',
        HAB_Q: '/EDW_AGREGARE_HAB/MapServer/27',
        DISTRIB: SPECIES_DISTRIBUTION_URL,
        RANGE: SPECIES_RANGE_URL,
    },
    None: {
        DISTRIB: SPECIES_DISTRIBUTION_URL,
        RANGE: SPECIES_RANGE_URL,
    }
}

HABITAT_MAPPING = {
    AD: {
        BIBLIO: '/EDW_AGREGARE_HAB/MapServer/5',
        PRES_THRE: '/EDW_AGREGARE_HAB/MapServer/4',
        DISTRIB: HABITAT_DISTRIBUTION_URL,
        RANGE: HABITAT_RANGE_URL,
    },
    DN: {
        BIBLIO: '/EDW_AGREGARE_HAB/MapServer/10',
        PRES_THRE: '/EDW_AGREGARE_HAB/MapServer/9',
        DISTRIB: HABITAT_DISTRIBUTION_URL,
        RANGE: HABITAT_RANGE_URL,
    },
    HM: {
        BIBLIO: '/EDW_AGREGARE_HAB/MapServer/12',
        PRES_THRE: '/EDW_AGREGARE_HAB/MapServer/11',
        TYPICAL: '/EDW_AGREGARE_HAB/MapServer/13',
        DISTRIB: HABITAT_DISTRIBUTION_URL,
        RANGE: HABITAT_RANGE_URL,
    },
    PS: {
        TREND: '/EDW_AGREGARE_HAB/MapServer/47',
        LAST_10: '/EDW_AGREGARE_HAB/MapServer/46',
        TYPICAL: '/EDW_AGREGARE_HAB/MapServer/45',
        PRES_THRE: '/EDW_AGREGARE_HAB/MapServer/48',
        DISTRIB: HABITAT_DISTRIBUTION_URL,
        RANGE: HABITAT_RANGE_URL,
    },
    ML: {
        BIBLIO: '/EDW_AGREGARE_HAB/MapServer/19',
        PRES_THRE: '/EDW_AGREGARE_HAB/MapServer/18',
        TYPICAL: '/EDW_AGREGARE_HAB/MapServer/20',
        DISTRIB: HABITAT_DISTRIBUTION_URL,
        RANGE: HABITAT_RANGE_URL,
    },
    PD: {
        BIBLIO: '/EDW_AGREGARE_HAB/MapServer/49',
        PRES_THRE: '/EDW_AGREGARE_HAB/MapServer/50',
        TYPICAL: '/EDW_AGREGARE_HAB/MapServer/51',
        DISTRIB: HABITAT_DISTRIBUTION_URL,
        RANGE: HABITAT_RANGE_URL,
    },
    PJ: {
        BIBLIO: '/EDW_AGREGARE_HAB/MapServer/31',
        PRES_THRE: '/EDW_AGREGARE_HAB/MapServer/30',
        DISTRIB: HABITAT_DISTRIBUTION_URL,
        RANGE: HABITAT_RANGE_URL,
    },
    SR: {
        BIBLIO: '/EDW_AGREGARE_HAB/MapServer/33',
        PRES_THRE: '/EDW_AGREGARE_HAB/MapServer/32',
        DISTRIB: HABITAT_DISTRIBUTION_URL,
        RANGE: HABITAT_RANGE_URL,
    },
    None: {
        DISTRIB: HABITAT_DISTRIBUTION_URL,
        RANGE: HABITAT_RANGE_URL,
    }
}


def _log_error(url):
    sentry = current_app.extensions.get('sentry')
    if sentry:
        pass
        # TODO Uncomment this once we have a reliable web service
        # sentry.captureMessage(message='Webservice down: %s' % url)
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
    return SPECIES_MAPPING[subgroup].get(service)


def _get_habitat_url(subgroup, service):
    if subgroup not in HABITAT_MAPPING:
        logging.debug(
            'No url found for service {0} in subgroup {1} H'.format(service,
                                                                    subgroup))
        return None
    return HABITAT_MAPPING[subgroup].get(service)


def uglycache(f):
    def _f(url, *args, **kwargs):
        if url is None:
            return {}
        params = url + ''.join(str(a) for a in args)
        params += ''.join(str(v) for v in kwargs.values())
        m = hashlib.md5()
        m.update(params)
        filename = m.hexdigest()
        path = os.path.join(current_app.config['UGLY_CACHE'], filename)
        result = None
        if os.path.exists(path):
            try:
                result = json.load(open(path))
            except:
                print "Invalid cache."
                pass
        if result is not None:
            print "Returning from cache: ", filename, url, args, kwargs
            return result
        result = f(url, *args, **kwargs)
        with open(path, 'w') as fout:
            json.dump(result, fout)
            print "Saving in cache: ", filename, url, args, kwargs
        return result

    return _f


@uglycache
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
    return sum(r['attributes']['NR_INDIVIZI'] or 0 for r in data)


def get_species_habitat_quality(subgroup, specnum, region):
    OK_VALUE_LIST = [1, 2, 3]
    VALUE_MAP = {
        1: 'Bad',
        2: 'Moderate',
        3: 'Good',
    }
    where_query = "SPECIE='%s' AND REG_BIOGEO='%s'" % (specnum, region)
    url = _get_species_url(subgroup, HAB_Q)
    data = generic_rest_call(url, where_query) or []
    values = [r['attributes']['CALITATE_HAB'] for r in data]
    ok_values = [v for v in values if v in OK_VALUE_LIST]

    if ok_values:
        avg = sum(ok_values) * 1. / len(ok_values)
        return VALUE_MAP[int(round(avg))]

    else:
        return 'Unknown'


def get_habitat_published(subgroup, habcode, region):
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
    where_query = "HABITAT='%s' AND REG_BIOGEO='%s'" % (habcode, region)
    url = _get_habitat_url(subgroup, BIBLIO)
    data = generic_rest_call(url, where_query) or []

    rv = []
    for row in data:
        rv.append(', '.join(row['attributes'][k] for k in FIELDS) + '\n')
    return ''.join(rv), len(data)


def get_habitat_typical_species(subgroup, habcode, region):
    where_query = "HABITAT='%s' AND REG_BIOGEO='%s'" % (habcode, region)
    url = _get_habitat_url(subgroup, TYPICAL)
    data = generic_rest_call(url, where_query) or []
    return [r['attributes']['SPECIE'] for r in data]


def get_habitat_pressures_threats(subgroup, habcode, region):
    type_map = {
        None: None,  # ???
        1: 't',  # threat
        2: 'p',  # pressure
    }
    where_query = "HABITAT='%s' AND REG_BIOGEO='%s'" % (habcode, region)
    url = _get_habitat_url(subgroup, PRES_THRE)
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


def generic_surface_call(url, where_query, out_fields=""):
    features = generic_rest_call(url, where_query, out_fields=out_fields)
    result = (features and features[0]['attributes']) or {}
    if ',' in out_fields:
        surface = {c: result.get(c) for c in out_fields.split(',')}
    else:
        surface = result.get(out_fields)
    return surface


def get_habitat_dist_surface(subgroup, habcode, region):
    where_query = "HABITAT='%s'" % habcode
    url = _get_habitat_url(subgroup, DISTRIB)
    return generic_surface_call(url, where_query, region)


def get_habitat_range_surface(subgroup, habcode, region):
    where_query = "HABITAT='%s'" % habcode
    url = _get_habitat_url(subgroup, RANGE)
    return generic_surface_call(url, where_query, region)


def get_species_dist_surface(subgroup, speccode, region):
    where_query = "SPECNUM='%s'" % speccode
    url = _get_species_url(subgroup, DISTRIB)
    return generic_surface_call(url, where_query, region)


def get_species_range_surface(subgroup, speccode, region):
    where_query = "SPECNUM='%s'" % speccode
    url = _get_species_url(subgroup, RANGE)
    return generic_surface_call(url, where_query, region)


def get_seasonal_avg(values, fields, mean_func):
    seasonal_values = {key: {} for key in fields}
    for field in fields:
        for value in values:
            if not value[field]:
                continue
            season = get_season(value['DATA'])
            seasonal_values[field].setdefault(season, []).append(value[field])
    return {key: {k: mean_func(v) for k, v in val.iteritems()}
            for key, val in seasonal_values.iteritems()}


def get_seasonal_intervals(values, fields):
    deviations = get_seasonal_avg(values, fields, root_mean_square)
    averages = get_seasonal_avg(values, fields, average)
    return {key: {k: (averages[key][k] - 2 * v, averages[key][k] + 2 * v)
                  for k, v in val.iteritems()}
            for key, val in deviations.iteritems()}


def get_PS_trend(habcode, region):
    where_query = "HABITAT='%s' AND REG_BIOGEO='%s'" % (habcode, region)
    url = _get_habitat_url(PS, TREND)
    data = generic_rest_call(url, where_query) or []
    values = [r['attributes'] for r in data]

    if not values:
        return

    grad = most_common(get_values(values, 'GRAD'))
    rang = most_common(get_values(values, 'RANG'))

    morf_fields = ['MORFOLOGIE_LOC_ST', 'UMPLUTURA', 'REGIM_HIDRO',
                   'ACUMULARE_APA', 'IVIRE_APA', 'SURSA_MICRO_PICATURI']
    morf_frequencies = []
    for field in morf_fields:
        morf_values = get_values(values, field)
        if not morf_values:
            continue
        most_common_value = most_common(morf_values)
        frequency = (morf_values.count(most_common_value) /
                     float(len(morf_values) or 1))
        morf_frequencies.append(frequency)
    morf_frequency = average(morf_frequencies)

    env_fields = ['TEMP_INT', 'UMITIDATE_REL']
    seasonal_averages = get_seasonal_avg(values, env_fields, average)

    url = _get_habitat_url(PS, LAST_10)
    data = generic_rest_call(url, where_query) or []
    values = [r['attributes'] for r in data]

    hist_seasonal_intervals = get_seasonal_intervals(values, env_fields)

    env_characteristics = 0
    for field, seasonal_values in seasonal_averages.iteritems():
        for season, value in seasonal_values.iteritems():
            min, max = hist_seasonal_intervals[field][season]
            if min <= value <= max:
                env_characteristics += 1
            else:
                env_characteristics -= 1

    return grad, rang, (env_characteristics >= 0), morf_frequency


def get_LL_range_trend(specnum, region):
    where_query = "SPECIE='%s' AND REG_BIOGEO='%s'" % (specnum, region)
    url = _get_species_url(LL, TREND)
    data = generic_rest_call(url, where_query) or []
    values = [r['attributes'] for r in data]

    if not values:
        return

    trend = most_common(get_values(values, 'TREND'))
    cons = most_common(get_values(values, 'STARE_CONS'))
    rang = most_common(get_values(values, 'RANG'))

    return trend, cons, rang


def get_LL_population(specnum, region):
    where_query = "SPECIE='%s' AND REG_BIOGEO='%s'" % (specnum, region)
    url = _get_species_url(LL, POP_INT)
    data = generic_rest_call(url, where_query) or []
    values_int = [r['attributes'] for r in data]

    url = _get_species_url(LL, POP_EXT)
    data = generic_rest_call(url, where_query) or []
    values_ext = [r['attributes'] for r in data]

    return values_int, values_ext


def get_LL_habitat_trend(specnum, region):
    where_query = "SPECIE='%s' AND REG_BIOGEO='%s'" % (specnum, region)
    url = _get_species_url(LL, TREND_HAB)
    data = generic_rest_call(url, where_query) or []
    values = [r['attributes'] for r in data]
    if not values:
        return

    hab_q = most_common(get_values(values, 'CALITATE_HAB'))
    cons = most_common(get_values(values, 'STARE_CONS'))

    return hab_q, cons
