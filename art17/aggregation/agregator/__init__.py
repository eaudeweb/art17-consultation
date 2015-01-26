from StringIO import StringIO
from collections import defaultdict
from art17 import models, ROLE_AGGREGATED, ROLE_MISSING
from art17.aggregation.agregator.conclusions import \
    get_habitat_conclusion_future, get_overall_habitat_conclusion, \
    get_overall_species_conclusion, get_species_conclusion_future
from art17.aggregation.agregator.n2k import get_habitat_cover_range, \
    get_species_population_range
from art17.aggregation.agregator.rest import get_species_bibliography, \
    get_species_pressures_threats, get_species_population_size, \
    get_species_habitat_quality, get_habitat_typical_species, \
    get_habitat_published
from art17.aggregation.agregator.trends import get_species_range_trend, \
    get_species_population_trend, get_species_habitat_trend, \
    get_habitat_range_trend
from art17.aggregation.prev import load_species_prev, load_habitat_prev, \
    get_subject_prev
from art17.aggregation.refvalues import (
    refvalue_ok, load_species_refval, load_habitat_refval,
    get_subject_refvals_mixed,
)
from art17.aggregation.agregator.primary import (
    get_pressures_threats,
)
from art17.aggregation.utils import (
    get_reporting_id, get_habitat_checklist, get_species_checklist,
    get_checklist)
from art17.aggregation.agregator.gis import (
    get_habitat_dist_surface,
    get_habitat_range_surface,
    get_species_dist_surface,
    get_species_range_surface,
)
from art17.models import DataHabitatSpecies


EXPERT_OPINION = 'Expert opinion'

EXPERT_METHOD = '1'
EXTRAPOLATION_METHOD = '2'
COMPLETE_METHOD = '3'
MISSING_METHOD = '0'
UNKNOWN_METHOD = ''

UNKNOWN_TREND = 'x'
MISSING_DATA = '0'
TERRAIN_DATA = '1'


def get_period(year, length):
    return '%d-%d' % (year - length, year)


def get_conclusion(surface, refvals, refval_type):
    vals = refvals[refval_type]
    fv_text = "adecvat" if refval_type == 'habitat' else "favorabil"
    FV = extract_key(vals, fv_text)
    U1 = extract_key(vals, "U1")
    U2 = extract_key(vals, "U2")

    FV = FV and int(FV)
    U1 = U1 and int(U1)
    U2 = U2 and int(U2)

    if not surface or not FV:
        return 'XX'

    if surface >= FV:
        return 'FV'
    elif surface >= U1:
        return 'U1'
    elif surface >= U2:
        return 'U2'
    return ''


def parse_complementary(refval):
    value, op, unknown = None, None, None
    for k, v in refval.iteritems():
        if 'favorabil' in k:
            value = v or None
        elif 'Operator' in k:
            op = v or None
        elif 'Necunoscut' in k:
            unknown = 1 if v else None
    return value, op, unknown


def set_typical_species(obj, species):
    for sp in species:
        species_obj = DataHabitatSpecies(habitats=obj,
                                         speciesname=sp)
        models.db.session.add(species_obj)


def set_pressures_threats(obj, pressures_threats):
    if isinstance(obj, models.DataHabitattypeRegion):
        foreign_key = {'habitat': obj}
    elif isinstance(obj, models.DataSpeciesRegion):
        foreign_key = {'species': obj}
    else:
        raise RuntimeError('Unknown type %r' % type(obj))

    for row in pressures_threats:
        pressure_obj = models.DataPressuresThreats(
            pressure=row['pressure'],
            ranking=row['ranking'],
            type=row['type'],
            **foreign_key
        )
        pollution_obj = models.DataPressuresThreatsPollution(
            pressure=pressure_obj,
            pollution_qualifier=row['pollution'],
        )
        models.db.session.add(pressure_obj)
    obj.threats_method = TERRAIN_DATA
    obj.pressures_method = TERRAIN_DATA


def extract_key(refval, key):
    for k, v in refval.iteritems():
        if key in k:
            return v
    return None


def get_method(count):
    if count is None:
        return UNKNOWN_METHOD
    if count < 99:
        return EXPERT_METHOD
    elif count < 299:
        return EXTRAPOLATION_METHOD
    else:
        return COMPLETE_METHOD


