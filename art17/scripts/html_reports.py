import flask
from art17 import models
from art17.scripts import exporter


def species_report(dataset_id):
    species = (models.DataSpeciesRegion.query
               .filter_by(cons_dataset_id=dataset_id))
    species_struct = {}
    for s in species:
        key = (s.species.code, s.species.lu.display_name)
        if key not in species_struct:
            species_struct[key] = {}
        if s.region not in species_struct[key]:
            species_struct[key][s.region] = s

    return flask.render_template('xml_export/report.html', **{
        'species': species_struct,
    })


def habitat_report(dataset_id):
    habitats = (models.DataHabitattypeRegion.query
                .filter_by(cons_dataset_id=dataset_id))
    habitat_struct = {}
    for h in habitats:
        key = (h.habitat.code, h.habitat.lu.display_name)
        if key not in habitat_struct:
            habitat_struct[key] = {}
        if h.region not in habitat_struct[key]:
            habitat_struct[key][h.region] = h

    return flask.render_template('xml_export/report.html', **{
        'habitat': habitat_struct,
    })


@exporter.command
def html_report(dataset_id, subject):
    if subject == 'species':
        data = species_report(dataset_id)
    elif subject == 'habitat':
        data = habitat_report(dataset_id)
    with open('Report_{}_{}.html'.format(dataset_id, subject), 'w') as f:
        f.write(data.encode('utf-8'))
