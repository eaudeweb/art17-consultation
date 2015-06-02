# coding=utf-8
"""
    This file will export the reference values from an existing dataset, i.e.:
    the initial one.
"""
import os.path
from art17 import models
from art17.scripts import exporter, DEFAULT_DATASET_ID
from utils import do_csv_export


COMMON_HEADER = ('Cod specie', 'Nume', 'Bioregiune')


def generic_species_exporter(format_row_cb, dataset_id=None):
    dataset_id = dataset_id or DEFAULT_DATASET_ID
    columns = []
    groups = models.LuGrupSpecie.query.all()
    for group in groups:
        columns.append([group.description, ''])
        data_species = (
            models.DataSpecies.query
            .join(models.DataSpecies.lu)
            .filter(models.LuHdSpecies.group_code == group.code)
            .order_by(models.LuHdSpecies.speciesname)
        )
        for sp in data_species:
            data_species_regions = (
                sp.regions
                .filter_by(
                    cons_dataset_id=dataset_id,
                    cons_role='assessment',
                )
                .order_by(models.DataSpeciesRegion.region)
            )
            for sr in data_species_regions:
                row = format_row_cb(sp, sr)
                columns.append(row)
    return columns


def generic_habitat_exporter(format_row_cb, dataset_id=None):
    dataset_id = dataset_id or DEFAULT_DATASET_ID
    rows = []
    data_habitats = (
        models.DataHabitat.query
        .join(models.DataHabitat.lu)
        .order_by(models.LuHabitattypeCodes.hd_name)
    )
    for hb in data_habitats:
        data_habitats_regions = (
            hb.regions
            .filter_by(
                cons_dataset_id=dataset_id,
                cons_role='assessment',
            )
            .order_by(models.DataHabitattypeRegion.region)
        )
        for hr in data_habitats_regions:
            row = format_row_cb(hb, hr)
            rows.append(row)
    return rows


@exporter.command
def species_magnitude(filename=None, exporter=generic_species_exporter,
                      dataset_id=None):
    header = COMMON_HEADER + (
        'Magn. min scurt', 'Magn. max scurt', 'Magn. min lung',
        'Magn. max lung',
    )

    def format_row(sp, sr):
        name = None
        if sp.lu:
            name = sp.lu.display_name
        name = name or ''

        row = [
            sp.code,
            name,
            sr.region,
            unicode(sr.range_trend_magnitude_min or ''),
            unicode(sr.range_trend_magnitude_max or ''),
            unicode(sr.range_trend_long_magnitude_min or ''),
            unicode(sr.range_trend_long_magnitude_max or ''),
        ]
        return row

    columns = exporter(format_row, dataset_id=dataset_id)

    do_csv_export(header, columns, filename)


@exporter.command
def species_range(filename=None, exporter=generic_species_exporter,
                  dataset_id=None):
    header = COMMON_HEADER + (
        'Areal favorabil referinta',
        'Operator - areal',
        'Necunoscut',
        'U1',
        'U2',
    )

    def format_row(sp, sr):
        name = None
        if sp.lu:
            name = sp.lu.display_name
        name = name or ''
        return [
            sp.code,
            name,
            sr.region,
            unicode(sr.complementary_favourable_range)
            if sr.complementary_favourable_range else '',
            unicode(sr.complementary_favourable_range_op)
            if sr.complementary_favourable_range_unknown else '',
            'x' if sr.complementary_favourable_range_unknown else '',
            '',
            '',
        ]

    columns = exporter(format_row, dataset_id=dataset_id)
    do_csv_export(header, columns, filename)


@exporter.command
def species_habitat(filename=None, dataset_id=None):
    header = COMMON_HEADER + (
        u'Suprafața habitat',
        u'Suprafața adecvata',
        u'U1',
        u'U2',
    )

    def format_row(sp, sr):
        name = None
        if sp.lu:
            name = sp.lu.display_name
        name = name or ''

        return [
            sp.code,
            name,
            sr.region,
            unicode(sr.habitat_surface_area or ''),
            unicode(sr.habitat_area_suitable or ''),
            '', ''
        ]

    columns = generic_species_exporter(format_row, dataset_id=dataset_id)
    do_csv_export(header, columns, filename)


@exporter.command
def species_population_range(filename=None, dataset_id=None):
    header = COMMON_HEADER + (
        'Populatia favorabila de referinta', 'Operator', 'Necunoscut', 'U1',
        'U2',
    )

    def format_row(sp, sr):
        name = None
        if sp.lu:
            name = sp.lu.display_name
        name = name or ''
        return [
            sp.code,
            name,
            sr.region,
            unicode(sr.complementary_favourable_population)
            if sr.complementary_favourable_population else '',
            unicode(sr.complementary_favourable_population_op)
            if sr.complementary_favourable_population_unknown else '',
            'x' if sr.complementary_favourable_population_unknown else '',
            '', '',
        ]

    columns = generic_species_exporter(format_row, dataset_id=dataset_id)
    do_csv_export(header, columns, filename)


