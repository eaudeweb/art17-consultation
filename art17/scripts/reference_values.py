from art17 import models
from art17.scripts import exporter
from utils import do_csv_export

DATASET = 1


@exporter.command
def species_magnitude(filename=None):
    header = ('Cod specie', 'Nume', 'Bioregiune', 'Magn. min scurt',
              'Magn. max scurt', 'Magn. min lung', 'Magn. max lung')

    groups = models.LuGrupSpecie.query.all()
    columns = []
    for group in groups:
        columns.append([group.description])
        data_species = (
            models.DataSpecies.query
            .join(models.DataSpecies.lu)
            .filter(models.LuHdSpecies.group_code==group.code)
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
                columns.append(row)

    do_csv_export(header, columns, filename)


@exporter.command
def species_range_reference(filename=None):
    header = ('Cod specie', 'Nume', 'Bioregiune',
              'Areal favorabil referinta',
              'Operator - areal',
              'Necunoscut')

    groups = models.LuGrupSpecie.query.all()
    columns = []
    for group in groups:
        columns.append([group.description])
        data_species = (
            models.DataSpecies.query
            .join(models.DataSpecies.lu)
            .filter(models.LuHdSpecies.group_code==group.code)
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
                    if sr.complementary_favourable_range_x else '',
                    'x' if sr.complementary_favourable_range_x else '',
                ]
                columns.append(row)

    do_csv_export(header, columns, filename)


@exporter.command
def all():
    available = {
        'species_magnitude': species_magnitude,
        'species_range_reference': species_range_reference,
    }
    for k, v in available.iteritems():
        filename = '%s.csv' % k
        print "Exporting %s..." % k
        v(filename)
    print "Done."
