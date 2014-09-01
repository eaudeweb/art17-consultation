from StringIO import StringIO
from collections import defaultdict
import flask
from art17 import models
from art17.aggregation.refvalues import (
    refvalue_ok, load_species_refval, load_habitat_refval,
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


def execute_on_primary(query):
    app = flask.current_app
    aggregation_engine = models.db.get_engine(app, 'primary')
    return models.db.session.execute(query, bind=aggregation_engine)


def get_period(year, length):
    return '%d-%d' % (year - length, year)


def aggregate_species(obj, result, refvals):
    short_period = get_period(result.dataset.year_end, 12)
    long_period = get_period(result.dataset.year_end, 24)
    # Areal
    result.range_surface_area = get_species_range_surface(obj.code,
                                                          result.region)

    result.range_trend_period = short_period
    result.range_trend_magnitude_min = refvals["magnitude"]["Magn. min scurt"]
    result.range_trend_magnitude_max = refvals["magnitude"]["Magn. max scurt"]
    result.range_trend_long_period = long_period
    result.range_trend_long_magnitude_min = refvals["magnitude"]["Magn. min lung"]
    result.range_trend_long_magnitude_max = refvals["magnitude"]["Magn. max lung"]

    # Populatie
    result.population_trend_period = short_period
    result.population_trend_magnitude_min = refvals["population_magnitude"]["Magn. min scurt"]
    result.population_trend_magnitude_max = refvals["population_magnitude"]["Magn. max scurt"]
    result.population_trend_magnitude_ci = refvals["population_magnitude"]["Interval incredere scurt"]
    result.population_trend_long_period = long_period
    result.population_trend_long_magnitude_min = refvals["population_magnitude"]["Magn. min lung"]
    result.population_trend_long_magnitude_max = refvals["population_magnitude"]["Magn. max lung"]
    result.population_trend_long_magnitude_ci = refvals["population_magnitude"]["Interval incredere lung"]

    # Habitat
    result.habitat_surface_area = get_species_dist_surface(obj.code,
                                                           result.region)
    result.habitat_trend_period = short_period
    result.habitat_trend_long_period = long_period

    # Presiuni

    # Amenintari

    # Complementar

    # Natura 2000

    # Masuri de conservare

    # Concluzii

    # Bibliografie / surse publicate

    return result


def aggregate_habitat(obj, result, refvals):
    short_period = get_period(result.dataset.year_end, 12)
    long_period = get_period(result.dataset.year_end, 24)
    # Areal
    result.range_surface_area = get_habitat_range_surface(obj.code,
                                                          result.region)
    result.range_trend_period = short_period
    result.range_trend_magnitude_min = refvals["magnitude"]["Magn. min scurt"]
    result.range_trend_magnitude_max = refvals["magnitude"]["Magn. max scurt"]
    result.range_trend_long_period = long_period
    result.range_trend_long_magnitude_min = refvals["magnitude"]["Magn. min lung"]
    result.range_trend_long_magnitude_max = refvals["magnitude"]["Magn. max lung"]

    # Suprafata
    result.coverage_surface_area = get_habitat_dist_surface(obj.code,
                                                            result.region)
    result.coverage_trend_period = short_period
    result.coverage_trend_magnitude_min = refvals["coverage_magnitude"]["Magn. min scurt"]
    result.coverage_trend_magnitude_max = refvals["coverage_magnitude"]["Magn. max scurt"]
    result.coverage_trend_magnitude_ci = refvals["coverage_magnitude"]["Interval incredere scurt"]
    result.coverage_trend_long_period = long_period
    result.coverage_trend_long_magnitude_min = refvals["coverage_magnitude"]["Magn. min lung"]
    result.coverage_trend_long_magnitude_max = refvals["coverage_magnitude"]["Magn. max lung"]
    result.coverage_trend_long_magnitude_ci = refvals["coverage_magnitude"]["Interval incredere lung"]

    # Presiuni

    # Amenintari

    # Specii tipice

    # Natura 2000

    # Masuri de conservare

    # Concluzii

    # Bibliografie

    return result


def aggregate_object(obj, dataset, refvals, timestamp, user_id):
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
    refval_key = obj.code + "-" + obj.bio_region
    if refval_key not in refvals or not refvalue_ok(refvals[refval_key]):
        result.cons_role = 'missing'
        return result

    # Agregation starts here
    result.cons_role = 'assessment'
    if isinstance(obj, models.DataHabitatsCheckList):
        result = aggregate_habitat(obj, result, refvals[refval_key])
    else:
        result = aggregate_species(obj, result, refvals[refval_key])
    return result


def create_aggregation(timestamp, user_id):
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

    habitat_id_map = dict(
        models.db.session.query(
            models.DataHabitat.code,
            models.DataHabitat.id,
        )
    )

    habitat_checklist_query = get_habitat_checklist(dataset_id=curr_report_id)

    habitat_report = defaultdict(set)
    for row in habitat_checklist_query:
        habitat_row = aggregate_object(row, dataset, habitat_refvals,
                                       timestamp, user_id)
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
        species_row = aggregate_object(row, dataset, species_refvals,
                                       timestamp, user_id)
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
        refvals = load_habitat_refval()
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
        refvals = load_species_refval()
    else:
        raise NotImplementedError()

    bioregions = []
    for row in rows:
        record = aggregate_object(row, dataset, refvals, timestamp, user_id)
        record.subject_id = id_map.get(row.code)
        models.db.session.add(record)
        bioregions.append(row.bio_region)
    report = ', '.join(bioregions)
    return report, dataset
