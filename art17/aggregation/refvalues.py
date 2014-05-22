import json
import os
from flask import current_app


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


def load_species_refval():
    return load_refval('species.json')


def load_habitat_refval():
    return load_refval('habitats.json')


def refvalue_ok(refvalue):
    if not refvalue:
        return None
    for k, v in refvalue.iteritems():
        v2 = v.values()
        if ('' in v2) or (None in v2):
            return False
    return True
