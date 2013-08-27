import flask
from art17 import models


species = flask.Blueprint('species', __name__)

@species.route('/specii')
def species_view():
    species = models.DataSpecies.query.filter_by(speciescode='1308').first()
    species_checklist = (models.DataSpeciesCheckList.query
                            .filter_by(natura_2000_code=species.speciescode)
                            .first())
    return flask.render_template('species/view.html', **{
        'name': species_checklist.species_name,
    })
