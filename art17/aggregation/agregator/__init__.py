# coding=utf-8
from StringIO import StringIO
from collections import defaultdict

from art17 import models, ROLE_AGGREGATED, ROLE_MISSING
from art17.aggregation.agregator.conclusions import (
    get_species_conclusion_range, get_species_conclusion_population,
    get_species_conclusion_habitat, get_overall_species_conclusion,
    get_habitat_conclusion_range, get_habitat_conclusion_area,
    get_conclusion_future, get_overall_habitat_conclusion, get_grade,
)
from art17.aggregation.agregator.n2k import get_habitat_cover_range, \
    get_species_population_range
from art17.aggregation.agregator.rest import get_species_bibliography, \
    get_species_pressures_threats, get_species_population_size, \
    get_species_dist_surface, get_species_range_surface, \
    get_species_habitat_quality, get_habitat_typical_species, \
    get_habitat_published, get_habitat_dist_surface, \
    get_habitat_range_surface, get_habitat_pressures_threats
from art17.aggregation.agregator.subgroups import get_species_subgroup, \
    get_habitat_subgroup, TYPICAL_SPECIES_METHOD
from art17.aggregation.agregator.trends import get_species_range_trend, \
    get_species_population_trend, get_species_habitat_trend, \
    get_habitat_range_trend, get_habitat_coverage_trend, get_future_trend, \
    SHORT_TERM, LONG_TERM, get_assessment_trend, get_conclusion_trend, \
    get_species_conclusion_trend
from art17.aggregation.prev import load_species_prev, load_habitat_prev, \
    get_subject_prev, get_acronym
from art17.aggregation.refvalues import (
    refvalue_ok, load_species_refval, load_habitat_refval,
    get_subject_refvals_mixed, extract_key,
)
from art17.aggregation.utils import (
    get_reporting_id, get_habitat_checklist, get_species_checklist,
    get_checklist)
from art17.models import DataHabitatSpecies


UNKNOWN_TREND = 'x'
MISSING_DATA = '0'
EXPERT_OPINION = '1'
TERRAIN_DATA = '3'

RANKING_SLICES = {
    'H': 5,
    'M': 5,
    'L': 10,
}


def get_period(year, length):
    return '%d-%d' % (year - length, year)


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

    d = {}
    for row in pressures_threats:
        typ = row['type']
        rank = row['ranking']
        if not typ or not rank:
            continue
        (
            d.setdefault(typ, {})
            .setdefault(rank, {})
            .setdefault(row['pressure'], [])
            .append(row['pollution'])
        )

    for typ, data in d.iteritems():
        for rank, tp in data.iteritems():
            tp = sorted(tp.items(), key=lambda x: len(x[1]), reverse=True)
            tp = tp[:RANKING_SLICES[rank]]
            for p, pollutions in tp:
                pressure_obj = models.DataPressuresThreats(
                    pressure=p,
                    ranking=rank,
                    type=typ,
                    **foreign_key
                )
                for pol in set(pollutions):
                    if not pol:
                        continue
                    pollution_obj = models.DataPressuresThreatsPollution(
                        pressure=pressure_obj,
                        pollution_qualifier=pol,
                    )
                    models.db.session.add(pollution_obj)
                models.db.session.add(pressure_obj)


