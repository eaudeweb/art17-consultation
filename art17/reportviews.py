import flask
from art17 import models
from art17 import schemas
from art17 import config

reportviews = flask.Blueprint('reportviews', __name__)

with reportviews.open_resource('reportviews_species.json') as f:
    cites_species_names = set(flask.json.load(f)['species'])


@reportviews.route('/raport_specii/cites')
def table():
    dataset_id = int(config.get_config_value('CONSULTATION_DATASET', '1'))

    prefilter_query = (
        models.db.session.query(
            models.DataSpecies.id,
            models.LuHdSpecies.speciesname,
        )
        .join(models.DataSpecies.lu)
    )
    species_id_list = []
    for species_id, name in prefilter_query:
        if name in cites_species_names:
            species_id_list.append(species_id)

    species_query = (
        models.db.session.query(
            models.LuHdSpecies.speciesname,
            models.DataSpeciesRegion,
        )
        .join(models.DataSpeciesRegion.species)
        .join(models.DataSpecies.lu)
        .filter(models.DataSpeciesRegion.cons_dataset_id == dataset_id)
        .filter(models.DataSpeciesRegion.cons_role == 'assessment')
        .filter(models.DataSpecies.id.in_(species_id_list))
    )

    return flask.render_template('reportviews_table.html', **{
        'species_list': [
            (name, schemas.parse_species(record))
            for name, record in species_query.limit(5)  # TODO remove limit
        ],
    })
