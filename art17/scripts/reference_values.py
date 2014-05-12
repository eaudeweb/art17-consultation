# coding=utf-8
import os.path
from art17 import models
from art17.scripts import exporter
from utils import do_csv_export

DATASET = 1


def generic_species_exporter(format_row_cb):
    columns = []
    groups = models.LuGrupSpecie.query.all()
    for group in groups:
        columns.append([group.description])
        data_species = (
            models.DataSpecies.query
            .join(models.DataSpecies.lu)
            .filter(models.LuHdSpecies.group_code == group.code)
            .order_by(models.DataSpecies.code)
        )
        for sp in data_species:
            data_species_regions = (
                sp.regions
                .filter_by(
                    cons_dataset_id=DATASET,
                    cons_role='assessment',
                )
                .order_by(models.DataSpeciesRegion.region)
            )
            for sr in data_species_regions:
                row = format_row_cb(sp, sr)
                columns.append(row)
    return columns


@exporter.command
def species_magnitude(filename=None):
    header = ('Cod specie', 'Nume', 'Bioregiune', 'Magn. min scurt',
              'Magn. max scurt', 'Magn. min lung', 'Magn. max lung')

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

    columns = generic_species_exporter(format_row)
    do_csv_export(header, columns, filename)


@exporter.command
def species_range(filename=None):
    header = ('Cod specie', 'Nume', 'Bioregiune',
              'Areal favorabil referinta',
              'Operator - areal',
              'Necunoscut')

    def format_row(sp, sr):
        name = None
        if sp.lu:
            name = sp.lu.display_name
        name = name or ''
        row = [
            sp.code,
            name,
            sr.region,
            unicode(sr.complementary_favourable_range)
            if sr.complementary_favourable_range else '',
            unicode(sr.complementary_favourable_range_op)
            if sr.complementary_favourable_range_unknown else '',
            'x' if sr.complementary_favourable_range_unknown else '',
        ]
        return row

    columns = generic_species_exporter(format_row)
    do_csv_export(header, columns, filename)


@exporter.command
def species_population_range(filename=None):
    header = ('Cod specie', 'Nume', 'Bioregiune',
              'Populatia favorabila de referinta',
              'Operator',
              'Necunoscut')

    def format_row(sp, sr):
        name = None
        if sp.lu:
            name = sp.lu.display_name
        name = name or ''
        row = [
            sp.code,
            name,
            sr.region,
            unicode(sr.complementary_favourable_population)
            if sr.complementary_favourable_population else '',
            unicode(sr.complementary_favourable_population_op)
            if sr.complementary_favourable_population_unknown else '',
            'x' if sr.complementary_favourable_population_unknown else '',
        ]
        return row

    columns = generic_species_exporter(format_row)
    do_csv_export(header, columns, filename)



@exporter.command
def species_population_magnitude(filename=None):
    header = ('Cod specie', 'Nume', 'Bioregiune', 'Magn. min scurt',
              'Magn. max scurt', 'Interval incredere', 'Magn. min lung',
              'Magn. max lung', 'Interval incredere')

    def format_row(sp, sr):
        name = None
        if sp.lu:
            name = sp.lu.display_name
        name = name or ''
        row = [
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
        return row

    columns = generic_species_exporter(format_row)
    do_csv_export(header, columns, filename)


@exporter.command
def species_population_units(filename=None):
    pass


@exporter.command
def all(dest_dir=None):
    """ Export all reference values
    """
    dest_dir = dest_dir or '.'
    available = {
        'species_magnitude': species_magnitude,
        'species_range': species_range,
        'species_population_range': species_population_range,
        'species_population_magnitude': species_population_magnitude,
        'species_population_units': species_population_units,
    }
    for k, v in available.iteritems():
        filename = '%s.csv' % k
        print "Exporting %s..." % k
        filepath = os.path.join(dest_dir, filename)
        v(filepath)
    print "Done."
