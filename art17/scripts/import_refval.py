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

HABITAT_MAP = {
    'habitat_magnitude.csv': 'magnitude',
    'habitat_range.csv': 'range',
    'habitat_coverage_range.csv': 'coverage_range',
    'habitat_coverage_magnitude.csv': 'coverage_magnitude',
}


@importer.command
def species_refval(csv_dir='.', map=None, json_filename=None):
    json_filename = json_filename or 'species.json'
    data = load_refval(json_filename)
    map = map or SPECIES_MAP
    for filename, refval_key in map.iteritems():
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

    save_refval(json_filename, data)


@importer.command
def habitat_refval(csv_dir='.'):
    return species_refval(csv_dir=csv_dir, map=HABITAT_MAP,
                          json_filename='habitats.json')