def aggregate_species(obj, result, refvals, prev):
    current_year = result.dataset.year_end
    current_period = get_period(result.dataset.year_end, 6)
    short_period = get_period(result.dataset.year_end, 12)
    long_period = get_period(result.dataset.year_end, 24)
    # Bibliografie / surse publicate
    result.published, count = get_species_bibliography(obj.code, result.region)

    # Areal
    result.range_surface_area = get_species_range_surface(obj.code,
                                                          result.region)
    result.range_method = get_method(count)
    result.range_trend = get_species_range_trend(trends.SHORT_TERM,
                                                 current_year)
    result.range_trend_period = short_period
    result.range_trend_magnitude_min = refvals["magnitude"]["Magn. min scurt"]
    result.range_trend_magnitude_max = refvals["magnitude"]["Magn. max scurt"]
    result.range_trend_long = get_species_range_trend(trends.LONG_TERM,
                                                      current_year)
    result.range_trend_long_period = long_period
    result.range_trend_long_magnitude_min = refvals["magnitude"][
        "Magn. min lung"]
    result.range_trend_long_magnitude_max = refvals["magnitude"][
        "Magn. max lung"]
    (
        result.complementary_favourable_range,
        result.complementary_favourable_range_op,
        result.complementary_favourable_range_unknown,
    ) = parse_complementary(refvals["range"])
    result.complementary_favourable_range_method = EXPERT_OPINION
    result.conclusion_range = get_conclusion(result.range_surface_area,
                                             refvals, "range")

    # Populatie
    size = get_species_population_size(obj.code, result.region)
    result.population_size_unit = 'i'
    result.population_minimum_size = size
    result.population_maximum_size = size

    result.population_additional_locality = extract_key(
        refvals["population_units"], "localit")
    result.population_additional_method = extract_key(
        refvals["population_units"], "Metoda")
    result.population_additional_problems = extract_key(
        refvals["population_units"], "Dificult")
    result.population_trend = get_species_population_trend(trends.SHORT_TERM,
                                                           current_year)
    result.population_trend_period = short_period
    result.population_method = EXTRAPOLATION_METHOD
    result.population_date = current_period
    result.population_trend_magnitude_min = refvals["population_magnitude"][
        "Magn. min scurt"]
    result.population_trend_magnitude_max = refvals["population_magnitude"][
        "Magn. max scurt"]
    result.population_trend_magnitude_ci = refvals["population_magnitude"][
        "Interval incredere scurt"]
    result.population_trend_method = MISSING_DATA
    result.population_trend_long = get_species_population_trend(
        trends.LONG_TERM, current_year)
    result.population_trend_long_period = long_period
    result.population_trend_long_magnitude_min = \
        refvals["population_magnitude"]["Magn. min lung"]
    result.population_trend_long_magnitude_max = \
        refvals["population_magnitude"]["Magn. max lung"]
    result.population_trend_long_magnitude_ci = \
        refvals["population_magnitude"]["Interval incredere lung"]
    result.population_trend_long_method = MISSING_DATA
    (
        result.complementary_favourable_population,
        result.complementary_favourable_population_op,
        result.complementary_favourable_population_unknown,
    ) = parse_complementary(refvals["population_range"])
    result.complementary_favourable_population_method = EXPERT_OPINION


    # Habitat
    result.habitat_surface_area = get_species_dist_surface(obj.code,
                                                           result.region)
    result.habitat_method = get_method(count)

    result.habitat_quality = get_species_habitat_quality(obj.code,
                                                         result.region)

    result.habitat_trend = get_species_habitat_trend(trends.SHORT_TERM,
                                                     current_year)
    result.habitat_trend_period = short_period
    result.habitat_trend_long = get_species_habitat_trend(trends.LONG_TERM,
                                                          current_year)
    result.habitat_trend_long_period = long_period
    result.habitat_area_suitable = extract_key(refvals["habitat"], "adecvat")
    result.habitat_date = current_period

    result.conclusion_habitat = get_conclusion(result.habitat_surface_area,
                                               refvals, "habitat")

    # Presiuni & Amenintari
    pressure_threats = get_species_pressures_threats(obj.code, result.region)
    set_pressures_threats(result, pressure_threats)

    # Complementare

    # Natura 2000
    n2k_min, n2k_max, n2k_unit = get_species_population_range(obj.code, result.region)
    result.natura2000_population_unit = n2k_unit
    result.natura2000_population_min = n2k_min
    result.natura2000_population_max = n2k_max

    # Masuri de conservare

    # Future
    result.conclusion_future = get_species_conclusion_future(obj.code, result.region)

    # Concluzii Overall
    result.conclusion_assessment = get_overall_species_conclusion(result)

    return result


