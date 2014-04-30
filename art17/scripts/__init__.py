from flask.ext.script import Manager

exporter = Manager()
importer = Manager()

import art17.scripts.reference_values
import art17.scripts.import_eea
