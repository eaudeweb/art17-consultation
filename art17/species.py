import flask
from art17 import models


species = flask.Blueprint('species', __name__)

@species.route('/specii')
def species_view():
    species = models.DataSpecies.query.filter_by(speciescode='1308').first()
    return flask.render_template('species/view.html', **{
        'code': species.speciescode,
        'name': species.checklist.species_name,
    })
