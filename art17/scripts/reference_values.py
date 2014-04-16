from art17 import models
from art17.scripts import exporter

DATASET = 1

@exporter.command
def species_magnitude():
    header = ('Cod specie', 'Nume', 'Bioregiune', 'Magn. min scurt',
              'Magn. max scurt', 'Magn. min lung', 'Magn. max lung')
    print ','.join(header)

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
                sp.name or sp.alternative_speciesname or '',
                sr.region,
                unicode(sr.range_trend_magnitude_min or ''),
                unicode(sr.range_trend_magnitude_max or ''),
                unicode(sr.range_trend_long_magnitude_min or ''),
                unicode(sr.range_trend_long_magnitude_max or ''),
            ]
            print ','.join(row)


@exporter.command
def species_range_reference():
    header = ('Cod specie', 'Nume', 'Bioregiune',
              'Val. min areal favorabil referinta',
              'Val de la care arealul devine nefavorabil - inadecvat',
              'Valoare de la care arealul devine nefavorabil - rau',
              'Valoare de la care arealul devine necunoscut')

    print ','.join(header)

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
                sp.name or sp.alternative_speciesname or '',
                sr.region,
            ]
            row.extend([''] * 4)
            print ','.join(row)