@exporter.command
def species_population_magnitude(filename=None,
                                 exporter=generic_species_exporter,
                                 dataset_id=None):
    header = COMMON_HEADER + (
        'Magn. min scurt', 'Magn. max scurt', 'Interval incredere scurt',
        'Magn. min lung', 'Magn. max lung', 'Interval incredere lung',
    )

    def format_row(sp, sr):
        name = None
        if sp.lu:
            name = sp.lu.display_name
        name = name or ''
        return [
            sp.code,
            name,
            sr.region,
            unicode(sr.population_trend_magnitude_min or ''),
            unicode(sr.population_trend_magnitude_max or ''),
            unicode(sr.population_trend_magnitude_ci or ''),
            unicode(sr.population_trend_long_magnitude_min or ''),
            unicode(sr.population_trend_long_magnitude_max or ''),
            unicode(sr.population_trend_long_magnitude_ci or ''),
        ]

    columns = exporter(format_row, dataset_id=dataset_id)
    do_csv_export(header, columns, filename)


@exporter.command
def species_population_units(filename=None, dataset_id=None):
    header = COMMON_HEADER + (
        u'Unit. de măsură',
        u'Metoda conversie',
        u'Definiția localității',
        u'Dificultăți întâmpinate',
    )

    def format_row(sp, sr):
        name = sp.lu.display_name if sp.lu else None
        name = name or ''
        units = [sr.population_size_unit, sr.population_alt_size_unit]
        units = [str(unit) for unit in units if unit]
        return [
            sp.code,
            name,
            sr.region,
            ';'.join(units),
            sr.population_additional_method or '',
            sr.population_additional_locality or '',
            sr.population_additional_problems or '',
        ]

    columns = generic_species_exporter(format_row, dataset_id=dataset_id)
    do_csv_export(header, columns, filename)


@exporter.command
def all_species(folder=None, mapping=None, dataset_id=None):
    """ Export all species reference values
    """
    folder = folder or '.'
    available = mapping or {
        'species_magnitude': species_magnitude,
        'species_range': species_range,
        'species_habitat': species_habitat,
        'species_population_range': species_population_range,
        'species_population_magnitude': species_population_magnitude,
        'species_population_units': species_population_units,
    }
    for k, v in available.iteritems():
        filename = '%s.csv' % k
        print "Exporting %s..." % k
        filepath = os.path.join(folder, filename)
        v(filepath, dataset_id=dataset_id)
    print "Done."


@exporter.command
def habitat_magnitude(filename=None, dataset_id=None):
    return species_magnitude(filename=filename,
                             exporter=generic_habitat_exporter,
                             dataset_id=dataset_id)


@exporter.command
def habitat_range(filename=None, dataset_id=None):
    return species_range(filename=filename,
                         exporter=generic_habitat_exporter,
                         dataset_id=dataset_id)


@exporter.command
def habitat_coverage_range(filename=None, dataset_id=None):
    header = COMMON_HEADER + (
        'Suprafata favorabila referinta',
        'Operator',
        'Necunoscut',
        'U1',
        'U2',
    )

    def format_row(sp, sr):
        name = None
        if sp.lu:
            name = sp.lu.display_name
        name = name or ''
        return [
            sp.code,
            name,
            sr.region,
            unicode(sr.complementary_favourable_area)
            if sr.complementary_favourable_area else '',
            unicode(sr.complementary_favourable_area_op)
            if sr.complementary_favourable_area_unknown else '',
            'x' if sr.complementary_favourable_area_unknown else '',
            '',
            '',
        ]

    columns = generic_habitat_exporter(format_row, dataset_id=dataset_id)
    do_csv_export(header, columns, filename)


@exporter.command
def habitat_coverage_magnitude(filename=None, dataset_id=None):
    header = COMMON_HEADER + (
        'Magn. min scurt', 'Magn. max scurt', 'Interval incredere scurt',
        'Magn. min lung', 'Magn. max lung', 'Interval incredere lung',
    )

    def format_row(sp, sr):
        name = None
        if sp.lu:
            name = sp.lu.display_name
        name = name or ''
        return [
            sp.code,
            name,
            sr.region,
            unicode(sr.coverage_trend_magnitude_min or ''),
            unicode(sr.coverage_trend_magnitude_max or ''),
            unicode(sr.coverage_trend_magnitude_ci or ''),
            unicode(sr.coverage_trend_long_magnitude_min or ''),
            unicode(sr.coverage_trend_long_magnitude_max or ''),
            unicode(sr.coverage_trend_long_magnitude_ci or ''),
        ]

    columns = generic_habitat_exporter(format_row, dataset_id=dataset_id)
    do_csv_export(header, columns, filename)


@exporter.command
def all_habitat(folder=None, dataset_id=None):
    """ Export all habitat reference values
    """
    return all_species(folder=folder, mapping={
        'habitat_magnitude': habitat_magnitude,
        'habitat_range': habitat_range,
        'habitat_coverage_range': habitat_coverage_range,
        'habitat_coverage_magnitude': habitat_coverage_magnitude,
    }, dataset_id=dataset_id)
