from flask.ext.script import Manager

exporter = Manager()
importer = Manager()
modifier = Manager()

DEFAULT_DATASET_ID = 1

import art17.scripts.export_refval
import art17.scripts.xml_reports
import art17.scripts.html_reports
import art17.scripts.import_eea
import art17.scripts.import_refval
import art17.scripts.modify_dataset
