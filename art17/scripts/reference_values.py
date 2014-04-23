from art17 import models
from art17.scripts import exporter
from utils import generate_csv

DATASET = 1

@exporter.command
def species_magnitude():
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

    ret = generate_csv(header, columns)
    print ret


@exporter.command
def species_range_reference():
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
                    unicode(sr.complementary_favourable_range) or '',
                    unicode(sr.complementary_favourable_range_op) or '',
                    unicode(sr.complementary_favourable_range_x) or '',
                ]
                columns.append(row)

    ret = generate_csv(header, columns)
    print ret
