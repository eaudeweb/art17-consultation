from art17 import models
from art17.scripts import exporter
from utils import generate_csv

DATASET = 1

@exporter.command
def species_magnitude():
    header = ('Cod specie', 'Nume', 'Bioregiune', 'Magn. min scurt',
              'Magn. max scurt', 'Magn. min lung', 'Magn. max lung')

    columns = []
    data_species = models.DataSpecies.query.all()
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
            row = [
                sp.code,
                sp.checklist.name or '++++++++++'
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
              'Val. min areal favorabil referinta',
              'Val de la care arealul devine nefavorabil - inadecvat',
              'Valoare de la care arealul devine nefavorabil - rau',
              'Valoare de la care arealul devine necunoscut')

    columns = []
    data_species = models.DataSpecies.query.all()
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
            row = [
                sp.code,
                sp.checklist.name or '++++++++++'
                sr.region,
            ]
            row.extend([''] * 4)
            columns.append(row)

    ret = generate_csv(header, columns)
    print ret
