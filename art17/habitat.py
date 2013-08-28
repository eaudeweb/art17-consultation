import flask
from art17 import models

habitat = flask.Blueprint('habitat', __name__)


@habitat.route('/habitate/')
def habitats_index():
    return flask.render_template('habitat/index.html', **{
        'records': list(models.DataHabitat.query.order_by('habitatcode')),
    })


@habitat.route('/habitate/<habitatcode>')
def habitat_view(habitatcode):
    return "not implemented"
