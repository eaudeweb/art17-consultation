import flask
from art17 import models
from art17 import schemas
from art17 import config

reportviews = flask.Blueprint('reportviews', __name__)

with reportviews.open_resource('reportviews_species.json') as _f:
    _data = flask.json.load(_f)
    species_names = {
        'cbd': set(_data['cbd']),
        'cites': set(_data['cites']),
    }


@reportviews.route('/raport_specii/cbd', defaults={'species_list': 'cbd'})
@reportviews.route('/raport_specii/cites', defaults={'species_list': 'cites'})
def table(species_list):
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
        if name in species_names[species_list]:
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
        .order_by(
            models.LuHdSpecies.speciesname,
            models.DataSpeciesRegion.region,
        )
    )

    return flask.render_template('reportviews_table.html', **{
        'species_list': [
            (name, schemas.parse_species(record))
            for name, record in species_query
        ],
    })