def aggregate_species(obj, result, refvals, prev):
    current_year = result.dataset.year_end
    current_period = get_period(result.dataset.year_end, 6)
    short_period = get_period(result.dataset.year_end, 12)
    long_period = get_period(result.dataset.year_end, 24)

    prev = prev.get(get_acronym(obj.code, result.region), [])
    subgroup = get_species_subgroup(obj.code)

    # Bibliografie / surse publicate
    result.published, count = get_species_bibliography(
        subgroup, obj.code, result.region
    )

    # Populatie
    size = get_species_population_size(subgroup, obj.code, result.region)
    result.population_size_unit = refvals['population_units'][
        u'Unit. de măsură']
    result.population_minimum_size = size

    result.population_additional_locality = extract_key(
        refvals["population_units"], "localit")
    result.population_additional_method = extract_key(
        refvals["population_units"], "Metoda")
    result.population_additional_problems = extract_key(
        refvals["population_units"], "Dificult")
    result.population_trend = get_species_population_trend(
        subgroup, SHORT_TERM, current_year, size, prev
    )
    result.population_trend_period = short_period
    result.population_method = refvals['population_range']['Metoda populatie']
    result.population_date = current_period
    result.population_trend_magnitude_min = refvals["population_magnitude"][
        "Magn. min scurt"]
    result.population_trend_magnitude_max = refvals["population_magnitude"][
        "Magn. max scurt"]
    # result.population_trend_magnitude_ci = refvals["population_magnitude"][
    #     "Interval incredere scurt"]
    result.population_trend_method = MISSING_DATA
    result.population_trend_long = get_species_population_trend(
        subgroup, LONG_TERM, current_year, size, prev
    )
    result.population_trend_long_period = long_period
    result.population_trend_long_magnitude_min = \
        refvals["population_magnitude"]["Magn. min lung"]
    result.population_trend_long_magnitude_max = \
        refvals["population_magnitude"]["Magn. max lung"]
    # result.population_trend_long_magnitude_ci = \
    #     refvals["population_magnitude"]["Interval incredere lung"]
    result.population_trend_long_method = MISSING_DATA
    (
        result.complementary_favourable_population,
        result.complementary_favourable_population_op,
        result.complementary_favourable_population_unknown,
    ) = parse_complementary(refvals["population_range"])
    result.complementary_favourable_population_method = \
        "Expert opinion, correlated with the data reported in 2013"
    result.conclusion_population = get_species_conclusion_population(
        subgroup, result.population_minimum_size,
        result.population_maximum_size,
        refvals, prev, result.dataset.year_end
    )
    result.conclusion_population_trend = get_conclusion_trend(
        result.conclusion_population, result.population_trend,
        result.population_trend_long)

    # Habitat
    result.habitat_surface_area = get_species_dist_surface(
        subgroup, obj.code, result.region
    )
    result.habitat_method = refvals['habitat']['Metoda suprafata habitat']

    result.habitat_quality = get_species_habitat_quality(
        subgroup, obj.code, result.region
    )

    result.habitat_trend = get_species_habitat_trend(
        subgroup, SHORT_TERM, current_year, result.habitat_surface_area, prev
    )
    result.habitat_trend_period = short_period
    result.habitat_trend_long = get_species_habitat_trend(
        subgroup, LONG_TERM, current_year, result.habitat_surface_area, prev
    )
    result.habitat_trend_long_period = long_period
    result.habitat_area_suitable = extract_key(refvals["habitat"], "adecvat")
    result.habitat_date = current_period

    result.conclusion_habitat = get_species_conclusion_habitat(
        subgroup, result.habitat_surface_area, result.habitat_quality, refvals
    )
    result.conclusion_habitat_trend = get_conclusion_trend(
        result.conclusion_habitat, result.habitat_trend,
        result.habitat_trend_long)

    # Areal
    result.range_surface_area = get_species_range_surface(
        subgroup, obj.code, result.region
    )
    result.range_method = refvals['range']['Metoda areal']
    result.range_trend = get_species_range_trend(
        subgroup, SHORT_TERM, current_year, result.range_surface_area, prev,
        obj.code, result.region
    )
    result.range_trend_period = short_period
    result.range_trend_magnitude_min = refvals["magnitude"]["Magn. min scurt"]
    result.range_trend_magnitude_max = refvals["magnitude"]["Magn. max scurt"]
    result.range_trend_long = get_species_range_trend(
        subgroup, LONG_TERM, current_year, result.range_surface_area, prev,
        obj.code, result.region
    )
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
    result.complementary_favourable_range_method = \
        "Expert opinion, correlated with the data reported in 2013"
    result.conclusion_range = get_species_conclusion_range(
        subgroup, result.range_surface_area, refvals
    )
    result.conclusion_range_trend = get_species_conclusion_trend(
        subgroup,
        result.conclusion_range, result.range_trend, result.range_trend_long,
        result.conclusion_population, result.conclusion_population_trend,
        result.conclusion_habitat, result.conclusion_habitat_trend)

    # Presiuni & Amenintari
    pressure_threats = get_species_pressures_threats(
        subgroup, obj.code, result.region
    )
    set_pressures_threats(result, pressure_threats)
    result.pressures_method = TERRAIN_DATA
    result.threats_method = EXPERT_OPINION

    # Complementare

    # Natura 2000
    n2k_min, n2k_max, n2k_unit = get_species_population_range(
        subgroup, obj.code, result.region
    )
    result.natura2000_population_unit = n2k_unit
    result.natura2000_population_min = n2k_min
    result.natura2000_population_max = n2k_max

    # Masuri de conservare

    # Future
    conclusions_trends = [
        (result.conclusion_range, result.conclusion_range_trend),
        (result.conclusion_population, result.conclusion_population_trend),
        (result.conclusion_habitat, result.conclusion_habitat_trend)]
    conclusions = [c[0] for c in conclusions_trends]
    grade = get_grade(conclusions_trends)

    result.conclusion_future = get_conclusion_future(conclusions, grade)
    result.conclusion_future_trend = get_future_trend(
        result.conclusion_future, conclusions, grade)

    # Concluzii Overall
    result.conclusion_assessment = get_overall_species_conclusion(result)
    conclusions_trends.append(
        (result.conclusion_future, result.conclusion_future_trend))
    result.conclusion_assessment_trend = get_assessment_trend(
        result.conclusion_assessment, conclusions_trends)

    return result


