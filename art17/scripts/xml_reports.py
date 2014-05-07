import flask
from art17 import models
from art17.scripts import exporter


@exporter.command
def xml_species(filename=None):
    species = models.db.session.query(models.DataSpecies)
    data = flask.render_template(
                'xml_export/species.html',
                **{'species_list': species}
            )
    if filename:
        with open(filename, 'w') as file_out:
            file_out.write(data.encode('utf-8'))


@exporter.command
def xml_habitats(filename=None):
    habitats = models.db.session.query(models.DataHabitat)
    data = flask.render_template(
                'xml_export/habitats.html',
                **{'habitats': habitats}
            )
    if filename:
        with open(filename, 'w') as file_out:
            file_out.write(data.encode('utf-8'))
