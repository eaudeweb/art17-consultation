from art17 import models
from art17.scripts import exporter

DATASET = 1

def get_DataSpeciesRegion_magnitudes():
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
                unicode(sr.id),
                sr.region,
                unicode(sr.cons_dataset_id),
                unicode(sr.range_trend_magnitude_min or ''),
                unicode(sr.range_trend_magnitude_max or ''),
                unicode(sr.range_trend_long_magnitude_min or ''),
                unicode(sr.range_trend_long_magnitude_max or ''),
            ]
            print ','.join(row)

@exporter.command
def species():
    get_DataSpeciesRegion_magnitudes()