def aggregate_habitat(obj, result, refvals, prev):
    current_year = result.dataset.year_end
    current_period = get_period(result.dataset.year_end, 6)
    short_period = get_period(result.dataset.year_end, 12)
    long_period = get_period(result.dataset.year_end, 24)
    # Bibliografie
    result.published, count = get_habitat_published(obj.code, result.region)

    # Areal
    result.range_surface_area = get_habitat_range_surface(obj.code,
                                                          result.region)
    result.range_method = get_method(count)
    result.range_trend = get_habitat_range_trend(trends.SHORT_TERM,
                                                 current_year)
    result.range_trend_period = short_period
    result.range_trend_magnitude_min = refvals["magnitude"]["Magn. min scurt"]
    result.range_trend_magnitude_max = refvals["magnitude"]["Magn. max scurt"]
    result.range_trend_long = get_habitat_range_trend(trends.LONG_TERM,
                                                      current_year)
    result.range_trend_long_period = long_period
    result.range_trend_long_magnitude_min = refvals["magnitude"][
        "Magn. min lung"]
    result.range_trend_long_magnitude_max = refvals["magnitude"][
        "Magn. max lung"]
    (
        result.complementary_favourable_range,
        result.complementary_favourable_range_op,
        result.complementary_favourable_range_unknown,
    ) = parse_complementary(refvals["range"])
    result.complementary_favourable_range_method = EXPERT_OPINION
    result.conclusion_range = get_conclusion(result.range_surface_area,
                                             refvals, "range")

    # Suprafata
    result.coverage_surface_area = get_habitat_dist_surface(obj.code,
                                                            result.region)
    result.coverage_date = current_period
    result.coverage_method = get_method(count)
    result.coverage_trend = get_habitat_range_trend(trends.SHORT_TERM,
                                                    current_year)
    result.coverage_trend_period = short_period
    result.coverage_trend_magnitude_min = refvals["coverage_magnitude"][
        "Magn. min scurt"]
    result.coverage_trend_magnitude_max = refvals["coverage_magnitude"][
        "Magn. max scurt"]
    result.coverage_trend_magnitude_ci = refvals["coverage_magnitude"][
        "Interval incredere scurt"]
    result.coverage_trend_method = MISSING_DATA
    result.coverage_trend_long = get_habitat_range_trend(trends.LONG_TERM,
                                                         current_year)

    result.coverage_trend_long_period = long_period
    result.coverage_trend_long_magnitude_min = refvals["coverage_magnitude"][
        "Magn. min lung"]
    result.coverage_trend_long_magnitude_max = refvals["coverage_magnitude"][
        "Magn. max lung"]
    result.coverage_trend_long_magnitude_ci = refvals["coverage_magnitude"][
        "Interval incredere lung"]
    result.coverage_trend_long_method = MISSING_DATA
    (
        result.complementary_favourable_area,
        result.complementary_favourable_area_op,
        result.complementary_favourable_area_unknown,
    ) = parse_complementary(refvals["coverage_range"])
    result.complementary_favourable_area_method = EXPERT_OPINION
    result.conclusion_area = get_conclusion(result.coverage_surface_area,
                                            refvals, "coverage_range")


    # Presiuni & Amenintari ??

    # Natura 2000
    n2k_min, n2k_max = get_habitat_cover_range(obj.code, result.region)
    result.natura2000_area_min = n2k_min
    result.natura2000_area_max = n2k_max

    # Masuri de conservare

    # Specii tipice
    typical_species = get_habitat_typical_species(obj.code, result.region)
    set_typical_species(result, typical_species)

    # Presiuni, amenintari
    pressures_threats = get_pressures_threats(obj.code, result.region)
    set_pressures_threats(result, pressures_threats)

    # Future
    result.conclusion_future = get_habitat_conclusion_future(obj.code, result.region)

    # Concluzii Overall
    result.conclusion_assessment = get_overall_habitat_conclusion(result)

    return result


def aggregate_object(obj, dataset, refvals, timestamp, user_id, prev):
    """
    Aggregate a habitat or a species.
    Returns a new row to be inserted into database.
    """
    if isinstance(obj, models.DataHabitatsCheckList):
        region_code = obj.bio_region
        result = models.DataHabitattypeRegion(
            dataset=dataset,
            region=region_code,
        )
    elif isinstance(obj, models.DataSpeciesCheckList):
        region_code = obj.bio_region
        result = models.DataSpeciesRegion(
            dataset=dataset,
            region=region_code,
        )
    else:
        raise NotImplementedError('Unknown check list obj')

    result.cons_date = timestamp
    result.cons_user_id = user_id
    if not refvals or not refvalue_ok(refvals):
        result.cons_role = ROLE_MISSING
        return result

    # Agregation starts here
    result.cons_role = ROLE_AGGREGATED
    result.cons_generalstatus = obj.presence

    if isinstance(obj, models.DataHabitatsCheckList):
        result = aggregate_habitat(obj, result, refvals, prev)
    else:
        result = aggregate_species(obj, result, refvals, prev)
    return result


