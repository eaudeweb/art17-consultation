import flask
from art17 import models
from art17.scripts import exporter


@exporter.command
def xml_species():
    species = models.db.session.query(models.DataSpecies)
    template = flask.render_template(
                'xml_export/species.html',
                **{'species_list': species}
            )
    return template
