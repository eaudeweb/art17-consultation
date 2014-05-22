import json
import os
from csv import DictReader
from flask import current_app
from art17.scripts import importer


SPECIES_MAP = {
    'species_magnitude.csv': 'magnitude',
    'species_range.csv': 'range',
    'species_population_range.csv': 'population_range',
    'species_population_magnitude.csv': 'population_magnitude',
    'species_population_units.csv': 'population_units'
}


def load_refval(filename):
    dir = current_app.config.get('REFVAL_DIR', '.')
    filepath = os.path.join(dir, filename)

    data = {}
    if not os.path.exists(filepath):
        print "Missing: ", filepath
    else:
        with open(filepath, 'r') as fin:
            try:
                data = json.load(fin)
            except ValueError:
                print "Invalid json: ", filepath
    return data


def save_refval(filename, data):
    dir = current_app.config.get('REFVAL_DIR', '.')
    filepath = os.path.join(dir, filename)

    with open(filepath, 'w') as fout:
        json.dump(data, fout, indent=1)
        print "Saved: ", filepath
    
    
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
                data_key = (row.pop('Cod specie') + "-" +row.pop('Bioregiune'))
                row.pop('Nume')
                data[data_key] = data.get(data_key, {})
                data[data_key][refval_key] = row

    save_refval('species.json', data)