def create_aggregation(timestamp, user_id):
    """ Run the full aggregation on all items in the checklist.
    """
    curr_report_id = get_reporting_id()
    curr_checklist = get_checklist(curr_report_id)
    dataset = models.Dataset(
        date=timestamp,
        user_id=user_id,
        checklist_id=curr_report_id,
        year_start=curr_checklist.year_start, year_end=curr_checklist.year_end,
    )
    models.db.session.add(dataset)

    species_refvals = load_species_refval()
    habitat_refvals = load_habitat_refval()

    species_prev = load_species_prev(dataset)
    habitat_prev = load_habitat_prev(dataset)

    habitat_id_map = dict(
        models.db.session.query(
            models.DataHabitat.code,
            models.DataHabitat.id,
        )
    )

    habitat_checklist_query = get_habitat_checklist(dataset_id=curr_report_id)

    habitat_report = defaultdict(set)
    for row in habitat_checklist_query:
        refval_key = row.code + "-" + row.bio_region
        refvals = habitat_refvals.get(refval_key)
        habitat_row = aggregate_object(row, dataset, refvals,
                                       timestamp, user_id, habitat_prev)
        habitat_code = row.natura_2000_code
        habitat_id = habitat_id_map.get(habitat_code)

        habitat_row.subject_id = habitat_id
        models.db.session.add(habitat_row)

        habitat_report[habitat_code].add(habitat_row.region)

    species_id_map = dict(
        models.db.session.query(
            models.DataSpecies.code,
            models.DataSpecies.id,
        )
    )

    species_checklist_query = get_species_checklist(dataset_id=curr_report_id)

    species_report = defaultdict(set)
    for row in species_checklist_query:
        refval_key = row.code + "-" + row.bio_region
        refvals = species_refvals.get(refval_key)
        species_row = aggregate_object(row, dataset, refvals,
                                       timestamp, user_id, species_prev)
        species_code = row.natura_2000_code
        species_id = species_id_map.get(species_code)
        species_row.subject_id = species_id
        models.db.session.add(species_row)

        species_report[species_code].add(species_row.region)

    report = StringIO()
    print >> report, "Habitate:"
    for habitat_code, regions in sorted(habitat_report.items()):
        print >> report, "  %s: %s" % (
            habitat_code, ', '.join(sorted(regions)))

    print >> report, "\n\n"
    print >> report, "Specii:"
    for species_code, regions in sorted(species_report.items()):
        print >> report, "  %s: %s" % (
            species_code, ', '.join(sorted(regions)))

    return report.getvalue(), dataset


def create_preview_aggregation(page, subject, comment, timestamp, user_id):
    """ Aggregate a single species/habitat
    """
    curr_report_id = get_reporting_id()
    curr_checklist = get_checklist(curr_report_id)
    dataset = models.Dataset(
        date=timestamp,
        user_id=user_id,
        preview=True,
        comment=comment,
        year_start=curr_checklist.year_start, year_end=curr_checklist.year_end,
    )
    models.db.session.add(dataset)

    if page == 'habitat':
        id_map = dict(
            models.db.session.query(
                models.DataHabitat.code,
                models.DataHabitat.id,
            )
        )
        rows = (
            get_habitat_checklist(dataset_id=curr_report_id)
            .filter_by(code=subject)
        )
    elif page == 'species':
        id_map = dict(
            models.db.session.query(
                models.DataSpecies.code,
                models.DataSpecies.id,
            )
        )
        rows = (
            get_species_checklist(dataset_id=curr_report_id)
            .filter_by(code=subject)
        )
    else:
        raise NotImplementedError()

    bioregions = []
    refvals = get_subject_refvals_mixed(page, subject)
    prev = get_subject_prev(subject, dataset)
    for row in rows:
        record = aggregate_object(row, dataset, refvals.get(row.bio_region), timestamp, user_id)
        record.subject_id = id_map.get(row.code)
        models.db.session.add(record)
        bioregions.append(row.bio_region)
    report = ', '.join(bioregions)
    return report, dataset