def aggregate_habitat(obj, result, refvals, prev):
    current_year = result.dataset.year_end
    current_period = get_period(result.dataset.year_end, 6)
    short_period = get_period(result.dataset.year_end, 12)
    long_period = get_period(result.dataset.year_end, 24)

    prev = prev.get(get_acronym(obj.code, result.region), [])
    subgroup = get_habitat_subgroup(obj.code)

    # Bibliografie
    result.published, count = get_habitat_published(subgroup, obj.code,
                                                    result.region)

    # Areal
    result.range_surface_area = get_habitat_range_surface(
        subgroup, obj.code, result.region
    )
    result.range_method = refvals['range']['Metoda areal']
    result.range_trend = get_habitat_range_trend(
        subgroup, SHORT_TERM, current_year, result.range_surface_area, prev,
        obj.code, result.region)
    result.range_trend_period = short_period
    result.range_trend_magnitude_min = refvals["magnitude"]["Magn. min scurt"]
    result.range_trend_magnitude_max = refvals["magnitude"]["Magn. max scurt"]
    result.range_trend_long = get_habitat_range_trend(
        subgroup, LONG_TERM, current_year, result.range_surface_area, prev,
        obj.code, result.region)
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
    result.complementary_favourable_range_method = \
        "Expert opinion, correlated with the data reported in 2013"
    result.conclusion_range = get_habitat_conclusion_range(
        result.range_surface_area, refvals)
    result.conclusion_range_trend = get_conclusion_trend(
        result.conclusion_range, result.range_trend, result.range_trend_long)

    # Suprafata
    result.coverage_surface_area = get_habitat_dist_surface(subgroup, obj.code,
                                                            result.region)
    result.coverage_date = current_period
    result.coverage_method = refvals['coverage_range']['Metoda suprafata']
    result.coverage_trend = get_habitat_coverage_trend(
        subgroup, SHORT_TERM, current_year, result.coverage_surface_area, prev,
        obj.code, result.region)
    result.coverage_trend_period = short_period
    result.coverage_trend_magnitude_min = refvals["coverage_magnitude"][
        "Magn. min scurt"]
    result.coverage_trend_magnitude_max = refvals["coverage_magnitude"][
        "Magn. max scurt"]
    # result.coverage_trend_magnitude_ci = refvals["coverage_magnitude"][
    #     "Interval incredere scurt"]
    result.coverage_trend_method = MISSING_DATA
    result.coverage_trend_long = get_habitat_coverage_trend(
        subgroup, LONG_TERM, current_year, result.coverage_surface_area, prev,
        obj.code, result.region)

    result.coverage_trend_long_period = long_period
    result.coverage_trend_long_magnitude_min = refvals["coverage_magnitude"][
        "Magn. min lung"]
    result.coverage_trend_long_magnitude_max = refvals["coverage_magnitude"][
        "Magn. max lung"]
    # result.coverage_trend_long_magnitude_ci = refvals["coverage_magnitude"][
    #     "Interval incredere lung"]
    result.coverage_trend_long_method = MISSING_DATA
    (
        result.complementary_favourable_area,
        result.complementary_favourable_area_op,
        result.complementary_favourable_area_unknown,
    ) = parse_complementary(refvals["coverage_range"])
    result.conclusion_area = get_habitat_conclusion_area(
        result.coverage_surface_area, refvals)
    result.conclusion_area_trend = get_conclusion_trend(
        result.conclusion_area, result.coverage_trend,
        result.coverage_trend_long)

    # Natura 2000
    n2k_min, n2k_max = get_habitat_cover_range(subgroup, obj.code,
                                               result.region)
    result.natura2000_area_min = n2k_min
    result.natura2000_area_max = n2k_max

    # Masuri de conservare

    # Specii tipice
    typical_species = get_habitat_typical_species(
        subgroup, obj.code, result.region
    )
    set_typical_species(result, typical_species)
    result.structure_and_functions_method = (
        refvals['typical_species']['Metoda specii tipice'])
    result.typical_species_method = TYPICAL_SPECIES_METHOD.get(
        subgroup, "Average on multiple plots - field evaluation")

    # Presiuni, amenintari
    pressures_threats = get_habitat_pressures_threats(subgroup, obj.code,
                                                      result.region)
    set_pressures_threats(result, pressures_threats)
    result.pressures_method = TERRAIN_DATA
    result.threats_method = EXPERT_OPINION

    # Future
    conclusions_trends = [
        (result.conclusion_range, result.conclusion_range_trend),
        (result.conclusion_area, result.conclusion_area_trend),
        (result.conclusion_structure, result.conclusion_structure_trend)]
    conclusions = [c[0] for c in conclusions_trends]
    grade = get_grade(conclusions_trends)

    result.conclusion_future = get_conclusion_future(conclusions, grade)
    result.conclusion_future_trend = get_future_trend(
        result.conclusion_future, conclusions, grade)

    # Concluzii Overall
    result.conclusion_assessment = get_overall_habitat_conclusion(result)
    conclusions_trends.append(
        (result.conclusion_future, result.conclusion_future_trend))
    result.conclusion_assessment_trend = get_assessment_trend(
        result.conclusion_assessment, conclusions_trends)

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
        record_type = 'habitat'
    elif isinstance(obj, models.DataSpeciesCheckList):
        region_code = obj.bio_region
        result = models.DataSpeciesRegion(
            dataset=dataset,
            region=region_code,
        )
        record_type = 'species'
    else:
        raise NotImplementedError('Unknown check list obj')

    result.cons_date = timestamp
    result.cons_user_id = user_id
    result.cons_generalstatus = obj.presence

    if result.cons_generalstatus != '1':
        result.cons_role = ROLE_AGGREGATED
        return result

    if not refvalue_ok(refvals, record_type):
        result.cons_role = ROLE_MISSING
        return result

    # Agregation starts here
    result.cons_role = ROLE_AGGREGATED

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
        subgroup = 'n/a'
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
        subgroup = get_species_subgroup(subject)
    else:
        raise NotImplementedError()

    bioregions = {}
    refvals = get_subject_refvals_mixed(page, subject)
    prev = get_subject_prev(page, dataset)
    for row in rows:
        record = aggregate_object(row, dataset, refvals.get(row.bio_region),
                                  timestamp, user_id, prev)
        record.subject_id = id_map.get(row.code)
        models.db.session.add(record)
        bioregions[row.bio_region] = record.cons_role
    report = (
        ', '.join('{0}:{1}'.format(k, v) for k, v in
                  bioregions.items()) + ' [{0}]'.format(subgroup)
    )
    return report, dataset
