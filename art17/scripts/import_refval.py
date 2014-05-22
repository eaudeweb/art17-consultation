import os
from csv import DictReader
from art17.aggregation.refvalues import load_refval, save_refval
from art17.scripts import importer


SPECIES_MAP = {
    'species_magnitude.csv': 'magnitude',
    'species_range.csv': 'range',
    'species_population_range.csv': 'population_range',
    'species_population_magnitude.csv': 'population_magnitude',
    'species_population_units.csv': 'population_units'
}


@importer.command
def species_refval(csv_dir='.'):
    data = load_refval('species.json')
    for filename, refval_key in SPECIES_MAP.iteritems():
        path = os.path.join(csv_dir, filename)
        if not os.path.exists(path):
            print "Missing: ", path
            continue

        with open(path, 'r') as fin:
            reader = DictReader(fin)

            for row in reader:
                if not row['Nume']:
                    # ignore groups
                    continue
                data_key = (
                    row.pop('Cod specie') + "-" + row.pop('Bioregiune')
                )
                row.pop('Nume')
                data[data_key] = data.get(data_key, {})
                data[data_key][refval_key] = row

    save_refval('species.json', data)
